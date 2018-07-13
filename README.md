
## Stand-alone Version ##
### Installation ###
Check inside the `standalone` folder, if there is a `build` folder, then the stand-alone build was included with this distribution.
If not, the stand-alone executables need to be built according to the instructions in the next section.
Open `Dimension_standalone.xlsm` to use the tool.
If you are moving the tool, please ensure `Dimension_standalone.xlsm` is in the same folder as the `build` folder.

### Building the stand-alone ###
A stand-alone build may not be provided with this distribution.
To build the stand-alone executables, you need Python and all the depdencies listed in the dependencies section.
The recommended way to build the executables is through pyinstaller.
From the `python_src` folder, call the following commands in your command prompt.
```Shell
	pip install pyinstaller
	pyinstaller main.py
	pyinstaller plot.py
```
The stand-alone output should be in a directory called `build`.
Ensure `Dimension_standalone.xlsm` is in the same folder as the `build` folder.

## Python Version ##
### Dependencies ###
Before using the Python version, ensure the following packages are installed and visible to your Python distribution.
* `numpy`
* `matplotlib`
* `xlwings`

### Installation ###
By default the Python files are in the `python_src` directory.
Open `Dimension.xlsm` to begin using the tool.
If you are moving the tool, please ensure `Dimension.xlsm` is in the same folder as the other Python files such as `main.py` and `plot.py`. 

### Resources ###
Below are references for various packages used in the code.
https://matplotlib.org/users/index.html
https://docs.scipy.org/doc/numpy/reference/
http://docs.xlwings.org/en/stable/quickstart.html
https://pyinstaller.readthedocs.io/en/v3.3.1/
