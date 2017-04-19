from zope import component
from zope import interface
from sparc.configuration import container

@interface.implementer(container.ISparcPyDictValueIterator)
class SparcPyContainerValueIterator(object):
    
    def values(self, config, key):
        _list = config if not isinstance(config, dict) else [config]
        for i in _list:
            if not isinstance(i, dict):
                continue
            for k, v in i.items():
                if k == key:
                    yield v

@interface.implementer(container.IPyContainerConfigValue)
@component.adapter(container.ISparcAppPyContainerConfiguration)
class PyContainerConfigValue(object):
    def __init__(self, context):
        self.context = context
    
    #def get(self, key1, key2, ..., default=None): #<--signature
    def get(self, *args, **kwargs):
        has_default = True if 'default' in kwargs else False
        
        config = self.context
        for key in args:
            values = list(SparcPyContainerValueIterator().values(config, key))
            if not values:
                if has_default:
                    return kwargs['default']
                else:
                    raise KeyError(
                        "key: {} not available in configuration.".format(key))
            config = values[0] # set for next loop, if there is one
            v = values[0]
        return v

    def query(self, key):
        try:
            return self.get(key)
        except KeyError:
            return None