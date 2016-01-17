from xml.etree import ElementTree
from zope.component import IFactory
from zope.interface import alsoProvides
from zope.interface import implements
from zope.interface import providedBy
from interfaces import IAppElementTreeConfig

class AppConfigFactory(object):
    implements(IFactory)
    
    title = u"Create an XML based app configuration"
    description = u"returns a xml.etree.ElementTree marked with IAppElementTreeConfig"
    
    def __call__(self, xml_config):
        config = ElementTree.parse(xml_config).getroot()
        alsoProvides(config, IAppElementTreeConfig)
        return config
    
    def getInterfaces(self):
        etree = ElementTree.ElementTree()
        alsoProvides(etree, IAppElementTreeConfig)
        return providedBy(etree)
