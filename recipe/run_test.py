import os
from pathlib import Path
import subprocess
import sys

prefix = Path(os.environ["PREFIX"])
libs = ["event", "event_core", "event_extra", "event_openssl"]
if sys.platform != "win32":
    libs.append("event_pthreads")

for lib in libs:
    if sys.platform == "win32":
        assert (prefix / "Library" / "lib" / f"{lib}.lib").is_file()
        assert (prefix / "Library" / "bin" / f"{lib}.dll").is_file()
    else:
        suffix = "dylib" if sys.platform == "darwin" else "so"
        assert (prefix / "lib" / f"lib{lib}.{suffix}").is_file()
        assert not (prefix / "lib" / f"lib{lib}.a").exists()
    subprocess.run(
        ["pkg-config", "--print-errors", f"--exact-version={os.environ['PKG_VERSION']}", f"lib{lib}"],
        check=True,
    )
