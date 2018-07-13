"""
== SETUP.PY FILE FOR USE WITH CX_FREEZE AND PYTHON 3.6 ==
==== INSTRUCTIONS  ====
1. Make sure you have Python 3.6 installed.
2. Install cx_Freeze by typing `pip install cx_freeze` in the Terminal or Command Prompt. Make sure to use the pip for Python 3 (sometimes called pip3)
3. Create a new file called setup.py and paste the contents of this file in it (or just download this file)
4. Make sure to place the setup.py file in the same directory where your main Python application is located
5. From the Terminal/Command Prompt, run `python setup.py build`. Make sure that you're running Python 3.6 (use `python --version`)
6. Enjoy!
The script should have created another folder called `build/`. You will find your generated .exe file.
"""

from cx_Freeze import setup, Executable

base = None
executables = [Executable("main.py", base=base), 
               Executable("plot.py", base=base)]

packages = ["idna"]
additonal_mods = ['numpy.core._methods',
                  'matplotlib.backends.backend_tkagg']
#exclude_mods = []
options = {
    'build_exe': {
        'packages':packages,
        'includes': additonal_mods,
#        "excludes": exclude_mods,
        'build_exe':'..\\build\\'
    },
}

setup(
    name = "main",
    options = options,
    version = "0.1.0.0",
    description = 'Tolerance stackup analysis build to integrate with Excel',
    executables = executables
)
