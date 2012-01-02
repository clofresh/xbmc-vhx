from pprint import pformat

from .common import *

__all__ = ['VhxScraper']

class VhxScraper(object):
    base_url = "http://api.vhx.tv"

    channels = [
        ('boingboing',      'BoingBoing'), 
        ('buzzfeed',        'BuzzFeed'),
        ('devour',          'Devour'), 
        ('facebook',        'Facebook'), 
        ('laughingsquid',   'Laughing Squid'), 
        ('trailers',        'Movie trailers'), 
        ('reddit',          'Reddit'),
        ('tumblr',          'Tumblr'), 
        ('twitter',         'Twitter'), 
        ('community',       'VHX community'), 
        ('staff',           'VHX staff'), 
    ]
    
    @classmethod
    def from_config(cls):
        return cls(addon.getSetting('login'), addon.getSetting('api_token'))
    
    def __init__(self, login, api_token):
        self.login = login
        self.api_token = api_token
    
    def request(self, endpoint, format='json'):
        credentials = {
            "login":     self.login,
            "api_token": self.api_token,
        }
        query_string = urllib.urlencode(credentials)
        url = "{0}/{1}.{2}?{3}".format(self.base_url, endpoint, format, 
                                       query_string)
        log.debug("GET {0}".format(url))
        response = requests.get(url, timeout=2.0)
        if response.status_code == 404:
            return []
        elif response.status_code == 401:
            raise AuthenticationError("Invalid credentials: {0}/{1}".format(self.login, self.api_token))
        
        response.raise_for_status()
        try:
            videos = json.loads(response.content)
        except:
            log.error("Could not parse {0} as json {1}".format(url, response.content))
            raise
        
        vhx_videos = []
        for video_data in videos:
            try:
                log.debug(pformat(video_data))
                vhx_videos.append(VhxVideo.from_json_dict(video_data))
            except:
                log.error("Could not process video", exc_info=True)

        vhx_videos.sort(key=lambda v: v.created_at, reverse=True)
        return vhx_videos
    
    def all(self):
        videos = []
        for channel, _label in self.channels:
            videos.extend(self.request(channel))
        videos.sort(key=lambda v: v.created_at, reverse=True)
        return videos

