"""Set of printable characters."""

from string import ascii_letters, digits,  punctuation

_ascii_printables_chars = r""" {0}{1}{2}""".format(digits, ascii_letters, punctuation)
_ascii_printables_codes = [ord(printable) for printable in _ascii_printables_chars]

_ascii_printables_codes.sort()
MIN_ASCII_CODE = _ascii_printables_codes[0]
MAX_ASCII_CODE = _ascii_printables_codes[-1]

ASCII_CODES_TABLE_SIZE = len(_ascii_printables_codes)

ASCII_PRINTABLES_CODES = _ascii_printables_codes

pass