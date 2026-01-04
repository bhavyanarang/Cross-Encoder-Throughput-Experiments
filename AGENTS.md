dont create docs or summary until asked
dont add doc strings or comments
follow architecture and DRY principle
use source venv to run anything (source .venv/bin/activate)
Run the experiments for any changes in the flow (even small subset is fine but we want to make sure the dashboard metrics and experiments don't break)
Code should be inside /src folder always, bash scripts in scripts
Follow best practices and DRY principle, dataclasses and models should be in separate files and the main classes should call others and be orchestrator and should not contain any other logical code.
Only use prometheus metrics for collection and grafana dashboard should have these metrics.
after the complete code changes run tests and fix in case they are failing for code changes (only once per request, again if they fail)
