import importlib
from zope import component
from zope.component.factory import Factory
from zope import interface

from sparc.configuration import container
from . import IZCMLFile
from . import IZCMLFiles

@interface.implementer(IZCMLFile)
class ZCMLFile(object):
    def __init__(self, package=None, file_=None):
        self.package = package
        self.file = file_
ZCMLFileFactory = Factory(ZCMLFile)

@interface.implementer(IZCMLFiles)
@component.adapter(container.ISparcAppPyContainerConfiguration)
class ZCMLFilesFromContainerConfig(object):
    def __init__(self, context):
        self.context = context
    
    def __iter__(self):
        
        zcml_values = list(component.getUtility(container.\
                        ISparcPyDictValueIterator).values(self.context, 
                                                          'ZCMLConfiguration'))
        
        for zcml_entry in zcml_values:
            zcml_entry = zcml_entry if not isinstance(zcml_entry, dict) else [zcml_entry]
            for zcml_config in zcml_entry:
                file_name = zcml_config.get('file', 'configure.zcml')
                yield ZCMLFile(
                    package = importlib.import_module(zcml_config['package']) \
                                            if 'package' in zcml_config else None,
                    file_ = file_name)