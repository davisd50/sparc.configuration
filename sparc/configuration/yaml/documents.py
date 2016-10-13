from os.path import isfile
import yaml
from zope import interface
from zope.component.factory import Factory

from .interfaces import ISparcYamlDocuments
from .interfaces import ISparcYamlDocumentValueIterator

@interface.implementer(ISparcYamlDocuments)
class SparcYamlDocuments(object):
    
    def documents(self, config):
        config = config if not isfile(config) else open(config)
        for doc in yaml.load_all(config):
            yield doc

    def first(self, config):
        return self.documents(config).next()
sparcYamlDocumentsFactory = Factory(SparcYamlDocuments)

@interface.implementer(ISparcYamlDocumentValueIterator)
class SparcYamlDocumentValueIterator(object):
    
    def values(self, document, key):
        _list = document if not isinstance(document, dict) else [document]
        for i in _list:
            if not isinstance(i, dict):
                continue
            for k, v in i.items():
                if k == key:
                    yield v