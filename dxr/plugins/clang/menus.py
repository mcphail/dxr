"""All menu constructors for the C/C++ refs."""

from os.path import basename

from flask import url_for

from dxr.app import DXR_BLUEPRINT
from dxr.utils import search_url


BROWSE = DXR_BLUEPRINT + '.browse'


def quote(qualname):
    """Wrap qualname in quotes if it contains spaces."""
    if ' ' in qualname:
        qualname = '"' + qualname + '"'
    return qualname


def include_menu(tree, include):
    """Return menu for include reference."""
    # TODO: Check against the ignore patterns, and don't link to files we
    # won't build pages for.
    return [{'html': 'Jump to file',
             'title': 'Jump to what is included here.',
             'href': url_for(BROWSE,
                             tree=tree.name,
                             path=include['target_path']),
             'icon': 'jump'}]


def macro_menu(tree, macro):
    """Return menu for macro reference."""
    name = macro['name']
    return [{'html': "Find references",
             'title': "Find references to macros with this name",
             'href': search_url(tree, "+macro-ref:%s" % name),
             'icon': 'reference'}]


def type_menu(tree, type):
    """Return menu for type reference."""
    qualname, kind = type['qualname'], type.get('kind')
    menu = [{'html': "Find declarations",
             'title': "Find declarations of this class",
             'href': search_url(tree, "+type-decl:%s" % quote(qualname)),
             'icon': 'reference'}]
    if kind == 'class' or kind == 'struct':
        menu.append({'html': "Find subclasses",
                     'title': "Find subclasses of this class",
                     'href': search_url(tree, "+derived:%s" % quote(qualname)),
                     'icon': 'type'})
        menu.append({'html': "Find base classes",
                     'title': "Find base classes of this class",
                     'href': search_url(tree, "+bases:%s" % quote(qualname)),
                     'icon': 'type'})
    menu.append({'html': "Find members",
                 'title': "Find members of this class",
                 'href': search_url(tree, "+member:%s" % quote(qualname)),
                 'icon': 'members'})
    menu.append({'html': "Find references",
                 'title': "Find references to this class",
                 'href': search_url(tree, "+type-ref:%s" % quote(qualname)),
                 'icon': 'reference'})
    return menu


def typedef_menu(tree, typedef):
    """Build menu for typedef."""
    qualname = typedef['qualname']
    return [{'html': "Find references",
             'title': "Find references to this typedef",
             'href': search_url(tree, "+type-ref:%s" % quote(qualname)),
             'icon': 'reference'}]


def variable_menu(tree, variable):
    """Build menu for a variable."""
    qualname = variable['qualname']
    return [{'html': "Find declarations",
             'title': "Find declarations of this variable",
             'href': search_url(tree, "+var-decl:%s" % quote(qualname)),
             'icon': 'reference'},
            {'html': "Find references",
             'title': "Find reference to this variable",
             'href': search_url(tree, "+var-ref:%s" % quote(qualname)),
             'icon': 'field'}]


def namespace_menu(tree, namespace):
    """Build menu for a namespace."""
    qualname = namespace['qualname']
    return [{'html': "Find definitions",
             'title': "Find definitions of this namespace",
             'href': search_url(tree, "+namespace:%s" % quote(qualname)),
             'icon': 'jump'},
            {'html': "Find references",
             'title': "Find references to this namespace",
             'href': search_url(tree, "+namespace-ref:%s" % quote(qualname)),
             'icon': 'reference'}]


def namespace_alias_menu(tree, namespace_alias):
    """Build menu for a namespace."""
    qualname = namespace_alias['qualname']
    return [{'html': "Find references",
             'title': "Find references to this namespace alias",
             'href': search_url(tree, "+namespace-alias-ref:%s" % quote(qualname)),
             'icon': 'reference'}]


# TODO: Shouldn't we have a menu on calls pointing to the function called?
# Prod does.


def function_menu(tree, func):
    """Build menu for a function."""
    qualname = func['qualname']
    isvirtual = 'override' in func
    # Things we can do with qualified name
    menu = [{'html': "Find declarations",
             'title': "Find declarations of this function",
             'href': search_url(tree, "+function-decl:%s" % quote(qualname)),
             'icon': 'reference'},
            {'html': "Find callers",
             'title': "Find functions that call this function",
             'href': search_url(tree, "+callers:%s" % quote(qualname)),
             'icon': 'method'},
            {'html': "Find references",
             'title': "Find references to this function",
             'href': search_url(tree, "+function-ref:%s" % quote(qualname)),
             'icon': 'reference'}]
    if isvirtual:
        menu.append({'html': "Find overridden",
                     'title': "Find functions that this function overrides",
                     'href': search_url(tree, "+overridden:%s" % quote(qualname)),
                     'icon': 'method'})
        menu.append({'html': "Find overrides",
                     'title': "Find overrides of this function",
                     'href': search_url(tree, "+overrides:%s" % quote(qualname)),
                     'icon': 'method'})
    return menu


def definition_menu(tree, path, row):
    """Return a one-item menu for jumping directly to something's definition."""
    return [{'html': "Jump to definition",
             'title': "Jump to the definition in '%s'" % basename(path),
             'href': url_for(BROWSE, tree=tree.name, path=path, _anchor=row),
             'icon': 'jump'}]
