
"""
PoC-6 Chargeback Lifecycle Tracker - Deployed-site Selenium E2E audit.

Run from the project root:
    pip install -r tests/selenium-requirements.txt
    python tests/test_live_application.py

Override the site under test:
    $env:TARGET_URL="https://your-deployed-frontend.example/"
    python tests/test_live_application.py

Optional:
    $env:BACKEND_API_URL="https://your-backend.example/api/chargebacks"
    $env:HEADLESS="1"
    $env:WAIT_SECONDS="30"

Generated files:
    tests/test-results/Test_Report.txt
    tests/screenshots/*.png
"""

from __future__ import annotations

import json
import os
import unittest
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import urlopen

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


DEFAULT_TARGET_URL = (
    "https://poc6-chargeback-frontend.onrender.com/"
)

TARGET_URL = os.environ.get(
    "TARGET_URL",
    DEFAULT_TARGET_URL,
).strip()

WAIT_SECONDS = int(
    os.environ.get("WAIT_SECONDS", "30")
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]

RESULTS_DIR = (
    PROJECT_ROOT / "tests" / "test-results"
)

SCREENSHOTS_DIR = (
    PROJECT_ROOT / "tests" / "screenshots"
)

REPORT_PATH = (
    RESULTS_DIR / "Test_Report.txt"
)

RESULTS_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

SCREENSHOTS_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

TEST_RESULTS: list[dict[str, str]] = []


def frontend_base_url() -> str:
    return TARGET_URL.rstrip("/") + "/"


def backend_api_url() -> str:
    return os.environ.get(
        "BACKEND_API_URL",
        "https://poc6-chargeback-backend.onrender.com/api/chargebacks",
    )


def record_result(
    name: str,
    status: str,
    detail: str = "",
) -> None:
    TEST_RESULTS.append({
        "test": name,
        "status": status,
        "detail": detail.replace("\n", " ").strip(),
    })


def capture(
    driver,
    filename: str,
) -> str:
    path = SCREENSHOTS_DIR / filename

    driver.save_screenshot(str(path))

    return str(
        path.relative_to(PROJECT_ROOT)
    )


def click_with_scroll(
    driver,
    element,
) -> None:
    """Scroll an element into view and click it through the browser DOM."""

    driver.execute_script(
        "arguments[0].scrollIntoView({block: 'center'});",
        element,
    )

    driver.execute_script(
        "arguments[0].click();",
        element,
    )


def get_horizontal_overflowing_elements(driver):
    """Return visible elements extending beyond the right viewport edge."""

    return driver.execute_script("""
        const viewportWidth =
            document.documentElement.clientWidth;

        return [...document.querySelectorAll('body *')]
            .map(element => {
                const rect = element.getBoundingClientRect();

                return {
                    tag: element.tagName,
                    className:
                        typeof element.className === 'string'
                            ? element.className
                            : '',
                    left: Math.round(rect.left),
                    right: Math.round(rect.right),
                    width: Math.round(rect.width),
                    scrollWidth: element.scrollWidth,
                    clientWidth: element.clientWidth
                };
            })
            .filter(element =>
                element.width > 0 &&
                element.right > viewportWidth + 1
            )
            .sort((a, b) => b.right - a.right)
            .slice(0, 12);
    """)


