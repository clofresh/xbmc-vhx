import xbmcaddon
from resources.lib import vhx

# xbmc hooks
__settings__ = xbmcaddon.Addon(id='plugin.video.vhx')
__language__ = __settings__.getLocalizedString
__dbg__ = __settings__.getSetting("debug") == "true"
__dbglevel__ = 1


vhx.config['login']     = 'clofresh'
vhx.config['api_token'] = 'FMx3jhNhg79xL1t03IGA'

if __name__ == "__main__" :
    vhx.main()
