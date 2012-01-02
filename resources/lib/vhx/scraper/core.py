from pprint import pformat

from .common import *

__all__ = ['VhxScraper']

class VhxScraper(object):
    base_url = "http://api.vhx.tv"
    
    @classmethod
    def from_config(cls):
        return cls(config['login'], config['api_token'])
    
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
    
    def facebook(self):
        return self.request('facebook')
    
    def twitter(self):
        return self.request('twitter')

    def tumblr(self):
        return self.request('tumblr')
    
    def all(self):
        videos = []
        
        try:
            videos.extend(self.facebook())
        except requests.exceptions.HTTPError:
            pass
        
        try:
            videos.extend(self.twitter())
        except requests.exceptions.HTTPError:
            pass
        
        try:
            videos.extend(self.tumblr())
        except requests.exceptions.HTTPError:
            pass
        
        videos.sort(key=lambda v: v.created_at, reverse=True)
        return videos

