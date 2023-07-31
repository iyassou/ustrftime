import time
import re

__DIRECTIVE_REGEX_STR: str  = '%[aAbBcdHIjmMpSUwWxXyY%]'
__DIRECTIVE_REGEX: object   = re.compile(__DIRECTIVE_REGEX_STR)
__DATE_TIME_FMTDIR: str     = '%a %b %d %H:%M:%S %Y'    # %c
__DATE_FMTDIR: str          = '%d/%m/%y'                # %x
__TIME_FMTDIR: str          = '%H:%M:%S'                # %X

__DOTW: tuple = (
    'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'
)
__MOTY: tuple = (
    'January', 'February', 'March', 'April', 'May', 'June', 'July',
    'August', 'September', 'October', 'November', 'December'
)

__YEAR      = const(0)
__MONTH     = const(1)
__MDAY      = const(2)
__HOUR      = const(3)
__MINUTE    = const(4)
__SECOND    = const(5)
__WEEKDAY   = const(6)
__YEARDAY   = const(7)

def __zfill(format_me, width: int) -> str:
    # str.zfill, but can format objects directly.
    return '{:0>{}}'.format(format_me, width)

def strftime(_fmt: str, st_time: tuple=None) -> str:
    if st_time is None:
        st_time: tuple = time.localtime()
    # Expand recursive formatting directives.
    fmt = re.sub('%c', __DATE_TIME_FMTDIR, _fmt)
    fmt = re.sub('%x', __DATE_FMTDIR, fmt)
    fmt = re.sub('%X', __TIME_FMTDIR, fmt)
    # Look for and implement formatting directives:
    # => re.findall with formatting-as-you-go
    # NOTE: https://github.com/arnoldrobbins/strftime/blob/master/strftime.c#L991
    #       for how to handle %U and %W
    left = 0
    fmtdirs = []
    m = re.search(__DIRECTIVE_REGEX_STR, fmt)
    while m is not None:
        # Take the character.
        token: str = m.group(0)[1]
        # Implement directive.
        fmtdir: str
        if token == 'a':
            # abbreviated weekday name
            fmtdir = __DOTW[st_time[__WEEKDAY]][:3]
        elif token == 'A':
            # full weekday name
            fmtdir = __DOTW[st_time[__WEEKDAY]]
        elif token == 'b':
            # abbreviated month name
            fmtdir = __MOTY[st_time[__MONTH] - 1][:3]
        elif token == 'B':
            # full month name
            fmtdir = __MOTY[st_time[__MONTH] - 1]
        elif token == 'd':
            # day of the month
            fmtdir = __zfill(st_time[__MDAY], 2)
        elif token == 'H':
            # hour (24-hour clock)
            fmtdir = __zfill(st_time[__HOUR], 2)
        elif token == 'I':
            # hour (12-hour clock)
            hour = st_time[__HOUR] % 12
            fmtdir = '12' if not hour else __zfill(hour, 2)
        elif token == 'j':
            # day of the year
            fmtdir = __zfill(st_time[__YEARDAY], 3)
        elif token == 'm':
            # month as decimal number
            fmtdir = __zfill(st_time[__MONTH], 2)
        elif token == 'M':
            # minute as decimal number
            fmtdir = __zfill(st_time[__MINUTE], 2)
        elif token == 'p':
            # AM or PM
            fmtdir = 'PM' if st_time[__HOUR] >= 12 else 'AM'
        elif token == 'S':
            # second as a decimal number
            fmtdir = __zfill(st_time[__SECOND], 2)
        elif token == 'U':
            # week number of the year (Sunday = 0), [00, 53]
            fmtdir = __zfill((st_time[__YEARDAY] + 7 - st_time[__WEEKDAY]) // 7, 2)
        elif token == 'w':
            # weekday as a decimal number [0(Sunday), 6]
            wday: int = st_time[__WEEKDAY]
            fmtdir = '0' if wday == 6 else str(wday + 1)
        elif token == 'W':
            # week number of the year (Monday = 0), [00, 53]
            wday: int = st_time[__WEEKDAY]
            wday = 6 if not wday else wday - 1
            fmtdir = __zfill((st_time[__YEARDAY] + 7 - wday) // 7, 2)
        elif token == 'y':
            # year without century number as a decimal number
            fmtdir = __zfill(st_time[__YEAR] % 100, 2)
        elif token == 'Y':
            # year with century as decimal number
            fmtdir = str(st_time[__YEAR])
        elif token == '%':
            # literal '%'
            fmtdir = token
        fmtdirs.append(fmtdir)
        # Advance left index.
        left += fmt[left:].index(token) + len(token)
        # Search again.
        m = re.search(__DIRECTIVE_REGEX_STR, fmt[left:])
    if not fmtdirs:
        # Return original format string.
        return _fmt
    # Get non-(formatting directive) bits, interleave with formatted results,
    # and ''.join(the whole).
    non_fmtdirs: list = __DIRECTIVE_REGEX.split(fmt)
    # NOTE: len(non_fmtdirs) == len(fmtdirs) + 1
    fmtdirs.append('')
    return ''.join(x for pair in zip(non_fmtdirs, fmtdirs) for x in pair)
