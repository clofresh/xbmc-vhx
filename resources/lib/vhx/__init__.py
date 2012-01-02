import sys
from .common import *
from .ui import VhxPlugin
from .handlers import handlers, default_handler

def main():
    init_logging()
    plugin = VhxPlugin.from_sys_argv(sys.argv, handlers, 
        default_handler=default_handler)
    plugin.route()

