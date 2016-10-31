import argparse
from importlib import import_module
import sys
from zope import component
from zope import interface
from zope.configuration.xmlconfig import XMLConfig
from zope.interface.exceptions import DoesNotImplement
from sparc.configuration import container
from sparc.configuration import yaml
from sparc.configuration import zcml
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
    def __init__(self, args):
        """Init
        
        Args:
            args: argparse.ArgumentParser object with config_file, --verbose,
                  and --debug argument options.
        """
        self.setLoggers(args)
        #Setup the Zope component registry
        zcml.Configure(packages=[self.app_zcml]) # base app configuration
        self.logger.debug("Zope Component Registry initialized")
        #Load the application config
        yaml_doc = component.getUtility(\
                            yaml.ISparcYamlDocuments).first(args.config_file)
        self.config = component.createObject(\
                                    u'sparc.configuration.container', yaml_doc)
        #Search/load any additional zcml
        yml_iter = component.getUtility(container.ISparcPyDictValueIterator)
        for zcml_ in yml_iter.values(self.config, 'ZCMLConfiguration'):
            pkg = import_module(zcml_['package'])
            file_ = zcml_['file'] if 'file' in zcml_ else 'configure.zcml'
            XMLConfig(file_, pkg)()
            self.logger.info("zcml configuration processed for {}:{}".format(zcml_['package'], file_))

    def setLoggers(self, args):
        logger = logging.getLogger() # root logger
        if args.verbose:
            logger.setLevel('INFO')
        if args.debug:
            logger.setLevel('DEBUG')

    # OVERRIDES
    #  Class extenders need to implement these artifacts
    
    logger = None #override with app specific logger
    app_zcml = None #Optional, override with tuple (py_package_object, 'configure.zcml')
    def go(self):
        raise DoesNotImplement()