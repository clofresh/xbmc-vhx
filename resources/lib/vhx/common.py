import os
import logging
from resources.lib import requests
try:
	from xbmcaddon import Addon
except ImportError:
	class Addon(object):
		def __init__(self, *args):
			pass

		def getAddonInfo(self, *args):
			return "../../../"

log = logging.getLogger('xbmc.vhx')
plugin_id = 'plugin.video.vhx'
addon = Addon(plugin_id)
root_dir = addon.getAddonInfo("path")

def init_logging():
    standard_log_format = "%(asctime)s %(levelname)s %(filename)s:%(lineno)d %(message)s"
    log.propagate = False
    log.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(standard_log_format))
    log.addHandler(handler)

def base_path(path):
    return os.path.join(root_dir, path)

def resources_path(path):
    return os.path.join(root_dir, "resources", path)

def media_path(path):
    return os.path.join(root_dir, "resources", "media", path)