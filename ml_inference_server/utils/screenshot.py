"""
Dashboard Screenshot Utility

Captures screenshots of the metrics dashboard after experiments complete.
Uses Playwright for headless browser rendering.
"""

import os
import sys
import time
import logging
from pathlib import Path
from datetime import datetime

logger = logging.getLogger(__name__)


def capture_dashboard_screenshot(
    output_path: str,
    dashboard_url: str = "http://localhost:8080",
    wait_seconds: float = 3.0,
    width: int = 1400,
    height: int = 1200,
    timeout_ms: int = 120000,  # 2 minute timeout
    retries: int = 3,
) -> bool:
    """
    Capture a screenshot of the metrics dashboard.
    
    Args:
        output_path: Path to save the screenshot (PNG format)
        dashboard_url: URL of the dashboard
        wait_seconds: Time to wait for charts to render
        width: Screenshot width
        height: Screenshot height
        timeout_ms: Navigation timeout in milliseconds (default 2 minutes)
        retries: Number of retry attempts
        
    Returns:
        True if screenshot was captured successfully, False otherwise
    """
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        logger.warning("Playwright not installed. Install with: uv pip install playwright && playwright install chromium")
        return _fallback_screenshot(output_path, dashboard_url)
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    for attempt in range(retries):
        try:
            with sync_playwright() as p:
                # Launch headless browser with extended timeout
                browser = p.chromium.launch(
                    headless=True,
                    timeout=timeout_ms,
                )
                context = browser.new_context(
                    viewport={"width": width, "height": height},
                )
                page = context.new_page()
                page.set_default_timeout(timeout_ms)
                page.set_default_navigation_timeout(timeout_ms)
                
                # Navigate to dashboard with explicit timeout
                logger.info(f"Navigating to {dashboard_url} (attempt {attempt + 1}/{retries})...")
                page.goto(dashboard_url, wait_until="load", timeout=timeout_ms)
                
                # Wait for charts to load and render
                logger.info("Waiting for page to be fully loaded...")
                page.wait_for_load_state("networkidle", timeout=timeout_ms)
                
                # Extra time for Chart.js animations
                logger.info(f"Waiting {wait_seconds}s for charts to render...")
                time.sleep(wait_seconds)
                
                # Take screenshot
                logger.info(f"Taking screenshot: {output_path}")
                page.screenshot(path=output_path, full_page=True, timeout=timeout_ms)
                
                browser.close()
                
            logger.info(f"Dashboard screenshot saved: {output_path}")
            return True
            
        except Exception as e:
            logger.warning(f"Screenshot attempt {attempt + 1}/{retries} failed: {e}")
            if attempt < retries - 1:
                logger.info(f"Retrying in 2 seconds...")
                time.sleep(2)
            else:
                logger.error(f"All {retries} screenshot attempts failed")
                return _fallback_screenshot(output_path, dashboard_url)
    
    return False


def _fallback_screenshot(output_path: str, dashboard_url: str) -> bool:
    """
    Fallback method using system screenshot tools.
    Creates a simple HTML file with a link to the dashboard instead.
    """
    try:
        # Try using screencapture on macOS
        import subprocess
        
        # Create a simple redirect HTML as fallback
        html_path = output_path.replace('.png', '.html')
        with open(html_path, 'w') as f:
            f.write(f'''<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="refresh" content="0; url={dashboard_url}">
    <title>Dashboard Screenshot</title>
</head>
<body>
    <p>Screenshot not available. <a href="{dashboard_url}">View Dashboard</a></p>
    <p>To enable screenshots, install Playwright:</p>
    <pre>uv pip install playwright && playwright install chromium</pre>
</body>
</html>''')
        logger.info(f"Created dashboard link: {html_path}")
        return False
    except Exception as e:
        logger.error(f"Fallback screenshot also failed: {e}")
        return False


def capture_experiment_screenshot(
    experiment_name: str,
    output_dir: str = "ml_inference_server/docs/experiments/screenshots",
) -> str:
    """
    Capture a screenshot for a specific experiment.
    
    Args:
        experiment_name: Name of the experiment
        output_dir: Directory to save screenshots
        
    Returns:
        Path to the saved screenshot
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = experiment_name.replace(" ", "_").replace("/", "_")
    filename = f"{safe_name}_{timestamp}.png"
    output_path = os.path.join(output_dir, filename)
    
    success = capture_dashboard_screenshot(output_path)
    
    return output_path if success else ""


def main():
    """CLI interface for taking dashboard screenshots."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Capture dashboard screenshot")
    parser.add_argument("--output", "-o", default="dashboard_screenshot.png",
                       help="Output file path")
    parser.add_argument("--url", default="http://localhost:8080",
                       help="Dashboard URL")
    parser.add_argument("--wait", type=float, default=3.0,
                       help="Seconds to wait for rendering")
    parser.add_argument("--width", type=int, default=1400,
                       help="Screenshot width")
    parser.add_argument("--height", type=int, default=1200,
                       help="Screenshot height")
    parser.add_argument("--timeout", type=int, default=120000,
                       help="Timeout in milliseconds (default: 120000 = 2 minutes)")
    parser.add_argument("--retries", type=int, default=3,
                       help="Number of retry attempts (default: 3)")
    args = parser.parse_args()
    
    logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')
    
    success = capture_dashboard_screenshot(
        args.output,
        dashboard_url=args.url,
        wait_seconds=args.wait,
        width=args.width,
        height=args.height,
        timeout_ms=args.timeout,
        retries=args.retries,
    )
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

