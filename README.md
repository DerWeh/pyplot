# pyplot
-------------------------
Module to centralize plotting scripts.

In the `.config.cfg` file specified directories are made accessible via __pyplot__. If we have e.g. a directory _/home/user/plotter_, scripts can be dumped into the _plotter_ folder and then be launched centrally with the __pyplot__ script via 

    $ pyplot SCRIPTNAME {COMMAND LINE PARAMETERES}

It is also possible to structure them in _subfolders_ and launch them via 

    $ pyplot subfolder SCRIPTNAME {COMMAND LINE PARAMETERES}

Before scripts are available he command:

    $ pyplot configure update

has to be used, to make the module aware of the new script. It turns the directories, e.g. _plotter_, into modules by creating a `__init__.py` file. Currently existing `__init__.py` files will be overwritten.

-------------------------

# Developement state

The script can currently be installed with the `setup.py` script. It would howver advise to only use 

    $ python setup develop

This is the only thing I tried so far. If it is installed, autocompletion works. It is just a bit slow so far.

## Issues:
1. Currently a config file has to be created before the script can be used, even to add config entries.

-------------------------

# Required structure for the scripts:

Currently the scripts to be launched form `pyplot` have to fulfill *either* of the following structures:

1. 
   1. Implement a function `get_parser(add_help)` which returns a `ArgumentParser` the argument parser 
      has to be created with `ArgumentParser(..., add_help=add_help)`. This is necessary that the parser 
      can be used as a parent. This way the help is also availible in the **pyplot** script.
   2. Implement a `main(args)` function which takes the namespace object which would be created by the 
      argument parser as argument.
2. 
   1. don't have a function `get_parser(add_help)`
   2. implement a function `main()` which doesn't need any arguments. `sys.argv` will be replaced 
      to mimic a native call.

## Examples:
1. Using `argparser`:
    ```python
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
    ```
2. Without `argparser`:
    ```python
    import sys


    def main(args):
        print('This is the main method, proper sys.args are available')
        print(sys.args)


    if __name__ == '__main__':
        main()
    ```
-------------------------

# Setting up argument completion:

The working version is to install the script and the use:

    $ eval "$(register-python-argcomplete pyplot)"
    

~~To set up argument completion execute~~

~~$ eval "$(register-python-argcomplete pyplot.py)"~~

~~or put it in your `.bash_rc`.~~

~~Note that it doesn't properly work yet. You can only argument completion when you explicitly type the path,
so e.g. `/home/user/pypot/pyplot.py` and `./pyplot.py`allow argument completion, but with `~/pyplot/pyplot.py`
or an alias it doesn't work yet.~~

-------------------------

# TODO:

 - [ ] fix config file issue
 - [ ] speed up autocompletion, maybe a shelf is possible
 - [ ] add test for `update clean` as files are removed
 - [ ] fix autocompletion of arguments
 - [ ] make it stable (adding test)
 - [ ] make the project structure more dynamic
   - [X] add config file to to specify included direcories
   - [ ] include direcotories via config script
   - [ ] allow root as well es subdirectories
   - [ ] show status
 - [x] allow subpoints to group scripts
 - [x] relax the structural requirements for the scripts (ArgumentParser optional)
 - [ ] convert readme to `rst` for python

