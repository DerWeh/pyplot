"""Constants and configuration needed by all scripts"""

import ConfigParser as configparser


class ConfigParser(configparser.SafeConfigParser):
    """Subclass of `SafeConfigParser`, able to handle lists."""
    def getlist(self, section, option, raw=False, vars=None):
        """
        Get an option list, from a list of lines

        Every item is a none empty line, starting with leading whitespace which
        will be striped.
        """
        value = self.get(section, option, raw, vars)
        items = [item.strip() for item in value.splitlines() if item.strip()]
        return items

    def setlist(self, section, option, value):
        """Write a list to the config file in format readable by `getlist`."""
        seperator = '\n\t'
        value_str = seperator + seperator.join(value)
        self.set(section, option, value_str)


CONFIG_FILE = '.pyplot.cfg'
CONFIG = ConfigParser()

with open(CONFIG_FILE, 'r') as config_fp:
   CONFIG.readfp(config_fp)
SCRIPT_DIRECTORIES = CONFIG.getlist('include', 'script_directories')

