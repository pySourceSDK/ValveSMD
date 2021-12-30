Quickstart
==========

Get yourself up and running quickly.

Installation
------------

PyPI
~~~~
ValveSMD is available on the Python Package Index. This makes installing it with pip as easy as:

.. code-block:: bash

   pip3 install valvesmd

Git
~~~

If you want the latest code or even feel like contributing, the code is available on GitHub.

You can easily clone the code with git:

.. code-block:: bash

   git clone git://github.com/pySourceSDK/ValveSMD.git

and install it from the repo directory with:

.. code-block:: bash

   python3 setup.py install

Usage
-----

Here's a few example usage of ValveSMD

Parsing
~~~~~~~

Parsing can be done by creating an instance of Smd with a path.

.. code-block:: python

   > from valvesmd import Smd, SmdMirror

   > smd = Smd('C:/modelsrc/tf/props_forest/rock_005.smd')
   > SmdMirror(smd, 'x')
   > smd.save()
