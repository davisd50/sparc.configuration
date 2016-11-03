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
    
    def get(self, key):
        values = list(component.getUtility(container.\
                        ISparcPyDictValueIterator).values(self.context, key))
        if not values:
            raise KeyError("key: {} not available in configuration.".format(key))
        return values[0]

    def query(self, key):
        try:
            return self.get(key)
        except KeyError:
            return None