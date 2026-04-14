# DCF Methodology

## FCF Definition
Fish uses unlevered free cash flow (UFCF):

```
UFCF = EBIT × (1 - Tax Rate)
     + D&A
     - Capex
     - Change in Net Working Capital
```

- **Tax rate:** Use the effective tax rate from the income statement if available. Default to 25% if not.
- **D&A:** Pull from the cash flow statement (add-back section), not the income statement footnotes.
- **Capex:** Pull from the cash flow statement (investing activities), expressed as a positive number.
- **NWC change:** Derived from the balance sheet. NWC = (Current Assets − Cash) − (Current Liabilities − Current Portion of Debt). A increase in NWC is a use of cash (negative).

## Projection Period
Default: 5 years. Ask the user if the model has a different explicit forecast horizon already built in.

## Terminal Value
Use the Gordon Growth Model (perpetuity growth method):

```
Terminal Value = FCF_final × (1 + g) / (WACC − g)
```

- `g` = terminal growth rate (default 2.5%, see industry knowledge for overrides)
- Apply at end of projection period

## Discounting Convention
- Use mid-year convention by default: discount period = 0.5, 1.5, 2.5, etc.
- If the user prefers end-of-year, apply period = 1, 2, 3, etc.
- Discount factor = 1 / (1 + WACC)^period

## WACC
Default: 9.0%. Always surface this assumption at confirmation — it is the most sensitive input.
See industry knowledge file for sector-specific defaults.

## DCF Tab Layout
Build the tab in this order, top to bottom:

### Block 1 — Assumptions (hardcoded, rows 1–10)
| Label | Value |
|---|---|
| WACC | 9.0% |
| Terminal Growth Rate | 2.5% |
| Tax Rate | 25.0% |
| Projection Period | 5 years |
| Discounting Convention | Mid-year |

### Block 2 — FCF Bridge (linked rows)
Year headers matching the source model columns.
Rows: Revenue, EBIT, NOPAT, + D&A, − Capex, − ΔNWC, = UFCF

### Block 3 — Discounting
Discount period, discount factor, PV of UFCF per year, sum of PV FCFs.

### Block 4 — Terminal Value
Terminal FCF, terminal value (Gordon Growth), PV of terminal value.

### Block 5 — Valuation Bridge
PV of FCFs + PV of terminal value = Enterprise Value
− Net Debt (pulled from balance sheet) = Equity Value
÷ Shares outstanding (ask user if not in model) = Implied Share Price

## Formatting Conventions
- Numbers in thousands unless the source model uses a different unit — match the source
- Percentages formatted as %, not decimals in display
- Negative values in parentheses for cash uses (capex, ΔNWC if increase)
- Bold the UFCF row, Enterprise Value row, and Implied Share Price row
