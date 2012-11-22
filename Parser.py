# -*- coding: utf-8 -*-
__author__ = 'palleymundsson'

from plex import *
from Lexical import *
from CodeGenerator import *

class SourceLine:
    def __init__(self):
        self.line = ""
        self.lineNr = 1
        self.errors = []
        self.number_of_errors = 0
    def addToken(self, token ):
        word = token.lexeme
        if token.line > self.lineNr:
            print (str(self.lineNr).rjust(3) + ': ' + self.line).strip('\n')
            for error in self.errors:
                print error
            self.lineNr = token.line
            for i in range(token.col):
                word = " " + word
            self.line = word
            self.errors = []
        else:
            #print '%s : %s' %(len(self.line), token.col)
            for i in range(token.col- len(self.line)):
                word = " " + word

            self.line += word
    def printing(self):
        print (str(self.lineNr).rjust(3) + ': ' + self.line).strip('\n')
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

class PascalParser:
    def __init__(self, filename):
        self.scanner = PascalScanner(filename)
        self.sourceLine = SourceLine()
        self.token = Token
        self.next_token()
        self.error = None
        self.code = Code()
    def get_token_code(self):
        return self.token.token_code
    def get_op_type(self):
        return self.token.op_type
    def next_token(self):
        self.token = self.scanner.next_token()

        if self.token.token_code != TokenCode.tc_EOF:
            self.sourceLine.addToken(self.token)
            if self.token.token_code == TokenCode.tc_NEWLINE:
                self.next_token()
            elif self.token.token_code == TokenCode.tc_COMMENT:
                self.next_token()
            elif self.token.token_code == TokenCode.tc_ERROR:
                self.sourceLine.addError('^ Illegal character', self.token.col)
                self.next_token()
        else:
            self.sourceLine.printing()
            print
            print self.scanner.symbol_table.__str__()
    def match(self, token_code):
        """ check if current token matches expected token.

        if token does not match we add error to member variable error
        """

        current_token_code = self.get_token_code()

        # we have a match
        if current_token_code == token_code:
            self.next_token()

        # we do not have a match
        else:
            self.error = 'Expected "%s"' % token_code

    def recover(self, non_terminal=None ):
        """ recovers from error

        recovers by eating up all tokens up to synchronizing tokens or follow set tokens of the
        where error originated.
        """
        sync_tokens = TokenCode.tc_VAR, TokenCode.tc_FUNCTION, TokenCode.tc_PROCEDURE, TokenCode.tc_BEGIN, TokenCode.tc_DOT
        stop_tokens = None

        # set follow token of non_terminal
        if non_terminal == NoneTerminal.nt_SIGN_FOLLOW:
            stop_tokens = (TokenCode.tc_ID, TokenCode.tc_NUMBER, TokenCode.tc_LPAREN, TokenCode.tc_NOT)

        elif non_terminal == NoneTerminal.nt_FACTOR_MARKED_FOLLOW or non_terminal == NoneTerminal.nt_FACTOR_FOLLOW:
            stop_tokens = (TokenCode.tc_ID, TokenCode.tc_NUMBER, TokenCode.tc_LPAREN, TokenCode.tc_NOT,
                             TokenCode.tc_ADDOP, TokenCode.tc_RPAREN, TokenCode.tc_RBRACK, TokenCode.tc_DO,
                             TokenCode.tc_THEN, TokenCode.tc_COMMA, TokenCode.tc_ELSE, TokenCode.tc_SEMICOL,
                             TokenCode.tc_END)

        elif non_terminal == NoneTerminal.nt_TERM_MARKED_FOLLOW or non_terminal == NoneTerminal.nt_TERM_FOLLOW:
            stop_tokens = (TokenCode.tc_ADDOP, TokenCode.tc_RPAREN, TokenCode.tc_RBRACK, TokenCode.tc_DO,
                             TokenCode.tc_THEN, TokenCode.tc_COMMA, TokenCode.tc_ELSE, TokenCode.tc_SEMICOL,
                             TokenCode.tc_END)

        elif non_terminal == NoneTerminal.nt_SIMPLE_EXPRESSION_MARKED_FOLLOW or\
             non_terminal == NoneTerminal.nt_SIMPLE_EXPRESSION_FOLLOW or\
             non_terminal == NoneTerminal.nt_EXPRESSION_MARKED_FOLLOW or\
             non_terminal == NoneTerminal.nt_EXPRESSION_FOLLOW:
            stop_tokens = (TokenCode.tc_RPAREN, TokenCode.tc_RBRACK, TokenCode.tc_DO,
                             TokenCode.tc_THEN, TokenCode.tc_COMMA, TokenCode.tc_ELSE, TokenCode.tc_SEMICOL,
                             TokenCode.tc_END)

        elif non_terminal == NoneTerminal.nt_EXPRESSION_LIST_MARKED_FOLLOW or\
             non_terminal == NoneTerminal.nt_EXPRESSION_LIST_FOLLOW or\
             non_terminal == NoneTerminal.nt_PARAMETER_LIST_MARKED_FOLLOW or\
             non_terminal == NoneTerminal.nt_PARAMETER_LIST_FOLLOW:
            stop_tokens = (TokenCode.tc_RPAREN,)

        elif non_terminal == NoneTerminal.nt_STATEMENT_MARKED_FOLLOW or\
             non_terminal == NoneTerminal.nt_STATEMENT_FOLLOW:
            stop_tokens = (TokenCode.tc_ELSE, TokenCode.tc_SEMICOL, TokenCode.tc_END)

        elif non_terminal == NoneTerminal.nt_STATEMENT_LIST_MARKED_FOLLOW or\
             non_terminal == NoneTerminal.nt_STATEMENT_LIST_FOLLOW or\
             non_terminal == NoneTerminal.nt_OPTIONAL_STATEMENT_FOLLOW:
            stop_tokens = (TokenCode.tc_END,)

        elif non_terminal == NoneTerminal.nt_COMPOUND_STATEMENT_FOLLOW:
            stop_tokens = (TokenCode.tc_ELSE, TokenCode.tc_SEMICOL, TokenCode.tc_END, TokenCode.tc_DOT)

        elif non_terminal == NoneTerminal.nt_ARGUMENTS_FOLLOW:
            stop_tokens = (TokenCode.tc_COLON, TokenCode.tc_SEMICOL)

        elif non_terminal == NoneTerminal.nt_SUBPROGRAM_HEAD_FOLLOW:
            stop_tokens = (TokenCode.tc_VAR, TokenCode.tc_FUNCTION, TokenCode.tc_PROCEDURE, TokenCode.tc_BEGIN)

        elif non_terminal == NoneTerminal.nt_SUBPROGRAM_DECLARATION_FOLLOW or\
             non_terminal == NoneTerminal.nt_STANDARD_TYPE_FOLLOW or\
             non_terminal == NoneTerminal.nt_TYPE_FOLLOW:
            stop_tokens = (TokenCode.tc_SEMICOL,)

        elif non_terminal == NoneTerminal.nt_SUBPROGRAM_DECLARATIONS_FOLLOW:
            stop_tokens = (TokenCode.tc_BEGIN,)

        elif non_terminal == NoneTerminal.nt_DECLARATIONS_FOLLOW:
            stop_tokens = (TokenCode.tc_FUNCTION, TokenCode.tc_PROCEDURE, TokenCode.tc_BEGIN)

        elif non_terminal == NoneTerminal.nt_IDENTIFIER_LIST_MARKED_FOLLOW or\
             non_terminal == NoneTerminal.nt_IDENTIFIER_LIST_FOLLOW:
            stop_tokens = (TokenCode.tc_RPAREN, TokenCode.tc_COLON)

        # set of first tokens
        elif non_terminal == NoneTerminal.nt_SIGN_FIRST:
            stop_tokens = (TokenCode.tc_ADDOP,)

        elif non_terminal == NoneTerminal.nt_FACTOR_MARKED_FIRST:
            stop_tokens = (TokenCode.tc_LPAREN, TokenCode.tc_LBRACK)

        elif non_terminal == NoneTerminal.nt_FACTOR_FIRST:
            stop_tokens = (TokenCode.tc_ID, TokenCode.tc_NUMBER, TokenCode.tc_LPAREN, TokenCode.tc_NOT)




        self.sourceLine.addError(self.error)
        self.error = None

        sync_and_stop_tokens = sync_tokens + stop_tokens
        run = True
        for token in sync_and_stop_tokens:
            if self.token.token_code == token:
                run = False
                break
        while run:
            self.next_token()
            for token in sync_and_stop_tokens:
                if self.token.token_code == token:
                    run = False
                    break

    def new_temp(self):
        symbol_table_entry = self.code.new_temp()
        self.scanner.symbol_table.insert(symbol_table_entry)
        self.code.generate(CodeOp.cd_VAR, None, None, symbol_table_entry)
        return symbol_table_entry
    def new_label(self):
        symbol_table_entry = self.code.new_label()
        self.scanner.symbol_table.insert(symbol_table_entry)
        self.code.generate(CodeOp.cd_LABEL, None, None, symbol_table_entry)
        return symbol_table_entry

    def program(self):
        """ implements the CFG

              program     ::=     program id ( identifier_list ) ;
                                  declarations
                                  subprogram_declarations
                                  compound_statement
                                  .

        return true if input is according to grammar, false otherwise
        """
        hasError = False

        #program
        if not self.match(TokenCode.tc_PROGRAM):
            self.sourceLine.addError('^ Expected "program"', self.token.col)
            hasError = True

        # program id
        if not self.match(TokenCode.tc_ID) and not hasError:
            self.sourceLine.addError('^ Expected "id"', self.token.col)
            hasError = True

        # program id (
        if not self.match(TokenCode.tc_LPAREN) and not hasError:
            self.sourceLine.addError('^ Expected "("', self.token.col)
            hasError = True

        if hasError:
            self.eat_up_to_stop_or_sync_tokens((TokenCode.tc_ID, TokenCode.tc_ID))
            hasError = False

        # program id ( identifier_list
        identifier_list = self.identifier_list()
        if not identifier_list[0]:
            self.sourceLine.addError(identifier_list[1], self.token.col)
            self.eat_up_to_stop_or_sync_tokens((TokenCode.tc_RPAREN, TokenCode.tc_COLON))

        # program id ( identifier_list )
        if not self.match(TokenCode.tc_RPAREN):
            self.sourceLine.addError('^ Expected ")"', self.token.col)
            hasError = True

        # program id ( identifier_list ) ;
        if not self.match(TokenCode.tc_SEMICOL) and not hasError:
            self.sourceLine.addError('^ Expected ";"', self.token.col)

        if hasError:
            self.eat_up_to_stop_or_sync_tokens((TokenCode.tc_VAR, TokenCode.tc_FUNCTION,
                                                TokenCode.tc_PROCEDURE, TokenCode.tc_BEGIN))
            hasError = False

        # program id ( identifier_list ) ;
        # declarations
        declarations = self.declarations()
        if not declarations[0]:
            self.sourceLine.addError(declarations[1], self.token.col)
            self.eat_up_to_stop_or_sync_tokens(( TokenCode.tc_FUNCTION, TokenCode.tc_PROCEDURE, TokenCode.tc_BEGIN))

        # program id ( identifier_list ) ;
        # declarations
        # subprogram_declarations
        subprogram_declarations = self.subprogram_declarations()
        if not subprogram_declarations[0]:
            self.sourceLine.addError(subprogram_declarations[1], self.token.col)
            self.eat_up_to_stop_or_sync_tokens((TokenCode.tc_BEGIN, TokenCode.tc_BEGIN))

        # program id ( identifier_list ) ;
        # declarations
        # subprogram_declarations
        # compound_statement
        compound_statement = self.compound_statement()
        if not compound_statement[0]:
            self.sourceLine.addError(compound_statement[1], self.token.col)
            self.eat_up_to_stop_or_sync_tokens((TokenCode.tc_ELSE, TokenCode.tc_SEMICOL, TokenCode.tc_END, TokenCode.tc_DOT))

        # program id ( identifier_list ) ;
        # declarations
        # subprogram_declarations
        # compound_statement
        # .
        if not self.match(TokenCode.tc_DOT):
            self.sourceLine.addError('^ Expected "."', self.token.col)

        return True, 'good'
    def identifier_list(self):
        """implements the CFG.

           identifier_list     ::=     id identifier_list_marked

        return true if input is according to grammar, false otherwise
        """
        # id
        if self.match(TokenCode.tc_ID):
            # id identifier_list_marked
            identifier_list_marked = self.identifier_list_marked()
            if not identifier_list_marked[0]:
                self.sourceLine.addError(identifier_list_marked[1], self.token.col)
                self.eat_up_to_stop_or_sync_tokens((TokenCode.tc_COLON, TokenCode.tc_RPAREN))
            return True, 'good'

        # error
        else:
            return False, '^ Expected "id"'
    def identifier_list_marked(self):
        """ implements the CFG

            identifier_list_marked  ::=     , id identifier_list_marked
                                   |       ϵ

        return true if input is according to grammar, false otherwise
        """
        # ,
        if self.match(TokenCode.tc_COMMA):
            # , id
            if not self.match(TokenCode.tc_ID):
                return False, '^ Expected "id"'

            #, id identifier_list_marked
            identifier_list_marked = self.identifier_list_marked()
            if not identifier_list_marked[0]:
                self.sourceLine.addError(identifier_list_marked[1], self.token.col)
                self.eat_up_to_stop_or_sync_tokens((TokenCode.tc_COLON, TokenCode.tc_RPAREN))
            return True, 'good'

        # ϵ
        else:
            return True, 'good'
    def declarations(self):
        """ implements the CFG

            declarations    ::=     var identifier_list : type ; declarations
                            |       ϵ

        return true if input is according to grammar, false otherwise
        """
        # var
        if self.match(TokenCode.tc_VAR):
            # var identifier_list
            identifier_list = self.identifier_list()
            if not identifier_list[0]:
                self.sourceLine.addError(identifier_list[1], self.token.col)
                self.eat_up_to_stop_or_sync_tokens((TokenCode.tc_COLON,TokenCode.tc_RPAREN))

            # var identifier_list :
            if not self.match(TokenCode.tc_COLON):
                self.sourceLine.addError('^ Expected ":"', self.token.col)
                self.eat_up_to_stop_or_sync_tokens((TokenCode.tc_INTEGER, TokenCode.tc_REAL,
                                                    TokenCode.tc_ARRAY))



            # var identifier_list : type
            type = self.type()
            if not type[0]:
                self.sourceLine.addError(type[1], self.token.col)
                self.eat_up_to_stop_or_sync_tokens((TokenCode.tc_SEMICOL, TokenCode.tc_SEMICOL))

            # var identifier_list : type ;
            if not self.match(TokenCode.tc_SEMICOL):
                self.sourceLine.addError('^ Expected ";"', self.token.col)
                self.eat_up_to_stop_or_sync_tokens((TokenCode.tc_VAR, TokenCode.tc_PROCEDURE,
                                                    TokenCode.tc_FUNCTION, TokenCode.tc_BEGIN))

            # var identifier_list : type ; declarations
            declarations = self.declarations()
            if not declarations[0]:
                self.sourceLine.addError(declarations[1], self.token.col)
                self.eat_up_to_stop_or_sync_tokens((TokenCode.tc_FUNCTION, TokenCode.tc_PROCEDURE, TokenCode.tc_BEGIN))
            return True, 'good'

        # ϵ
        else:
            return True, 'good'
    def type(self):
        """ implements the CFG

           type   ::=     standard_type
                  |        array [ num .. num ] of standard_type

        return true if input is according to grammar, false otherwise
        """
        # standard_type
        if self.standard_type()[0]:
            return True, "good"

        # array
        elif self.match(TokenCode.tc_ARRAY):

            # array [
            if not self.match(TokenCode.tc_LBRACK):
                return False, '^ Expected "["'

            # array [ num
            if not self.match(TokenCode.tc_NUMBER):
                return False, '^ Expected "number"'

            # array [ num ..
            if not self.match(TokenCode.tc_DOTDOT):
                return False, '^ Expected ".."'

            # array [ num .. num
            if not self.match(TokenCode.tc_NUMBER):
                return False, '^ Expected "number"'

            # array [ num .. num ]
            if not self.match(TokenCode.tc_RBRACK):
                return False, '^ Expected "]"'

            # array [ num .. num ] of
            if not self.match(TokenCode.tc_OF):
                return False, '^ Expected "of"'

            # array [ num .. num ] of standard_type
            standard_type = self.standard_type()
            if not standard_type[0]:
                self.sourceLine.addError(standard_type[1], self.token.col)
                self.eat_up_to_stop_or_sync_tokens((TokenCode.tc_SEMICOL, TokenCode.tc_SEMICOL))
            return True, 'good'

        # error
        else:
            return False, '^ Expected "type"'
    def standard_type(self):
        """ implements the CFG

           standard_type   ::=     integer
                           |       real

        return true if input is according to grammar, false otherwise
        """
        # integer
        if self.match(TokenCode.tc_INTEGER):
            return True, "good"

        # real
        elif self.match(TokenCode.tc_REAL):
            return True, "good"

        # error
        else:
            return False, '^ Expected "standard_type"'
    def subprogram_declarations(self):
        """ implements the CFG

           subprogram_declarations     ::=     subprogram_declaration ; subprogram_declarations
                                       |       ϵ

        return true if input is according to grammar, false otherwise
        """
        # subprogram_declaration
        subprogram_declaration = self.subprogram_declaration()
        if subprogram_declaration[0]:
            # subprogram_declaration ;
            if not self.match(TokenCode.tc_SEMICOL):
                return False, '^ Expected ";"'

            # subprogram_declaration ; subprogram_declarations
            subprogram_declarations = self.subprogram_declarations()
            if not subprogram_declarations[0]:
                self.sourceLine.addError(subprogram_declarations[1], self.token.col)
                self.eat_up_to_stop_or_sync_tokens((TokenCode.tc_BEGIN, TokenCode.tc_BEGIN))
            return True, 'good'

        # ϵ
        else:
            return True, 'good'
    def subprogram_declaration(self):
        """ implements the CFG

           subprogram_declaration      ::=     subprogram_head declarations compound_statement

        return true if input is according to grammar, false otherwise
        """
        # subprogram_head
        subprogram_head = self.subprogram_head()
        if subprogram_head[0]:
            # subprogram_head declarations
            declarations = self.declarations()
            if not declarations[0]:
                self.sourceLine.addError(declarations[1], self.token.col)
                self.eat_up_to_stop_or_sync_tokens((TokenCode.tc_FUNCTION, TokenCode.tc_PROCEDURE, TokenCode.tc_BEGIN))

            # subprogram_head declarations compound_statement
            compound_statement = self.compound_statement()
            if not compound_statement[0]:
                self.sourceLine.addError(compound_statement[1], self.token.col)
                self.eat_up_to_stop_or_sync_tokens((TokenCode.tc_ELSE, TokenCode.tc_SEMICOL, TokenCode.tc_END))
            return True, 'good'

        # error
        else:
            return subprogram_head
    def subprogram_head(self):
        """ implements the CFG

           subprogram_head     ::=     function id arguments : standard_type
                               |       procedure id arguments ;

        return true if input is according to grammar, false otherwise
        """
        # function
        if self.match(TokenCode.tc_FUNCTION):
            # function id
            if not self.match(TokenCode.tc_ID):
                return False, '^ Expected "id"'

            # function id arguments
            arguments = self.arguments()
            if not arguments[0]:
                self.sourceLine.addError(arguments[1], self.token.col)
                self.eat_up_to_stop_or_sync_tokens((TokenCode.tc_COLON, TokenCode.tc_SEMICOL))

            # function id arguments :
            if not self.match(TokenCode.tc_COLON):
                return False, '^ Expected ":"'

            # function id arguments : standard_type
            standard_type = self.standard_type()
            if not standard_type[0]:
                self.sourceLine.addError(standard_type[1], self.token.col)
                self.eat_up_to_stop_or_sync_tokens((TokenCode.tc_SEMICOL, TokenCode.tc_SEMICOL))

            # function id arguments : standard_type ;
            if not self.match(TokenCode.tc_SEMICOL):
                return False, '^ Expected ";"'

            return True, 'good'

        # procedure
        if self.match(TokenCode.tc_PROCEDURE):
            # procedure id
            if not self.match(TokenCode.tc_ID):
                return False, '^ Expected "id"'

            # procedure id arguments
            arguments = self.arguments()
            if not arguments[0]:
                self.sourceLine.addError(arguments[1], self.token.col)
                self.eat_up_to_stop_or_sync_tokens((TokenCode.tc_COLON, TokenCode.tc_SEMICOL))

            # procedure id arguments ;
            if not self.match(TokenCode.tc_SEMICOL):
                return False, '^ Expected ";"'

            return True, 'good'

        # error
        return False, 'Expected "subprogram_head'
    def arguments(self):
        """ implements the CFG

           arguments   ::=     ( parameter_list )
                        |      ϵ

        return true if input is according to grammar, false otherwise
        """
        # (
        if self.match(TokenCode.tc_LPAREN):
            # ( parameter_list
            parameter_list = self.parameter_list()
            if not parameter_list[0]:
                self.sourceLine.addError(parameter_list[1], self.token.col)
                self.eat_up_to_stop_or_sync_tokens((TokenCode.tc_RPAREN, TokenCode.tc_RPAREN))

            # ( parameter_list )
            if not self.match(TokenCode.tc_RPAREN):
                return False, '^ Expected ")"'

            return True, 'good'

        # ϵ
        else:
            return True, 'good'
    def parameter_list(self):
        """ inplements the CFG

           parameter_list      ::=     identifier_list : type parameter_list_marked

        return true if input is according to grammar, false otherwise
        """
        # identifier_list
        identifier_list = self.identifier_list()
        if identifier_list[0]:
            # identifier_list :
            if not self.match(TokenCode.tc_COLON):
                return False, '^ Expected ":"'

            # identifier_list : type
            type = self.type()
            if not type[0]:
                self.sourceLine.addError(type[1], self.token.col)
                self.eat_up_to_stop_or_sync_tokens((TokenCode.tc_SEMICOL, TokenCode.tc_SEMICOL))

            # identifier_list : type parameter_list_marked
            parameter_list_marked = self.parameter_list_marked()
            if not parameter_list_marked[0]:
                self.sourceLine.addError(parameter_list_marked[1], self.token.col)
                self.eat_up_to_stop_or_sync_tokens((TokenCode.tc_RPAREN, TokenCode.tc_RPAREN))
            return True, 'good'

        # error
        else:
            return identifier_list
    def parameter_list_marked(self):
        """ implements the CFG

           parameter_list_marked   ::=     ; identifier_list : type parameter_list_marked
                                   |       ϵ

        return true if input is according to grammar, false otherwise
        """
        # ;
        if self.match(TokenCode.tc_SEMICOL):
            # ; identifier_list
            identifier_list = self.identifier_list()
            if not identifier_list[0]:
                self.sourceLine.addError(identifier_list[1], self.token.col)
                self.eat_up_to_stop_or_sync_tokens((TokenCode.tc_RPAREN, TokenCode.tc_COLON))

            # ; identifier_list :
            if not self.match(TokenCode.tc_COLON):
                return False, '^ Expected ":"'

            # ; identifier_list : type
            type = self.type()
            if not type[0]:
                self.sourceLine.addError(type[1], self.token.col)
                self.eat_up_to_stop_or_sync_tokens((TokenCode.tc_SEMICOL, TokenCode.tc_SEMICOL))

            # ; identifier_list : type parameter_list_marked
            parameter_list_marked = self.parameter_list_marked()
            if not parameter_list_marked[0]:
                self.sourceLine.addError(parameter_list_marked[1], self.token.col)
                self.eat_up_to_stop_or_sync_tokens((TokenCode.tc_RPAREN, TokenCode.tc_RPAREN))
            return True, 'good'

        # ϵ
        return True, 'good'
    def compound_statement(self):
        """ implements the CFG

           compound_statement  ::=     begin optional_statement end


        return true if input is according to grammar, false otherwise
        """
        # begin
        if self.match(TokenCode.tc_BEGIN):
            # begin optional_statement
            self.optional_statement()

            # begin optional_statement end
            if not self.match(TokenCode.tc_END):
                return False, '^ Expected "end"'

            return True, 'good'

        # error
        return False, '^ Expected "begin"'
    def optional_statement(self):
        """ inplements the CFG

           optional_statement   ::=     statement_list
                               |       ϵ

        return true if input is according to grammar, false otherwise
        """
        self.statement_list()
        return True, 'good'
    def statement_list(self):
        """ implements the CFG

           statment_list   ::=     statement statement_list_marked


        return true if input is according to grammar, false otherwise
        """
        # statement
        statement = self.statement()
        if statement[0]:
            # statement statement_list_marked
            statement_list_marked = self.statement_list_marked()
            if not statement_list_marked[0]:
                self.sourceLine.addError(statement_list_marked[1], self.token.col)
                self.eat_up_to_stop_or_sync_tokens((TokenCode.tc_END, TokenCode.tc_END))

            return True, 'good'
        # error
        else:
            return statement
    def statement_list_marked(self):
        """ implements the CFG

           statement_list_marked   ::=     ; statement statement_list_marked
                                   |       ϵ

        return true if input is according to grammar, false otherwise
        """
        # ;
        if self.match(TokenCode.tc_SEMICOL):
            # ; statement
            statement = self.statement()
            if not statement[0]:
                self.sourceLine.addError(statement[1], self.token.line)
                self.eat_up_to_stop_or_sync_tokens((TokenCode.tc_ELSE, TokenCode.tc_SEMICOL, TokenCode.tc_END))

            # ; statement statement_list_marked
            statement_list_marked = self.statement_list_marked()
            if not statement_list_marked[0]:
                self.sourceLine.addError(statement_list_marked[1], self.token.col)
                self.eat_up_to_stop_or_sync_tokens((TokenCode.tc_END, TokenCode.tc_END))

            return True, 'good'
        # ϵ
        else:
            return True, 'good'
    def statement(self):
        """ inplements the CFG

           statement   ::=     id statment_marked
                       |       compound_statement
                       |       if expression then statement else statement
                       |       while expression do statement

        return true if input is according to grammar, false otherwise
        """
        # id
        if self.match(TokenCode.tc_ID):
            # id statement_marked
            statement_marked = self.statement_marked()
            if not statement_marked[0]:
                self.sourceLine.addError(statement_marked[1], self.token.col)
                self.eat_up_to_stop_or_sync_tokens((TokenCode.tc_ELSE, TokenCode.tc_SEMICOL, TokenCode.tc_END))
            return True, 'good'

        # compound_statement
        elif self.compound_statement()[0]:
            return True, 'good'

        # if
        elif self.match(TokenCode.tc_IF):
            # if expression
            expression = self.expression()
            if not expression[0]:
                self.sourceLine.addError(expression[1], self.token.col)
                self.eat_up_to_stop_or_sync_tokens((TokenCode.tc_RPAREN, TokenCode.tc_RBRACK,TokenCode.tc_DO,
                                                    TokenCode.tc_THEN, TokenCode.tc_COMMA, TokenCode.tc_ELSE,
                                                    TokenCode.tc_SEMICOL, TokenCode.tc_END))

            # if expression then
            if not self.match(TokenCode.tc_THEN):
                self.sourceLine.addError('^ Expected "then"', self.token.col)

            # if expression then statement
            statement = self.statement()
            if not statement[0]:
                self.sourceLine.addError(statement[1], self.token.col)
                self.eat_up_to_stop_or_sync_tokens((TokenCode.tc_ELSE, TokenCode.tc_SEMICOL, TokenCode.tc_END))

            # if expression then statement else
            if not self.match(TokenCode.tc_ELSE):
                self.sourceLine.addError('^ Expected "else"', self.token.col)

            # if expression then statement else statement
            statement = self.statement()
            if not statement[0]:
                self.sourceLine.addError(statement[1], self.token.col)
                self.eat_up_to_stop_or_sync_tokens((TokenCode.tc_ELSE, TokenCode.tc_SEMICOL, TokenCode.tc_END))

            return True, 'good'

        # while
        elif self.match(TokenCode.tc_WHILE):
            # while expression
            expression = self.expression()
            if not expression[0]:
                self.sourceLine.addError(expression[1], self.token.col)
                self.eat_up_to_stop_or_sync_tokens((TokenCode.tc_RPAREN, TokenCode.tc_RBRACK,TokenCode.tc_DO,
                                                    TokenCode.tc_THEN, TokenCode.tc_COMMA, TokenCode.tc_ELSE,
                                                    TokenCode.tc_SEMICOL, TokenCode.tc_END))

            # while expression do
            if not self.match(TokenCode.tc_DO):
                self.sourceLine.addError('^ Expected "do"', self.token.col)

            # while expression do statement
            statement = self.statement()
            if not statement[0]:
                self.sourceLine.addError(statement[1], self.token.col)
                self.eat_up_to_stop_or_sync_tokens((TokenCode.tc_ELSE, TokenCode.tc_SEMICOL, TokenCode.tc_END))

            return True, 'good'
        # error
        else:
            return False, '^ Expected "statement"'
    def statement_marked(self):
        """ implements the CFG

           statement_marked   ::=      [ expression ] assignop expression
                               |       assignop expression
                               |       ( expression_list )
                               |       ϵ
        """
        current_token_code = self.get_token_code()

        # [
        if current_token_code == TokenCode.tc_LBRACK:
            self.match(TokenCode.tc_LBRACK)

            # [ expression
            self.expression()

            # if we had had error in last function we try to recover
            if self.error:
                self.recover(NoneTerminal.nt_EXPRESSION)

            # [ expression ]
            self.match(TokenCode.tc_RBRACK)

            if not self.error:

                # [ expression ] assignop
                self.match(TokenCode.tc_ASSIGNOP)

                # [ expression ] assignop expression
            expression = self.expression()
            if not expression[0]:
                self.sourceLine.addError(expression[1], self.token.col)
                self.eat_up_to_stop_or_sync_tokens((TokenCode.tc_RPAREN, TokenCode.tc_RBRACK,TokenCode.tc_DO,
                                                    TokenCode.tc_THEN, TokenCode.tc_COMMA, TokenCode.tc_ELSE,
                                                    TokenCode.tc_SEMICOL, TokenCode.tc_END))
            return True, 'good'

        # :=
        elif current_token_code == TokenCode.tc_ASSIGNOP:
            self.match(TokenCode.tc_ASSIGNOP)

            # := expression
            expression = self.expression()
            if not expression[0]:
                self.sourceLine.addError(expression[1], self.token.col)
                self.eat_up_to_stop_or_sync_tokens((TokenCode.tc_RPAREN, TokenCode.tc_RBRACK,TokenCode.tc_DO,
                                                    TokenCode.tc_THEN, TokenCode.tc_COMMA, TokenCode.tc_ELSE,
                                                    TokenCode.tc_SEMICOL, TokenCode.tc_END))
            return True, 'good'
        # (
        elif current_token_code == TokenCode.tc_LPAREN:
            self.match(TokenCode.tc_LPAREN)

            # ( expression_list
            expression_list = self.expression_list()
            if not expression_list[0]:
                self.sourceLine.addError(expression_list[1], self.token.col)
                self.eat_up_to_stop_or_sync_tokens((TokenCode.tc_RPAREN, TokenCode.tc_RPAREN))

            # ( expression_list )
            if not self.match(TokenCode.tc_RPAREN):
                return False, '^ Expected ")"'

            return True, "good"

        # ϵ
        else:
            return True, "good"
    def expression_list(self):
        """ implements the CFG

           expression_list     ::=     expression expression_list_marked
        """
        # expression
        self.expression()

        # if we had had error in last function we try to recover
        if self.error:
            self.recover(NoneTerminal.nt_EXPRESSION)

        self.expression_list_marked()

        # if we had had error in last function we try to recover
        if self.error:
            self.recover(NoneTerminal.nt_EXPRESSION_LIST_MARKED)
    def expression_list_marked(self):
        """ inplements the CFG

           expression_list_marked      ::=     , expression expression_list_marked
                                       |       ϵ
        """
        current_token_code = self.get_token_code()

        # ,
        if current_token_code == TokenCode.tc_COMMA:
            self.match(TokenCode.tc_COMMA)

            # , expression
            self.expression()

            # if we had had error in last function we try to recover
            if self.error:
                self.recover(NoneTerminal.nt_EXPRESSION)

            # , expression expression_list_marked
            self.expression_list_marked()

            # if we had had error in last function we try to recover
            if self.error:
                self.recover(NoneTerminal.nt_EXPRESSION_LIST_MARKED)

        # ϵ
        else:
            pass
    def expression(self):
        """ implements the CFG

           expression      ::=     simple_expression1 expression_marked
        """
        # simple_expression
        self.simple_expression()

        # if we had had error in last function we try to recover
        if self.error:
            self.recover(NoneTerminal.nt_SIMPLE_EXPRESSION)

        # simple_expression expression_marked
        self.expression_marked()

        # if we had had error in last function we try to recover
        if self.error:
            self.recover(NoneTerminal.nt_EXPRESSION_MARKED)
    def expression_marked(self):
        """ implements the CFG

           expression_marked   ;;=     relop simple_expression1
                               |       ϵ
        """
        current_token_code = self.get_token_code()

        # relop
        if current_token_code == TokenCode.tc_RELOP:
            self.match(TokenCode.tc_RELOP)

            # relop simple_expression
            self.simple_expression()

            # if we had had error in last function we try to recover
            if self.error:
                self.recover(NoneTerminal.nt_SIMPLE_EXPRESSION)

        # ϵ
        else:
            pass
    def simple_expression(self):
        """ implements the CFG

           simple_expresson    ::=     term simple_expression_marked
                               |       sign term simple_expression_marked
        """
        current_token_code = self.get_token_code()

        # sign
        if current_token_code == TokenCode.tc_ADDOP:
            self.sign()

            # if we had had error in last function we try to recover
            if self.error:
                self.recover(NoneTerminal.nt_SIGN)

            # sign term
            self.term()

            # if we had had error in last function we try to recover
            if self.error:
                self.recover(NoneTerminal.nt_TERM)

            # sign term simple_expression_marked
            self.simple_expression_marked()

            # if we had had error in last function we try to recover
            if self.error:
                self.recover(NoneTerminal.nt_SIMPLE_EXPRESSION_MARKED)

        # term
        elif current_token_code == TokenCode.tc_ID or\
             current_token_code == TokenCode.tc_NUMBER or\
             current_token_code == TokenCode.tc_LPAREN or\
             current_token_code == TokenCode.tc_NOT:

            self.term()

            # if we had had error in last function we try to recover
            if self.error:
                self.recover(NoneTerminal.nt_TERM)

            # term simple_expression_marked
            self.simple_expression_marked()

            # if we had had error in last function we try to recover
            if self.error:
                self.recover(NoneTerminal.nt_SIMPLE_EXPRESSION_MARKED)

        # error
        else:
            self.match(NoneTerminal.nt_SIMPLE_EXPRESSION)
    def simple_expression_marked(self):
        """ implements the CFG

           simple_expression_marked    ::=     addop term simple_expression_marked
                                       |       ϵ

        return true if input is according to grammar, false otherwise
        """
        current_token_code = self.get_token_code()

        # addop
        if current_token_code == TokenCode.tc_ADDOP:
            self.match(TokenCode.tc_ADDOP)

            # addop term
            self.term()

            # if we had had error in last function we try to recover
            if self.error:
                self.recover(NoneTerminal.nt_TERM)

            # addop term simple_expression_marked
            self.simple_expression_marked()

            # if we had had error in last function we try to recover
            if self.error:
                self.recover(NoneTerminal.nt_SIMPLE_EXPRESSION_MARKED)

        # ϵ
        else:
            pass
    def term(self):
        """ implements the CFG

           term    ::=     factor term_marked
        """
        # factor
        self.factor()

        # if we had had error in last function we try to recover
        if self.error:
            self.recover(NoneTerminal.nt_FACTOR)

        # factor term_marked
        self.term_marked()

        # if we had had error in last function we try to recover
        if self.error:
            self.recover(NoneTerminal.nt_FACTOR)
    def term_marked(self):
        """ implements the CFG

           term_marked    ::=     mulop factor factor term_marked
                           |      ϵ
        """
        current_token_code = self.get_token_code()

        # mulop
        if current_token_code == TokenCode.tc_MULOP:
            self.match(TokenCode.tc_MULOP)

            # mulop factor
            self.factor()

            # if we had had error in last function we try to recover
            if self.error:
                self.recover(NoneTerminal.nt_FACTOR)

            # mulop factor term_marked
            self.term_marked()

            # if we had had error in last function we try to recover
            if self.error:
                self.recover(NoneTerminal.nt_TERM_MARKED)

        # ϵ
        else:
            pass
    def factor(self):
        """ implements the CFG

           factor  ::=     id factor_marked
                   |       num
                   |       ( expression )
                   |       not factor

        return true if input is according to grammar, false otherwise
        """
        current_token_code = self.get_token_code()

        # id
        if current_token_code == TokenCode.tc_ID:
            self.match(TokenCode.tc_ID)

            # id factor_marked
            self.factor_marked()

            # if we had had error in last function we try to recover
            if self.error:
                self.recover(NoneTerminal.nt_FACTOR_MARKED)

        # num
        elif current_token_code == TokenCode.tc_NUMBER:
            self.match(TokenCode.tc_NUMBER)

        # (
        elif current_token_code == TokenCode.tc_LPAREN:
            self.match(TokenCode.tc_LPAREN)

            # ( expression
            self.expression()

            # if we had had error in last function we try to recover
            if self.error:
                self.recover(NoneTerminal.nt_EXPRESSION)

            # ( expression )
            self.match(TokenCode.tc_RPAREN)

        # not
        elif current_token_code == TokenCode.tc_NOT:
            self.match(TokenCode.tc_NOT)

            # not factor
            self.factor()

            # if we had had error in last function we try to recover
            if self.error:
                self.recover(NoneTerminal.nt_FACTOR)

        # error
        else:
            self.match(NoneTerminal.nt_FACTOR)
    def factor_marked(self):
        """ implements the CFG.

              factor_marked   ::=     ( expression_list )
                              |       [ expression ]
                              |       ϵ
        """
        current_token_code = self.get_token_code()

        # (
        if current_token_code == TokenCode.tc_LPAREN:
            self.match(TokenCode.tc_LPAREN)

            # ( expression_list
            self.expression_list()
            if self.error:
                self.recover(NoneTerminal.nt_EXPRESSION_LIST)

            # ( expression_list )
            self.match(TokenCode.tc_RPAREN)

        # [
        elif current_token_code == TokenCode.tc_LBRACK:
            self.match(TokenCode.tc_LBRACK)

            # [ expression
            self.expression()

            # if we had had error in last function we try to recover
            if self.error:
                self.recover(NoneTerminal.nt_EXPRESSION)

            # [ expression ]
            self.match(TokenCode.tc_RBRACK)

        # ϵ
        else:
            pass
    def sign(self):
        """ implements the CFG.

              sign    ::=     +
                      |       -
        """
        current_op_type = self.get_op_type()

        if current_op_type == OpType.op_PLUS:
            self.match(TokenCode.tc_ADDOP)

        elif current_op_type == OpType.op_MINUS:
            self.match(TokenCode.tc_ADDOP)

        # does not fit syntax
        else:
            self.match(TokenCode.tc_SIGN)


class PascalParserTester:
    def testLexical(self):
        filename = "test_files/pascal_lex1"
        parser = PascalParser.PascalParser(filename)
        sign = parser.program()
        if not sign[0]:
            print "sign error"
            print sign[1]
    def testSign(self):
        filename = "test_files/sign"
        parser = PascalParser.PascalParser(filename)
        sign = parser.sign()
        if not sign[0]:
            print "sign error"
            print sign[1]
    def testType(self):
        filename = "test_files/type"
        parser = PascalParser.PascalParser(filename)
        sign = parser.type()
        if not sign[0]:
            print "sign error"
            print sign[1]
    def testParser1(self):
        filename = "test_files/parser1"
        parser = PascalParser(filename)
        sign = parser.program()
        if not sign[0]:
            print "sign error"
            print sign[1]
    def testProgramCorrect(self):
        filename = "test_files/pas_syntax_ok"
        parser = PascalParser(filename)
        sign = parser.program()
        if not sign[0]:
            print "sign error"
            print sign[1]
    def testProgramError(self):
        filename = "test_files/pas_syntax_err"
        parser = PascalParser(filename)
        sign = parser.program()
        if not sign[0]:
            print "sign error"
            print sign[1]

tester = PascalParserTester()
tester.testProgramError()