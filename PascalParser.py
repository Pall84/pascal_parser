# -*- coding: utf-8 -*-
__author__ = 'palleymundsson'

from plex import *
import PascalLexer
import OpType
import TokenCode
import SourceLine
import Token

class PascalParser:
    def __init__(self, filename):
        lexicon = PascalLexer.getLexer()

        #filename = "test_files/pascal_lex1.txt"
        f = open(filename, "r")
        self.scanner = Scanner(lexicon, f, filename)
        self.sourceLine = SourceLine.SourceLine()
        self.token = Token
        self.nextToken()
    def nextToken(self):
        temp = self.scanner.read()
        if temp[0]:
            token = Token.Token(temp[0][0], temp[0][1], temp[0][2], self.scanner.start_line, self.scanner.start_col, temp[1])
            self.sourceLine.addToken(token)
            self.token = token
            if self.token.token_code == TokenCode.tc_NEWLINE:
                self.nextToken()
            if self.token.token_code == TokenCode.tc_COMMENT:
                self.nextToken()
            if self.token.token_code == TokenCode.tc_ERROR:
                self.sourceLine.addError('^ Illegal character', token.col)
                self.nextToken()
        else:
            self.sourceLine.printing()
    def match(self, token_code):
        if self.token.token_code == token_code:
            self.nextToken()
            return True
        else:
            return False
    def eat_up_to_stop_or_sync_tokens(self, stop_tokens=tuple()):
        sync_tokens = TokenCode.tc_VAR, TokenCode.tc_FUNCTION, TokenCode.tc_PROCEDURE, TokenCode.tc_BEGIN, TokenCode.tc_DOT
        sync_and_stop_tokens = sync_tokens + stop_tokens
        run = True
        for token in sync_and_stop_tokens:
            if self.token.token_code == token:
                run = False
                break
        while run:
            self.nextToken()
            for token in sync_and_stop_tokens:
                if self.token.token_code == token:
                    run = False
                    break

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
            self.sourceLine.addError('^ expecting "program"', self.token.col)
            hasError = True

        # program id
        if not self.match(TokenCode.tc_ID) and not hasError:
            self.sourceLine.addError('^ expecting "id"', self.token.col)
            hasError = True

        # program id (
        if not self.match(TokenCode.tc_LPAREN) and not hasError:
            self.sourceLine.addError('^ expecting "("', self.token.col)
            hasError = True

        if hasError:
            self.eat_up_to_stop_or_sync_tokens((TokenCode.tc_ID, TokenCode.tc_COMMA))
            hasError = False

        # program id ( identifier_list
        identifier_list = self.identifier_list()
        if not identifier_list[0]:
            self.sourceLine.addError(identifier_list[1], self.token.col)
            self.eat_up_to_stop_or_sync_tokens((TokenCode.tc_RPAREN, TokenCode.tc_SEMICOL))

        # program id ( identifier_list )
        if not self.match(TokenCode.tc_RPAREN):
            self.sourceLine.addError('^ expecting ")"', self.token.col)
            hasError = True

        # program id ( identifier_list ) ;
        if not self.match(TokenCode.tc_SEMICOL) and not hasError:
            self.sourceLine.addError('^ expecting ";"', self.token.col)

        if hasError:
            self.eat_up_to_stop_or_sync_tokens()
            hasError = False

        # program id ( identifier_list ) ;
        # declarations
        declarations = self.declarations()
        if not declarations[0]:
            self.sourceLine.addError(declarations[1], self.token.col)
            self.eat_up_to_stop_or_sync_tokens()

        # program id ( identifier_list ) ;
        # declarations
        # subprogram_declarations
        subprogram_declarations = self.subprogram_declarations()
        if not subprogram_declarations[0]:
            self.sourceLine.addError(subprogram_declarations[1], self.token.col)
            self.eat_up_to_stop_or_sync_tokens()

        # program id ( identifier_list ) ;
        # declarations
        # subprogram_declarations
        # compound_statement
        compound_statement = self.compound_statement()
        if not compound_statement[0]:
            self.sourceLine.addError(compound_statement[1], self.token.col)
            self.eat_up_to_stop_or_sync_tokens()

        # program id ( identifier_list ) ;
        # declarations
        # subprogram_declarations
        # compound_statement
        # .
        if not self.match(TokenCode.tc_DOT):
            self.sourceLine.addError('^ expecting "."', self.token.col)

        return True, 'good'
    def identifier_list(self):
        """implements the CFG.

           identifier_list     ::=     id identifier_list_marked

        return true if input is according to grammar, false otherwise
        """
        # id
        if self.match(TokenCode.tc_ID):
            # id identifier_list_marked
            return self.identifier_list_marked()

        # error
        else:
            return False, '^ expecting "id"'
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
                return False, '^ expecting "id"'

            #, id identifier_list_marked
            return self.identifier_list_marked()

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
                self.eat_up_to_stop_or_sync_tokens((TokenCode.tc_COLON,TokenCode.tc_ARRAY,TokenCode.tc_INTEGER,
                                                    TokenCode.tc_REAL, TokenCode.tc_SEMICOL))

            # var identifier_list :
            if not self.match(TokenCode.tc_COLON):
                self.sourceLine.addError('^ expecting ":"', self.token.col)
                self.eat_up_to_stop_or_sync_tokens((TokenCode.tc_ARRAY,TokenCode.tc_INTEGER,
                                                    TokenCode.tc_REAL, TokenCode.tc_SEMICOL))


            # var identifier_list : type
            type = self.type()
            if not type[0]:
                self.sourceLine.addError(type[1], self.token.col)
                self.eat_up_to_stop_or_sync_tokens((TokenCode.tc_SEMICOL, TokenCode.tc_SEMICOL))

            # var identifier_list : type ;
            if not self.match(TokenCode.tc_SEMICOL):
                self.sourceLine.addError('^ expecting ";"', self.token.col)


            # var identifier_list : type ; declarations
            return self.declarations()

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
                return False, '^ expecting "["'

            # array [ num
            if not self.match(TokenCode.tc_NUMBER):
                return False, '^ expecting "number"'

            # array [ num ..
            if not self.match(TokenCode.tc_DOTDOT):
                return False, '^ expecting ".."'

            # array [ num .. num
            if not self.match(TokenCode.tc_NUMBER):
                return False, '^ expecting "number"'

            # array [ num .. num ]
            if not self.match(TokenCode.tc_RBRACK):
                return False, '^ expecting "]"'

            # array [ num .. num ] of
            if not self.match(TokenCode.tc_OF):
                return False, '^ expecting "of"'

            # array [ num .. num ] of standard_type
            return self.standard_type()

        # error
        else:
            return False, '^ expecting "type"'
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
            return False, '^ expecting "standard_type"'
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
                return False, '^ expecting ";"'

            # subprogram_declaration ; subprogram_declarations
            return self.subprogram_declarations()

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
                return declarations

            # subprogram_head declarations compound_statement
            return self.compound_statement()

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
                return False, '^ expecting "id"'

            # function id arguments
            arguments = self.arguments()
            if not arguments[0]:
                return arguments

            # function id arguments :
            if not self.match(TokenCode.tc_COLON):
                return False, '^ expecting ":"'

            # function id arguments : standard_type
            standard_type = self.standard_type()
            if not standard_type[0]:
                return standard_type

            # function id arguments : standard_type ;
            if not self.match(TokenCode.tc_SEMICOL):
                return False, '^ expecting ";"'

            return True, 'good'

        # procedure
        if self.match(TokenCode.tc_PROCEDURE):
            # procedure id
            if not self.match(TokenCode.tc_ID):
                return False, '^ expecting "id"'

            # procedure id arguments
            arguments = self.arguments()
            if not arguments[0]:
                return arguments

            # procedure id arguments ;
            if not self.match(TokenCode.tc_SEMICOL):
                return False, '^ expecting ";"'

            return True, 'good'

        # error
        return False, 'expecting "subprogram_head'
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
                return parameter_list

            # ( parameter_list )
            if not self.match(TokenCode.tc_RPAREN):
                return False, '^ expecting ":"'

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
                return False, '^ expecting ":"'

            # identifier_list : type
            type = self.type()
            if not type[0]:
                return type

            # identifier_list : type parameter_list_marked
            return self.parameter_list_marked()

        # error
        else:
            return False, '^ expecting "identifier_list"'
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
                return identifier_list

            # ; identifier_list :
            if not self.match(TokenCode.tc_COLON):
                return False, '^ expecting ":"'

            # ; identifier_list : type
            type = self.type()
            if not type[0]:
                return type

            # ; identifier_list : type parameter_list_marked
            return self.parameter_list_marked()

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
                self.sourceLine.addError('^ expecting "end"', self.token.col)

            return True, 'good'

        # error
        return False, '^ expecting "begin"'
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
            return self.statement_list_marked()

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
                return statement

            # ; statement statement_list_marked
            return self.statement_list_marked()

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
            return self.statement_marked()

        # compound_statement
        elif self.compound_statement()[0]:
            return True, 'good'

        # if
        elif self.match(TokenCode.tc_IF):
            # if expression
            expression = self.expression()
            if not expression[0]:
                self.sourceLine.addError(expression[1], self.token.col)
                self.eat_up_to_stop_or_sync_tokens((TokenCode.tc_THEN, TokenCode.tc_ELSE, TokenCode.tc_ID,
                                                    TokenCode.tc_IF, TokenCode.tc_WHILE))

            # if expression then
            if not self.match(TokenCode.tc_THEN):
                self.sourceLine.addError('^ expecting "then"', self.token.col)
                self.eat_up_to_stop_or_sync_tokens((TokenCode.tc_THEN, TokenCode.tc_ELSE, TokenCode.tc_ID,
                                                    TokenCode.tc_IF, TokenCode.tc_WHILE))

            # if expression then statement
            statement = self.statement()
            if not statement[0]:
                self.sourceLine.addError(statement[1], self.token.col)
                self.eat_up_to_stop_or_sync_tokens((TokenCode.tc_THEN, TokenCode.tc_ELSE, TokenCode.tc_ID,
                                                    TokenCode.tc_IF, TokenCode.tc_WHILE))

            # if expression then statement else
            if not self.match(TokenCode.tc_ELSE):
                self.sourceLine.addError('^ expecting "else"', self.token.col)
                self.eat_up_to_stop_or_sync_tokens((TokenCode.tc_THEN, TokenCode.tc_ELSE, TokenCode.tc_ID,
                                                    TokenCode.tc_IF, TokenCode.tc_WHILE))

            # if expression then statement else statement
            return self.statement()

        # while
        if self.match(TokenCode.tc_WHILE):
            # while expression
            expression = self.expression()
            if not expression[0]:
                self.sourceLine.addError(expression[1], self.token.col)
                self.eat_up_to_stop_or_sync_tokens((TokenCode.tc_DO,TokenCode.tc_THEN, TokenCode.tc_ELSE, TokenCode.tc_ID,
                                                    TokenCode.tc_IF, TokenCode.tc_WHILE))

            # while expression do
            if not self.match(TokenCode.tc_DO):
                self.sourceLine.addError('^ expecting "do"', self.token.col)
                self.eat_up_to_stop_or_sync_tokens((TokenCode.tc_DO,TokenCode.tc_THEN, TokenCode.tc_ELSE, TokenCode.tc_ID,
                                                    TokenCode.tc_IF, TokenCode.tc_WHILE))

            # while expression do statement
            return self.statement()

        # error
        else:
            return False, '^ expecting "statement"'
    def statement_marked(self):
        """ implements the CFG

           statement_marked   ::=      [ expression ] assignop expression
                               |       assignop expression
                               |       ( expression_list )
                               |       ϵ

        return true if input is according to grammar, false otherwise
        """
        # [
        if self.match(TokenCode.tc_LBRACK):
            # [ expression
            expression = self.expression()
            if not expression[0]:
                return expression

            # [ expression ]
            if not self.match(TokenCode.tc_RBRACK):
                return False, '^ expecting "]"'

            # [ expression ] assignop
            if not self.match(TokenCode.tc_ASSIGNOP):
                return False, '^ expecting ":="'

                # [ expression ] assignop expression
            return self.expression()

        # :=
        elif self.match(TokenCode.tc_ASSIGNOP):
            # := expression
            return self.expression()

        # (
        elif self.match(TokenCode.tc_LPAREN):
            # ( expression_list
            expression_list = self.expression_list()
            if not expression_list[0]:
                return  expression_list

            # ( expression_list )
            if not self.match(TokenCode.tc_RPAREN):
                return False, '^ expecting ")"'

            return True, "good"

        # ϵ
        else:
            return True, "good"
    def expression_list(self):
        """ implements the CFG

           expression_list     ::=     expression expression_list_marked

        return true if input is according to grammar, false otherwise
        """
        # expression
        expression = self.expression()
        if expression[0]:
            # expression expression_list_marked
            return self.expression_list_marked()

        # error
        else:
            return expression
    def expression_list_marked(self):
        """ inplements the CFG

           expression_list_marked      ::=     , expression expression_list_marked
                                       |       ϵ

        return true if input is according to grammar, false otherwise
        """
        # ,
        if self.match(TokenCode.tc_COMMA):
            # , expression
            expression = self.expression()
            if not expression[0]:
                return expression

            # , expression expression_list_marked
            return self.expression_list_marked()

        # ϵ
        else:
            return True, 'good'
    def expression(self):
        """ implements the CFG

           expression      ::=     simple_expression1 expression_marked

        return true if input is according to grammar, false otherwise
        """
        # simple_expression
        simple_expression = self.simple_expression()
        if simple_expression[0]:
            # simple_expression expression_marked
            return self.expression_marked()

        # error
        else:
            return simple_expression
    def expression_marked(self):
        """ inplements the CFG

           expression_marked   ;;=     relop simple_expression1
                               |       ϵ

        return true if input is according to grammar, false otherwise
        """
        # relop
        if self.match(TokenCode.tc_RELOP):
            # relop simple_expression
            return self.simple_expression()

        # ϵ
        else:
            return True, "good"
    def simple_expression(self):
        """ implements the CFG

           simple_expresson    ::=     term simple_expression_marked
                               |       sign term simple_expression_marked

        return true if input is according to grammar, false otherwise
        """
        # sign
        sign = self.sign()
        if sign[0]:
            # sign term
            term = self.term()
            if not term[0]:
                return term

            return self.simple_expression_marked()

        elif self.term()[0]:
            return self.simple_expression_marked()

        # error
        else:
            return False, '^ expecting "simple_expression"'
    def simple_expression_marked(self):
        """ implements the CFG

           simple_expression_marked    ::=     addop term simple_expression_marked
                                       |       ϵ

        return true if input is according to grammar, false otherwise
        """
        # addop
        if self.match(TokenCode.tc_ADDOP):
            # addop term
            term = self.term()
            if not term[0]:
                self.sourceLine.addError(term[1], self.token.col)

            # addop term simple_expression_marked
            return self.simple_expression_marked()

        # ϵ
        else:
            return True, "good"
    def term(self):
        """ implements the CFG

           term    ::=     factor term_marked

        return true if input is according to grammar, false otherwise
        """
        # factor
        factor = self.factor()
        if factor[0]:
            # factor term_marked
            return self.term_marked()

        # error
        else:
            return factor
    def term_marked(self):
        """ implements the CFG

           term_marked    ::=     mulop factor factor term_marked
                           |      ϵ

        return true if input is according to grammar, false otherwise
        """
        # mulop
        if self.match(TokenCode.tc_MULOP):

            # mulop factor
            factor = self.factor()
            if not factor[0]:
                self.sourceLine.addError(factor[1], self.token.col)

            # mulop factor term_marked
            return self.term_marked()

        # ϵ
        else:
            return True, "good"
    def factor(self):
        """ implements the CFG

           factor  ::=     id factor_marked
                   |       num
                   |       ( expression )
                   |       not factor

        return true if input is according to grammar, false otherwise
        """
        # id
        if self.match(TokenCode.tc_ID):

            # id factor_marked
            return self.factor_marked()

        # num
        elif self.match(TokenCode.tc_NUMBER):

            return True, 'good'

        # (
        elif self.match(TokenCode.tc_LPAREN):

            # ( expression
            expression = self.expression()
            if not expression[0]:
                self.sourceLine.addError(expression[1], self.token.col)

            # ( expression )
            if not self.match(TokenCode.tc_RPAREN):
                self.sourceLine.addError('^ expecting ")"', self.token.col)

            return True, 'good'

        # not
        elif self.match(TokenCode.tc_NOT):

            # not factor
            return self.factor()

        # error
        else:
            return False, '^ expecting "factor"'
    def factor_marked(self):
        """ implements the CFG.

              factor_marked   ::=     ( expression_list )
                              |       [ expression ]
                              |       ϵ

        return true if input is according to grammar, false otherwise
        """
        # (
        if self.match(TokenCode.tc_LPAREN):

            # ( expression_list
            expression_list = self.expression_list()
            if not expression_list[0]:
                self.sourceLine.addError(expression_list[1], self.token.col)

            # ( expression_list )
            if not self.match(TokenCode.tc_RPAREN):
                self.sourceLine.addError('^ expecting ")"', self.token.col)

            return True, "good"

        # [
        elif self.match(TokenCode.tc_LBRACK):

            # [ expression
            expression = self.expression()
            if not expression[0]:
                self.sourceLine.addError(expression[1], self.token.col)

            # [ expression ]
            if not self.match(TokenCode.tc_RBRACK):
                self.sourceLine.addError('^ expecting "]"', self.token.col)


            return True, "good"

        # ϵ
        else:
            return True, "good"
    def sign(self):
        """ implements the CFG.

              sign    ::=     +
                      |       -

        @return true if input is according to grammar false otherwise.
        """
        if self.token.op_type == OpType.op_PLUS:
            self.nextToken()
            return True, "good"

        elif self.token.op_type == OpType.op_MINUS:
            self.nextToken()
            return True, "good"

        # does not fit syntax
        else:
            return False, '^ expecting "sign"'