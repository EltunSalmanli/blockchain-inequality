# Blockchain Inequality — Mini-Thesis

Active-holder Gini coefficient analysis on Ethereum tokens.

**Student:** Eltun Salmanli (FJULHI)
**Supervisor:** Seres István András

## Research question

How does measured wealth inequality on Ethereum change when we
restrict the holder set to *active* addresses (those that issued
transactions in a recent window) rather than all historical holders?

## Tokens analyzed

ETH, DAI, USDT, USDC, UNI, AAVE

## Repository structure

- `sql/` — Dune Analytics queries (source code)
- `data/` — exported results (CSV)
- `results/` — Dune query result screenshots
- `scripts/` — Python scripts (matplotlib) for charts
- `charts/` — generated figures

## Method

For each token T and each window W ∈ {1d, 1w, 1m, 3m, 6m, 1y, all-time},
the active set A_T(W) is defined as addresses that sent at least one
transfer of T in the last W. Gini and Nakamoto coefficients are then
computed on the current balances of A_T(W).

## Live Dune queries

| # | Description | Dune URL |
|---|---|---|
| 01 | Pilot — UNI, 30-day window, sent-only | https://dune.com/queries/7501844 |

## Results so far

| Query | Token | Window | Active def. | Active addresses | Gini |
|---|---|---|---|---|---|
| 01 | UNI | 30d | sent only | 3,676 | 0.9838 |

## References

- Yaish, Chemaya, Malkhi, Cong (2026). *Inequality in the Age of Pseudonymity.* AAAI-26.
- Chemaya, Yaish, Yacouel, Malkhi, Cong (2025). *Quantifying Inequality in Blockchain Networks.* SSRN.
- Fritsch, Müller, Wattenhofer (2024). *Analyzing Voting Power in Decentralized Governance: Who Controls DAOs?*
