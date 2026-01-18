import logging
import sys
import time
from pathlib import Path

# Add project root to sys.path
sys.path.append(str(Path(__file__).resolve().parents[2]))

import requests

from src.server.services.metrics_service import MetricsService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_metrics_endpoint():
    port = 8010
    service = MetricsService(prometheus_port=port)
    service.start()

    try:
        time.sleep(2)

        service.record(100.0, 5)
        service.record(50.0, 1)
        service.record_stage_timings(t_model_inference=20.0)

        url = f"http://localhost:{port}"
        logger.info(f"Fetching metrics from {url}")

        response = requests.get(url)
        if response.status_code == 200:
            logger.info("Successfully fetched metrics!")
            logger.info("Content preview:")
            print("\n".join(response.text.split("\n")[:20]))

            if "request_count_total 6.0" in response.text:
                logger.info("SUCCESS: verified request_count updated")
            else:
                logger.error("FAILURE: request_count not found or incorrect")

            if "inference_latency_seconds_bucket" in response.text:
                logger.info("SUCCESS: verified histograms present")
            else:
                logger.error("FAILURE: histograms not found")

        else:
            logger.error(f"Failed to fetch metrics: {response.status_code}")

    except Exception as e:
        logger.error(f"Test failed with exception: {e}")
    finally:
        service.stop()


if __name__ == "__main__":
    test_metrics_endpoint()
