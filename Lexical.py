__author__ = 'Palli'

__author__ = 'palleymundsson'

from plex import *
from Enums import *

class Lexicons:
    def __init__(self):
        pass
    def getLexer(self):

        letter = Range("azAZ")
        digit = Range("09")
        digits = Rep1(digit)
        id = letter + Rep( letter | digits)
        int_num = digits
        optional_fraction = Opt(Str(".") + int_num)
        optional_exponent = Opt(Str("E") + Opt(Str("+")|Str("-")) + int_num )
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
            (comment,                   (TokenCode.tc_COMMENT, DataType.dt_NONE, OpType.op_NONE)),
            (Rep1(Str("\t")),                 IGNORE),
            (Str(" "),                  (TokenCode.tc_SPACE, DataType.dt_NONE, OpType.op_NONE)),
            (Any("\n\r"),               (TokenCode.tc_NEWLINE, DataType.dt_NONE, OpType.op_NONE)),
            (AnyChar,                   (TokenCode.tc_ERROR, DataType.dt_NONE, OpType.op_NONE))
        ])
        return lexicon
class Token:
    def __init__(self, token_code, data_type, op_type, line, col, lexeme):
        self.token_code = token_code
        self.data_type = data_type
        self.op_type = op_type
        self.line = line
        self.col = col
        self.lexeme = lexeme
        self.symbol_table_entry = None
class SymbolTable:
    # an array of symbol_table_entries.
    def __init__(self):
        self.symbolTableEntries = []
        self.insert('0')
        self.insert('1')
    def insert(self, lexeme):
        # insert lexeme and return pointer to entry
        symbol_table_entry = self.lookup(lexeme)

        # lexeme is not already in table
        if not  symbol_table_entry:
            symbol_table_entry = SymbolTableEntry()
            symbol_table_entry.lexeme = lexeme
            self.symbolTableEntries.append(symbol_table_entry)
            return symbol_table_entry

        # lexeme is already in table
        return symbol_table_entry
    def lookup(self, lexeme):
        # find and return pointer to entry of lexeme in symbol_entry_table.
        for symbol_table_entry in self.symbolTableEntries:
            if symbol_table_entry.lexeme == lexeme:

                # lexeme is in table.
                return symbol_table_entry

        # lexeme is not in table
        return None
    def __str__(self):
        # formats contents of symbol_table to be more human readable.
        header = 'Entry'.rjust(6) + 'Lexeme'.rjust(15) + '\n'
        body = ""
        index = 1
        for entry in self.symbolTableEntries:
            body += str(index).rjust(6) + str(entry.lexeme).rjust(15) + '\n'
            index +=1

        return header + body
class SymbolTableEntry:
    def __init__(self):
        self.lexeme = None
class SourceLine:
    def __init__(self):
        self.buffer = ""
        self.lineNr = 1
        self.errors = []
        self.number_of_errors = 0
    def addToken(self, token ):
        if token.token_code == TokenCode.tc_NEWLINE or token.token_code == TokenCode.tc_EOF:
            print str(self.lineNr).rjust(3) + ": " + self.buffer
            for error in self.errors:
                print error

            self.buffer = ""
            self.errors = []
            self.lineNr += 1
        else:
            self.buffer += token.lexeme
    def printing(self):
        print (str(self.lineNr).rjust(3) + ': ' + self.buffer).strip('\n')
        for error in self.errors:
            print error

        print
        if self.number_of_errors <= 0:
            print "No errors"
        else:
            print 'Number of errors: %i' %self.number_of_errors
    def addError(self, error, spaces):
        self.number_of_errors += 1
        for i in range(spaces+5):
            error = " " + error
        self.errors.append(error)

class PascalScanner:
    # scans file and returns stream of Tokens
    def __init__(self, filename):
        lexer = Lexicons().getLexer()
        f = open(filename, "r")
        self.scanner = Scanner(lexer, f, filename)
        self.symbol_table = SymbolTable()
        self.source_line = SourceLine()
    def next_token(self):
        # returns a pointer to next token found

        # read returns tuple on the form
        # ( ( token_code, data_type, op_type ) lexeme )
        temp = self.scanner.read()

        # verify read return a lexeme
        if temp[0]:
            # move data from temp variable into Token, insert into symbol_table
            token = Token(temp[0][0], temp[0][1], temp[0][2], self.scanner.start_line, self.scanner.start_col, temp[1])
            if token.token_code == TokenCode.tc_ID or token.token_code == TokenCode.tc_NUMBER:
                token.symbol_table_entry = self.symbol_table.insert(token.lexeme)

            self.source_line.addToken(token)

            if token.token_code == TokenCode.tc_NEWLINE or\
               token.token_code == TokenCode.tc_SPACE or token.token_code == TokenCode.tc_COMMENT:
                return self.next_token()
            elif token.token_code == TokenCode.tc_ERROR:
                self.source_line.addError("^ Illegal character", token.col)
                return self.next_token()
            else:
                return token

        # end of file
        #else:
            #token = Token(TokenCode.tc_EOF, DataType.dt_NONE, OpType.op_NONE, 0, 0, "EOF")
            #self.source_line.addToken(token)
            #return token
    def add_error(self, error, spaces):
        self.source_line.addError(error, spaces)

class PascalScannerTester:
    def __init__(self):
        scanner = PascalScanner("test_files/lex_test")
        buffer = ""
        line_length = 10
        while True:
            token = scanner.next_token()
            while token.token_code == TokenCode.tc_NEWLINE or\
                  token.token_code == TokenCode.tc_COMMENT:
                token = scanner.next_token()
            if token.data_type == DataType.dt_KEYWORD or token.data_type == DataType.dt_NONE:
                buffer += token.token_code +" "
            else:
                buffer += token.token_code + "(%s) " % token.lexeme

            line_length -= 1
            if line_length <= 0:
                buffer += "\n"
                line_length = 10

            if token.token_code == TokenCode.tc_EOF:
                break

        print buffer
        print
        print scanner.symbol_table.__str__()
#lex_tester = PascalScannerTester()
