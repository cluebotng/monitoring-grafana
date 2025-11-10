# Grafana

This is a hack to get `grafana` into a container using `pack` so it can be deployed on Toolforge.

Runtime configuration is managed by `scripts/entrypoint.py`

## Production configuration

* `TOOL_TOOLSDB_USER` - MySQL username
* `TOOL_TOOLSDB_PASSWORD` - MySQL password
