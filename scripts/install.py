#!/usr/bin/env python3
import os
import subprocess
from pathlib import PosixPath


def main():
    release_version, release_hash = "12.2.1", "18655849634"

    package_path = PosixPath("/workspace/monitoring_grafana")
    package_path.mkdir()
    (package_path / "__init__.py").open("w").close()

    target_path = PosixPath("/workspace/grafana")
    target_path.mkdir(parents=True, exist_ok=True)

    subprocess.run(
        [
            "curl",
            "--silent",
            "--show-error",
            "--fail",
            "-L",
            "-o",
            f"/tmp/grafana_{release_version}_{release_hash}_linux_amd64.tar.gz",
            f"https://dl.grafana.com/grafana/release/{release_version}/"
            f"grafana_{release_version}_{release_hash}_linux_amd64.tar.gz",
        ],
        check=True,
    )

    subprocess.run(
        [
            "tar",
            "-C",
            target_path.as_posix(),
            "-xf",
            f"/tmp/grafana_{release_version}_{release_hash}_linux_amd64.tar.gz",
            "--strip-components=1",
        ],
        check=True,
    )
    os.remove(f"/tmp/grafana_{release_version}_{release_hash}_linux_amd64.tar.gz")


if __name__ == "__main__":
    main()
