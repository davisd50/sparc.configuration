from os.path import isfile
import yaml
from zope import interface
from zope import component

from sparc.configuration.container import container
from . import ISparcYamlDocuments

@interface.implementer(ISparcYamlDocuments)
class SparcYamlDocuments(object):

    def documents(self, config):
        config = config if not isfile(config) else open(config)
        for doc in yaml.load_all(config):
            if container.SparcAppPyContainerConfiguration.is_container(doc):
                yield component.createObject(\
                                        u'sparc.configuration.container', doc)
            else:
                return doc

    def first(self, config):
        return next(self.documents(config))