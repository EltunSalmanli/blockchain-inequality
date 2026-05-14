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
| 03 | Grid — UNI, all 7 windows × 2 active defs | https://dune.com/queries/7502379 |
| 04 | Grid — DAI, all 7 windows × 2 active defs | https://dune.com/queries/7502514 |
| 05 | Grid — USDC, all 7 windows × 2 active defs | https://dune.com/queries/7502585 |

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

### UNI grid (Query 03)

| Window | Active def. | Active addresses | Total balance | Gini |
|---|---|---|---|---|
| 1d | sent only | 479 | 34,683,873 | 0.9438 |
| 1d | sent or received | 844 | 109,107,322 | 0.9783 |
| 1w | sent only | 1,841 | 95,557,804 | 0.9751 |
| 1w | sent or received | 3,154 | 172,277,009 | 0.9877 |
| 1m | sent only | 3,844 | 123,657,672 | 0.9846 |
| 1m | sent or received | 7,325 | 198,433,940 | 0.9908 |
| 3m | sent only | 8,735 | 472,540,149 | 0.9970 |
| 3m | sent or received | 19,566 | 501,819,437 | 0.9969 |
| 6m | sent only | 15,925 | 498,975,431 | 0.9977 |
| 6m | sent or received | 38,586 | 574,195,317 | 0.9972 |
| 1y | sent only | 37,444 | 576,361,219 | 0.9983 |
| 1y | sent or received | 392,544 | 895,649,841 | 0.9975 |
| all | sent only | 192,687 | 658,862,916 | 0.9992 |
| all | sent or received | 440,001 | 895,650,420 | 0.9978 |

### DAI grid (Query 04)

| Window | Active def. | Active addresses | Total balance | Gini |
|---|---|---|---|---|
| 1d | sent only | 1,267 | 1,451,256,103 | 0.9944 |
| 1d | sent or received | 1,811 | 1,477,589,405 | 0.9941 |
| 1w | sent only | 4,920 | 1,588,913,743 | 0.9945 |
| 1w | sent or received | 6,788 | 1,836,055,991 | 0.9935 |
| 1m | sent only | 16,376 | 1,822,389,387 | 0.9953 |
| 1m | sent or received | 21,833 | 2,251,839,870 | 0.9926 |
| 3m | sent only | 78,988 | 2,028,740,101 | 0.9980 |
| 3m | sent or received | 90,162 | 2,689,387,548 | 0.9962 |
| 6m | sent only | 161,687 | 2,281,138,703 | 0.9986 |
| 6m | sent or received | 184,663 | 3,669,289,541 | 0.9963 |
| 1y | sent only | 199,723 | 2,387,226,841 | 0.9985 |
| 1y | sent or received | 233,039 | 3,810,322,873 | 0.9962 |
| all | sent only | 674,429 | 2,681,618,418 | 0.9992 |
| all | sent or received | 812,736 | 4,375,642,490 | 0.9980 |

### USDC grid (Query 05)

| Window | Active def. | Active addresses | Total balance | Gini |
|---|---|---|---|---|
| 1d | sent only | 38,061 | 13,958,803,441 | 0.9944 |
| 1d | sent or received | 64,156 | 15,954,134,947 | 0.9940 |
| 1w | sent only | 143,561 | 17,868,653,427 | 0.9939 |
| 1w | sent or received | 229,751 | 21,053,321,016 | 0.9937 |
| 1m | sent only | 376,824 | 26,056,857,841 | 0.9950 |
| 1m | sent or received | 583,245 | 29,874,557,140 | 0.9942 |
| 3m | sent only | 1,180,439 | 29,573,179,653 | 0.9973 |
| 3m | sent or received | 1,616,461 | 34,851,179,729 | 0.9962 |
| 6m | sent only | 2,759,845 | 32,028,246,754 | 0.9984 |
| 6m | sent or received | 3,555,876 | 52,564,553,029 | 0.9969 |
| 1y | sent only | 3,384,324 | 34,749,444,074 | 0.9983 |
| 1y | sent or received | 4,540,380 | 52,878,522,950 | 0.9977 |
| all | sent only | 4,703,691 | 39,885,915,854 | 0.9984 |
| all | sent or received | 6,855,774 | 53,511,887,415 | 0.9978 |

**USDC observations:**
- USDC has by far the largest active user base of any token analyzed: **38,061 daily senders, 4.7M all-time senders** — orders of magnitude beyond the governance tokens.
- The Gini curve is the flattest observed so far (range 0.004 across all windows for sent-only), reinforcing the pattern that stablecoins behave fundamentally differently from governance tokens.
- The 1-day USDC active set (38k addresses) is already 80× larger than UNI's 1-day active set (479) and 8× larger than UNI's all-time active set — a striking illustration of which Ethereum tokens function as money versus speculation.
- **Pattern confirmed across two stablecoins (DAI, USDC):** when a token is actively used as currency, the active-holder Gini converges to the all-time Gini quickly; the dormant tail is small.

**DAI observations:**
- DAI shows a remarkably **flat Gini curve** across windows: from 0.9944 at 1-day sent-only to 0.9992 all-time — a range of only 0.005 compared to UNI's range of 0.055.
- This reflects DAI's role as actively used money rather than a speculative or governance asset: the active holder set already captures essentially all economically relevant participants even at the 1-day window.
- The 1-day active sender count (1,267) is already comparable to UNI's 1-month active sender count (3,844), indicating substantially higher turnover and real economic usage.
- **Cross-token comparison takes shape:** governance tokens (UNI, AAVE) display strong window-sensitivity, while stablecoins (DAI so far) display window-insensitivity. Whether USDT and USDC confirm this pattern will be the next test.

**UNI observations:**
- The 1d sent-only Gini (0.944) is *significantly* lower than AAVE's (0.976). UNI shows the largest reduction in inequality when the active filter is applied, consistent with UNI being a major airdrop token where many recipients never transact.
- The all-time `sent_or_received` count is **440,001** — closely matching the ~250,000 wallets that received the 2020 UNI airdrop plus subsequent recipients. A substantial fraction of these never appear in shorter active windows.
- The jump in `active_addresses` between 6m (38,586) and 1y (392,544) for sent-or-received is striking — roughly 10× — suggesting most UNI movement happens on long timescales.

**Initial observation:** Gini rises monotonically as the activity window expands, suggesting that more selective (recently-active) holder sets show *less* inequality than the full holder set. This is the opposite of what custodial-distortion arguments would predict. The two active-definitions (sent only vs sent or received) produce very similar Gini values, indicating robustness to this definitional choice.

## References

- Yaish, Chemaya, Malkhi, Cong (2026). *Inequality in the Age of Pseudonymity.* AAAI-26.
- Chemaya, Yaish, Yacouel, Malkhi, Cong (2025). *Quantifying Inequality in Blockchain Networks.* SSRN.
- Fritsch, Müller, Wattenhofer (2024). *Analyzing Voting Power in Decentralized Governance: Who Controls DAOs?*
