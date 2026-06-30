#!/usr/bin/env python3

# Python 3.14 Compatibility Monkeypatches:
# Older versions of pytest (7.2.0) and werkzeug (2.2.2) rely on deprecated/removed ast module attributes
# (like ast.Str, ast.NameConstant, and the .s / .n properties on Constant).
# These patches dynamically restore them for runtime compatibility on Python 3.14.
import ast
if not hasattr(ast, 'Str'):
    ast.Str = ast.Constant
if not hasattr(ast, 'NameConstant'):
    ast.NameConstant = ast.Constant
if not hasattr(ast.Constant, 's'):
    ast.Constant.s = property(lambda self: self.value, lambda self, val: setattr(self, 'value', val))
if not hasattr(ast.Constant, 'n'):
    ast.Constant.n = property(lambda self: self.value, lambda self, val: setattr(self, 'value', val))


def pytest_itemcollected(item):
    par = item.parent.obj
    node = item.obj
    pref = par.__doc__.strip() if par.__doc__ else par.__class__.__name__
    suf = node.__doc__.strip() if node.__doc__ else node.__name__
    if pref or suf:
        item._nodeid = ' '.join((pref, suf))


