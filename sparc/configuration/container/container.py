from zope import interface
from zope.component.factory import Factory
from . import ISparcAppPyContainerConfiguration

@interface.implementer(ISparcAppPyContainerConfiguration)
class SparcAppPyContainerConfiguration(object):
    def __new__(self, container):
        if isinstance(container, dict):
            return SparcAppPyDictConfiguration(container)
        if isinstance(container, list):
            return SparcAppPyListConfiguration(container)
        if isinstance(container, tuple):
            return SparcAppPyTupleConfiguration(container)
        if isinstance(container, set):
            return SparcAppPySetConfiguration(container)
        raise ValueError('Expected container to be dict, list, tuple, or set')
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
