from zope.interface import Interface

class IElementTree(Interface):
    """Marker for an ElementTree instance"""

class IAppElementTreeConfig(IElementTree):
    """Marker for a ElementTree based application configuration instance"""