"""Tests for sweep utilities."""

from src.models.sweep import expand_sweep_config, get_sweep_name


class TestExpandSweepConfig:
    def test_no_sweep_params(self):
        """Test config with no sweep parameters."""
        config = {"model": {"name": "test-model"}}
        expanded = expand_sweep_config(config)
        assert len(expanded) == 1
        assert expanded[0] == config

    def test_backend_sweep(self):
        """Test expanding backend sweep."""
        config = {
            "model": {
                "name": "test-model",
                "backend": ["pytorch", "mps", "mlx"],
            }
        }
        expanded = expand_sweep_config(config)
        assert len(expanded) == 3
        assert expanded[0]["model"]["backend"] == "pytorch"
        assert expanded[1]["model"]["backend"] == "mps"
        assert expanded[2]["model"]["backend"] == "mlx"

    def test_timeout_sweep(self):
        """Test expanding timeout sweep."""
        config = {
            "batching": {
                "timeout_ms": [50, 100, 200],
            }
        }
        expanded = expand_sweep_config(config)
        assert len(expanded) == 3
        assert expanded[0]["batching"]["timeout_ms"] == 50
        assert expanded[1]["batching"]["timeout_ms"] == 100
        assert expanded[2]["batching"]["timeout_ms"] == 200

    def test_batch_size_sweep(self):
        """Test expanding batch size sweep."""
        config = {
            "batching": {
                "max_batch_size": [8, 16, 32],
            }
        }
        expanded = expand_sweep_config(config)
        assert len(expanded) == 3
        assert expanded[0]["batching"]["max_batch_size"] == 8
        assert expanded[1]["batching"]["max_batch_size"] == 16
        assert expanded[2]["batching"]["max_batch_size"] == 32

    def test_multiple_sweeps(self):
        """Test expanding multiple sweep parameters."""
        config = {
            "model": {
                "backend": ["pytorch", "mps"],
            },
            "batching": {
                "timeout_ms": [50, 100],
            },
        }
        expanded = expand_sweep_config(config)
        # Should have 2 * 2 = 4 combinations
        assert len(expanded) == 4

        # Check all combinations exist
        backends = [c["model"]["backend"] for c in expanded]
        timeouts = [c["batching"]["timeout_ms"] for c in expanded]

        assert "pytorch" in backends
        assert "mps" in backends
        assert 50 in timeouts
        assert 100 in timeouts

    def test_sweep_preserves_other_config(self):
        """Test that sweep preserves other configuration."""
        config = {
            "model": {
                "name": "test-model",
                "backend": ["pytorch", "mps"],
                "device": "cpu",
            },
            "server": {
                "port": 50051,
            },
        }
        expanded = expand_sweep_config(config)
        assert len(expanded) == 2

        # All configs should preserve other fields
        for c in expanded:
            assert c["model"]["name"] == "test-model"
            assert c["model"]["device"] == "cpu"
            assert c["server"]["port"] == 50051


class TestGetSweepName:
    def test_name_with_backend(self):
        """Test generating name with backend."""
        config = {"model": {"backend": "pytorch"}}
        name = get_sweep_name(config, "base")
        assert "base" in name
        assert "pytorch" in name

    def test_name_with_timeout(self):
        """Test generating name with timeout."""
        config = {"batching": {"timeout_ms": 100}}
        name = get_sweep_name(config, "base")
        assert "base" in name
        assert "100ms" in name

    def test_name_with_batch_size(self):
        """Test generating name with batch size."""
        config = {"batching": {"max_batch_size": 16}}
        name = get_sweep_name(config, "base")
        assert "base" in name
        assert "batch16" in name

    def test_name_with_multiple_params(self):
        """Test generating name with multiple parameters."""
        config = {
            "model": {"backend": "mps"},
            "batching": {"timeout_ms": 100, "max_batch_size": 16},
        }
        name = get_sweep_name(config, "base")
        assert "base" in name
        assert "mps" in name
        assert "100ms" in name
        assert "batch16" in name

    def test_name_without_sweep_params(self):
        """Test generating name without sweep parameters."""
        config = {"model": {"name": "test-model"}}
        name = get_sweep_name(config, "base")
        assert name == "base"
