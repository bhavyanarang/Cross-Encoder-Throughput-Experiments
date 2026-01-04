import argparse
import logging
import time
import requests
import json
import sys

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

GRAFANA_URL = "http://localhost:3000"
API_KEY = ("admin", "admin")  # Basic auth

def get_dashboard_uid(title="Cross Encoder Throughput"):
    """Find dashboard UID by title"""
    try:
        resp = requests.get(f"{GRAFANA_URL}/api/search?query={title}", auth=API_KEY)
        resp.raise_for_status()
        dashboards = resp.json()
        if dashboards:
            return dashboards[0]['uid']
    except Exception as e:
        logger.warning(f"Could not search dashboards: {e}")
    return None

def create_snapshot(start_ts, end_ts, name="Experiment Snapshot"):
    """Create a local snapshot in Grafana"""
    try:
        # 1. Get the dashboard model
        uid = get_dashboard_uid()
        dashboard = {}
        
        if uid:
            resp = requests.get(f"{GRAFANA_URL}/api/dashboards/uid/{uid}", auth=API_KEY)
            if resp.status_code == 200:
                dashboard = resp.json().get('dashboard', {})
        
        if not dashboard:
            # If no dashboard exists yet, we can't really snapshot anything useful 
            # unless we upload a model.
            logger.error("No dashboard found to snapshot.")
            return None

        # 2. Prepare snapshot payload
        # Note: 'time' dict in dashboard JSON controls the time range for the snapshot
        dashboard['time'] = {
            "from": str(int(start_ts * 1000)),
            "to": str(int(end_ts * 1000))
        }
        
        payload = {
            "dashboard": dashboard,
            "name": name,
            "expires": 0,  # Never
            "external": False
        }

        # 3. Create snapshot
        resp = requests.post(f"{GRAFANA_URL}/api/snapshots", json=payload, auth=API_KEY)
        resp.raise_for_status()
        
        result = resp.json()
        url = result.get('url')
        key = result.get('key')
        logger.info(f"Snapshot created: {url}")
        return url

    except Exception as e:
        logger.error(f"Failed to create snapshot: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description="Snapshot Grafana Dashboard")
    parser.add_argument("--start", type=float, required=True, help="Start timestamp (epoch seconds)")
    parser.add_argument("--end", type=float, required=True, help="End timestamp (epoch seconds)")
    parser.add_argument("--name", type=str, default="Experiment Run", help="Snapshot name")
    
    args = parser.parse_args()
    
    # Wait a bit for metrics to be scraped
    logger.info("Waiting 5s for metrics propagation...")
    time.sleep(5)
    
    url = create_snapshot(args.start, args.end, args.name)
    if url:
        print(f"Grafana Snapshot: {url}")
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
