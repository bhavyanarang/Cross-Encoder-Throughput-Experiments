#!/usr/bin/env python3
"""Dashboard Screenshot Utility - captures screenshots of the metrics dashboard."""

import argparse
import logging
import os
import sys
import time
from datetime import datetime

logger = logging.getLogger(__name__)


def capture_dashboard_screenshot(
    output_path: str,
    dashboard_url: str = "http://localhost:8080",
    wait_seconds: float = 3.0,
    width: int = 1400,
    height: int = 1200,
    timeout_ms: int = 120000,
    retries: int = 3,
    require_playwright: bool = True,
) -> bool:
    """Capture a screenshot of the metrics dashboard using Playwright."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        if require_playwright:
            logger.error("Playwright is required for PNG screenshots!")
            logger.error("Install with: pip install playwright && playwright install chromium")
            return False
        logger.warning(
            "Playwright not installed. Install with: pip install playwright && playwright install chromium"
        )
        return _fallback_screenshot(output_path, dashboard_url)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    for attempt in range(retries):
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True, timeout=timeout_ms)
                context = browser.new_context(viewport={"width": width, "height": height})
                page = context.new_page()
                page.set_default_timeout(timeout_ms)
                page.set_default_navigation_timeout(timeout_ms)

                logger.info(f"Navigating to {dashboard_url} (attempt {attempt + 1}/{retries})...")
                page.goto(dashboard_url, wait_until="load", timeout=timeout_ms)

                logger.info("Waiting for page to be fully loaded...")
                page.wait_for_load_state("networkidle", timeout=timeout_ms)

                logger.info(f"Waiting {wait_seconds}s for charts to render...")
                time.sleep(wait_seconds)

                logger.info(f"Taking screenshot: {output_path}")
                page.screenshot(path=output_path, full_page=True, timeout=timeout_ms)

                browser.close()

            logger.info(f"Dashboard screenshot saved: {output_path}")
            return True

        except Exception as e:
            logger.warning(f"Screenshot attempt {attempt + 1}/{retries} failed: {e}")
            if attempt < retries - 1:
                logger.info("Retrying in 2 seconds...")
                time.sleep(2)
            else:
                logger.error(f"All {retries} screenshot attempts failed")
                return _fallback_screenshot(output_path, dashboard_url)

    return False


def _fallback_screenshot(output_path: str, dashboard_url: str) -> bool:
    """Fallback: save HTML snapshot of the dashboard metrics."""
    try:
        import urllib.request

        html_path = output_path.replace(".png", ".html")

        # Try to fetch the actual dashboard HTML with current metrics
        try:
            with urllib.request.urlopen(dashboard_url, timeout=5) as response:
                response.read().decode("utf-8")

            # Also fetch metrics to embed
            metrics_url = dashboard_url.rstrip("/") + "/metrics"
            with urllib.request.urlopen(metrics_url, timeout=5) as response:
                metrics_json = response.read().decode("utf-8")

            # Create HTML with embedded metrics
            with open(html_path, "w") as f:
                f.write(
                    f"""<!DOCTYPE html>
<html>
<head>
    <title>Dashboard Snapshot - {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 20px; background: #0d1117; color: #c9d1d9; }}
        pre {{ background: #161b22; padding: 15px; border-radius: 6px; overflow-x: auto; border: 1px solid #30363d; }}
        .header {{ margin-bottom: 20px; padding-bottom: 10px; border-bottom: 1px solid #30363d; }}
        a {{ color: #58a6ff; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Dashboard Snapshot</h1>
        <p>Captured: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
        <p><a href="{dashboard_url}">View Live Dashboard</a></p>
    </div>
    <h2>Metrics JSON</h2>
    <pre>{metrics_json}</pre>
    <p style="margin-top: 20px; color: #8b949e;">
        To enable PNG screenshots, install Playwright:<br>
        <code>pip install playwright && playwright install chromium</code>
    </p>
</body>
</html>"""
                )
            logger.info(f"Saved HTML snapshot: {html_path}")
            return True
        except Exception as e:
            logger.warning(f"Could not fetch dashboard: {e}")

            # Create simple redirect HTML
            with open(html_path, "w") as f:
                f.write(
                    f"""<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="refresh" content="0; url={dashboard_url}">
    <title>Dashboard Link</title>
</head>
<body>
    <p>Screenshot not available. <a href="{dashboard_url}">View Dashboard</a></p>
</body>
</html>"""
                )
            logger.info(f"Created dashboard link: {html_path}")
            return False

    except Exception as e:
        logger.error(f"Fallback screenshot failed: {e}")
        return False


def capture_experiment_screenshot(
    experiment_name: str,
    output_dir: str = "experiments/results/screenshots",
) -> str:
    """Capture screenshot for a specific experiment."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = experiment_name.replace(" ", "_").replace("/", "_")
    filename = f"{safe_name}_{timestamp}.png"
    output_path = os.path.join(output_dir, filename)

    success = capture_dashboard_screenshot(output_path)
    return output_path if success else ""


def main():
    parser = argparse.ArgumentParser(description="Capture dashboard screenshot")
    parser.add_argument(
        "--output", "-o", default="dashboard_screenshot.png", help="Output file path"
    )
    parser.add_argument("--url", default="http://localhost:8080", help="Dashboard URL")
    parser.add_argument("--wait", type=float, default=3.0, help="Seconds to wait for rendering")
    parser.add_argument("--width", type=int, default=1400, help="Screenshot width")
    parser.add_argument("--height", type=int, default=1200, help="Screenshot height")
    parser.add_argument("--timeout", type=int, default=120000, help="Timeout in milliseconds")
    parser.add_argument("--retries", type=int, default=3, help="Number of retry attempts")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")

    success = capture_dashboard_screenshot(
        args.output,
        dashboard_url=args.url,
        wait_seconds=args.wait,
        width=args.width,
        height=args.height,
        timeout_ms=args.timeout,
        retries=args.retries,
        require_playwright=True,  # Require Playwright for PNG screenshots
    )

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
