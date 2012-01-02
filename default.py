import xbmcaddon
from resources.lib import vhx

# xbmc hooks
__settings__ = xbmcaddon.Addon(id='plugin.video.vhx')
__language__ = __settings__.getLocalizedString
__dbg__ = __settings__.getSetting("debug") == "true"
__dbglevel__ = 1

if __name__ == "__main__" :
    vhx.main()
