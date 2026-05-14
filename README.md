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
| 02 | Grid — AAVE, all 7 windows × 2 active defs | https://dune.com/queries/7502010 |

## Results so far

### Pilot (Query 01)

| Token | Window | Active def. | Active addresses | Gini |
|---|---|---|---|---|
| UNI | 30d | sent only | 3,676 | 0.9838 |

### AAVE grid (Query 02)

| Window | Active def. | Active addresses | Total balance | Gini |
|---|---|---|---|---|
| 1d | sent only | 436 | 5,082,888 | 0.9756 |
| 1d | sent or received | 657 | 5,609,503 | 0.9782 |
| 1w | sent only | 1,482 | 6,425,820 | 0.9853 |
| 1w | sent or received | 2,588 | 6,983,500 | 0.9874 |
| 1m | sent only | 3,976 | 7,267,281 | 0.9900 |
| 1m | sent or received | 7,775 | 9,594,127 | 0.9905 |
| 3m | sent only | 8,471 | 7,848,346 | 0.9932 |
| 3m | sent or received | 17,747 | 10,967,759 | 0.9932 |
| 6m | sent only | 15,768 | 9,668,776 | 0.9953 |
| 6m | sent or received | 32,670 | 12,894,531 | 0.9942 |
| 1y | sent only | 30,020 | 10,353,804 | 0.9964 |
| 1y | sent or received | 63,901 | 13,832,657 | 0.9948 |
| all | sent only | 83,013 | 11,143,777 | 0.9974 |
| all | sent or received | 215,294 | 17,000,900 | 0.9928 |

**Initial observation:** Gini rises monotonically as the activity window expands, suggesting that more selective (recently-active) holder sets show *less* inequality than the full holder set. This is the opposite of what custodial-distortion arguments would predict. The two active-definitions (sent only vs sent or received) produce very similar Gini values, indicating robustness to this definitional choice.

## References

- Yaish, Chemaya, Malkhi, Cong (2026). *Inequality in the Age of Pseudonymity.* AAAI-26.
- Chemaya, Yaish, Yacouel, Malkhi, Cong (2025). *Quantifying Inequality in Blockchain Networks.* SSRN.
- Fritsch, Müller, Wattenhofer (2024). *Analyzing Voting Power in Decentralized Governance: Who Controls DAOs?*
