from zope import interface
from zope.interface.interfaces import ObjectEvent
from .interfaces import ISparcApplicationConfiguredEvent

@interface.implementer(ISparcApplicationConfiguredEvent)
class SparcApplicationConfiguredEvent(ObjectEvent):
    """A configuration has been applied to a ISparcApplication"""