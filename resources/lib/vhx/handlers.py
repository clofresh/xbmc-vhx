from contextlib import contextmanager
import re
import xbmcgui
from .common import *
from .scraper import VhxScraper, AuthenticationError

def main_handler(x, **params):

    item = xbmcgui.ListItem(
        label='All videos', 
        iconImage=base_path("icon.png"), 
        thumbnailImage=base_path("icon.png")
    )
    x.addDirectoryItem(item, '/combined', isFolder=True)
    
    item = xbmcgui.ListItem(
        label='Facebook videos', 
        iconImage=media_path("facebook.png"), 
        thumbnailImage=media_path("facebook.png")
    )
    x.addDirectoryItem(item, '/facebook', isFolder=True)

    item = xbmcgui.ListItem(
        label='Twitter videos', 
        iconImage=media_path("twitter.png"), 
        thumbnailImage=media_path("twitter.png")
    )
    x.addDirectoryItem(item, '/twitter', isFolder=True)

    item = xbmcgui.ListItem(
        label='Tumblr videos', 
        iconImage=media_path("tumblr.png"), 
        thumbnailImage=media_path("tumblr.png")
    )
    x.addDirectoryItem(item, '/tumblr', isFolder=True)
    

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
        
def combined_handler(x, **params):
    listing_handler(x, 'all', **params)

def facebook_handler(x, **params):
    listing_handler(x, 'facebook', **params)

def twitter_handler(x, **params):
    listing_handler(x, 'twitter', **params)

def tumblr_handler(x, **params):
    listing_handler(x, 'tumblr', **params)

handlers = [
    (re.compile('/combined'), combined_handler),
    (re.compile('/facebook'), facebook_handler),
    (re.compile('/twitter'),  twitter_handler),
    (re.compile('/tumblr'),   tumblr_handler),
]

default_handler = main_handler



