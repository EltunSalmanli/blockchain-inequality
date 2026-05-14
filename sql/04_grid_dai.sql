-- Active-Holder Gini Grid: DAI (OPTIMIZED — single combined scan)
-- Token: DAI (0x6b175474e89094c44da98b954eedeac495271d0f, 18 decimals)

WITH
events AS (
    SELECT
        "from" AS wallet,
        -CAST(value AS DOUBLE) AS signed_value,
        evt_block_time AS block_time,
        true AS is_send
    FROM erc20_ethereum.evt_Transfer
    WHERE contract_address = 0x6b175474e89094c44da98b954eedeac495271d0f

    UNION ALL

    SELECT
        "to" AS wallet,
        CAST(value AS DOUBLE) AS signed_value,
        evt_block_time AS block_time,
        false AS is_send
    FROM erc20_ethereum.evt_Transfer
    WHERE contract_address = 0x6b175474e89094c44da98b954eedeac495271d0f
),

holders AS (
    SELECT
        wallet,
        SUM(signed_value) / 1e18 AS balance,
        MAX(CASE WHEN is_send THEN block_time END) AS last_sent,
        MAX(block_time) AS last_seen
    FROM events
    WHERE wallet NOT IN (
        0x0000000000000000000000000000000000000000,
        0x000000000000000000000000000000000000dead
    )
    GROUP BY wallet
    HAVING SUM(signed_value) > 0
),

exploded AS (
    SELECT '1d' AS window, 'sent_only' AS active_def, wallet, balance
    FROM holders WHERE last_sent >= NOW() - INTERVAL '1' DAY
    UNION ALL
    SELECT '1d', 'sent_or_received', wallet, balance
    FROM holders WHERE last_seen >= NOW() - INTERVAL '1' DAY
    UNION ALL
    SELECT '1w', 'sent_only', wallet, balance
    FROM holders WHERE last_sent >= NOW() - INTERVAL '7' DAY
    UNION ALL
    SELECT '1w', 'sent_or_received', wallet, balance
    FROM holders WHERE last_seen >= NOW() - INTERVAL '7' DAY
    UNION ALL
    SELECT '1m', 'sent_only', wallet, balance
    FROM holders WHERE last_sent >= NOW() - INTERVAL '30' DAY
    UNION ALL
    SELECT '1m', 'sent_or_received', wallet, balance
    FROM holders WHERE last_seen >= NOW() - INTERVAL '30' DAY
    UNION ALL
    SELECT '3m', 'sent_only', wallet, balance
    FROM holders WHERE last_sent >= NOW() - INTERVAL '90' DAY
    UNION ALL
    SELECT '3m', 'sent_or_received', wallet, balance
    FROM holders WHERE last_seen >= NOW() - INTERVAL '90' DAY
    UNION ALL
    SELECT '6m', 'sent_only', wallet, balance
    FROM holders WHERE last_sent >= NOW() - INTERVAL '180' DAY
    UNION ALL
    SELECT '6m', 'sent_or_received', wallet, balance
    FROM holders WHERE last_seen >= NOW() - INTERVAL '180' DAY
    UNION ALL
    SELECT '1y', 'sent_only', wallet, balance
    FROM holders WHERE last_sent >= NOW() - INTERVAL '365' DAY
    UNION ALL
    SELECT '1y', 'sent_or_received', wallet, balance
    FROM holders WHERE last_seen >= NOW() - INTERVAL '365' DAY
    UNION ALL
    SELECT 'all', 'sent_only', wallet, balance
    FROM holders WHERE last_sent IS NOT NULL
    UNION ALL
    SELECT 'all', 'sent_or_received', wallet, balance
    FROM holders
),

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

SELECT
    'DAI'                                               AS token,
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
