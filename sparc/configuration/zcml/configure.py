from zope.component import getGlobalSiteManager
from zope.component.interfaces import ComponentLookupError

import zope.configuration.xmlconfig
import zope.component
import zope.security

import sparc.common.log
import logging
logger = logging.getLogger('sparc.common.configure')

def Configure(packages = None):
    """Setup Zope Component global registry
    
    Usage:
        Simple configuration of ZCA directives, makes ZCA available for use
        >>> Configure()
        
        Configure a package that has a configure.zcml file available
        >>> import sparc.cache
        >>> Configure([sparc.cache])
        
        Configure a list of packages, some of which require a custom zcml spec
        >>> import sparc.cache, sparc.db
        >>> myPackages = [
        ...               sparc.cache, # loads the configure.zcml file in package
        ...               sparc.db,  # loads the configure.zcml file in package
        ...               (sparc.db, 'memory.zcml') # loads the memory.zcml file in package
        ...              ]
    
    Args:
        packages: A package or list of packages that are to be configured.
                  By default, each package is expected to have a configure.zcml
                  file located in the package root.  Optionally, a package
                  can be identified as a sequence whose first entry is the
                  Python package, and whose second entry is the zcml file name
                  (string) that is to be configured.
    """
    try:
        iter(packages)
        packages = list(packages)
    except TypeError:
        packages = [packages]
    packages = [
                 (zope.component, 'meta.zcml'),
                 (zope.security, 'meta.zcml'),
                 (zope.component, 'configure.zcml')
                 ] + packages
    for config in packages:
        try:
            iter(config)
        except:
            config = (config, 'configure.zcml',)
        package, zcml = config
        zope.configuration.xmlconfig.XMLConfig(zcml, package)()
        logger.debug("Configured package %s with zcml file %s", str(package), str(zcml))


def ConfigurationRequired(classThatRequiresConfigration):
    """Decorator for callables that require ZCA registry configuration
    
    Mostly, the sparc framework does not require use of ZCA.  The *.zcml
    files allows users of the framework to interact via ZCA, however, it
    is not a strict requirement for use.  Because of this, most things in 
    sparc will not utilize component lookups.
    
    However, on occasion, it makes sense to put common code such as mixins
    that *do* require component lookups.  For these cases, we decorate them 
    in order to make it clear that these items require a configured registry
    to function.
    """
    def _checkForZCARegistry(*args, **kwargs):
        gsm = getGlobalSiteManager()
        configured = False
        for a in gsm.registeredAdapters():
            configured = True
            break
        for h in gsm.registeredSubscriptionAdapters():
            configured = True
            break
        for u in gsm.registeredUtilities():
            configured = True
            break
        for h in gsm.registeredHandlers():
            configured = True
            break
        if not configured:
            raise ComponentLookupError("Use of this class requires sparc component registration.")
        return classThatRequiresConfigration(*args, **kwargs)
    return _checkForZCARegistry