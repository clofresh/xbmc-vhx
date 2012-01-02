from ..common import *

import json
import urllib
from datetime import datetime

class ParseError(Exception):    pass
class UnknownFormat(Exception): pass
class UnknownUrl(Exception):    pass


class VhxVideo(object):
    valid_videos = []
    date_format = "%Y-%m-%dT%H:%M:%SZ"
    
    @classmethod
    def register(cls, video_cls):
        cls.valid_videos.append(video_cls)
    
    @classmethod
    def from_json_dict(cls, data):
        video = data['video']
        url = cls.video_url(video['url'])
        try:
            created_at = datetime.strptime(video['created_at'], cls.date_format)
        except:
            created_at = None 
        
        return cls(
            url=url,
            title=video['title'],
            description=video['description'],
            thumbnail_url=video['thumbnail_url'],
            created_at=created_at,
            duration=video['duration']
        )

    @classmethod
    def video_url(cls, url):
        log.info("Possible video urls: {0}".format(cls.valid_videos))
        for video_cls in cls.valid_videos:
            if video_cls.matched(url):
                return video_cls.from_url(url).highest_res()
        raise UnknownUrl(url)

    
    def __init__(self, url, title, description, thumbnail_url, created_at, duration):
        self.url = url
        self.title = title
        self.description = description
        self.thumbnail_url = thumbnail_url
        self.created_at = created_at
        self.duration = duration
    
    def __str__(self):
        return u"{0} ({1})".format(self.title, self.url)
    
