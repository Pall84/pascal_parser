__author__ = 'palleymundsson'

from plex import *
import TokenCode
import DataType
import OpType

def getLexer():

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
        (NoCase(Str("procedure")),  (TokenCode.tc_PROCEDURE, DataType.dt_KEYWORD, OpType.op_NONE)),
        (NoCase(Str("begin")),      (TokenCode.tc_BEGIN, DataType.dt_KEYWORD, OpType.op_NONE)),
        (NoCase(Str("end")),        (TokenCode.tc_END, DataType.dt_KEYWORD, OpType.op_NONE)),
        (NoCase(Str("if")),         (TokenCode.tc_IF, DataType.dt_KEYWORD, OpType.op_NONE)),
        (NoCase(Str("then")),       (TokenCode.tc_THEN, DataType.dt_KEYWORD, OpType.op_NONE)),
        (NoCase(Str("else")),       (TokenCode.tc_ELSE, DataType.dt_KEYWORD, OpType.op_NONE)),
        (NoCase(Str("while")),      (TokenCode.tc_WHILE, DataType.dt_KEYWORD, OpType.op_NONE)),
        (NoCase(Str("do")),         (TokenCode.tc_DO, DataType.dt_KEYWORD, OpType.op_NONE)),
        (NoCase(Str("not")),        (TokenCode.tc_NOT, DataType.dt_KEYWORD, OpType.op_NONE)),
        (Str(':'),                  (TokenCode.tc_COLON, DataType.dt_KEYWORD, OpType.op_NONE)),
        (Str(';'),                  (TokenCode.tc_SEMICOL, DataType.dt_KEYWORD, OpType.op_NONE)),
        (Str(','),                  (TokenCode.tc_COMMA, DataType.dt_KEYWORD, OpType.op_NONE)),
        (Str('..'),                 (TokenCode.tc_DOTDOT, DataType.dt_KEYWORD, OpType.op_NONE)),
        (Str('.'),                  (TokenCode.tc_DOT, DataType.dt_KEYWORD, OpType.op_NONE)),
        (Str('('),                  (TokenCode.tc_LPAREN, DataType.dt_KEYWORD, OpType.op_NONE)),
        (Str('['),                  (TokenCode.tc_LBRACK, DataType.dt_KEYWORD, OpType.op_NONE)),
        (Str(')'),                  (TokenCode.tc_RPAREN, DataType.dt_KEYWORD, OpType.op_NONE)),
        (Str(']'),                  (TokenCode.tc_RBRACK, DataType.dt_KEYWORD, OpType.op_NONE)),

        # numbers
        (int_num,                   (TokenCode.tc_NUMBER, DataType.dt_INTEGER, OpType.op_NONE)),
        (real_num,                  (TokenCode.tc_NUMBER, DataType.dt_REAL, OpType.op_NONE)),

        # relop
        (Str("="),                  (TokenCode.tc_RELOP, DataType.dt_OP, OpType.op_EQ)),
        (Str("<>"),                 (TokenCode.tc_RELOP, DataType.dt_OP, OpType.op_NE)),
        (Str("<"),                  (TokenCode.tc_RELOP, DataType.dt_OP, OpType.op_LT)),
        (Str("<="),                 (TokenCode.tc_RELOP, DataType.dt_OP, OpType.op_LE)),
        (Str(">="),                 (TokenCode.tc_RELOP, DataType.dt_OP, OpType.op_GE)),
        (Str(">"),                  (TokenCode.tc_RELOP, DataType.dt_OP, OpType.op_GT)),

        # addop
        (Str("-"),                  (TokenCode.tc_ADDOP, DataType.dt_OP, OpType.op_MINUS)),
        (Str("+"),                  (TokenCode.tc_ADDOP, DataType.dt_OP, OpType.op_PLUS)),
        (NoCase(Str("or")),         (TokenCode.tc_ADDOP, DataType.dt_OP, OpType.op_OR)),

        # mulop
        (Str("/"),                  (TokenCode.tc_MULOP, DataType.dt_OP, OpType.op_DIVIDE)),
        (Str("*"),                  (TokenCode.tc_MULOP, DataType.dt_OP, OpType.op_MULT)),
        (NoCase(Str("div")),        (TokenCode.tc_MULOP, DataType.dt_OP, OpType.op_DIV)),
        (NoCase(Str("mod")),        (TokenCode.tc_MULOP, DataType.dt_OP, OpType.op_MOD)),
        (NoCase(Str("and")),        (TokenCode.tc_MULOP, DataType.dt_OP, OpType.op_AND)),

        # assignop
        (Str(':='),                 (TokenCode.tc_ASSIGNOP, DataType.dt_OP, OpType.op_NONE)),


        (id,                        (TokenCode.tc_ID, DataType.dt_ID, OpType.op_NONE)),
        (comment,               IGNORE),
        (Rep1(Any(" \t\n")),    IGNORE),
        (AnyChar,                   (TokenCode.tc_ERROR, DataType.dt_NONE, OpType.op_NONE))
    ])

    return lexicon