from zope import interface
from zope.component.factory import Factory
from . import ISparcAppPyContainerConfiguration

@interface.implementer(ISparcAppPyContainerConfiguration)
class SparcAppPyContainerConfiguration(object):

    @classmethod
    def is_container(cls, value):
        return True if (isinstance(value, dict)  or \
                                isinstance(value, list) or \
                                isinstance(value, tuple) or \
                                isinstance(value, set)) \
                                else False

    @classmethod
    def create(cls, container):
        """Return shallow-copied container marked with ISparcAppPyContainerConfiguration"""
        if isinstance(container, dict):
            return SparcAppPyDictConfiguration(container)
        if isinstance(container, list):
            return SparcAppPyListConfiguration(container)
        if isinstance(container, tuple):
            return SparcAppPyTupleConfiguration(container)
        if isinstance(container, set):
            return SparcAppPySetConfiguration(container)
        raise ValueError('Expected container to be dict, list, tuple, or set. Got: {}'.format(type(container)))

    def __new__(cls, container):
        config = cls.create(container)
        if isinstance(config, dict):
            for k,v in config.items():
                if cls.is_container(v):
                    config[k] = cls(v)
        if isinstance(config, list):
            for i,v in enumerate(config):
                if cls.is_container(v):
                    config[i] = cls(v)
        if isinstance(config, set):
            for v in config:
                if cls.is_container(v):
                    config.delete(v)
                    config.add(cls(v))
        if isinstance(config, tuple):
            new_tuple = [] # we'll convert to tuple below...need it mutable for now
            has_container = False
            for v in config:
                if cls.is_container(v):
                    has_container = True
                    new_tuple.append(cls(v))
                else:
                    new_tuple.append(v)
            if has_container:
                config = tuple(new_tuple)
        return config
sparcAppPyContainerConfigurationFactory = Factory(SparcAppPyContainerConfiguration)

@interface.implementer(ISparcAppPyContainerConfiguration)
class SparcAppPyDictConfiguration(dict):
    pass
sparcAppPyDictConfigurationFactory = Factory(SparcAppPyDictConfiguration)

@interface.implementer(ISparcAppPyContainerConfiguration)
class SparcAppPyListConfiguration(list):
    pass
sparcAppPyListConfigurationFactory = Factory(SparcAppPyListConfiguration)

@interface.implementer(ISparcAppPyContainerConfiguration)
class SparcAppPyTupleConfiguration(tuple):
    pass
sparcAppPyTupleConfigurationFactory = Factory(SparcAppPyTupleConfiguration)

@interface.implementer(ISparcAppPyContainerConfiguration)
class SparcAppPySetConfiguration(set):
    pass
sparcAppPySetConfigurationFactory = Factory(SparcAppPySetConfiguration)
