from xml.etree import ElementTree
from zope import interface
from zope.component import IFactory
from .interfaces import IAppElementTreeConfig

@interface.implementer(IFactory)
class AppConfigFactory(object):
    
    title = u"Create an XML based app configuration"
    description = u"returns a xml.etree.ElementTree marked with IAppElementTreeConfig"
    
    def __call__(self, xml_config):
        config = ElementTree.parse(xml_config).getroot()
        interface.alsoProvides(config, IAppElementTreeConfig)
        return config
    
    def getInterfaces(self):
        etree = ElementTree.ElementTree()
        interface.alsoProvides(etree, IAppElementTreeConfig)
        return interface.providedBy(etree)
