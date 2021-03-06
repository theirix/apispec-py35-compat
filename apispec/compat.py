# -*- coding: utf-8 -*-
import sys
import itertools
import functools
import inspect

PY2 = int(sys.version_info[0]) == 2
PY26 = PY2 and int(sys.version_info[1]) < 7

if PY2:
    import urlparse
    urlparse = urlparse
    text_type = unicode
    binary_type = str
    string_types = (str, unicode)
    unicode = unicode
    basestring = basestring
    iterkeys = lambda d: d.iterkeys()
    itervalues = lambda d: d.itervalues()
    iteritems = lambda d: d.iteritems()
    zip_longest = itertools.izip_longest
    if PY26:
        from .ordereddict import OrderedDict
    else:
        from collections import OrderedDict
    OrderedDict = OrderedDict
    def get_func_args(func):
        if isinstance(func, functools.partial):
            return list(inspect.getargspec(func.func).args)
        if inspect.isfunction(func) or inspect.ismethod(func):
            return list(inspect.getargspec(func).args)
        if callable(func):
            return list(inspect.getargspec(func.__call__).args)
else:
    import urllib.parse
    urlparse = urllib.parse
    text_type = str
    binary_type = bytes
    string_types = (str,)
    unicode = str
    basestring = (str, bytes)
    iterkeys = lambda d: d.keys()
    itervalues = lambda d: d.values()
    iteritems = lambda d: d.items()
    zip_longest = itertools.zip_longest
    from collections import OrderedDict
    OrderedDict = OrderedDict
    def get_func_args(func):
        if isinstance(func, functools.partial):
            return list(inspect.signature(func.func).parameters)
        if inspect.isfunction(func):
            return list(inspect.signature(func).parameters)
        if callable(func) or inspect.ismethod(func):
            return ['self'] + list(inspect.signature(func.__call__).parameters)


# From six
def with_metaclass(meta, *bases):
    """Create a base class with a metaclass."""
    # This requires a bit of explanation: the basic idea is to make a dummy
    # metaclass for one level of class instantiation that replaces itself with
    # the actual metaclass.
    class metaclass(meta):  # noqa

        def __new__(cls, name, this_bases, d):
            return meta(name, bases, d)
    return type.__new__(metaclass, 'temporary_class', (), {})

