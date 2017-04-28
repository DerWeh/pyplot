.. sectnum::

=======
pyplot
=======

.. sidebar:: TOC

  .. contents::
    :local:
    :backlinks: top


This modules main intend is to centralize plotting scripts.

I often have the problem that I create dozens of plotting scripts which are 
spread all over the file system. It is quite bothersome to keep track of them 
and launch them, as I always need to specify their path. Of course I could just 
dump them all in one directory and add it to my path. But I don't want to 
pollute my path and I want a better structure. This module is my attempt to do 
so.



Specified directories are made accessible via **pyplot**. If we have e.g. a 
directory */home/user/plotter*, scripts can be dumped into the *plotter* folder 
and then be launched centrally with the **pyplot** script via:

.. code:: bash

    $ pyplot SCRIPTNAME {COMMAND LINE PARAMETERES}

It is also possible to structure them in *subfolders* and launch them via:

.. code:: bash

    $ pyplot subfolder SCRIPTNAME {COMMAND LINE PARAMETERES}


Usage
=======

First you have to specify the directories **pyplot** is supposed to keep track of. This can be done by

.. code:: bash

   $ pyplot configure addroot

or

.. code:: bash

   $ pyplot configure addsub


Scripts in directories added as root are directly available via ``pyplot 
SCRIPTNAME``, for directories added as  subdirectory the subdirectory has to be 
given first ``pyplot subdirectory SCRIPTNAME``. Subdirectories so to speak 
create a new namespace.

Before scripts are available the command:

.. code:: bash

    $ pyplot configure update

has to be used, to make the module aware of the new script. All scripts have to 
satisfy a `certain structure`__.  The scripts can be placed in the directory or 
in subdirectories of it.

__ `Required structure for the scripts`_

-------------------------

Required structure for the scripts
======================================

Currently the scripts to be launched form **pyplot** have to fulfill *either* of the following structures:

1. 
   i. Implement a function **get_parser(add_help)** which returns a **ArgumentParser**. The argument parser 
      has to be created with **ArgumentParser(..., add_help=add_help)**. This is necessary for the parser to be
      used as a parent. This way the help is also available in the **pyplot** script.
   #. Implement a **main(args)** function which takes the namespace object which would be created by the 
      argument parser as argument.
#. 
   i. Do *not* implement a function **get_parser(add_help**)
   #. Implement a function **main()** which doesn't need any arguments. **sys.argv** will be replaced 
      to mimic a native call.

Examples:
------------

1. Using **argparser**:

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

2. Without **argparser**:

.. code:: python

    import sys


    def main():
        print('This is the main method, proper sys.args are available')
        print(sys.args)


    if __name__ == '__main__':
        main()

-------------------------

Setting up argument completion:
==================================
argcomplete_ is used to realize the dynamic argument completion.

bash
-------
Install the package and use:

.. code:: bash

    $ eval "$(register-python-argcomplete pyplot)"

Add this line to your *.bash_rc* if you want to have this permanently.

zsh
----
argcomplete_ currently doesn't support *zsh*. The bash_ argument completion can 
however be used. To set this up you additionally need to execute the following 
commands:

.. code:: bash

   $ autoload bashcompinit
   $ bashcompinit

Then the same command as in bash_ can be used:

.. code:: bash

   $ eval "$(register-python-argcomplete pyplot)"

Again, if you want this permanetly and not  only per session add these three lines to your *.zsh_rc*.

.. _argcomplete: https://pypi.python.org/pypi/argcomplete

_________________________

Developement state
====================


The script can currently be installed from source with the `setup.py` script or 
using pip. I would however advise to only use:

.. code:: bash

    $ python setup develop

This is the only thing I tried so far. If it is installed, auto completion 
works if `setup accordingly`__. It is just a bit slow so far.

__ `Setting up argument completion:`_

Issues:
----------

Currently no known issue

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
   * [X] allow root as well es subdirectories
   * [O] show status
   * [X] remove directories via config script

 - [X] allow subpoints to group scripts
 - [X] relax the structural requirements for the scripts (ArgumentParser optional)
 - [X] convert readme to `rst` for python

