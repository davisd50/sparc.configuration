from os.path import isfile
import yaml
from zope import interface
from zope.component.factory import Factory

from .interfaces import ISparcYamlDocuments
from .interfaces import ISparcYamlDocumentValueIterator

class SparcYamlDocuments(object):
    interface.implements(ISparcYamlDocuments)
    
    def documents(self, config):
        config = config if not isfile(config) else open(config)
        for doc in yaml.load_all(config):
            yield doc

    def first(self, config):
        return self.documents(config).next()
sparcYamlDocumentsFactory = Factory(SparcYamlDocuments)

class SparcYamlDocumentValueIterator(object):
    interface.implements(ISparcYamlDocumentValueIterator)
    
    def values(self, document, key):
        _list = document if not isinstance(document, dict) else [document]
        for i in _list:
            if not isinstance(i, dict):
                continue
            for k, v in i.iteritems():
                if k == key:
                    yield v