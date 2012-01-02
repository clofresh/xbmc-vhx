from contextlib import contextmanager
import re
import xbmcgui
from .common import *
from .scraper import VhxScraper, AuthenticationError

listings = [
    ('all', {
        'label':            'All videos',
        'iconImage':        base_path('icon.png'),
        'thumbnailImage':   base_path('icon.png'),
    }), 
    ('facebook', {
        'label':            'Facebook videos',
        'iconImage':        media_path('facebook.png'),
        'thumbnailImage':   media_path('facebook.png'),
    }), 
    ('twitter', {
        'label':            'Twitter videos',
        'iconImage':        media_path('twitter.png'),
        'thumbnailImage':   media_path('twitter.png'),
    }), 
    ('tumblr', {
        'label':            'Tumblr videos',
        'iconImage':        media_path('tumblr.png'),
        'thumbnailImage':   media_path('tumblr.png'),
    }),
]

def scrape(listing):
    videos = None
    while videos is None:
        vhx = VhxScraper.from_config()
        try:
            videos = getattr(vhx, listing)()
        except AuthenticationError, e:
            jump_to_settings = xbmcgui.Dialog().yesno("Authentication Error",
                str(e), "Update settings?")
            if jump_to_settings:
                addon.openSettings()
            else:
                videos = []
    return videos
    
def main_handler(x, **params):
    for listing, attributes in listings:
        x.addDirectoryItem(xbmcgui.ListItem(**attributes), 
            '/{0}'.format(listing), isFolder=True)    

def listing_handler(x, listing, **params):
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
        

handlers = [
    (re.compile('/(?P<listing>{0})'.format('|'.join(l for l, _ in listings))), 
        listing_handler),
]

default_handler = main_handler



