#!/usr/bin/env python3
import os
import subprocess
from pathlib import PosixPath

WORKSPACE_DIR = PosixPath("/workspace")
TARGET_RELEASE_VERSION = "13.0.2"
TARGET_RELEASE_HASH = "26816849631"


def download_release():
    target_path = WORKSPACE_DIR / "grafana"
    target_path.mkdir(parents=True, exist_ok=True)

    subprocess.run(
        [
            "curl",
            "--silent",
            "--show-error",
            "--fail",
            "-L",
            "-o",
            f"/tmp/grafana_{TARGET_RELEASE_VERSION}_{TARGET_RELEASE_HASH}_linux_amd64.tar.gz",
            f"https://dl.grafana.com/grafana/release/{TARGET_RELEASE_VERSION}/"
            f"grafana_{TARGET_RELEASE_VERSION}_{TARGET_RELEASE_HASH}_linux_amd64.tar.gz",
        ],
        check=True,
    )

    subprocess.run(
        [
            "tar",
            "-C",
            target_path.as_posix(),
            "-xf",
            f"/tmp/grafana_{TARGET_RELEASE_VERSION}_{TARGET_RELEASE_HASH}_linux_amd64.tar.gz",
            "--strip-components=1",
        ],
        check=True,
    )
    os.remove(f"/tmp/grafana_{TARGET_RELEASE_VERSION}_{TARGET_RELEASE_HASH}_linux_amd64.tar.gz")


def main():
    if not WORKSPACE_DIR.is_dir():
        print(f"Skipping setup, workspace does not exist: {WORKSPACE_DIR}")
        return

    download_release()


if __name__ == "__main__":
    main()
