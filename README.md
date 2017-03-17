# pyplot
-------------------------
Module to centralize plotting scripts.

Currently scripts with the right structure can be dropped into the plotter directory.
The command:

    $ pyplot configure update

makes the module aware of the new script.
It can then be run via

    $ pyplot SCRIPTNAME {COMMAND LINE PARAMETERES}
-------------------------
==================================================
# Required structure for the scripts:

Currently the scripts to be launched form `pyplot` have to fulfill *either* of the following structures:

1. 
  1. implement a function `get_parser(add_help)` which returns a `ArgumentParser` the argument parser 
        has to be created with `ArgumentParser(..., add_help=add_help)`. This is necessary that the parser 
        can be used as a parent.
  2. implement a `main(args)` function which takes the namespace object which would be created by the 
        argument parser as argument
2. 
  1. don't have a function `get_parser(add_help)`
  2. implement a function `main()` which doesn't need any arguments. `sys.argv` will be replaced 
     to mimic a native call.

-------------------------
==================================================
# Setting up argument completion:

To set up argument completion execute

    $ eval "$(register-python-argcomplete pyplot.py)"

or put it in your `.bash_rc`.

Note that it doesn't properly work yet. You can only argument completion when you explicitly type the path,
so e.g. `/home/user/pypot/pyplot.py` and `./pyplot.py`allow argument completion, but with `~/pyplot/pyplot.py`
or an alias it doesn't work yet.

-------------------------
==================================================
# TODO:

 - [ ] add test for `update clean` as files are removed
 - [ ] fix autocompletion of arguments (enable it via `configure`)
 - [ ] make it stable (adding test)
 - [ ] make the project structure more dynamic
 - [x] allow subpoints to group scripts
 - [x] relax the structural requirements for the scripts (ArgumentParser optional)

