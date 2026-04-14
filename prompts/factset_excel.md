# Excel Rules
General Excel rules (project-specific)
---
name: FactSet Excel Automation
description: Guidelines and troubleshooting steps for automating FactSet-enabled Excel workbooks via Python COM (pywin32).
---

# FactSet Excel Automation Skill

When automating FactSet (or Bloomberg/CapIQ) Excel workbooks via Python `pywin32` (COM), you must follow these specific handling rules. FactSet behaves differently than standard Excel files due to cloud data fetching, authentication requirements, and proprietary add-in mechanics.

## 1. Authentication and Background Processes
**Rule:** Always use `win32.Dispatch("Excel.Application")`, NOT `DispatchEx`.
**Why:** `win32.DispatchEx` launches a sterile, isolated background process. FactSet requires authentication and usually fails to latch onto the user's desktop login in these isolated instances. Standard `Dispatch` (often with `excel.Visible = True`) brings the active FactSet connection along.

## 2. Triggering the Refresh
**Rule:** Use UI simulation (SendKeys) instead of native COM refresh methods.
**Why:** A standard `Workbook.RefreshAll()` or calling the COM object directly (`factset_addin.Object`) often fails or is blocked for background scripts.
**Implementation:** Activate the workbook and simulate the FactSet Ribbon Refresh shortcut:
```python
excel.SendKeys("%srw") # Simulates Alt + S + R + W
```

## 3. Handling Asynchronous Data Loading
**Rule:** Implement a manual pause before interacting with the refreshed data.
**Why:** FactSet formulas fetch data asynchronously from the cloud. If you attempt to copy/paste or flatten cells (`UsedRange.Value = UsedRange.Value`) before the download completes, the cells will return `#CALC!` (`-2146826259` in COM) or `#N/A`.
**Implementation:** Add a forced sleep (e.g., `time.sleep(30)`) after the refresh trigger to allow the server query to finish before touching the cells.

## 4. Ticker Formatting (Project Specific)
When inputting tickers into FactSet templates in this project, ensure the proper regional suffix is appended:
- **US Equities**: Add `-US` (e.g., `AAPL-US`, `MSFT-US`)
- **Canadian Equities**: Add `-CA` (e.g., `T-CA`, `WELL-CA`)
