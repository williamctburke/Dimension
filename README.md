
## Stand-alone Version ##
### Installation ###
Check inside the `standalone` folder. If there is a `build` folder, then the stand-alone executables were included with this distribution.
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

If the executable has DLL or import errors when run, there may be missing imports. In the `python_src` folder there should be `.spec` files with the same name as the build executables.
Add the following path to the `pathex` variable to fix missing Scipy DLLs. The actual path varies depending on where your files are installed.
```python
pathex=['\\Dimension\\python_src',
        '~\\Python36\\Lib\\site-packages\\scipy\\extra-dll']
```
For missing imports, add the desired import to the `hidden-imports` variable
```python
hiddenimports=['scipy._lib.messagestream']
```
After these modifications make sure to call `pyinstaller main.spec` instead of `main.py`, or your changes to the `.spec` file will be overwritten.

## Python Version ##
### Dependencies ###
Before using the Python version, ensure the following packages are installed and visible to your Python distribution. The Anaconda distribution is an easy way to set this up.
* `numpy`
* `scipy`
* `matplotlib`
* `xlwings`

### Installation ###
By default the Python files are in the `python_src` directory.
Open `Dimension.xlsm` to begin using the tool.
If you are moving the tool, please ensure `Dimension.xlsm` is in the same folder as the other Python files such as `main.py` and `plot.py`. 

### Resources ###
Below are references for various packages used in the code.

* [matplotlib](https://matplotlib.org/users/index.html)
* [numpy](https://docs.scipy.org/doc/numpy/reference/)
* [xlwings](http://docs.xlwings.org/en/stable/quickstart.html)
* [pyinstaller](https://pyinstaller.readthedocs.io/en/v3.3.1/)
* [scipy.stats](https://docs.scipy.org/doc/scipy/reference/stats.html)
