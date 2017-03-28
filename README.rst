.. sectnum::

=======
pyplot
=======

Module to centralize plotting scripts.

In the `.config.cfg` file specified directories are made accessible via **pyplot**. If we have e.g. a directory */home/user/plotter*, scripts can be dumped into the *plotter* folder and then be launched centrally with the **pyplot** script via:

.. code:: bash

    $ pyplot SCRIPTNAME {COMMAND LINE PARAMETERES}

It is also possible to structure them in *subfolders* and launch them via:

.. code:: bash

    $ pyplot subfolder SCRIPTNAME {COMMAND LINE PARAMETERES}

Before scripts are available he command:

.. code:: bash

    $ pyplot configure update

has to be used, to make the module aware of the new script. It turns the directories, e.g. *plotter*, into modules by creating a ``__init__.py`` file. Currently existing ``__init__.py`` files will be overwritten.

-------------------------

Developement state
====================


The script can currently be installed with the `setup.py` script. It would however advise to only use:

.. code:: bash

    $ python setup develop

This is the only thing I tried so far. If it is installed, auto completion works. It is just a bit slow so far.

Issues:
----------

1. Currently a config file has to be created before the script can be used, even to add config entries.

-------------------------

Required structure for the scripts:
======================================

Currently the scripts to be launched form `pyplot` have to fulfill *either* of the following structures:

1. 
   i. Implement a function `get_parser(add_help)` which returns a `ArgumentParser` the argument parser 
      has to be created with `ArgumentParser(..., add_help=add_help)`. This is necessary that the parser 
      can be used as a parent. This way the help is also availible in the **pyplot** script.
   #. Implement a `main(args)` function which takes the namespace object which would be created by the 
      argument parser as argument.
#. 
   i. don't have a function `get_parser(add_help)`
   #. implement a function `main()` which doesn't need any arguments. `sys.argv` will be replaced 
      to mimic a native call.

Examples:
------------

1. Using `argparser`:

.. code:: python

   import argparse


   def get_parser(add_help=True):
       parser = argparse.ArgumentParser(description="an example", add_help=add_help)
       return parser


   def main(args):
       print('This is the main method which can use args')


   if __name__ == '__main__':
       PARSER = get_parser()
       ARGS = PARSER.parse_args()
       main(ARGS)

2. Without `argparser`:

.. code:: python

    import sys


    def main(args):
        print('This is the main method, proper sys.args are available')
        print(sys.args)


    if __name__ == '__main__':
        main()

-------------------------

Setting up argument completion:
==================================

The working version is to install the script and the use:

.. code:: bash

    $ eval "$(register-python-argcomplete pyplot)"


**Old**:


.. container:: strike

  To set up argument completion execute

  .. code:: bash

      $ eval "$(register-python-argcomplete pyplot.py)"

  or put it in your `.bash_rc`.

  Note that it doesn't properly work yet. You can only argument completion when you explicitly type the path,
  so e.g. `/home/user/pypot/pyplot.py` and `./pyplot.py`allow argument completion, but with `~/pyplot/pyplot.py`
  or an alias it doesn't work yet.


-------------------------

TODO:
==========


 - [X] fix config file issue
 - [O] speed up autocompletion, maybe a shelf is possible
 - [O] add test for `update clean` as files are removed
 - [O] make it stable (adding test)
 - [O] make the project structure more dynamic

   * [X] add config file to to specify included direcories
   * [X] include direcotories via config script
   * [O] allow root as well es subdirectories
   * [O] show status
   * [O] remove directories via config script

 - [X] allow subpoints to group scripts
 - [X] relax the structural requirements for the scripts (ArgumentParser optional)
 - [X] convert readme to `rst` for python

