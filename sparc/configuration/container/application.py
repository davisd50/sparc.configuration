import argparse
import sys
from zope import component
from zope import event
from zope import interface
from zope.configuration.xmlconfig import XMLConfig
from zope.interface.exceptions import DoesNotImplement
from sparc.configuration import zcml
from sparc.configuration.container.zcml import IZCMLFiles
from sparc.configuration.events import SparcApplicationConfiguredEvent
from sparc.logging import logging

import zope.component.event #needed in order to initialize the event notification environment

from . import ISparcPyContainerConfiguredApplication


def getScriptArgumentParser(description, args=sys.argv):
    """Return ArgumentParser object
    
    Args:
        description: Text description of application ArgumentParser will be
                     applied to.
    
    Kwargs:
        args (list):        list of arguments that will be parsed.  The default
                            is the sys.argv list, and should be correct for most
                            use cases.
    
    Returns:
        ArgumentParser object that can be used to validate and execute the
        current script invocation.
    """
    # Description
    parser = argparse.ArgumentParser(
            description=description)

    # config_file
    parser.add_argument('config_file',
            help="Valid script configuration file.  This should be the path to "\
                 "the script YAML configuration file.  See config_sample.yaml"\
                 "for detailed specifications.")
    
    # --verbose
    parser.add_argument('--verbose',
            action='store_true',
            help="Echo verbose messages to stdout.")
    
    # --debug
    parser.add_argument('--debug',
            action='store_true',
            help="Echo debug messages to stdout.")
    
    return parser


@interface.implementer(ISparcPyContainerConfiguredApplication)
class YamlCliAppMixin(object):
    def __init__(self, config=None, verbose=False, debug=False):
        """Init
        
        Args:
            config: ISparcAppPyContainerConfiguration compatible Py container for runtime configuration (i.e. a dict or list)
            verbose: True indicates verbose logging
            debug: True indicate debug logging
        """
        self.setLoggers(verbose, debug)
        #Setup the Zope component registry
        zcml.Configure(packages=[self.app_zcml]) # base app component registrations
        self.logger.debug("Zope Component Registry initialized")
        if not config:
            config = {}
        self._config = component.createObject(u'sparc.configuration.container', config) # initialize
    
    def get_config(self):
        return self._config
    
    def set_config(self, config):
        if not ISparcPyContainerConfiguredApplication.providedBy(config):
            config = component.createObject(u'sparc.configuration.container', config)
        self._config = config

    def configure(self):
        #Search/load any additional runtime config zcml
        for z_file in IZCMLFiles(self.get_config()):
            XMLConfig(z_file.file, z_file.package)()
            self.logger.info("zcml configuration processed for {}:{}".format(z_file.package.__name__ if z_file.package else None, z_file.file))
        event.notify(SparcApplicationConfiguredEvent(self))

    def setLoggers(self, verbose, debug):
        logger = logging.getLogger() # root logger
        if verbose:
            logger.setLevel('INFO')
        if debug:
            logger.setLevel('DEBUG')

    # OVERRIDES
    #  Class extenders need to implement these artifacts
    
    logger = None #override with app specific logger
    app_zcml = None #Optional, override with tuple (py_package_object, 'configure.zcml')
    def go(self):
        raise DoesNotImplement()