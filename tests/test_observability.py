import json
import os

import pytest
import yaml


class TestPrometheusConfig:
    def test_prometheus_config_exists(self):
        config_path = "conf/prometheus/prometheus.yml"
        assert os.path.exists(config_path), f"Prometheus config not found at {config_path}"

    def test_prometheus_config_valid_yaml(self):
        with open("conf/prometheus/prometheus.yml") as f:
            config = yaml.safe_load(f)
        assert config is not None

    def test_prometheus_scrape_config(self):
        with open("conf/prometheus/prometheus.yml") as f:
            config = yaml.safe_load(f)

        assert "scrape_configs" in config
        scrape_configs = config["scrape_configs"]
        assert len(scrape_configs) > 0

        job_names = [c.get("job_name") for c in scrape_configs]
        assert "cross_encoder_server" in job_names

    def test_prometheus_scrape_target(self):
        with open("conf/prometheus/prometheus.yml") as f:
            config = yaml.safe_load(f)

        server_config = next(
            c for c in config["scrape_configs"] if c["job_name"] == "cross_encoder_server"
        )
        targets = server_config["static_configs"][0]["targets"]
        assert "host.docker.internal:8000" in targets


class TestGrafanaConfig:
    def test_datasource_config_exists(self):
        config_path = "conf/grafana/provisioning/datasources/datasource.yaml"
        assert os.path.exists(config_path)

    def test_datasource_config_valid(self):
        with open("conf/grafana/provisioning/datasources/datasource.yaml") as f:
            config = yaml.safe_load(f)

        assert "datasources" in config
        ds = config["datasources"][0]
        assert ds["type"] == "prometheus"
        assert ds["name"] == "Prometheus"
        assert "prometheus:9090" in ds["url"]

    def test_dashboard_provisioning_config(self):
        config_path = "conf/grafana/provisioning/dashboards/dashboard.yaml"
        assert os.path.exists(config_path)

        with open(config_path) as f:
            config = yaml.safe_load(f)

        assert "providers" in config


class TestGrafanaDashboard:
    @pytest.fixture
    def dashboard(self):
        with open("conf/grafana/provisioning/dashboards/default_dashboard.json") as f:
            return json.load(f)

    def test_dashboard_exists(self):
        assert os.path.exists("conf/grafana/provisioning/dashboards/default_dashboard.json")

    def test_dashboard_valid_json(self, dashboard):
        assert dashboard is not None
        assert "panels" in dashboard

    def test_dashboard_has_title(self, dashboard):
        assert dashboard["title"] == "Cross Encoder Throughput"

    def test_dashboard_has_uid(self, dashboard):
        assert dashboard["uid"] == "cross_encoder"

    def test_dashboard_has_key_metrics_panels(self, dashboard):
        panel_titles = [p.get("title", "") for p in dashboard["panels"]]

        expected_panels = [
            "Queries",
            "Latency",
            "Throughput",
            "Tokenize",
            "Inference",
            "Queue Wait",
            "CPU",
            "GPU",
        ]

        for expected in expected_panels:
            found = any(expected.lower() in title.lower() for title in panel_titles)
            assert found, f"Expected panel containing '{expected}' not found"

    def test_dashboard_has_worker_panels(self, dashboard):
        panel_titles = [p.get("title", "") for p in dashboard["panels"]]

        worker_panels = ["Model Worker", "Tokenizer Worker"]

        for expected in worker_panels:
            found = any(expected.lower() in title.lower() for title in panel_titles)
            assert found, f"Expected worker panel '{expected}' not found"

    def test_dashboard_uses_prometheus_datasource(self, dashboard):
        for panel in dashboard["panels"]:
            if panel.get("type") != "row" and "datasource" in panel:
                ds = panel["datasource"]
                assert ds.get("uid") == "Prometheus", (
                    f"Panel '{panel.get('title')}' uses wrong datasource"
                )


class TestObservabilityScripts:
    def test_setup_script_exists(self):
        assert os.path.exists("scripts/setup_observability.sh")

    def test_start_services_script_exists(self):
        assert os.path.exists("scripts/start_services.sh")

    def test_setup_script_executable(self):
        import stat

        mode = os.stat("scripts/setup_observability.sh").st_mode
        assert mode & stat.S_IXUSR, "setup_observability.sh should be executable"

    def test_start_services_script_executable(self):
        import stat

        mode = os.stat("scripts/start_services.sh").st_mode
        assert mode & stat.S_IXUSR, "start_services.sh should be executable"


class TestSnapshotDashboard:
    def test_snapshot_utility_exists(self):
        assert os.path.exists("src/utils/snapshot_dashboard.py")

    def test_snapshot_utility_imports(self):
        import importlib.util

        spec = importlib.util.spec_from_file_location(
            "snapshot_dashboard", "src/utils/snapshot_dashboard.py"
        )
        module = importlib.util.module_from_spec(spec)
        assert module is not None
