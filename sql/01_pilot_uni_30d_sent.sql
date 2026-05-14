-- Active-Holder Gini Pilot: UNI, 30-day window, sent-only definition
-- Computes Gini coefficient on current UNI balances of addresses
-- that issued at least one outbound UNI transfer in the last 30 days.

WITH
-- Step 1: identify active senders in the last 30 days
active_senders AS (
    SELECT DISTINCT "from" AS wallet
    FROM erc20_ethereum.evt_Transfer
    WHERE contract_address = 0x1f9840a85d5af5bf1d1762f925bdaddc4201f984
      AND evt_block_time >= NOW() - INTERVAL '30' DAY
      AND "from" NOT IN (
          0x0000000000000000000000000000000000000000,
          0x000000000000000000000000000000000000dead
      )
),

-- Step 2: reconstruct current balance for each active sender
-- (full historical net flow, not just the window)
balances AS (
    SELECT wallet, SUM(amount) / 1e18 AS balance
    FROM (
        SELECT "from" AS wallet, -CAST(value AS DOUBLE) AS amount
        FROM erc20_ethereum.evt_Transfer
        WHERE contract_address = 0x1f9840a85d5af5bf1d1762f925bdaddc4201f984
        UNION ALL
        SELECT "to" AS wallet, CAST(value AS DOUBLE) AS amount
        FROM erc20_ethereum.evt_Transfer
        WHERE contract_address = 0x1f9840a85d5af5bf1d1762f925bdaddc4201f984
    )
    WHERE wallet IN (SELECT wallet FROM active_senders)
    GROUP BY wallet
    HAVING SUM(amount) > 0
),

-- Step 3: rank balances ascending for Gini computation
ranked AS (
    SELECT
        balance,
        ROW_NUMBER() OVER (ORDER BY balance ASC) AS rnk,
        COUNT(*) OVER () AS n,
        SUM(balance) OVER () AS total
    FROM balances
)

SELECT
    'UNI'                                   AS token,
    '30d'                                   AS window,
    'sent_only'                             AS active_definition,
    MAX(n)                                  AS active_addresses,
    MAX(total)                              AS total_balance,
    (2.0 * SUM(rnk * balance) / (MAX(n) * MAX(total)))
        - ((MAX(n) + 1.0) / MAX(n))         AS gini
FROM ranked;
