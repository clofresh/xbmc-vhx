''' Don't work yet
'''

from urlparse import urlparse
from xml.etree import ElementTree

from .common import *

__all__ = ['VimeoVideo']

class VimeoVideo(object):
    
    video_data_url_format = "http://vimeo.com/moogaloop/load/clip:{0}/"
    video_url_format = "http://player.vimeo.com/play_redirect?clip_id={0}&sig={1}&time={2}&quality={3}&codecs=H264,VP8,VP6&type=moogaloop_local&embed_location="
    
    def __init__(self, url, video_url):
        self.url = url
        self.video_url = video_url
    
    @classmethod
    def matched(cls, url):
        return 'vimeo' in url
    
    @classmethod
    def from_id(cls, id):
        url = cls.video_data_url_format.format(id)
        response = requests.get(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-GB; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8'
        })
        response.raise_for_status()
        
        xml = ElementTree.fromstring(response.content)
        request_sig = xml.find('request_signature').text
        request_sig_expires = xml.find('request_signature_expires').text
        vid_quality = 'hd'
        video_url = cls.video_url_format.format(
            id, request_sig, request_sig_expires, vid_quality
        )
                
        return cls(url, video_url)
    
    @classmethod
    def from_url(cls, url):
        parsed = urlparse(url)
        return cls.from_id(parsed.path.split('/')[1])

VhxVideo.register(VimeoVideo) 