class LiveApplicationE2E(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        if not TARGET_URL.startswith(
            ("https://", "http://")
        ):
            raise RuntimeError(
                "TARGET_URL must be an http:// or https:// URL"
            )

        options = Options()

        if os.environ.get(
            "HEADLESS",
            "",
        ).lower() in {
            "1",
            "true",
            "yes",
        }:
            options.add_argument("--headless=new")

        options.add_argument(
            "--window-size=1440,1000"
        )

        options.add_argument(
            "--disable-dev-shm-usage"
        )

        options.add_argument(
            "--no-sandbox"
        )

        options.add_argument(
            "--disable-gpu"
        )

        options.add_argument(
            "--log-level=3"
        )

        # Do not wait for every resource to finish loading.
        options.page_load_strategy = "eager"

        cls.driver = webdriver.Chrome(
            options=options
        )

        cls.wait = WebDriverWait(
            cls.driver,
            90,
        )

        cls.driver.set_page_load_timeout(90)

        try:
            cls.driver.get(
                frontend_base_url()
            )

        except TimeoutException:
            print(
                "Page-load timeout; checking whether the dashboard loaded..."
            )

        # Wait for the dashboard and its case records.
        cls.wait.until(
            EC.visibility_of_element_located(
                (
                    By.CSS_SELECTOR,
                    ".command-center",
                )
            )
        )

        cls.wait.until(
            EC.visibility_of_element_located(
                (
                    By.CSS_SELECTOR,
                    ".case-table tbody tr",
                )
            )
        )

    @classmethod
    def tearDownClass(cls):

        try:
            if hasattr(cls, "driver"):
                cls.driver.quit()

        finally:
            write_report()

    def test_01_live_page_load_and_visualization(self):
        """Live URL opens and dashboard visualizations render."""

        try:
            self.assertEqual(
                urlparse(
                    self.driver.current_url
                ).scheme,
                "https",
            )

            self.assertTrue(
                self.driver.title
                or self.driver.find_element(
                    By.TAG_NAME,
                    "body",
                ).text
            )

            self.assertTrue(
                self.driver.find_element(
                    By.CSS_SELECTOR,
                    ".command-center",
                ).is_displayed()
            )

            self.assertTrue(
                self.driver.find_element(
                    By.CSS_SELECTOR,
                    ".lifecycle-track",
                ).is_displayed()
            )

            self.assertTrue(
                self.driver.find_element(
                    By.CSS_SELECTOR,
                    ".distribution-grid",
                ).is_displayed()
            )

            shot = capture(
                self.driver,
                "01_dashboard_visual_load.png",
            )

            record_result(
                "Live page load + visualization",
                "PASS",
                (
                    "Dashboard and visualizations visible; "
                    f"screenshot: {shot}"
                ),
            )

        except Exception as exc:

            capture(
                self.driver,
                "01_dashboard_visual_load_FAIL.png",
            )

            record_result(
                "Live page load + visualization",
                "FAIL",
                str(exc),
            )

            raise

    def test_02_frontend_backend_handshake_and_data(self):
        """Backend responds and browser renders the returned records."""

        try:
            with urlopen(
                backend_api_url(),
                timeout=WAIT_SECONDS,
            ) as response:

                self.assertEqual(
                    response.status,
                    200,
                )

                api_cases = json.loads(
                    response.read().decode("utf-8")
                )

            self.assertIsInstance(
                api_cases,
                list,
            )

            self.assertGreater(
                len(api_cases),
                0,
            )

            # Reset filters before comparing API and dashboard records.
            reset = self.wait.until(
                EC.presence_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        ".reset-button",
                    )
                )
            )

            click_with_scroll(
                self.driver,
                reset,
            )

            self.wait.until(
                lambda driver: len(
                    driver.find_elements(
                        By.CSS_SELECTOR,
                        ".case-table tbody tr",
                    )
                ) == len(api_cases)
            )

            rows = self.driver.find_elements(
                By.CSS_SELECTOR,
                ".case-table tbody tr",
            )

            self.assertEqual(
                len(rows),
                len(api_cases),
            )

            total_cases = self.driver.find_element(
                By.XPATH,
                "//article[contains(@class,'metric-card')][.//span[normalize-space()='TOTAL CASES']]/strong",
            ).text

            self.assertEqual(
                int(total_cases),
                len(api_cases),
            )

            shot = capture(
                self.driver,
                "02_data_loaded.png",
            )

            record_result(
                "Frontend/backend handshake + data load",
                "PASS",
                (
                    f"API HTTP 200; API records={len(api_cases)}; "
                    f"dashboard rows={len(rows)}; "
                    f"screenshot: {shot}"
                ),
            )

        except Exception as exc:

            capture(
                self.driver,
                "02_data_loaded_FAIL.png",
            )

            record_result(
                "Frontend/backend handshake + data load",
                "FAIL",
                str(exc),
            )

            raise

    def test_03_case_selection_opens_and_closes_intelligence_panel(self):
        """Selecting a case opens and closes the Intelligence Panel."""

        try:
            row = self.wait.until(
                EC.element_to_be_clickable(
                    (
                        By.CSS_SELECTOR,
                        ".case-table tbody tr",
                    )
                )
            )

            case_id = row.find_element(
                By.CSS_SELECTOR,
                "td strong",
            ).text

            row.click()

            panel = self.wait.until(
                EC.visibility_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        "aside.insight-panel",
                    )
                )
            )

            self.assertIn(
                case_id,
                panel.text,
            )

            shot = capture(
                self.driver,
                "03_intelligence_panel_open.png",
            )

            close_button = self.driver.find_element(
                By.CSS_SELECTOR,
                "button.panel-close[aria-label='Close panel']",
            )

            click_with_scroll(
                self.driver,
                close_button,
            )

            self.wait.until(
                EC.invisibility_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        "aside.insight-panel",
                    )
                )
            )

            record_result(
                "Case selection opens/closes Intelligence Panel",
                "PASS",
                (
                    f"Selected {case_id}; panel opened and closed; "
                    f"screenshot: {shot}"
                ),
            )

        except Exception as exc:

            capture(
                self.driver,
                "03_intelligence_panel_FAIL.png",
            )

            record_result(
                "Case selection opens/closes Intelligence Panel",
                "FAIL",
                str(exc),
            )

            raise

    def test_04_project_info_modal_contains_architect_name(self):
        """Project Info modal opens and displays the architect name."""

        try:
            trigger = self.wait.until(
                EC.presence_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        "button.metadata-trigger[aria-label='Open project information']",
                    )
                )
            )

            click_with_scroll(
                self.driver,
                trigger,
            )

            modal = self.wait.until(
                EC.visibility_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        ".metadata-modal[role='dialog']",
                    )
                )
            )

            self.assertIn(
                "Jona Peter",
                modal.text,
            )

            shot = capture(
                self.driver,
                "04_project_info_modal.png",
            )

            close_button = self.driver.find_element(
                By.CSS_SELECTOR,
                ".metadata-modal button.panel-close[aria-label='Close project information']",
            )

            click_with_scroll(
                self.driver,
                close_button,
            )

            self.wait.until(
                EC.invisibility_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        ".metadata-modal",
                    )
                )
            )

            record_result(
                "Project-info modal + architect signature",
                "PASS",
                (
                    "Modal shows Jona Peter and closes; "
                    f"screenshot: {shot}"
                ),
            )

        except Exception as exc:

            capture(
                self.driver,
                "04_project_info_FAIL.png",
            )

            record_result(
                "Project-info modal + architect signature",
                "FAIL",
                str(exc),
            )

            raise

    def test_05_filter_interaction_and_reset(self):
        """Outcome filter narrows records and reset restores them."""

        try:
            outcome_select = self.driver.find_element(
                By.XPATH,
                "//label[.//span[normalize-space()='OUTCOME']]/select",
            )

            outcome_select.send_keys(
                "Lost"
            )

            self.wait.until(
                lambda driver: len(
                    driver.find_elements(
                        By.CSS_SELECTOR,
                        ".case-table tbody tr",
                    )
                ) == 2
            )

            self.assertEqual(
                self.driver.find_element(
                    By.CSS_SELECTOR,
                    ".section-count",
                ).text,
                "2 RECORDS",
            )

            reset = self.driver.find_element(
                By.CSS_SELECTOR,
                ".reset-button",
            )

            click_with_scroll(
                self.driver,
                reset,
            )

            self.wait.until(
                lambda driver: len(
                    driver.find_elements(
                        By.CSS_SELECTOR,
                        ".case-table tbody tr",
                    )
                ) == 6
            )

            shot = capture(
                self.driver,
                "05_filter_reset.png",
            )

            record_result(
                "Filter interaction + reset",
                "PASS",
                (
                    "Lost filter narrowed to 2 records; "
                    f"reset restored 6; screenshot: {shot}"
                ),
            )

        except Exception as exc:

            capture(
                self.driver,
                "05_filter_FAIL.png",
            )

            record_result(
                "Filter interaction + reset",
                "FAIL",
                str(exc),
            )

            raise

    def test_06_basic_responsive_layout(self):
        """At mobile width, dashboard remains visible without page overflow."""

        try:
            # Emulate an actual mobile viewport rather than relying on
            # the desktop browser's outer window dimensions.
            self.driver.execute_cdp_cmd(
                "Emulation.setDeviceMetricsOverride",
                {
                    "width": 390,
                    "height": 844,
                    "deviceScaleFactor": 1,
                    "mobile": True,
                },
            )

            self.wait.until(
                EC.visibility_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        ".command-center",
                    )
                )
            )

            self.assertTrue(
                self.driver.find_element(
                    By.CSS_SELECTOR,
                    ".metrics-grid",
                ).is_displayed()
            )

            self.assertTrue(
                self.driver.find_element(
                    By.CSS_SELECTOR,
                    ".table-wrap",
                ).is_displayed()
            )

            # Allow the browser to apply the mobile viewport dimensions.
            self.driver.execute_script(
                "return document.documentElement.clientWidth"
            )

            viewport_width = self.driver.execute_script(
                "return document.documentElement.clientWidth"
            )

            page_width = self.driver.execute_script(
                "return document.documentElement.scrollWidth"
            )

            inner_width = self.driver.execute_script(
                "return window.innerWidth"
            )

            self.assertEqual(
                viewport_width,
                390,
                (
                    "Mobile viewport was not applied correctly: "
                    f"actual width={viewport_width}px, expected=390px"
                ),
            )

            # The table itself may scroll inside its wrapper.
            # The document must not overflow horizontally.
            self.assertLessEqual(
                page_width,
                viewport_width + 5,
                (
                    f"Page width overflow: {page_width}px "
                    f"> viewport {viewport_width}px"
                ),
            )

            overflowing_elements = (
                get_horizontal_overflowing_elements(
                    self.driver
                )
            )

            shot = capture(
                self.driver,
                "06_mobile_responsive.png",
            )

            record_result(
                "Basic responsive check",
                "PASS",
                (
                    f"Mobile viewport={viewport_width}px; "
                    f"window.innerWidth={inner_width}px; "
                    f"document width={page_width}px; "
                    f"elements extending beyond viewport="
                    f"{len(overflowing_elements)}; "
                    f"screenshot: {shot}"
                ),
            )

        except Exception as exc:

            capture(
                self.driver,
                "06_mobile_responsive_FAIL.png",
            )

            record_result(
                "Basic responsive check",
                "FAIL",
                str(exc),
            )

            raise

        finally:
            # Remove mobile emulation and restore desktop dimensions.
            self.driver.execute_cdp_cmd(
                "Emulation.clearDeviceMetricsOverride",
                {},
            )

            self.driver.set_window_size(
                1440,
                1000,
            )


