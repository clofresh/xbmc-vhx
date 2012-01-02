import re
import xbmcgui
from .common import *
from .scraper import VhxScraper

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
    
def combined_handler(x, **params):
    total = 0
    for video in VhxScraper.from_config().all():
        item = xbmcgui.ListItem(
            label=video.title, 
            label2=video.description, 
            iconImage=video.thumbnail_url, 
            thumbnailImage=video.thumbnail_url
        )
        total += 1
        x.addDirectoryItem(item, video.url, totalItems=total)

def facebook_handler(x, **params):
    total = 0
    for video in VhxScraper.from_config().facebook():
        item = xbmcgui.ListItem(
            label=video.title, 
            label2=video.description, 
            iconImage=video.thumbnail_url, 
            thumbnailImage=video.thumbnail_url
        )
        total += 1
        x.addDirectoryItem(item, video.url, totalItems=total)

def twitter_handler(x, **params):
    total = 0
    for video in VhxScraper.from_config().twitter():
        item = xbmcgui.ListItem(
            label=video.title, 
            label2=video.description, 
            iconImage=video.thumbnail_url, 
            thumbnailImage=video.thumbnail_url
        )
        total += 1
        x.addDirectoryItem(item, video.url, totalItems=total)

def tumblr_handler(x, **params):
    total = 0
    for video in VhxScraper.from_config().tumblr():
        item = xbmcgui.ListItem(
            label=video.title, 
            label2=video.description, 
            iconImage=video.thumbnail_url, 
            thumbnailImage=video.thumbnail_url
        )
        total += 1
        x.addDirectoryItem(item, video.url, totalItems=total)


handlers = [
    (re.compile('/combined'), combined_handler),
    (re.compile('/facebook'), facebook_handler),
    (re.compile('/twitter'),  twitter_handler),
    (re.compile('/tumblr'),   tumblr_handler),
]

default_handler = main_handler



