__author__ = 'Palli'

__author__ = 'palleymundsson'

from plex import *
from Enums import *

class Lexicons:
    """ lexicons in subset of pascal source code.

    list of lexicons that make up subset of pascal language.
    when we find lexicon we return tuple containing a tuple and lexeme.
    ( ( token_code, data_type, op_type ) lexeme )

    use getLexer to return list of lexicons for subset of pascal language.

    """

    def get_lexer(self):
        """ returns list of lexicons in subset of pascal language."""

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
            (Str("\t"),                 (TokenCode.tc_TAB, DataType.dt_NONE, OpType.op_NONE)),
            (Str(" "),                  (TokenCode.tc_SPACE, DataType.dt_NONE, OpType.op_NONE)),
            (Any("\n\r"),               (TokenCode.tc_NEWLINE, DataType.dt_NONE, OpType.op_NONE)),
            (AnyChar,                   (TokenCode.tc_ERROR, DataType.dt_NONE, OpType.op_NONE))
        ])
        return lexicon

class Token:
    """ class for storing information about token for lexeme

    stores token code, data type, op type, line lexeme is in, distance from start of line,
    lexeme and pointer to where token is in symbol table.
    """
    def __init__(self, token_code="", data_type="", op_type="", line=-1, col=-1, lexeme=""):
        self.token_code = token_code
        self.data_type = data_type
        self.op_type = op_type
        self.line = line
        self.col = col
        self.lexeme = lexeme
        self.symbol_table_entry = None

class SymbolTable:
    """ class for storing symbol table entries.

    each entry is of the class SymbolTable.

    use insert to insert lexeme into the table.
    use lookup to find lexeme in the table.
    """
    def __init__(self):
        self.symbolTableEntries = []
        self.insert('0')
        self.insert('1')

    def __str__(self):
        # formats contents of symbol_table to be more human readable.
        header = 'Entry'.rjust(6) + 'Lexeme'.rjust(15) + '\n'
        body = ""
        index = 1
        for entry in self.symbolTableEntries:
            body += str(index).rjust(6) + str(entry.lexeme).rjust(15) + '\n'
            index +=1

        return header + body

    def insert(self, lexeme):
        """insert lexeme.

        insert lexeme into symbol table and return reference to entry.
        if lexeme is already in table we do nothing and return None.
        """
        symbol_table_entry = self.lookup(lexeme)

        # lexeme is not already in table
        if not  symbol_table_entry:
            symbol_table_entry = SymbolTableEntry()
            symbol_table_entry.lexeme = lexeme
            self.symbolTableEntries.append(symbol_table_entry)
        return symbol_table_entry

    def lookup(self, lexeme):
        """ find lexeme.

         tries to find lexeme in table and returns reference to entry if
         we find it, otherwise we return None.
        """

        # find and return pointer to entry of lexeme in symbol_entry_table.
        for symbol_table_entry in self.symbolTableEntries:
            if symbol_table_entry.lexeme == lexeme:

                # lexeme is in table.
                return symbol_table_entry

        # lexeme is not in table
        return None

class SymbolTableEntry:
    """ entry in symbol table

    includes pointer to lexeme
    """
    def __init__(self):
        self.lexeme = None
    def __str__(self):
        return self.lexeme

class SourceLine:
    """ stores source code with error checking.

    stores source code in buffer and adds any error to source code
    with marking to where error is.

    use addToken to add source code to buffer.

    use addError to add error to source code.
    """
    def __init__(self):
        self.line = ""
        self.lines = ""
        self.lineNr = 1
        self.errors = []
        self.number_of_errors = 0
        self.tabs = 0

    def __str__(self):
        return self.lines

    def add_token(self, token ):
        """ adds token to output of SourceLine.

            takes lexeme of input token and adds to buffer.
            if lexeme is new line character we also add every error of current line
            to buffer and then clear errors.
        """
        if token.token_code == TokenCode.tc_NEWLINE:
            self.lines += str(self.lineNr).rjust(3) + ": " + self.line + "\n"
            for error in self.errors:
                self.lines += error + "\n"

            self.line = ""
            self.errors = []
            self.lineNr += 1
            self.tabs = 0
        else:
            self.line += token.lexeme

        if token.token_code == TokenCode.tc_TAB:
            self.tabs += 1

    def add_error(self, error, spaces):
        """ adds error message to list of errors in class.
            error messages has the form <offset>< spaces > <error>
            where offset is the line number and spaces in every line and spaces
            are as many number of spaces as the error is originated from start of line
            and error is the error message itself.
            we also increment the error count.
        """
        self.number_of_errors += 1
        for i in range(spaces-self.tabs):
            error = " " + error
        for j in range(self.tabs):
            error = "\t" + error
        for i in range(5):
            error = " " + error
        self.tabs = 0
        self.errors.append(error)

    def number_of_errors(self):
        """ return number of errors in code."""
        return self.number_of_errors

