from zope import interface
from zope.interface.interfaces import IObjectEvent

class ISparcApplicationConfiguredEvent(IObjectEvent):
    """A configuration has been applied to a ISparcApplication"""

class ISparcAppConfiguration(interface.Interface):
    """Marker for Sparc application configuration data"""

class ISparcApplication(interface.Interface):
    """An Application"""
    def get_config():
        """Return ISparcAppConfiguration provider for current runtime configuration settings"""
    def set_config(config):
        """Set ISparcAppConfiguration for current runtime configuration settings
        
        Args:
            config: ISparcAppConfiguration provider
        """
    def configure():
        """Configure runtime environment to settings to current config.
        Issues a ISparcApplicationConfiguredEvent
        """
    def go():
        """Run the application"""