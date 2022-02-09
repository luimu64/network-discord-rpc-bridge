import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == "win32":
    base = "Win32GUI"

target = Executable(
    "app.py",
    base=base,
    icon="icon.ico"
)

setup(
    name="rpc-bridge",
    version="0.1",
    description="Program for bridging rpc between vm and host",
    options={"build_exe": {
        "optimize": 2,
        "include_files": ["icon.png", "config.ini"]
    }},
    executables=[target]
)
