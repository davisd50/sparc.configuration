from zope import interface
from .. import ISparcAppConfiguration
from .. import ISparcApplication

class ISparcAppPyContainerConfiguration(ISparcAppConfiguration):
    """Marker for a dict/list/tuple/set based Sparc app config
    
    This type of configuration will be based on a native Python data container.
    """

class ISparcPyContainerConfiguredApplication(ISparcApplication):
    config = interface.Attribute("ISparcAppPyContainerConfiguration")

class ISparcPyDictValueIterator(interface.Interface):
    """Find Yaml document values based on a key"""
    def values(config, key):
        """Iterator of values in document matching given key
        
        This acts based on the top level document type.  For dict, this will 
        search dict keys and return the corresponding value.
        
        For others, this will iterate the container and search for dicts.
        Each dict found will be processed as above.
        
        Note:
            This is not a recursive method, it will only search 1 level deep
            on non-dict  
        
        Args:
            config: ISparcAppPyContainerConfiguration provider.
            key: Hashable key to match on
        """
