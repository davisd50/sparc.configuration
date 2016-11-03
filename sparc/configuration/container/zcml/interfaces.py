from zope import interface

class IZCMLFile(interface.Interface):
    """ZCML File descriptor"""
    file = interface.Attribute("Sting zcml file name")
    package = interface.Attribute("Python module object of package containing file")

class IZCMLFiles(interface.Interface):
    """Identifies ZCML files"""
    def __iter__():
        """Iterator of IZCMLFile providers"""