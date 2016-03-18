sparc.configuration
====================

Basic common configuration tools used in the SPARC platform.  Includes, but 
not limited to Zope Component ZCML utilities.

ZCA Configuration
-----------------
Tools that leverage SPARC packages are usually also dependant on Zope 
Component Architecture (http://docs.zope.org/zope.component/narr.html).  Use 
of ZCA requires component configuration,which SPARC does via ZCML 
(https://github.com/zopefoundation/zope.component/blob/master/docs/zcml.rst).

Among other things, sparc.common provides access to Configure(), an easy 
function that can be used to configure dependant applications.

### Usage - ZCA configuration
    This simplifies your ability to create components via ZCML and have 
    your application parse the ZCML files to allow them to be registered for 
    lookup.
    >>> import a.package.that.contains.a.configure.zcml
    >>> import another.package.that.contains.a.configure.zcml
    >>> from sparc.common import Configure
    >>> Configure([your.package.that.contains.a.configure.zcml,
    ...            another.package.that.contains.a.configure.zcml])
    
    You will now have access to components configured within those packages.

### Usage - Retrieve user feedback from CLI application
    This simplifies the process of getting feedback for processing within 
    a CLI application.
    >>> import sparc.common
    >>> from sparc.common import Configure
    >>> from sparc.common import ICallable
    >>> from zope.component import getUtility
    >>> Configure([sparc.common])
    >>> asker = getUtiliy(ICallable, 'sparc.common.ask_question')
    >>> answer = asker(u"How are you?", required = True, answers = \
    ... 				{'1':'awesome','2':'ok','3':'not so good'}, tries = 3)
    How are you?
    (1) awesome
    (2) ok
    (3) not so good
    
    >>> print answer
    '1'
  