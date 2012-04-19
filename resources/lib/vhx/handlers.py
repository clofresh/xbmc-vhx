from contextlib import contextmanager
import re
from .common import *
from .scraper import VhxScraper, AuthenticationError

listings = [
    ('all', {
        'label':            'All videos',
        'iconImage':        base_path('icon.png'),
        'thumbnailImage':   base_path('icon.png'),
    }), 
]

for channel, label in VhxScraper.channels:
    icon_path = media_path('{0}.png'.format(channel))
    listings.append((channel, {
        'label':            label,
        'iconImage':        icon_path,
        'thumbnailImage':   icon_path,
    }))

def scrape(listing):
    videos = None
    while videos is None:
        vhx = VhxScraper.from_config()
        try:
            if listing == 'all':
                videos = vhx.all()
            else:
                videos = vhx.request(listing)
        except AuthenticationError, e:
            jump_to_settings = xbmcgui.Dialog().yesno("Authentication Error",
                str(e), "Update settings?")
            if jump_to_settings:
                addon.openSettings()
            else:
                videos = []
    return videos
    
def main_handler(x, **params):
    import xbmcgui
    for listing, attributes in listings:
        x.addDirectoryItem(xbmcgui.ListItem(**attributes), 
            '/{0}'.format(listing), isFolder=True)    

def listing_handler(x, listing, **params):
    import xbmc, xbmcgui
    playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
    playlist.clear()
    total = 0
    videos = scrape(listing)
    for video in videos:
        item = xbmcgui.ListItem(
            label=video.title, 
            label2=video.description, 
            iconImage=video.thumbnail_url, 
            thumbnailImage=video.thumbnail_url
        )
        total += 1
        x.addDirectoryItem(item, video.url, totalItems=total)
        playlist.add(video.url, item)
    xbmc.Player().play(playlist)
        
handlers = [
    (re.compile('/(?P<listing>{0})'.format('|'.join(l for l, _ in listings))), 
        listing_handler),
]

default_handler = main_handler



