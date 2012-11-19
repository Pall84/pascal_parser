__author__ = 'palleymundsson'

from plex import *

letter = Range("azAZ")
digit = Range("09")
digits = Rep1(digit)
id = letter + Rep( letter | digits)
int_num = digits
optional_fraction = Opt(Str(".") + int_num)
optional_exponent = Opt(Str("E") + Opt(Str("+")|Str("-'")) + int_num )
real_num = int_num + optional_fraction + optional_exponent
comment = Str("{") + Rep(AnyChar) + Str("}")


lexicon = Lexicon([
    (NoCase(Str("program")), "my_program"),
    (NoCase(Str("var")),   'my_var'),
    (NoCase(Str("of")),      'my_of'),
    (NoCase(Str("integer")), 'my_integer'),
    (NoCase(Str("real")),    'my_real'),
    (NoCase(Str("function")),    'my_function'),
    (NoCase(Str('procedure')),   'my_procedure'),
    (NoCase(Str('begin')),   'my_begin'),
    (NoCase(Str('end')),     'my_end'),
    (NoCase(Str('if')),      'my_end'),
    (NoCase(Str('then')),    'my_then'),
    (NoCase(Str('else')),    'my_else'),
    (NoCase(Str('while')),   'my_while'),
    (NoCase(Str('do')),  'my_do'),
    (NoCase(Str('not')), 'my_not'),
    (int_num,   'my_num'),
    (real_num,  'my_num'),
    (Str('='),   'my_='),
    (Str('<>'),  'my_<>'),
    (Str('<'),   'my_<'),
    (Str('<='),   'my_<='),
    (Str('>='),  'my_>='),
    (Str('>'),   'my_>'),
    (Str('-'),   'my_-'),
    (Str('+'),   'my_+'),
    (NoCase(Str('or')),  "my_or"),
    (Str('/'),   "my_/"),
    (NoCase(Str('div')), "my_div"),
    (NoCase(Str('mod')), "my_mod"),
    (NoCase(Str('and')), "my_and"),
    (Str(':='),  "my_:="),
    (Str(':'),   "my_:"),
    (Str(';'),   "my_;"),
    (Str(','),   "my_,"),
    (Str('..'),  "my_.."),
    (Str('.'),   "my_."),
    (Str('('),   "my_("),
    (Str('['),   "my_["),
    (Str(')'),   "my_)"),
    (Str(']'),   "my-]"),
    (id,    "my_id"),
    (comment,   "my_comments"),
    (Rep1(Any(" \t\n")), IGNORE),
    (AnyChar, "my_error")
])

filename = "test_files/pascal_lex1.txt"
f = open(filename, "r")
scanner = Scanner(lexicon, f, filename)
while 1:
    token = scanner.read()
    print token
    if token[0] is None:
        break