def write_report():
    """Write a text report containing all recorded test results."""

    timestamp = datetime.now(
        timezone.utc
    ).strftime(
        "%Y-%m-%d %H:%M:%S UTC"
    )

    passed = sum(
        item["status"] == "PASS"
        for item in TEST_RESULTS
    )

    failed = sum(
        item["status"] == "FAIL"
        for item in TEST_RESULTS
    )

    skipped = sum(
        item["status"] == "SKIP"
        for item in TEST_RESULTS
    )

    status = (
        "PASS"
        if failed == 0 and passed > 0
        else "FAIL"
    )

    lines = [
        "PoC-6 Chargeback Lifecycle Tracker - Selenium E2E Test Report",
        "=" * 66,
        f"Run time: {timestamp}",
        f"Target URL: {TARGET_URL}",
        (
            "Target platform: "
            + (
                "Azure"
                if "azure" in urlparse(
                    TARGET_URL
                ).netloc.lower()
                else "Non-Azure deployment"
            )
        ),
        "Browser: Chrome via Selenium WebDriver / Selenium Manager",
        f"Overall result: {status}",
        (
            f"Summary: {passed} PASS, "
            f"{failed} FAIL, {skipped} SKIP"
        ),
        "",
        "Test cases:",
    ]

    for item in TEST_RESULTS:

        detail = (
            f" - {item['detail']}"
            if item["detail"]
            else ""
        )

        lines.append(
            f"[{item['status']}] {item['test']}{detail}"
        )

    lines += [
        "",
        f"Screenshots directory: {SCREENSHOTS_DIR}",
        "",
        "Notes:",
        "- This report is generated by the script after execution.",
        "- Azure validation requires TARGET_URL to be an actual Azure deployment URL.",
        "- The application uses synthetic JSON data; no production payment system is exercised.",
        "- The mobile test uses Chrome device emulation at a 390px viewport.",
        "- The mobile test checks document-level horizontal overflow.",
        "- The table may scroll horizontally inside its own wrapper.",
    ]

    REPORT_PATH.write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )

    print(
        "\n" + "\n".join(lines)
    )


if __name__ == "__main__":

    print(
        f"Running Selenium E2E against: {TARGET_URL}"
    )

    print(
        "Browser: Chrome (visible unless HEADLESS=1)"
    )

    unittest.main(
        verbosity=2
    )
