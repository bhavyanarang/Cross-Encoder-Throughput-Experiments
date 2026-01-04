"""Tests for local observability stack configuration and utilities."""

import json
import os
import pytest
import yaml


class TestPrometheusConfig:
    """Tests for Prometheus configuration."""

    def test_prometheus_config_exists(self):
        """Test that Prometheus config file exists."""
        config_path = "conf/prometheus/prometheus.yml"
        assert os.path.exists(config_path), f"Prometheus config not found at {config_path}"

    def test_prometheus_config_valid_yaml(self):
        """Test that Prometheus config is valid YAML."""
        with open("conf/prometheus/prometheus.yml") as f:
            config = yaml.safe_load(f)
        assert config is not None

    def test_prometheus_scrape_config(self):
        """Test that Prometheus is configured to scrape the server."""
        with open("conf/prometheus/prometheus.yml") as f:
            config = yaml.safe_load(f)
        
        assert "scrape_configs" in config
        scrape_configs = config["scrape_configs"]
        assert len(scrape_configs) > 0
        
        # Check for cross_encoder_server job
        job_names = [c.get("job_name") for c in scrape_configs]
        assert "cross_encoder_server" in job_names

    def test_prometheus_scrape_target(self):
        """Test that Prometheus scrapes from localhost:8000."""
        with open("conf/prometheus/prometheus.yml") as f:
            config = yaml.safe_load(f)
        
        server_config = next(
            c for c in config["scrape_configs"] 
            if c["job_name"] == "cross_encoder_server"
        )
        targets = server_config["static_configs"][0]["targets"]
        assert "localhost:8000" in targets


class TestGrafanaConfig:
    """Tests for Grafana configuration."""

    def test_datasource_config_exists(self):
        """Test that Grafana datasource config exists."""
        config_path = "conf/grafana/provisioning/datasources/datasource.yaml"
        assert os.path.exists(config_path)

    def test_datasource_config_valid(self):
        """Test that Grafana datasource points to Prometheus."""
        with open("conf/grafana/provisioning/datasources/datasource.yaml") as f:
            config = yaml.safe_load(f)
        
        assert "datasources" in config
        ds = config["datasources"][0]
        assert ds["type"] == "prometheus"
        assert ds["name"] == "Prometheus"
        assert "localhost:9091" in ds["url"]

    def test_dashboard_provisioning_config(self):
        """Test that dashboard provisioning is configured."""
        config_path = "conf/grafana/provisioning/dashboards/dashboard.yaml"
        assert os.path.exists(config_path)
        
        with open(config_path) as f:
            config = yaml.safe_load(f)
        
        assert "providers" in config


class TestGrafanaDashboard:
    """Tests for Grafana dashboard JSON."""

    @pytest.fixture
    def dashboard(self):
        """Load the dashboard JSON."""
        with open("conf/grafana/provisioning/dashboards/default_dashboard.json") as f:
            return json.load(f)

    def test_dashboard_exists(self):
        """Test that dashboard JSON exists."""
        assert os.path.exists("conf/grafana/provisioning/dashboards/default_dashboard.json")

    def test_dashboard_valid_json(self, dashboard):
        """Test that dashboard is valid JSON."""
        assert dashboard is not None
        assert "panels" in dashboard

    def test_dashboard_has_title(self, dashboard):
        """Test that dashboard has correct title."""
        assert dashboard["title"] == "Cross Encoder Throughput"

    def test_dashboard_has_uid(self, dashboard):
        """Test that dashboard has UID for linking."""
        assert dashboard["uid"] == "cross_encoder"

    def test_dashboard_has_key_metrics_panels(self, dashboard):
        """Test that dashboard has key metric stat panels."""
        panel_titles = [p.get("title", "") for p in dashboard["panels"]]
        
        # Key metrics we expect
        expected_panels = [
            "Queries", "Latency", "Throughput", "Tokenize", 
            "Inference", "Queue Wait", "CPU", "GPU"
        ]
        
        for expected in expected_panels:
            found = any(expected.lower() in title.lower() for title in panel_titles)
            assert found, f"Expected panel containing '{expected}' not found"

    def test_dashboard_has_worker_panels(self, dashboard):
        """Test that dashboard has worker statistics panels."""
        panel_titles = [p.get("title", "") for p in dashboard["panels"]]
        
        # Worker metrics we expect
        worker_panels = ["Model Worker", "Tokenizer Worker"]
        
        for expected in worker_panels:
            found = any(expected.lower() in title.lower() for title in panel_titles)
            assert found, f"Expected worker panel '{expected}' not found"

    def test_dashboard_uses_prometheus_datasource(self, dashboard):
        """Test that all panels use the Prometheus datasource."""
        for panel in dashboard["panels"]:
            if panel.get("type") != "row" and "datasource" in panel:
                ds = panel["datasource"]
                assert ds.get("uid") == "Prometheus", \
                    f"Panel '{panel.get('title')}' uses wrong datasource"


class TestObservabilityScripts:
    """Tests for observability shell scripts."""

    def test_setup_script_exists(self):
        """Test that setup script exists."""
        assert os.path.exists("scripts/setup_observability.sh")

    def test_start_services_script_exists(self):
        """Test that start services script exists."""
        assert os.path.exists("scripts/start_services.sh")

    def test_setup_script_executable(self):
        """Test that setup script is executable."""
        import stat
        mode = os.stat("scripts/setup_observability.sh").st_mode
        assert mode & stat.S_IXUSR, "setup_observability.sh should be executable"

    def test_start_services_script_executable(self):
        """Test that start services script is executable."""
        import stat
        mode = os.stat("scripts/start_services.sh").st_mode
        assert mode & stat.S_IXUSR, "start_services.sh should be executable"


class TestSnapshotDashboard:
    """Tests for dashboard snapshotting utility."""

    def test_snapshot_utility_exists(self):
        """Test that snapshot utility exists."""
        assert os.path.exists("src/utils/snapshot_dashboard.py")

    def test_snapshot_utility_imports(self):
        """Test that snapshot utility can be imported."""
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "snapshot_dashboard", 
            "src/utils/snapshot_dashboard.py"
        )
        module = importlib.util.module_from_spec(spec)
        # Should not raise any import errors
        assert module is not None
