# Industry Knowledge

This file grows over time. Add notes here when Fish makes a bad assumption or when you want to encode a preference.

---

## General Overrides

- If the model has no explicit tax line, check the cash flow statement for "income taxes paid" as a cross-reference before defaulting to 25%.
- If D&A is not broken out on the cash flow statement, check the income statement for a combined EBITDA disclosure or footnotes.
- Shares outstanding: prefer diluted shares from the income statement (EPS denominator). If not available, ask the user.

---

## Sector Defaults

### Software / SaaS
- Terminal growth rate: 3.0%
- WACC: 10.0%
- Capex is typically minimal — if capex looks unusually high, confirm it's not being confused with capitalized software development costs
- NWC change is often negative (deferred revenue grows with the business — this is a source of cash, not a use)

### Industrials / Manufacturing
- Terminal growth rate: 2.0%
- WACC: 9.0%
- Watch for pension liabilities — these are debt-like and should be included in net debt
- Stated capex often mixes maintenance and growth capex; if the user has a split, use maintenance capex for the terminal year

### Consumer / Retail
- Terminal growth rate: 2.0%
- WACC: 8.5%
- NWC swings can be large — flag any year where ΔNWC exceeds 10% of revenue as unusual

### Energy / Resources
- Terminal growth rate: 1.5%
- WACC: 10.0%–12.0% depending on commodity exposure — ask the user
- Depletion is treated like D&A (non-cash add-back)
- Reserve life matters for terminal value — flag if the projection period exceeds stated reserve life

### Financial Services (Banks, Insurance)
- Standard UFCF DCF does not apply — do not attempt to build one without explicit user guidance
- Flag this to the user and ask how they want to approach valuation (dividend discount model, excess returns, etc.)

---

## Add Notes Below As You Teach Fish
<!-- Example format:
[Date] — [Company or sector]: [What you learned]
-->
