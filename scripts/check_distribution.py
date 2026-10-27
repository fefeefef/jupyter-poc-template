"""Install the built wheel in a fresh environment and exercise its public API."""

import subprocess
import sys
import tempfile
import venv
from pathlib import Path


def main() -> None:
    """Verify exactly one wheel from dist/ without importing the source checkout."""
    root = Path(__file__).resolve().parents[1]
    wheels = sorted((root / "dist").glob("*.whl"))
    if len(wheels) != 1:
        raise SystemExit(
            "Expected exactly one wheel in dist/; remove stale builds and run uv build."
        )
    with tempfile.TemporaryDirectory(prefix="package-smoke-") as temporary:
        work = Path(temporary)
        environment = work / "venv"
        # Match the venv CLI: POSIX symlinks also support uv-managed Python builds.
        venv.EnvBuilder(with_pip=True, symlinks=sys.platform != "win32").create(environment)
        python = environment / ("Scripts/python.exe" if sys.platform == "win32" else "bin/python")
        subprocess.run(
            [
                str(python),
                "-m",
                "pip",
                "install",
                "--disable-pip-version-check",
                "--no-cache-dir",
                "--no-deps",
                "--no-index",
                str(wheels[0]),
            ],
            cwd=work,
            check=True,
        )
        subprocess.run(
            [
                str(python),
                "-I",
                "-c",
                'from project_name import greet; assert greet("NXAI") == "Hello, NXAI!"',
            ],
            cwd=work,
            check=True,
        )
    print("Built wheel installed successfully; the README quickstart passed.")


if __name__ == "__main__":
    main()
