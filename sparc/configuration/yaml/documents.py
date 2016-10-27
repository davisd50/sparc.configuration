from os.path import isfile
import yaml
from zope import interface
from zope import component

from ..container import ISparcAppPyContainerConfiguration
from . import ISparcYamlDocuments

@interface.implementer(ISparcYamlDocuments)
class SparcYamlDocuments(object):
    
    def is_container(self, value):
        return True if (isinstance(value, dict)  or \
                                isinstance(value, list) or \
                                isinstance(value, tuple) or \
                                isinstance(value, set)) \
                                else False

    def mark_config(self, config):
        if self.is_container(config):
            if not ISparcAppPyContainerConfiguration.providedBy(config):
                config = component.createObject(\
                                    u'sparc.configuration.container', config)
            if isinstance(config, dict):
                for k,v in config.items():
                    if self.is_container(v):
                        config[k] = self.mark_config(v)
            if isinstance(config, list):
                for i,v in enumerate(config):
                    if self.is_container(v):
                        config[i] = self.mark_config(v)
            if isinstance(config, set):
                for v in config:
                    if self.is_container(v):
                        config.delete(v)
                        config.add(self.mark_config(v))
            if isinstance(config, tuple):
                new_tuple = [] # we'll convert to tuple below...need it mutable for now
                has_container = False
                for v in config:
                    if self.is_container(v):
                        has_container = True
                        new_tuple.append(self.mark_config(v))
                    else:
                        new_tuple.append(v)
                if has_container:
                    config = tuple(new_tuple)
        return config

    def documents(self, config):
        config = config if not isfile(config) else open(config)
        for doc in yaml.load_all(config):
            yield self.mark_config(doc)

    def first(self, config):
        return next(self.documents(config))