import logging
import os
import tkinter as tk

from typing import Any, Optional, Tuple, Union

from config import appname

from activitymanager import ActivityManager
from ui import UI


# This could also be returned from plugin_start3()
plugin_name = os.path.basename(os.path.dirname(__file__))

# A Logger is used per 'found' plugin to make it easy to include the plugin's
# folder name in the logging output format.
# NB: plugin_name here *must* be the plugin's folder name as per the preceding
#     code, else the logger won't be properly set up.
logger = logging.getLogger(f'{appname}.{plugin_name}')

# If the Logger has handlers then it was already set up by the core code, else
# it needs setting up here.
if not logger.hasHandlers():
    level = logging.INFO  # So logger.info(...) is equivalent to print()

    logger.setLevel(level)
    logger_channel = logging.StreamHandler()
    logger_formatter = logging.Formatter(f'%(asctime)s - %(name)s - %(levelname)s - %(module)s:%(lineno)d:%(funcName)s: %(message)s')
    logger_formatter.default_time_format = '%Y-%m-%d %H:%M:%S'
    logger_formatter.default_msec_format = '%s.%03d'
    logger_channel.setFormatter(logger_formatter)
    logger.addHandler(logger_channel)

# ----------------------------------------------------------------------------

activity_manager = ActivityManager(logger)
ui = UI(activity_manager)


def plugin_start3(plugin_dir: str) -> str:
   """
   Load this plugin into EDMarketConnector
   """
   logger.error(f"I am loaded! My plugin folder is {plugin_dir}")
   activity_manager.plugin_start3(plugin_dir)
   return "PP-Tracker"


def plugin_app(parent: tk.Frame) -> Union[tk.Widget, Tuple[tk.Widget, tk.Widget]]:
    return ui.get_plugin_frame(parent)


def journal_entry(cmdr: str, is_beta: bool, system: str, station: str, entry: dict[str, Any], state: dict[str, Any]) -> Optional[str]:
    """
    Parse an incoming journal entry and store the data we need
    """
    activity_manager.journal_entry(cmdr, is_beta, system, station, entry, state)
    
