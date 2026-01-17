import logging
import os
from datetime import datetime

logger = logging.getLogger(__name__)


class ResultsWriter:
    def save(
        self,
        results: list,
        config: dict,
        output_file: str,
        append: bool = False,
        timeseries_file: str = None,
    ):
        dirname = os.path.dirname(output_file)
        if dirname:
            os.makedirs(dirname, exist_ok=True)
        mode = "a" if append else "w"

        with open(output_file, mode) as f:
            if not append:
                f.write(f"# Benchmark run at {datetime.now()}\n\n")
            f.write(
                "Manual statistics computation has been disabled. Please refer to Promethues/Grafana for experimental results.\n\n"
            )

            for r in results:
                if "error" in r:
                    f.write(f"- Run failed: {r.get('error')}\n")
                else:
                    batch_size = r.get("batch_size", "n/a")
                    concurrency = r.get("concurrency", "n/a")
                    f.write(
                        f"- Run completed: batch_size={batch_size}, concurrency={concurrency}, "
                        f"{r.get('num_requests')} requests in {r.get('total_time_s', 0):.2f}s\n"
                    )

        logger.info(f"Simple run log saved to {output_file}. Check Grafana for metrics.")
