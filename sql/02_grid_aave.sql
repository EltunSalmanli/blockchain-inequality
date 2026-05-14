-- Active-Holder Gini Grid: AAVE
-- For each of 7 windows × 2 active-definitions, computes:
--   - active address count
--   - total balance across active set
--   - Gini coefficient on current balances of active addresses
-- Token: AAVE (0x7fc66500c84a76ad7e9c93437bfc5ac33e2ddae9, 18 decimals)

WITH
-- ============================================================
-- Step 1: compute CURRENT balance for every address that ever held AAVE
-- (this is done once; later we filter to active subsets)
-- ============================================================
all_balances AS (
    SELECT wallet, SUM(amount) / 1e18 AS balance
    FROM (
        SELECT "from" AS wallet, -CAST(value AS DOUBLE) AS amount
        FROM erc20_ethereum.evt_Transfer
        WHERE contract_address = 0x7fc66500c84a76ad7e9c93437bfc5ac33e2ddae9
        UNION ALL
        SELECT "to" AS wallet, CAST(value AS DOUBLE) AS amount
        FROM erc20_ethereum.evt_Transfer
        WHERE contract_address = 0x7fc66500c84a76ad7e9c93437bfc5ac33e2ddae9
    )
    WHERE wallet NOT IN (
        0x0000000000000000000000000000000000000000,
        0x000000000000000000000000000000000000dead
    )
    GROUP BY wallet
    HAVING SUM(amount) > 0
),

-- ============================================================
-- Step 2: build active-address sets for all 7 windows × 2 defs
-- ============================================================
activity AS (
    SELECT
        wallet,
        MAX(CASE WHEN role = 'sent' THEN block_time END) AS last_sent,
        MAX(block_time) AS last_seen
    FROM (
        SELECT "from" AS wallet, 'sent' AS role, evt_block_time AS block_time
        FROM erc20_ethereum.evt_Transfer
        WHERE contract_address = 0x7fc66500c84a76ad7e9c93437bfc5ac33e2ddae9
        UNION ALL
        SELECT "to" AS wallet, 'received' AS role, evt_block_time AS block_time
        FROM erc20_ethereum.evt_Transfer
        WHERE contract_address = 0x7fc66500c84a76ad7e9c93437bfc5ac33e2ddae9
    )
    WHERE wallet NOT IN (
        0x0000000000000000000000000000000000000000,
        0x000000000000000000000000000000000000dead
    )
    GROUP BY wallet
),

-- ============================================================
-- Step 3: join balances with activity timestamps
-- ============================================================
holders AS (
    SELECT
        b.wallet,
        b.balance,
        a.last_sent,
        a.last_seen
    FROM all_balances b
    JOIN activity a ON a.wallet = b.wallet
),

-- ============================================================
-- Step 4: explode into one row per (window, definition, wallet)
-- ============================================================
exploded AS (
    -- 1 day, sent only
    SELECT '1d' AS window, 'sent_only' AS active_def, wallet, balance
    FROM holders WHERE last_sent >= NOW() - INTERVAL '1' DAY
    UNION ALL
    SELECT '1d', 'sent_or_received', wallet, balance
    FROM holders WHERE last_seen >= NOW() - INTERVAL '1' DAY
    UNION ALL
    -- 1 week
    SELECT '1w', 'sent_only', wallet, balance
    FROM holders WHERE last_sent >= NOW() - INTERVAL '7' DAY
    UNION ALL
    SELECT '1w', 'sent_or_received', wallet, balance
    FROM holders WHERE last_seen >= NOW() - INTERVAL '7' DAY
    UNION ALL
    -- 1 month
    SELECT '1m', 'sent_only', wallet, balance
    FROM holders WHERE last_sent >= NOW() - INTERVAL '30' DAY
    UNION ALL
    SELECT '1m', 'sent_or_received', wallet, balance
    FROM holders WHERE last_seen >= NOW() - INTERVAL '30' DAY
    UNION ALL
    -- 3 months
    SELECT '3m', 'sent_only', wallet, balance
    FROM holders WHERE last_sent >= NOW() - INTERVAL '90' DAY
    UNION ALL
    SELECT '3m', 'sent_or_received', wallet, balance
    FROM holders WHERE last_seen >= NOW() - INTERVAL '90' DAY
    UNION ALL
    -- 6 months
    SELECT '6m', 'sent_only', wallet, balance
    FROM holders WHERE last_sent >= NOW() - INTERVAL '180' DAY
    UNION ALL
    SELECT '6m', 'sent_or_received', wallet, balance
    FROM holders WHERE last_seen >= NOW() - INTERVAL '180' DAY
    UNION ALL
    -- 1 year
    SELECT '1y', 'sent_only', wallet, balance
    FROM holders WHERE last_sent >= NOW() - INTERVAL '365' DAY
    UNION ALL
    SELECT '1y', 'sent_or_received', wallet, balance
    FROM holders WHERE last_seen >= NOW() - INTERVAL '365' DAY
    UNION ALL
    -- all time
    SELECT 'all', 'sent_only', wallet, balance
    FROM holders WHERE last_sent IS NOT NULL
    UNION ALL
    SELECT 'all', 'sent_or_received', wallet, balance
    FROM holders
),

-- ============================================================
-- Step 5: rank balances within each (window, def) group
-- ============================================================
ranked AS (
    SELECT
        window,
        active_def,
        balance,
        ROW_NUMBER() OVER (PARTITION BY window, active_def ORDER BY balance ASC) AS rnk,
        COUNT(*) OVER (PARTITION BY window, active_def) AS n,
        SUM(balance) OVER (PARTITION BY window, active_def) AS total
    FROM exploded
)

-- ============================================================
-- Step 6: compute Gini per (window, def)
-- ============================================================
SELECT
    'AAVE'                                              AS token,
    window,
    active_def                                          AS active_definition,
    MAX(n)                                              AS active_addresses,
    MAX(total)                                          AS total_balance,
    (2.0 * SUM(rnk * balance) / (MAX(n) * MAX(total)))
        - ((MAX(n) + 1.0) / MAX(n))                     AS gini
FROM ranked
GROUP BY window, active_def
ORDER BY
    CASE window
        WHEN '1d'  THEN 1
        WHEN '1w'  THEN 2
        WHEN '1m'  THEN 3
        WHEN '3m'  THEN 4
        WHEN '6m'  THEN 5
        WHEN '1y'  THEN 6
        WHEN 'all' THEN 7
    END,
    active_def;
