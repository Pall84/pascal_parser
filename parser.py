__author__ = 'palleymundsson'

from plex import *
import TokenCode
import DataType
import OpType

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

    # keywords                     tokencode            datatype            optype
    (NoCase(Str("program")),    (TokenCode.tc_PROGRAM, DataType.dt_KEYWORD, OpType.op_NONE)),
    (NoCase(Str("var")),        (TokenCode.tc_VAR, DataType.dt_KEYWORD, OpType.op_NONE)),
    (NoCase(Str("array")),      (TokenCode.tc_ARRAY, DataType.dt_KEYWORD, OpType.op_NONE)),
    (NoCase(Str("of")),         (TokenCode.tc_OF, DataType.dt_KEYWORD, OpType.op_NONE)),
    (NoCase(Str("integer")),    (TokenCode.tc_INTEGER, DataType.dt_KEYWORD, OpType.op_NONE)),
    (NoCase(Str("real")),       (TokenCode.tc_REAL, DataType.dt_KEYWORD, OpType.op_NONE)),
    (NoCase(Str("function")),   (TokenCode.tc_FUNCTION, DataType.dt_KEYWORD, OpType.op_NONE)),
    (NoCase(Str('procedure')),  (TokenCode.tc_PROCEDURE, DataType.dt_KEYWORD, OpType.op_NONE)),
    (NoCase(Str('begin')),      (TokenCode.tc_BEGIN, DataType.dt_KEYWORD, OpType.op_NONE)),
    (NoCase(Str('end')),        (TokenCode.tc_END, DataType.dt_KEYWORD, OpType.op_NONE)),
    (NoCase(Str('if')),         (TokenCode.tc_IF, DataType.dt_KEYWORD, OpType.op_NONE)),
    (NoCase(Str('then')),       (TokenCode.tc_THEN, DataType.dt_KEYWORD, OpType.op_NONE)),
    (NoCase(Str('else')),       (TokenCode.tc_ELSE, DataType.dt_KEYWORD, OpType.op_NONE)),
    (NoCase(Str('while')),      (TokenCode.tc_WHILE, DataType.dt_KEYWORD, OpType.op_NONE)),
    (NoCase(Str('do')),         (TokenCode.tc_DO, DataType.dt_KEYWORD, OpType.op_NONE)),
    (NoCase(Str('not')),        (TokenCode.tc_NOT, DataType.dt_KEYWORD, OpType.op_NONE)),

    # numbers
    (int_num,                   (TokenCode.tc_NUMBER, DataType.dt_INTEGER, OpType.op_NONE)),
    (real_num,                  (TokenCode.tc_NUMBER, DataType.dt_REAL, OpType.op_NONE)),

    # relop
    (Str('='),   (TokenCode.tc_RELOP, DataType.dt_OP, OpType.op_NONE)),
    (Str('<>'),  'my_<>'),
    (Str('<'),   'my_<'),
    (Str('<='),   'my_<='),
    (Str('>='),  'my_>='),
    (Str('>'),   'my_>'),

    # addop
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