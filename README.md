# pyplot
-------------------------
Module to centralize plotting scripts.

Currently scripts with the right structure can be dropped into the plotter directory.
The command:

    $ pyplot configure update

makes the module aware of the new script.
It can then be run via

    $ pyplot SCRIPTNAME {COMMAND LINE PARAMETERES}

==================================================
Required structure for the scripts:
-------------------------
Currently the scripts to be launched form `pyplot` have to fulfill the following structure:

 # implement a function `get_parser(add_help)` which returns a `ArgumentParser` the argument parser 
   has to be created with `ArgumentParser(..., add_help=add_help)`. This is necessary that the parser 
   can be used as a parent.
 # implement a `main(args)` function which takes the namespace object which would be created by the 
   argument parser as argument

==================================================
#TODO:

 - fix autocompletion of arguments (enable it via `configure`)
 - make it stable (adding test)
 - make the project structure more dynamic
 - allow subpoints to group scripts
 - relax the structural requirements for the scripts (ArgumentParser optional)

