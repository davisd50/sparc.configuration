from zope.component import getSiteManager
from zope.component.interfaces import ComponentLookupError
from zope.component import getUtility
from zope.interface import implements
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.interfaces import IVocabularyRegistry
from zope.schema.vocabulary import setVocabularyRegistry
import zope.configuration.xmlconfig
import zope.component
import zope.security

import sparc.common.log
import logging
logger = logging.getLogger('sparc.common.configure')

#Copied from Zope2.App.schema
class Zope2VocabularyRegistry(object):
    """IVocabularyRegistry that supports global and local utilities.
    """

    implements(IVocabularyRegistry)
    __slots__ = ()

    def get(self, context, name):
        """See zope.schema.interfaces.IVocabularyRegistry.
        """
        factory = getUtility(IVocabularyFactory, name)
        return factory(context)

#Copied from Zope2.App.schema
def configure_vocabulary_registry():
    setVocabularyRegistry(Zope2VocabularyRegistry())


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
                 (zope.component, 'configure.zcml'),
                 (zope.security, 'configure.zcml')
                 ] + packages
    for config in packages:
        try:
            iter(config)
        except:
            config = (config, 'configure.zcml',)
        package, zcml = config
        zope.configuration.xmlconfig.XMLConfig(zcml, package)()
        logger.debug("Configured package %s with zcml file %s", str(package), str(zcml))
    #This allows vocabulary lookups from schemas via IVocabularyFactory interface
    configure_vocabulary_registry()


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
        sm = getSiteManager()
        configured = False
        for a in sm.registeredAdapters():
            configured = True
            break
        for h in sm.registeredSubscriptionAdapters():
            configured = True
            break
        for u in sm.registeredUtilities():
            configured = True
            break
        for h in sm.registeredHandlers():
            configured = True
            break
        if not configured:
            raise ComponentLookupError("Use of this class requires sparc component registration.")
        return classThatRequiresConfigration(*args, **kwargs)
    return _checkForZCARegistry