class PascalScanner:
    """ class for scanning pascal source code.

    scans source code and returns stream of tokens.
    keeps track of source code and error in it.

    use next to get next token in source code.
    use add_error to add error to source code.
    """
    def __init__(self, filename):
        """ initializer class

        gets list of lexicons in pascal language.
        opens file containing source code.
        initializer plex scanner to read from file.
        initializer symbol table.
        initializer source line.
        """
        lexer = Lexicons().get_lexer()
        f = open(filename, "r")
        self.scanner = Scanner(lexer, f, filename)
        self.symbol_table = SymbolTable()
        self.source_line = SourceLine()

    def __str__(self):
        """ returns source code with error marking.

         returns string containing source code with error
         marking, plus number of error in code.

        """
        number_of_errors = self.source_line.number_of_errors
        if number_of_errors <= 0:
            error_number_str = "\n\nNo errors"
        else:
            error_number_str = "\n\nNumber of errors: %s" %number_of_errors

        return self.source_line.__str__() + error_number_str + "\n\n" + self.symbol_table.__str__()

    def next_token(self):
        """ returns next token in source code.

        asks plex scanner for next lexicon in input. plex scanner returns tuple containing
        tuple and lexeme on the format. ( ( token_coce, data_type, op_type ) lexeme ).
        we map those values into Token class. and if token is space, tab or newline we call recursively
        our self and return the Token that call returns. If plex returns None we know we have reached
        end of file and do noting.

        """

        temp = self.scanner.read()

        # verify plex scanner returns something.
        # returns None at end of file <EOF>.
        if temp[0]:
            token_code = temp[0][0]

            # map data from temp variable into Token.
            token = Token(temp[0][0], temp[0][1], temp[0][2], self.scanner.start_line, self.scanner.start_col, temp[1])

            # insert into symbol table if lexeme is number or id.
            if token_code == TokenCode.tc_ID or token_code == TokenCode.tc_NUMBER:
                token.symbol_table_entry = self.symbol_table.insert(token.lexeme)

            # add token to source line for logging.
            self.source_line.add_token(token)

            # call recursively if token is newline, tab, comment or space
            if token_code == TokenCode.tc_NEWLINE or token_code == TokenCode.tc_TAB or\
               token_code == TokenCode.tc_SPACE or token_code == TokenCode.tc_COMMENT:
                return self.next_token()

            # call recursively if token is error and therefore illegal character
            # adds error to source line
            elif token.token_code == TokenCode.tc_ERROR:
                self.source_line.add_error("^ Illegal character", token.col)
                return self.next_token()

            # call recursively if token is error2 and therefore identifier to long
            # adds error to source line
            elif token.token_code == TokenCode.tc_ERROR2:
                self.source_line.add_error("^ Identifier too long", token.col)
                return self.next_token()

            else:
                return token

        # at end of file we add newline to add last line into source code lines
        token = Token()
        token.token_code = TokenCode.tc_NEWLINE
        self.source_line.add_token(token)

    def add_error(self, error, spaces):
        """ adds error to source line. """
        self.source_line.add_error(error, spaces)



class PascalScannerTester:
    """ tester for pascal scanner. """
    def __init__(self):
        scanner = PascalScanner("test_files/lex_test")
        token = scanner.next_token()
        while token:
            token = scanner.next_token()

        print scanner

#lex_tester = PascalScannerTester()
