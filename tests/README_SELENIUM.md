# Selenium E2E — PoC-6 Chargeback Lifecycle Tracker

This folder contains Selenium browser automation for the **deployed** Chargeback Lifecycle Tracker.

## Target URL

Default target: `https://poc6-chargeback-frontend.onrender.com/` (Render).

The supplied Infocreon Selenium guide asks for an **Azure** URL. The current known deployment is Render, so do not describe a Render run as Azure validation. Set `TARGET_URL` to the Azure deployment URL after deploying there.

## Prerequisites

- Python 3.10+
- Google Chrome
- Internet access to the deployed frontend and backend
- Selenium 4

Selenium Manager will attempt to resolve the compatible ChromeDriver automatically. If your environment blocks that, install the matching ChromeDriver and make it available on PATH.

## Run (PowerShell)

From the repository root:

```powershell
python -m pip install -r tests/selenium-requirements.txt
python tests/test_live_application.py
```

For Azure deployment:

```powershell
$env:TARGET_URL = "https://YOUR-AZURE-FRONTEND-URL/"
python tests/test_live_application.py
```

Optional headless execution:

```powershell
$env:HEADLESS = "1"
python tests/test_live_application.py
```

Optional API endpoint override:

```powershell
$env:BACKEND_API_URL = "https://YOUR-BACKEND/api/chargebacks"
```

## Checks automated

1. Live page load and CSS visualization rendering
2. Frontend/backend handshake and data loading (API HTTP 200 and dashboard rows)
3. Case-row selection opens and closes the slide-over Intelligence Panel
4. Project-info modal opens and displays `Jona Peter`
5. Outcome filter narrows cases and Reset restores the records
6. Basic mobile viewport responsiveness (390 × 844)

## Outputs

- `tests/test-results/Test_Report.txt`
- `tests/screenshots/01_dashboard_visual_load.png`
- `tests/screenshots/02_data_loaded.png`
- `tests/screenshots/03_intelligence_panel_open.png`
- `tests/screenshots/04_project_info_modal.png`
- `tests/screenshots/05_filter_reset.png`
- `tests/screenshots/06_mobile_responsive.png`

A report is written after the test runner exits. The script is rerunnable and does not modify application data.

## Known limitations

- The supplied guide requests Azure. The default URL is Render, and the report identifies this distinction.
- The app uses synthetic JSON data, not a production database or payment gateway.
- This is a basic responsive smoke test, not exhaustive browser/device coverage.
- The test relies on existing CSS classes and accessible labels in `frontend/app/page.tsx`.
