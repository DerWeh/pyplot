"""Constants and configuration needed by all scripts"""
from __future__ import print_function, absolute_import

try:
    import configparser
except ImportError:
    # import ConfigParser as configparser
    raise ImportError
from os.path import expanduser


class ConfigParser(configparser.SafeConfigParser):
    """Subclass of `SafeConfigParser`, able to handle lists."""
    def getlist(self, section, option, raw=False, vars=None):
        """
        Get an *option* list, from a list of lines
        
        Every item  of the list is a none empty line, starting with leading 
        whitespace which will be striped.
        If *vars* is provided, it must be a dictionary. The *option* is looked 
        up in *vars* (if provided), *section*, and in *defaults* in that order.

        All the ``'%'`` interpolations are expanded in the return values, unless 
        the *raw* argument is true. Values for interpolation keys are looked up 
        in the same manner as the option.
        """
        value = self.get(section, option, raw=raw, vars=vars)
        items = [item.strip() for item in value.splitlines() if item.strip()]
        return items

    def setlist(self, section, option, value):
        """Write a list to the config file in format readable by `getlist`.
        
        If the given *section* exists, set the given option to the specified 
        *value*; otherwise raise NoSectionError. *value* must be a string (str 
        or unicode); if not, TypeError is raised.
        """
        seperator = '\n\t'
        value_str = seperator + seperator.join(value)
        self.set(section, option, value_str)


CONFIG_FILE = expanduser('~/.pyplot.cfg')
CONFIG = ConfigParser(defaults={'root_directories': [], 'sub_directories': []})

try:
    with open(CONFIG_FILE, 'r') as config_fp:
        CONFIG.readfp(config_fp)
except IOError:
    ROOT_DIRECTORIES = []
    SUB_DIRECTORIES = []
else:
    ROOT_DIRECTORIES = CONFIG.getlist('include', 'root_directories')
    SUB_DIRECTORIES = CONFIG.getlist('include', 'sub_directories')
