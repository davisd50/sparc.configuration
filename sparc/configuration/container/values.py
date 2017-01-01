from zope import component
from zope import interface
from sparc.configuration import container

@interface.implementer(container.ISparcPyDictValueIterator)
class SparcPyContainerValueIterator(object):
    
    def values(self, document, key):
        _list = document if not isinstance(document, dict) else [document]
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
    
    #def get(self, key, default=None): #<--signature
    def get(self, *args, **kwargs):
        key = args[0]
        has_default = False
        if len(args) > 1:
            has_default = True
            default = args[1]
        if not has_default and 'default' in kwargs:
            has_default = True
            default = kwargs['default']
            
        values = list(component.getUtility(container.\
                        ISparcPyDictValueIterator).values(self.context, key))
        if not values and not has_default:
            raise KeyError("key: {} not available in configuration.".format(key))
        return values[0] if len(values) else default

    def query(self, key):
        try:
            return self.get(key)
        except KeyError:
            return None