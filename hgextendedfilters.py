# hgextendedfilters.py - A collection of extra template filters for Mercurial
#
# Copyright 2011 Nat Williams <nat.williams@gmail.com>
#
# Since hg is GPL2, I'm guessing that this is too.  So blah blah blah whatever
# that entails

"""A few nice filters for templates and style files

trailingspace,
parens, squarebrackets, anglebrackets,
colors
"""

from functools import partial

from mercurial import templatefilters


def trailingspace(thing):
    """Template filter to add trailing space after non-empty item.
    Note that this filter implicitly calls stringify on the item.

    """
    thing = templatefilters.filters['stringify'](thing)
    if thing:
        return thing + " "
    else:
        return thing


def surround(thing, left, right):
    thing = templatefilters.filters['stringify'](thing)
    if thing:
        return "%s%s%s" % (left, thing, right)
    else:
        return thing


color_codes = {
    'black': '0;30',
    'red': '0;31',
    'green': '0;32',
    'brown': '0;33',
    'blue': '0;34',
    'purple': '0;35',
    'magenta': '0;35',
    'cyan': '0;36',
    'light_gray': '0;37',
    'dark_gray': '1;30',
    'light_red': '1;31',
    'light_green': '1;32',
    'yellow': '1;33',
    'light_blue': '1;34',
    'light_purple': '1;35',
    'light_magenta': '1;35',
    'light_cyan': '1;36',
    'white': '1;37',
    'reset': '0',
}

def colorize(text, color):
    # TODO: make this controled by the color plugin?
    text = templatefilters.filters['stringify'](text)
    return '\033[%sm%s\033[%sm' % (color_codes[color], text,
                                    color_codes['reset'])


def notnone(thing):
    """Template filter to convert literal None or "None" values to an empty
    string.  Useful when you want to stringify things like `branches` that can
    return None

    """
    if thing is None or thing == 'None':
        return ''
    return thing


def reposetup(ui, repo):
    templatefilters.filters.update({
        'trailingspace': trailingspace,
        'parens': lambda x: surround(x, '(', ')'),
        'squarebrackets': lambda x: surround(x, '[', ']'),
        'anglebrackets': lambda x: surround(x, '<', '>'),
        'notnone': notnone,
    })
    for code in color_codes:
        templatefilters.filters[code] = partial(colorize, color=code)
