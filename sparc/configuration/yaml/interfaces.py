from zope import interface

class ISparcYamlDocuments(interface.Interface):
    def documents(config):
        """Generator of 
        sparc.configuration.container.ISparcAppPyContainerConfiguration objects
        based on config
        
        All Python container based items within the top level 
        ISparcAppPyContainerConfiguration will also be marked as
        ISparcAppPyContainerConfiguration objects.
        
        Args:
            config: Unicode valid file path to a Yaml configuration or a valid
                    Yaml content string.
        """
    def first(config):
        """sparc.configuration.container.ISparcAppPyContainerConfiguration 
        object for first document in config
        
        Args:
            config: [same as documents()]
        """