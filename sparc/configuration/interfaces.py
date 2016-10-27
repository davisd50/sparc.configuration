from zope import interface

class ISparcAppConfiguration(interface.Interface):
    """Marker for Sparc application configuration data"""

class ISparcApplication(interface.Interface):
    """An Application"""
    config = interface.Attribute("ISparcAppConfiguration object")
    def go():
        """Run the application"""