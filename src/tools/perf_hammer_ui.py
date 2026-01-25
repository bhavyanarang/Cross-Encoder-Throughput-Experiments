import logging
import sys
import threading
import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk

sys.path.append(str(Path(__file__).resolve().parents[2]))

from src.tools.perf_hammer import PerfHammer


class PerfHammerUI:
    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        self.hammer: PerfHammer | None = None
        self.worker_thread: threading.Thread | None = None
        self.is_running = False
        self.run_done = False

        self.root = tk.Tk()
        self.root.title("PerfHammer UI")
        self.root.resizable(False, False)

        self.status_var = tk.StringVar(value="Idle")
        self.stats_var = tk.StringVar(value="")
        self.mode_var = tk.StringVar(value="duration")

        self.fields: dict[str, ttk.Entry] = {}
        self.mode_select: ttk.Combobox | None = None
        self.start_button: ttk.Button | None = None
        self.stop_button: ttk.Button | None = None

        self._build_layout()
        self._update_mode_fields()
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
        self._schedule_stats_update()

    def run(self) -> None:
        self.root.mainloop()

    def _build_layout(self) -> None:
        frame = ttk.Frame(self.root, padding=12)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.columnconfigure(1, weight=1)

        row = 0
        row = self._add_field(frame, "Host", "host", "localhost", row)
        row = self._add_field(frame, "Port", "port", "50051", row)
        row = self._add_field(frame, "Users", "concurrency", "256", row)
        row = self._add_field(frame, "Batch size", "batch_size", "64", row)
        row = self._add_field(frame, "Target RPS", "target_rps", "", row)

        ttk.Label(frame, text="Stop after").grid(row=row, column=0, sticky="w", pady=4)
        self.mode_select = ttk.Combobox(
            frame,
            textvariable=self.mode_var,
            values=("duration", "requests"),
            state="readonly",
            width=22,
        )
        self.mode_select.grid(row=row, column=1, sticky="ew", pady=4)
        self.mode_select.bind("<<ComboboxSelected>>", self._on_mode_selected)
        row += 1

        row = self._add_field(frame, "Duration (s)", "duration", "60", row)
        row = self._add_field(frame, "Requests", "requests", "", row)

        ttk.Separator(frame, orient="horizontal").grid(
            row=row, column=0, columnspan=2, sticky="ew", pady=8
        )
        row += 1

        self.start_button = ttk.Button(frame, text="Start", command=self._on_start)
        self.start_button.grid(row=row, column=0, sticky="ew", pady=4)

        self.stop_button = ttk.Button(frame, text="Stop", command=self._on_stop, state="disabled")
        self.stop_button.grid(row=row, column=1, sticky="ew", pady=4)
        row += 1

        ttk.Label(frame, textvariable=self.status_var).grid(
            row=row, column=0, columnspan=2, sticky="w"
        )
        row += 1

        ttk.Label(frame, textvariable=self.stats_var, justify="left").grid(
            row=row, column=0, columnspan=2, sticky="w"
        )

    def _add_field(self, parent: ttk.Frame, label: str, key: str, default: str, row: int) -> int:
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky="w", pady=4)
        entry = ttk.Entry(parent, width=24)
        entry.insert(0, default)
        entry.grid(row=row, column=1, sticky="ew", pady=4)
        self.fields[key] = entry
        return row + 1

    def _on_mode_selected(self, _: tk.Event) -> None:
        if not self.is_running:
            self._update_mode_fields()

    def _update_mode_fields(self) -> None:
        mode = self.mode_var.get()
        duration_state = "normal" if mode == "duration" else "disabled"
        requests_state = "normal" if mode == "requests" else "disabled"
        self.fields["duration"].configure(state=duration_state)
        self.fields["requests"].configure(state=requests_state)

    def _set_controls_state(self, running: bool) -> None:
        self.is_running = running
        entry_state = "disabled" if running else "normal"
        for entry in self.fields.values():
            entry.configure(state=entry_state)

        if self.mode_select:
            self.mode_select.configure(state="disabled" if running else "readonly")

        if self.start_button:
            self.start_button.configure(state="disabled" if running else "normal")

        if self.stop_button:
            self.stop_button.configure(state="normal" if running else "disabled")

        if not running:
            self._update_mode_fields()

    def _parse_int(self, key: str, minimum: int | None = None) -> int:
        raw = self.fields[key].get().strip()
        if not raw:
            raise ValueError(f"{key} is required")
        value = int(raw)
        if minimum is not None and value < minimum:
            raise ValueError(f"{key} must be >= {minimum}")
        return value

    def _parse_float(self, key: str, minimum: float | None = None) -> float:
        raw = self.fields[key].get().strip()
        if not raw:
            raise ValueError(f"{key} is required")
        value = float(raw)
        if minimum is not None and value < minimum:
            raise ValueError(f"{key} must be >= {minimum}")
        return value

    def _parse_float_optional(self, key: str, minimum: float | None = None) -> float | None:
        raw = self.fields[key].get().strip()
        if not raw:
            return None
        value = float(raw)
        if minimum is not None and value < minimum:
            raise ValueError(f"{key} must be >= {minimum}")
        return value

    def _build_hammer(self) -> PerfHammer:
        host = self.fields["host"].get().strip() or "localhost"
        port = self._parse_int("port", minimum=1)
        concurrency = self._parse_int("concurrency", minimum=1)
        batch_size = self._parse_int("batch_size", minimum=1)
        target_rps = self._parse_float_optional("target_rps", minimum=0.0)

        duration = None
        requests = None
        if self.mode_var.get() == "duration":
            duration = self._parse_float("duration", minimum=0.1)
        else:
            requests = self._parse_int("requests", minimum=1)

        return PerfHammer(
            host=host,
            port=port,
            concurrency=concurrency,
            batch_size=batch_size,
            duration=duration,
            num_requests=requests,
            target_rps=target_rps,
        )

    def _on_start(self) -> None:
        if self.worker_thread and self.worker_thread.is_alive():
            return

        try:
            self.hammer = self._build_hammer()
        except ValueError as exc:
            messagebox.showerror("Invalid input", str(exc))
            return

        self.status_var.set("Running")
        self.run_done = False
        self._set_controls_state(True)
        self.worker_thread = threading.Thread(target=self._run_hammer, daemon=True)
        self.worker_thread.start()

    def _run_hammer(self) -> None:
        try:
            if self.hammer:
                self.hammer.run()
        except Exception:
            self.logger.exception("PerfHammer run failed")
        finally:
            self.run_done = True

    def _on_run_finished(self) -> None:
        self.status_var.set("Completed")
        self._set_controls_state(False)
        self.run_done = False

    def _on_stop(self) -> None:
        if self.hammer:
            self.status_var.set("Stopping")
            self.hammer.stop()

    def _schedule_stats_update(self) -> None:
        self._update_stats()
        self.root.after(500, self._schedule_stats_update)

    def _update_stats(self) -> None:
        if self.run_done:
            self._on_run_finished()

        if not self.hammer:
            self.stats_var.set("")
            return

        snapshot = self.hammer.stats_snapshot()
        if not snapshot:
            self.stats_var.set("")
            return

        stats = (
            f"Elapsed: {snapshot['elapsed_s']:.1f}s | Requests: {snapshot['total_requests']} | "
            f"Errors: {snapshot['errors']}\n"
            f"QPS: {snapshot['qps']:.1f} | Throughput: {snapshot['throughput']:.1f} pairs/s\n"
            f"Latency (ms): avg {snapshot['lat_avg_ms']:.1f} | "
            f"p50 {snapshot['lat_p50_ms']:.1f} | "
            f"p95 {snapshot['lat_p95_ms']:.1f} | "
            f"p99 {snapshot['lat_p99_ms']:.1f}"
        )
        self.stats_var.set(stats)

    def _on_close(self) -> None:
        if self.hammer and self.is_running:
            self.hammer.stop()
        self.root.destroy()


def main() -> None:
    ui = PerfHammerUI()
    ui.run()


if __name__ == "__main__":
    main()
