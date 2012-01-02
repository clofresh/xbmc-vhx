import sys
from .common import init_logging
from .ui import VhxPlugin
from .handlers import handlers, default_handler
from .common import config

def main():
    init_logging()
    plugin = VhxPlugin.from_sys_argv(sys.argv, handlers, 
        default_handler=default_handler)
    plugin.route()

