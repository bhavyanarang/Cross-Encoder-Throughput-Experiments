from src.server.dto.metrics import MetricsCollector
from src.server.services.metrics_service import MetricsService
from src.server.services.process_monitor_service import ProcessMonitorService


class TestProcessMonitorService:
    def test_process_monitor_init(self):
        monitor = ProcessMonitorService()
        cpu = monitor.get_cpu_percent()

        assert isinstance(cpu, float)
        assert cpu >= 0


class TestMetricsCollector:
    def test_metrics_collector_experiment_info(self):
        collector = MetricsCollector()
        collector.set_experiment_info(
            name="test-exp",
            description="Test experiment",
            backend="pytorch",
            device="cpu",
        )

        assert collector.experiment_name == "test-exp"
        assert collector.experiment_description == "Test experiment"
        assert collector.backend_type == "pytorch"
        assert collector.device == "cpu"

    def test_metrics_collector_gpu_memory(self):
        service = MetricsService()
        memory = service.get_gpu_memory_mb()

        assert isinstance(memory, float)
        assert memory >= 0
