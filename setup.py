# This file is for creating a build for the game (Located in the 'build' folder).
from cx_Freeze import setup, Executable
import sys
sys.path.append("res"); #Change path to the modules folder.

setup(
    name = "Rocket Pal",
    version = "1.0",
    description = "Fun addicive rocket game, try to get the highscore!",
    options={"build_exe": {"packages":["pygame"],
                           "include_files":["res/"],
                           "includes":["modules.GameObject", "modules.GUI", "modules.TextBox"]
                           }},
    executables = [Executable("RocketPal.py")])
