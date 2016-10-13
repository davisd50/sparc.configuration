from zope import interface

class ISparcYamlDocuments(interface.Interface):
    def documents(config):
        """Generator of Python List/Dict based on yaml config file
        
        Args:
            config: Unicode valid file path to a Yaml configuration or a valid
                    Yaml string.
        """
    def first(config):
        """Return first document (Python List/Dict) in yaml config
        
        Args:
            config: [same as documents()]
        """

class ISparcYamlDocumentValueIterator(interface.Interface):
    """Find Yaml document values based on a key"""
    def values(document, key):
        """Iterator of values in document matching given key
        
        This acts based on the top level document type.  For dict, this will 
        search dict keys and return the corresponding value.
        
        For lists, this will iterate the list values and search for dicts.
        Each dict found will be processed as above.
        
        Args:
            document: Python list or Dict, usually based on a valid Yaml config
                      file.
            key: key to match on
        """