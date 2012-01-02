import re
from .common import *

__all__ = ['YouTubeVideo']

class Resolution(object):
    RES_1080P =  100
    RES_720P  =  200
    RES_480P  =  300
    RES_360P  =  400
    RES_240P  =  500
    UNKNOWN   = 1000
    
    highest_to_lowest = (RES_1080P, RES_720P, RES_480P, 
                         RES_360P,  RES_240P, UNKNOWN)

class Codec(object):
    H264    =  100
    VP8     =  200
    H263    =  300
    RTMPE   =  400
    UNKNOWN = 1000

class Container(object):
    FLV     =  100
    WEBM    =  200
    MP4     =  300
    RTMPE   =  400
    UNKNOWN = 1000

class YouTubeVideo(object):
    
    video_url_format = "http://www.youtube.com/watch?v={0}"
    
    FORMATS = {
        26: (Resolution.UNKNOWN,   Codec.UNKNOWN, Container.UNKNOWN),
         5: (Resolution.RES_240P,  Codec.H263,    Container.FLV),
        34: (Resolution.RES_360P,  Codec.H264,    Container.FLV),
        43: (Resolution.RES_360P,  Codec.H264,    Container.FLV),
        18: (Resolution.RES_360P,  Codec.H264,    Container.MP4),
        78: (Resolution.RES_360P,  Codec.RTMPE,   Container.RTMPE),
        35: (Resolution.RES_480P,  Codec.H264,    Container.FLV),
        44: (Resolution.RES_480P,  Codec.VP8,     Container.WEBM),
        59: (Resolution.RES_480P,  Codec.RTMPE,   Container.RTMPE),
        22: (Resolution.RES_720P,  Codec.H264,    Container.MP4),
        38: (Resolution.RES_720P,  Codec.VP8,     Container.WEBM),
        45: (Resolution.RES_720P,  Codec.VP8,     Container.WEBM),
        37: (Resolution.RES_1080P, Codec.H264,    Container.MP4),
    }
    
    def __init__(self, url, videos_by_res=None):
        self.url = url
        self.videos_by_res = videos_by_res
    
    @classmethod
    def matched(cls, url):
        return 'youtube' in url
    
    @classmethod
    def from_id(cls, id):
        url = cls.video_url_format.format(id)
        return cls.from_url(url)
    
    @classmethod
    def from_url(cls, url):
        response = requests.get(url)
        matched = re.search('yt.setConfig\(({\s*\'PLAYER_CONFIG.*?)\);', response.content, re.DOTALL)
        if matched:
            json_str = matched.group(1).replace("'PLAYER_CONFIG'", 
                                                '"PLAYER_CONFIG"')
            try:
                player_config = json.loads(json_str)
            except Exception:
                log.error(json_str)
                raise
            
            links = getVideoUrlMap(player_config['PLAYER_CONFIG'])
            video_urls = {}
            for format_id, video_url in links.items():
                try:
                    res, codec, container = cls.FORMATS[format_id]
                except KeyError:
                    log.error("Unknown format: {0}".format(format_id))
                else:
                    if res not in video_urls:
                        video_urls[res] = []
                    video_urls[res].append((codec, container, video_url))
            
            return cls(url, video_urls)
        else:
            raise ParseError("Could not parse video links from {0} ({1})".format(url, response.content))
    
    def highest_res(self):
        all_videos = self.videos_by_res.items()
        all_videos.sort()
        _resolution, videos = all_videos[0]
        videos.sort()
        _codec, _container, url = videos[0]
        return url

def getVideoUrlMap(pl_obj, video = {}):
	links = {}
	video["url_map"] = "true"
				
	html = ""
	if pl_obj["args"].has_key("fmt_stream_map"):
		html = pl_obj["args"]["fmt_stream_map"]

	if len(html) == 0 and pl_obj["args"].has_key("url_encoded_fmt_stream_map"):
		html = urllib.unquote(pl_obj["args"]["url_encoded_fmt_stream_map"])

	if len(html) == 0 and pl_obj["args"].has_key("fmt_url_map"):
		html = pl_obj["args"]["fmt_url_map"]

	html = urllib.unquote_plus(html)

	if pl_obj["args"].has_key("liveplayback_module"):
		video["live_play"] = "true"

	fmt_url_map = [html]
	if html.find("|") > -1:
		fmt_url_map = html.split('|')
	elif html.find(",url=") > -1:
		fmt_url_map = html.split(',url=')
	elif html.find("&conn=") > -1:
		video["stream_map"] = "true"
		fmt_url_map = html.split('&conn=')
	
	
	if len(fmt_url_map) > 0:
		for index, fmt_url in enumerate(fmt_url_map):
			if (len(fmt_url) > 7 and fmt_url.find("&") > 7):
				quality = "5"
				final_url = fmt_url.replace(" ", "%20").replace("url=", "")
				
				if (final_url.rfind(';') > 0):
					final_url = final_url[:final_url.rfind(';')]
				
				if (final_url.rfind(',') > final_url.rfind('&id=')): 
					final_url = final_url[:final_url.rfind(',')]
				elif (final_url.rfind(',') > final_url.rfind('/id/') and final_url.rfind('/id/') > 0):
					final_url = final_url[:final_url.rfind('/')]

				if (final_url.rfind('itag=') > 0):
					quality = final_url[final_url.rfind('itag=') + 5:]
					if quality.find('&') > -1:
						quality = quality[:quality.find('&')]
					if quality.find(',') > -1:
						quality = quality[:quality.find(',')]
				elif (final_url.rfind('/itag/') > 0):
					quality = final_url[final_url.rfind('/itag/') + 6:]
				
				if final_url.find("&type") > 0:
					final_url = final_url[:final_url.find("&type")]
				
				if False: #self.__settings__.getSetting("preferred") == "false":
					pos = final_url.find("://")
					fpos = final_url.find("fallback_host")
					if pos > -1 and fpos > -1:
						host = final_url[pos + 3:]
						if host.find("/") > -1:
							host = host[:host.find("/")]
						fmt_fallback = final_url[fpos + 14:]
						if fmt_fallback.find("&") > -1:
							fmt_fallback = fmt_fallback[:fmt_fallback.find("&")]

						final_url = final_url.replace(host, fmt_fallback)
						final_url = final_url.replace("fallback_host=" + fmt_fallback, "fallback_host=" + host)

				if final_url.find("rtmp") > -1 and index > 0:
					if pl_obj.has_key("url") or True:
						final_url += " swfurl=" + pl_obj["url"] + " swfvfy=1"

					playpath = False
					if final_url.find("stream=") > -1:
						playpath = final_url[final_url.find("stream=")+7:]
						if playpath.find("&") > -1:
							playpath = playpath[:playpath.find("&")]
					else:
						playpath = fmt_url_map[index - 1]

					if playpath:
						if pl_obj["args"].has_key("ptk") and pl_obj["args"].has_key("ptchn"):
							final_url += " playpath=" + playpath + "?ptchn=" + pl_obj["args"]["ptchn"] + "&ptk=" + pl_obj["args"]["ptk"] 

				links[int(quality)] = final_url.replace('\/','/')
	
	return links
	
VhxVideo.register(YouTubeVideo)	

