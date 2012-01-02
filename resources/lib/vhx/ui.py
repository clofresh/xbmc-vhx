import re
import sys
from functools import partial
from urlparse import parse_qs, urlparse
import xbmcgui, xbmcplugin

from .common import *

class VhxPlugin(object):
    id = plugin_id
    
    def __init__(self, handle, path, params=None, handlers=None, 
                 default_handler=None):
        
        self.handle = int(handle)
        self.path = path
        self.params = params or {}
        self.handlers = handlers
        self.default_handler = default_handler or self.noop_handler
        
    def noop_handler(self, **params):
        return
    
    @classmethod
    def from_sys_argv(cls, argv=None, handlers=None, default_handler=None):
        argv = argv or sys.argv
        uri, handle, qstr = argv
        
        parsed = urlparse(uri)
        assert parsed.scheme == 'plugin'
        assert parsed.netloc == cls.id
        
        path = parsed.path
        
        params = {}
        for key, vals in parse_qs(re.sub('^\?', '', qstr)):
            if len(vals) == 1:
                params[key] = vals[0]
            elif len(vals) == 0:
                params[key] = None
            else:
                params[key] = vals        
        
        return cls(handle, path, params, handlers, default_handler)
    
    def route(self):
        x = self.xbmc()
        try:
            handled = False
            for pattern, handler in self.handlers:
                match = pattern.match(self.path)
                if match:
                    log.info("{0} {1}".format(self.path, handler))
                    params = match.groupdict()
                    params.update(self.params)
                    handler(x, **params)
                    handled = True
        
            if not handled:
                log.info("no match, using default handler {0} {1}".format(self.path, self.default_handler))
                self.default_handler(x, **self.params)
        finally:
            x.endOfDirectory()
        
    
    def xbmc(self):
        return Xbmc(self.handle)
        

class XbmcException(Exception): pass

class Xbmc(object):
    def __init__(self, handle):
        self.handle = handle
    
    def addDirectoryItem(self, listitem, url, **params):
        if not isinstance(listitem, xbmcgui.ListItem):
            listitem = xbmcgui.ListItem(listitem)
        
        if url.startswith('/'):
            url = 'plugin://{0}{1}'.format(VhxPlugin.id, url)
        
        success = xbmcplugin.addDirectoryItem(self.handle, url=url, listitem=listitem, **params)
        if not success:
            raise XbmcException()
    
    def __getattr__(self, key):
        return partial(getattr(xbmcplugin, key), self.handle)
        
        

