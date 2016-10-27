from zope import interface
from . import ISparcPyDictValueIterator

@interface.implementer(ISparcPyDictValueIterator)
class SparcPyContainerValueIterator(object):
    
    def values(self, document, key):
        _list = document if not isinstance(document, dict) else [document]
        for i in _list:
            if not isinstance(i, dict):
                continue
            for k, v in i.items():
                if k == key:
                    yield v