# ustrftime
A MicroPython implementation of `time.strftime`

## About

`ustrftime.strftime` accepts a formatting string and a `time.localtime()` 8-tuple ([whose MicroPython format is described here](https://docs.micropython.org/en/latest/library/time.html#time.localtime)).

## Usage

```python
>>> from ustrftime import strftime
>>> import time
>>> strftime('%c', time.localtime())
Mon Jul 31 14:42:14 2023
>>> strftime('%X', time.localtime())
14:42:34
>>> strftime('%x', time.localtime())
31/07/23
```

## Notes

A specific locale can be achieved by editing the `ustrftime.strftime` function as well as the `__DOTW`, `__MOTY`, `__DATE_TIME_FMTDIR`, `__DATE_FMTDIR`, `__TIME_FMTDIR` variables.

The following formatting directives are supported ([full list here](https://docs.python.org/3/library/time.html#time.strftime)):

| Directive | Meaning |
|:---:|:---|
| %a | Locale’s abbreviated weekday name. |
| %A | Locale’s full weekday name. |
| %b | Locale’s abbreviated month name. |
| %B | Locale’s full month name. |
| %c | Locale’s appropriate date and time representation. |
| %d | Day of the month as a decimal number [01,31]. |
| %H | Hour (24-hour clock) as a decimal number [00,23]. |
| %I | Hour (12-hour clock) as a decimal number [01,12]. |
| %j | Day of the year as a decimal number [001,366]. |
| %m | Month as a decimal number [01,12]. |
| %M | Minute as a decimal number [00,59]. |
| %p | Locale’s equivalent of either AM or PM. |
| %S | Second as a decimal number [00,61]. |
| %U | Week number of the year (Sunday as the first day of the week) as a decimal number [00,53]. All days in a new year preceding the first Sunday are considered to be in week 0. |
| %w | Weekday as a decimal number [0(Sunday),6]. |
| %W | Week number of the year (Monday as the first day of the week) as a decimal number [00,53]. All days in a new year preceding the first Monday are considered to be in week 0. |
| %x | Locale’s appropriate date representation. |
| %X | Locale’s appropriate time representation. |
| %y | Year without century as a decimal number [00,99]. |
| %Y | Year with century as a decimal number. |
| %% | A literal '%' character. |
