from zope import interface
from .. import ISparcAppConfiguration
from .. import ISparcApplication

class ISparcAppPyContainerConfiguration(ISparcAppConfiguration):
    """Marker for a dict/list/tuple/set based Sparc app config
    
    This type of configuration will be based on a native Python data container.
    """

class ISparcPyContainerConfiguredApplication(ISparcApplication):
    def get_config():
        """Return ISparcAppPyContainerConfiguration provider for current 
           runtime configuration settings"""
    def set_config(config):
        """Set ISparcAppPyContainerConfiguration provider or Python container 
           (dict, list, tuple, set) for current runtime configuration settings
        
        Args:
            config: ISparcAppConfiguration provider
        """

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

class IPyContainerConfigValue(interface.Interface):
    """Find Yaml document values based on a key"""
    def get(*args, **kwargs):
        """Get the first config value matching key
        
        See ISparcPyDictValueIterator for information on how search for key
        is performed.
        
        Raises: KeyError if key is not found and default is not given
        
        Args:
            Ordered keys to search in config.  To find 'value1' in this
            container {'key1': {'key2': 'value1'}}, you would make a call
            to get('key1', 'key2')
        Kwargs:
            default: value to return if given args are not referencable.
            
        Returns: object value from key or default
        """
    def query(*args):
        """Get the first config value matching key, if available
        
        See ISparcPyDictValueIterator for information on how search for key
        is performed.
        
        Args:
            [see get()]
            
        Returns: object value from key or None if key is not found
        """
