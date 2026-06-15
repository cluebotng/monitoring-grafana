#!/usr/bin/env python3
import configparser
import io
import os
from pathlib import PosixPath


def generate_configuration(persistent_path: PosixPath) -> str:
    tools_db_user = os.environ.get("TOOL_TOOLSDB_USER")
    if not tools_db_user:
        raise RuntimeError("Missing TOOL_TOOLSDB_USER")

    tools_db_password = os.environ.get("TOOL_TOOLSDB_PASSWORD")
    if not tools_db_password:
        raise RuntimeError("Missing TOOL_TOOLSDB_PASSWORD")

    config = configparser.ConfigParser()
    config["database"] = {
        "type": "mysql",
        "host": "tools-db",
        "name": f"{tools_db_user}__grafana",
        "user": tools_db_user,
        "password": tools_db_password,
        "max_idle_conn": 0,
        "conn_max_lifetime": 0,
    }
    config["users"] = {
        "allow_sign_up": False,
    }
    config["auth.anonymous"] = {
        "enabled": True,
        "hide_version": True,
        "org_name": "Main Org.",
        "org_role": "Viewer",
    }

    config["paths"] = {
        "data": (persistent_path / "data").as_posix(),
        "plugins": (persistent_path / "plugins").as_posix(),
        "provisioning": (persistent_path / "provisioning").as_posix(),
    }

    with io.StringIO() as fh:
        config.write(fh)
        fh.seek(0)
        return fh.read()


def main():
    persistent_path = PosixPath(os.environ.get("TOOL_DATA_DIR")) / "persistent-data" / "grafana"
    persistent_path.mkdir(parents=True, exist_ok=True)

    with open("/tmp/grafana.ini", "w") as fh:
        fh.write(generate_configuration(persistent_path))

    return os.execv(
        "/workspace/grafana/bin/grafana",
        [
            "/workspace/grafana/bin/grafana",
            "server",
            "--config",
            "/tmp/grafana.ini",
            "--homepath",
            "/workspace/grafana",
        ],
    )


if __name__ == "__main__":
    main()
