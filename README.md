[![GPLv3 license](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://github.com/pySourceSDK/ValveSMD/blob/master/LICENSE.txt)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/valvesmd.svg)](https://pypi.python.org/pypi/valvesmd/)
[![PyPI version fury.io](https://badge.fury.io/py/valvesmd.svg)](https://pypi.python.org/pypi/valvesmd/)
[![alt text](https://github.com/pySourceSDK/ValveSMD/blob/master/docs/source/coverage.svg "coverage")]()

# ValveSMD

ValveSMD is a Python library for parsing .smd files for the Source Engine. It provides ways to read, modify and write smd files.

Full documentation: https://pysourcesdk.github.io/ValveSMD/

## Installation

### PyPI

ValveSMD is available on the Python Package Index. This makes installing it with pip as easy as:

```bash
pip3 install valvesmd
```

### Git

If you want the latest code or even feel like contributing, the code is available on GitHub.

You can easily clone the code with git:

```bash
git clone git@github.com:pySourceSDK/ValveSMD.git
```

and install it with:

```bash
python3 setup.py install
```

## Usage

Here's a few example usage of valveSmd

### Parsing

Parsing can be done by creating an instance of Smd with a path.

```python
>>> from valvesmd import Smd
>>> smd = Smd('C:/modelsrc/tf/props_mining/rock005.smd')
```

### Utility functions

A few function are provided to perform basic transformations

```python
>>> from valvesmd import *
>>> SmdScale(smd, 2) # 2x scale
>>> SmdMirror(smd, 'x') # 'x', 'y' or 'z'
>>> SmdMatReplace(smd, 'wood', 'metal') # replace a material name
```