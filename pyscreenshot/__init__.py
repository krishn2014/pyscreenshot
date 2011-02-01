from path import path
from yapsy.PluginManager import PluginManager
import logging
import platform

__version__ = '0.1.2'



def get_plugin(backend_preference=None, force_backend=None):    
    places = [path(__file__).dirname()]
    ext = 'conf'

    pm = PluginManager()
    pm.setPluginInfoExtension(ext)
    pm.setPluginPlaces(places)
    pm.collectPlugins()
    
    if force_backend:
        return pm.activatePluginByName(force_backend)
        
    if backend_preference:
        for x in backend_preference:
            plugin = pm.activatePluginByName(x)
            if plugin:
                if plugin.is_available:
                    return plugin
    
    # get first
    all = pm.getAllPlugins()
    for x in all:
        plugin = pm.activatePluginByName(x.name)
        if plugin.is_available:
            return plugin
    
    if not len(all):
        raise(Exception('no plugin found!'))
        
    
    message = 'Install at least one backend!' 
    for x in all:
        message += '\n'
        message += '[%s]' % (x.name)
        if hasattr(x.plugin_object, 'home_url'):
            home_url=x.plugin_object.home_url
            message += '\n'
            message += '%s' % (home_url)
        message += '\n'
        if platform.dist()[0].lower() == 'ubuntu':
            message += 'You can install it in terminal:'
            message += '\n'
            message += '\t'
            message+= 'sudo apt-get install %s' % x.plugin_object.ubuntu_package
    raise Exception(message)

default_backend_preference = ['pil', 'scrot']
def grab(bbox=None, backend_preference=default_backend_preference, force_backend=None):  
    x = get_plugin(backend_preference=backend_preference, force_backend=force_backend)
    assert x
    return x.grab(bbox)

def grab_to_file(filename, backend_preference=default_backend_preference, force_backend=None):  
    x = get_plugin(backend_preference=backend_preference, force_backend=force_backend)
    assert x
    return x.grab_to_file(filename)


