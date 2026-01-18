dont create docs or summary until asked
dont add doc strings or comments
No global variables in python, follow best coding practices
follow architecture and DRY principle
use source venv to run anything (source venv/bin/activate)
Run the experiments for any changes in the flow (even small subset is fine but we want to make sure the dashboard metrics and experiments don't break)
Code should be inside /src folder always, bash scripts in scripts
Follow best practices and DRY principle, dataclasses and models should be in separate files and the main classes should call others and be orchestrator and should not contain any other logical code.
Only use prometheus metrics for collection (usage guage, counter, histogram etc) and grafana dashboard for visualisation should have these metrics. Don't compute metrics manually.
Remove any dead code you find and reduce complexity too.
We should have Model pool and tokeniser pool metrics and also individual worker metrics too.
We should have tokeniser throughput, model throughput, model latency, tokeniser latency, request count, RPS, Pipeline wise latency, queue sizes, padding wastage, cpu usage, gpu usage, per worker qps
Experiments should be through hydra config and we should save experiment results and stats after the run
after the complete code changes run tests and fix in case they are failing for code changes (only once per request, again if they fail)
Don't just add random code changes and slop code, any code additions should be precise and have laser precision.
CODE IS A LIABILITY, WE SHOULD USE MINIMIUM NUMBER OF LINES OF CODE AND THE SHORTEST CODE APPROACH.
