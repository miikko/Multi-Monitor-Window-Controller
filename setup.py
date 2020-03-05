import sys
from cx_Freeze import setup, Executable

build_exe_options = {"packages": ["keyboard", "pywin32"]}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="TBD",
    version="0.01",
    description="TODO: Write description",
    options={"build_exe": build_exe_options},
    executables=[Executable("gui/application.py", base=base)],
)
