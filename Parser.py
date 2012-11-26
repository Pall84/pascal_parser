# -*- coding: utf-8 -*-
__author__ = 'palleymundsson'

from Lexical import *
from CodeGenerator import *

class PascalParser:
    """ parser part of pascal language.

    repeatedly ask for next token in source code and checks if it
    fits the CFC for subset of pascal language, if it does not fit it
    tells scanner what token it was expecting and tries to recover from that
    error. Builds TAC intermediate code while parsing.
    """

    def __init__(self, filename):
        """ initializer pascal parser

        initializer pascal scanner with filename of source code.
        gets first token from scanner.
        sets error to none.
        initializer TAC code generator.
        """
        self.scanner = PascalScanner(filename)
        self.next_token()
        self.error = None
        self.code = Code()

    def __str__(self):
        printout = ""
        if self.scanner.source_line.number_of_errors > 0:
            printout = self.scanner.__str__()
        else:
            printout = self.code.__str__()

        return printout

    def get_token_code(self):
        """ returns token code from current token. """
        return self.token.token_code

    def get_op_type(self):
        """ returns op type of current token. """
        return self.token.op_type

    def next_token(self):
        """ loads next token from source code. """
        self.token = self.scanner.next_token()

    def match(self, token_code):
        """ check if token code matches current token token code.

        if token code matches current token token code we load next token.
        if token code does not match current token code we add error.
        """
        current_token_code = self.get_token_code()

        # we have a match
        if current_token_code == token_code:
            self.next_token()

        # we do not have a match
        else:
            self.error = '^ Expected "%s"' % token_code

    def recover(self, non_terminal=None ):
        """ recovers from error

        Recovers by eating up all tokens up to synchronizing tokens or stop tokens
        who are first or follow set of tokens for None terminal in pascal CFG
        We add error to source code and clear error variable.
        """
        sync_tokens = TokenCode.tc_VAR, TokenCode.tc_FUNCTION, TokenCode.tc_PROCEDURE, TokenCode.tc_BEGIN, TokenCode.tc_DOT
        stop_tokens = None

        # follow tokens of non_terminal
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

        elif non_terminal == NoneTerminal.nt_PROGRAM_FOLLOW:
            stop_tokens = (TokenCode.tc_EOF,)

        # first tokens of non_terminal
        elif non_terminal == NoneTerminal.nt_SIGN_FIRST:
            stop_tokens = (TokenCode.tc_ADDOP,)

        elif non_terminal == NoneTerminal.nt_FACTOR_MARKED_FIRST:
            stop_tokens = (TokenCode.tc_LPAREN, TokenCode.tc_LBRACK, TokenCode.tc_ID,
                           TokenCode.tc_NUMBER, TokenCode.tc_NOT, TokenCode.tc_ADDOP,
                           TokenCode.tc_RPAREN, TokenCode.tc_RBRACK, TokenCode.tc_DO,
                           TokenCode.tc_THEN, TokenCode.tc_COMMA, TokenCode.tc_ELSE,
                           TokenCode.tc_SEMICOL, TokenCode.tc_END)

        elif non_terminal == NoneTerminal.nt_FACTOR_FIRST or\
             non_terminal == NoneTerminal.nt_TERM_FIRST:
            stop_tokens = (TokenCode.tc_ID, TokenCode.tc_NUMBER, TokenCode.tc_LPAREN, TokenCode.tc_NOT)

        elif non_terminal == NoneTerminal.nt_TERM_MARKED_FIRST:
            stop_tokens = (TokenCode.tc_MULOP, TokenCode.tc_ADDOP, TokenCode.tc_RPAREN,
                           TokenCode.tc_RBRACK, TokenCode.tc_DO, TokenCode.tc_THEN,
                           TokenCode.tc_COMMA, TokenCode.tc_ELSE, TokenCode.tc_SEMICOL, TokenCode.tc_END)

        elif non_terminal == NoneTerminal.nt_SIMPLE_EXPRESSION_MARKED_FIRST:
            stop_tokens = (TokenCode.tc_ADDOP, TokenCode.tc_RPAREN,
                           TokenCode.tc_RBRACK, TokenCode.tc_DO, TokenCode.tc_THEN,
                           TokenCode.tc_COMMA, TokenCode.tc_ELSE, TokenCode.tc_SEMICOL, TokenCode.tc_END)

        elif non_terminal == NoneTerminal.nt_SIMPLE_EXPRESSION_FIRST or\
             non_terminal == NoneTerminal.nt_EXPRESSION_FIRST or\
             non_terminal == NoneTerminal.nt_EXPRESSION_LIST_FIRST:
            stop_tokens = (TokenCode.tc_ID, TokenCode.tc_NUMBER, TokenCode.tc_LPAREN,
                           TokenCode.tc_NOT, TokenCode.tc_ADDOP)

        elif non_terminal == NoneTerminal.nt_EXPRESSION_MARKED_FIRST:
            stop_tokens = (TokenCode.tc_RELOP, TokenCode.tc_RPAREN,
                           TokenCode.tc_RBRACK, TokenCode.tc_DO, TokenCode.tc_THEN,
                           TokenCode.tc_COMMA, TokenCode.tc_ELSE, TokenCode.tc_SEMICOL, TokenCode.tc_END)

        elif non_terminal == NoneTerminal.nt_EXPRESSION_LIST_MARKED_FIRST:
            stop_tokens = (TokenCode.tc_COMMA, TokenCode.tc_RPAREN)

        elif non_terminal == NoneTerminal.nt_STATEMENT_MARKED_FIRST:
            stop_tokens = (TokenCode.tc_LBRACK, TokenCode.tc_ASSIGNOP, TokenCode.tc_LPAREN,
                           TokenCode.tc_ELSE, TokenCode.tc_SEMICOL, TokenCode.tc_END)

        elif non_terminal == NoneTerminal.nt_STATEMENT_FIRST or\
             non_terminal == NoneTerminal.nt_STATEMENT_LIST_FIRST:
            stop_tokens = (TokenCode.tc_ID, TokenCode.tc_IF, TokenCode.tc_WHILE, TokenCode.tc_BEGIN)

        elif non_terminal == NoneTerminal.nt_STATEMENT_LIST_MARKED_FIRST:
            stop_tokens = (TokenCode.tc_SEMICOL, TokenCode.tc_END)

        elif non_terminal == NoneTerminal.nt_OPTIONAL_STATEMENT_FIRST:
            stop_tokens = (TokenCode.tc_ID, TokenCode.tc_IF, TokenCode.tc_WHILE,
                           TokenCode.tc_BEGIN, TokenCode.tc_END)

        elif non_terminal == NoneTerminal.nt_COMPOUND_STATEMENT_FIRST:
            stop_tokens = (TokenCode.tc_BEGIN,)

        elif non_terminal == NoneTerminal.nt_PARAMETER_LIST_MARKED_FIRST:
            stop_tokens = (TokenCode.tc_SEMICOL,)

        elif non_terminal == NoneTerminal.nt_PARAMETER_LIST_FIRST or\
             non_terminal == NoneTerminal.nt_IDENTIFIER_LIST_FIRST:
            stop_tokens = (TokenCode.tc_ID,)

        elif non_terminal == NoneTerminal.nt_ARGUMENTS_FIRST:
            stop_tokens = (TokenCode.tc_LPAREN, TokenCode.tc_COLON, TokenCode.tc_SEMICOL)

        elif non_terminal == NoneTerminal.nt_SUBPROGRAM_HEAD_FIRST or\
             non_terminal == NoneTerminal.nt_SUBPROGRAM_DECLARATION_FIRST or\
             non_terminal == NoneTerminal.nt_SUBPROGRAM_DECLARATIONS_FIRST:
            stop_tokens = (TokenCode.tc_FUNCTION, TokenCode.tc_PROCEDURE)

        elif non_terminal == NoneTerminal.nt_STANDARD_TYPE_FIRST:
            stop_tokens = (TokenCode.tc_INTEGER, TokenCode.tc_REAL)

        elif non_terminal == NoneTerminal.nt_TYPE_FIRST:
            stop_tokens = (TokenCode.tc_INTEGER, TokenCode.tc_REAL, TokenCode.tc_ARRAY)

        elif non_terminal == NoneTerminal.nt_DECLARATIONS_FIRST:
            stop_tokens = (TokenCode.tc_VAR, TokenCode.tc_FUNCTION, TokenCode.tc_PROCEDURE, TokenCode.tc_BEGIN)

        elif non_terminal == NoneTerminal.nt_IDENTIFIER_LIST_MARKED_FIRST:
            stop_tokens = (TokenCode.tc_COMMA, TokenCode.tc_RPAREN, TokenCode.tc_COLON)


        # add error to source code and clear error variable
        self.scanner.add_error(self.error, self.token.col)
        self.error = None

        # eating up tokens
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
        """ generates new temporal variable.

        returns reference to symbol table entry of temporal variable.
        """
        temp = self.code.new_temp()
        entry =  self.scanner.symbol_table.insert(temp)
        self.code.generate(CodeOp.cd_VAR, None, None, entry)
        return entry

    def new_label(self):
        """ generates new label

        returns reference to symbol table entry of new label
        """
        label = self.code.new_label()
        entry = self.scanner.symbol_table.insert(label)
        return entry

    def convert_optype_to_opcode(self, op_type):
        if op_type == OpType.op_AND:
            return CodeOp.cd_AND
        elif op_type == OpType.op_MINUS:
            return CodeOp.cd_SUB
        elif op_type == OpType.op_DIV:
            return CodeOp.cd_DIV
        elif op_type == OpType.op_DIVIDE:
            return CodeOp.cd_DIVIDE
        elif op_type == OpType.op_EQ:
            return CodeOp.cd_EQ
        elif op_type == OpType.op_GE:
            return CodeOp.cd_GE
        elif op_type == OpType.op_GT:
            return CodeOp.cd_GT
        elif op_type == OpType.op_LE:
            return CodeOp.cd_LE
        elif op_type == OpType.op_MOD:
            return CodeOp.cd_MOD
        elif op_type == OpType.op_MULT:
            return CodeOp.cd_MULT
        elif op_type == OpType.op_NE:
            return CodeOp.cd_NE
        elif op_type == OpType.op_OR:
            return CodeOp.cd_OR
        elif op_type == OpType.op_PLUS:
            return CodeOp.cd_ADD
        elif op_type == OpType.op_NONE:
            return CodeOp.cd_NOOP
        elif op_type == OpType.op_LT:
            return CodeOp.cd_LT

    def program(self):
        """ implements the CFG

              program     ::=     program id ( identifier_list ) ;
                                  declarations
                                  subprogram_declarations
                                  compound_statement
                                  .
        """
        #program
        self.match(TokenCode.tc_PROGRAM)

        if not self.error:
            # program id
            entry = self.token.symbol_table_entry
            self.match(TokenCode.tc_ID)

        if not self.error:
            # program id (
            self.match(TokenCode.tc_LPAREN)

        # if we had had error in last function we try to recover
        if self.error:
            self.recover(NoneTerminal.nt_IDENTIFIER_LIST_FIRST)

        # program id ( identifier_list
        self.identifier_list()

        # if we had had error in last function we try to recover
        if self.error:
            self.recover(NoneTerminal.nt_IDENTIFIER_LIST_FOLLOW)

        # program id ( identifier_list )
        self.match(TokenCode.tc_RPAREN)

        if not self.error:
            # program id ( identifier_list ) ;
            self.match(TokenCode.tc_SEMICOL)

        # if we had had error in last function we try to recover
        if self.error:
            self.recover(NoneTerminal.nt_DECLARATIONS_FIRST)

        # program id ( identifier_list ) ;
        # declarations
        self.declarations()

        # if we had had error in last function we try to recover
        if self.error:
            self.recover(NoneTerminal.nt_DECLARATIONS_FOLLOW)

        self.code.generate(CodeOp.cd_GOTO, None, None, entry)

        # program id ( identifier_list ) ;
        # declarations
        # subprogram_declarations
        self.subprogram_declarations()

        # if we had had error in last function we try to recover
        if self.error:
            self.recover(NoneTerminal.nt_SUBPROGRAM_DECLARATIONS_FOLLOW)

        self.code.generate(CodeOp.cd_LABEL, None, None, entry)

        # program id ( identifier_list ) ;
        # declarations
        # subprogram_declarations
        # compound_statement
        self.compound_statement()

        # if we had had error in last function we try to recover
        if self.error:
            self.recover(NoneTerminal.nt_COMPOUND_STATEMENT_FOLLOW)

        # program id ( identifier_list ) ;
        # declarations
        # subprogram_declarations
        # compound_statement
        # .
        self.code.generate(CodeOp.cd_RETURN, None, None, None)
        self.match(TokenCode.tc_DOT)


        # if we had had error in last function we try to recover
        if self.error:
            self.recover(NoneTerminal.nt_PROGRAM_FOLLOW)
    def identifier_list(self, entry_list=None):
        """implements the CFG.

           identifier_list     ::=     id identifier_list_marked

        return true if input is according to grammar, false otherwise
        """
        # id
        if not entry_list == None:
            entry = self.token.symbol_table_entry
            entry_list.append(entry)
        self.match(TokenCode.tc_ID)

        # if we had had error in last function we try to recover
        if self.error:
            self.recover(NoneTerminal.nt_IDENTIFIER_LIST_MARKED_FIRST)

        # id identifier_list_marked
        self.identifier_list_marked(entry_list)

        # if we had had error in last function we try to recover
        if self.error:
            self.recover(NoneTerminal.nt_IDENTIFIER_LIST_MARKED_FOLLOW)
    def identifier_list_marked(self, entry_list):
        """ implements the CFG

            identifier_list_marked  ::=     , id identifier_list_marked
                                   |       ϵ
        """
        current_token_code = self.get_token_code()

        # ,
        if current_token_code == TokenCode.tc_COMMA:
            self.match(TokenCode.tc_COMMA)

            # , id
            if entry_list:
                entry = self.token.symbol_table_entry
                entry_list.append(entry)
            self.match(TokenCode.tc_ID)

            # if we had had error in last function we try to recover
            if self.error:
                self.recover(NoneTerminal.nt_IDENTIFIER_LIST_MARKED_FIRST)

            #, id identifier_list_marked
            self.identifier_list_marked(entry_list)

            # if we had had error in last function we try to recover
            if self.error:
                self.recover(NoneTerminal.nt_IDENTIFIER_LIST_MARKED_FOLLOW)

        # ϵ
        else:
            pass
    def declarations(self):
        """ implements the CFG

            declarations    ::=     var identifier_list : type ; declarations
                            |       ϵ
        """
        current_token_code = self.get_token_code()

        # var
        if current_token_code == TokenCode.tc_VAR:
            self.match(TokenCode.tc_VAR)

            # var identifier_list
            entry_list = []
            self.identifier_list(entry_list)
            for entry in entry_list:
                self.code.generate(CodeOp.cd_VAR, None, None, entry)

            # if we had had error in last function we try to recover
            if self.error:
                self.recover(NoneTerminal.nt_IDENTIFIER_LIST_FOLLOW)

            # var identifier_list :
            self.match(TokenCode.tc_COLON)

            # if we had had error in last function we try to recover
            if self.error:
                self.recover(NoneTerminal.nt_TYPE_FIRST)

            # var identifier_list : type
            self.type()

            # if we had had error in last function we try to recover
            if self.error:
                self.recover(NoneTerminal.nt_TYPE_FOLLOW)

            # var identifier_list : type ;
            self.match(TokenCode.tc_SEMICOL)

            # if we had had error in last function we try to recover
            if self.error:
                self.recover(NoneTerminal.nt_DECLARATIONS_FIRST)

            # var identifier_list : type ; declarations
            self.declarations()

            # if we had had error in last function we try to recover
            if self.error:
                self.recover(NoneTerminal.nt_DECLARATIONS_FOLLOW)

        # ϵ
        else:
            pass
    def type(self):
        """ implements the CFG

           type   ::=     standard_type
                  |        array [ num .. num ] of standard_type
        """
        current_token_code = self.get_token_code()

        # standard_type
        if current_token_code == TokenCode.tc_INTEGER or current_token_code == TokenCode.tc_REAL:
            self.standard_type()

        # array
        elif current_token_code == TokenCode.tc_ARRAY:
            self.match(TokenCode.tc_ARRAY)

            # array [
            self.match(TokenCode.tc_LBRACK)

            if not self.error:
                # array [ num
                self.match(TokenCode.tc_NUMBER)

            if not self.error:
                # array [ num ..
                self.match(TokenCode.tc_DOTDOT)

            if not self.error:
                # array [ num .. num
                self.match(TokenCode.tc_NUMBER)

            if not self.error:
                # array [ num .. num ]
                self.match(TokenCode.tc_RBRACK)

            if not self.error:
                # array [ num .. num ] of
                self.match(TokenCode.tc_OF)

            # if we had had error in last function we try to recover
            if self.error:
                self.recover(NoneTerminal.nt_STANDARD_TYPE_FIRST)

            # array [ num .. num ] of standard_type
            self.standard_type()

            # if we had had error in last function we try to recover
            if self.error:
                self.recover(NoneTerminal.nt_STANDARD_TYPE_FOLLOW)

        # error
        else:
            self.match(TokenCode.tc_TYPE)
    def standard_type(self):
        """ implements the CFG

           standard_type   ::=     integer
                           |       real
        """
        current_token_code = self.get_token_code()

        # integer
        if current_token_code == TokenCode.tc_INTEGER:
            self.match(TokenCode.tc_INTEGER)

        # real
        elif current_token_code == TokenCode.tc_REAL:
            self.match(TokenCode.tc_REAL)

        # error
        else:
            self.match(TokenCode.tc_STANDARD_TYPE)
    def subprogram_declarations(self):
        """ implements the CFG

           subprogram_declarations     ::=     subprogram_declaration ; subprogram_declarations
                                       |       ϵ
        """
        current_token_code = self.get_token_code()

        # subprogram_declaration
        if current_token_code == TokenCode.tc_FUNCTION or current_token_code == TokenCode.tc_PROCEDURE:
            self.subprogram_declaration()

            # if we had had error in last function we try to recover
            if self.error:
                self.recover(NoneTerminal.nt_SUBPROGRAM_DECLARATION_FOLLOW)

            # subprogram_declaration ;
            self.match(TokenCode.tc_SEMICOL)
            self.code.generate(CodeOp.cd_RETURN, None, None, None)

            # if we had had error in last function we try to recover
            if self.error:
                self.recover(NoneTerminal.nt_SUBPROGRAM_DECLARATIONS_FIRST)

            # subprogram_declaration ; subprogram_declarations
            self.subprogram_declarations()

            # if we had had error in last function we try to recover
            if self.error:
                self.recover(NoneTerminal.nt_SUBPROGRAM_DECLARATIONS_FOLLOW)

        # ϵ
        else:
            pass
    def subprogram_declaration(self):
        """ implements the CFG

           subprogram_declaration      ::=     subprogram_head declarations compound_statement
        """
        # subprogram_head
        self.subprogram_head()

        # if we had had error in last function we try to recover
        if self.error:
            self.recover(NoneTerminal.nt_SUBPROGRAM_HEAD_FOLLOW)

        # subprogram_head declarations
        self.declarations()

        # if we had had error in last function we try to recover
        if self.error:
            self.recover(NoneTerminal.nt_DECLARATIONS_FOLLOW)

        # subprogram_head declarations compound_statement
        self.compound_statement()

        # if we had had error in last function we try to recover
        if self.error:
            self.recover(NoneTerminal.nt_COMPOUND_STATEMENT_FOLLOW)
    def subprogram_head(self):
        """ implements the CFG

           subprogram_head     ::=     function id arguments : standard_type
                               |       procedure id arguments ;
        """
        current_token_code = self.get_token_code()

        # function
        if current_token_code == TokenCode.tc_FUNCTION:
            self.match(TokenCode.tc_FUNCTION)

            # function id
            entry = self.token.symbol_table_entry
            self.code.generate(CodeOp.cd_LABEL, None, None, entry)
            self.match(TokenCode.tc_ID)

            # if we had had error in last function we try to recover
            if self.error:
                self.recover(NoneTerminal.nt_ARGUMENTS_FIRST)

            # function id arguments
            self.arguments()

            # if we had had error in last function we try to recover
            if self.error:
                self.recover(NoneTerminal.nt_ARGUMENTS_FOLLOW)

            # function id arguments :
            self.match(TokenCode.tc_COLON)

            # if we had had error in last function we try to recover
            if self.error:
                self.recover(NoneTerminal.nt_STANDARD_TYPE_FIRST)

            # function id arguments : standard_type
            self.standard_type()

            # if we had had error in last function we try to recover
            if self.error:
                self.recover(NoneTerminal.nt_STANDARD_TYPE_FOLLOW)

            # function id arguments : standard_type ;
            self.match(TokenCode.tc_SEMICOL)

        # procedure
        elif current_token_code == TokenCode.tc_PROCEDURE:
            self.match(TokenCode.tc_PROCEDURE)

            # procedure id
            entry = self.token.symbol_table_entry
            self.code.generate(CodeOp.cd_LABEL, None, None, entry)
            self.match(TokenCode.tc_ID)

            # if we had had error in last function we try to recover
            if self.error:
                self.recover(NoneTerminal.nt_ARGUMENTS_FIRST)

            # procedure id arguments
            self.arguments()

            # if we had had error in last function we try to recover
            if self.error:
                self.recover(NoneTerminal.nt_ARGUMENTS_FOLLOW)

            # procedure id arguments ;
            self.match(TokenCode.tc_SEMICOL)

        # error
        else:
            self.match(TokenCode.tc_SUBPROGRAM_HEAD)
    def arguments(self):
        """ implements the CFG

           arguments   ::=     ( parameter_list )
                        |      ϵ
        """
        current_token_code = self.get_token_code()

        # (
        if current_token_code == TokenCode.tc_LPAREN:
            self.match(TokenCode.tc_LPAREN)

            # ( parameter_list
            self.parameter_list()

            # if we had had error in last function we try to recover
            if self.error:
                self.recover(NoneTerminal.nt_PARAMETER_LIST_FOLLOW)

            # ( parameter_list )
            self.match(TokenCode.tc_RPAREN)

        # ϵ
        else:
            pass
    def parameter_list(self):
        """ implements the CFG

           parameter_list      ::=     identifier_list : type parameter_list_marked
        """
        # identifier_list
        entry_list = []
        self.identifier_list(entry_list)
        for e in entry_list:
            self.code.generate(CodeOp.cd_FPARAM, None, None, e)

        # if we had had error in last function we try to recover
        if self.error:
            self.recover(NoneTerminal.nt_IDENTIFIER_LIST_FOLLOW)

        # identifier_list :
        self.match(TokenCode.tc_COLON)

        # if we had had error in last function we try to recover
        if self.error:
            self.recover(NoneTerminal.nt_TYPE_FIRST)

        # identifier_list : type
        self.type()

        # if we had had error in last function we try to recover
        if self.error:
            self.recover(NoneTerminal.nt_TYPE_FOLLOW)

        # identifier_list : type parameter_list_marked
        self.parameter_list_marked()

        # if we had had error in last function we try to recover
        if self.error:
            self.recover(NoneTerminal.nt_PARAMETER_LIST_FOLLOW)
    def parameter_list_marked(self):
        """ implements the CFG

           parameter_list_marked   ::=     ; identifier_list : type parameter_list_marked
                                   |       ϵ
        """
        current_token_code = self.get_token_code()

        # ;
        if current_token_code == TokenCode.tc_SEMICOL:
            self.match(TokenCode.tc_SEMICOL)

            # ; identifier_list
            entry_list = []
            self.identifier_list(entry_list)
            for e in entry_list:
                self.code.generate(CodeOp.cd_FPARAM, None, None, e)

            # if we had had error in last function we try to recover
            if self.error:
                self.recover(NoneTerminal.nt_IDENTIFIER_LIST_FOLLOW)

            # ; identifier_list :
            self.match(TokenCode.tc_COLON)

            # if we had had error in last function we try to recover
            if self.error:
                self.recover(NoneTerminal.nt_TYPE_FIRST)

            # ; identifier_list : type
            self.type()

            # if we had had error in last function we try to recover
            if self.error:
                self.recover(NoneTerminal.nt_TYPE_FOLLOW)

            # ; identifier_list : type parameter_list_marked
            self.parameter_list_marked()

            # if we had had error in last function we try to recover
            if self.error:
                self.recover(NoneTerminal.nt_PARAMETER_LIST_FOLLOW)

        # ϵ
        pass
    def compound_statement(self):
        """ implements the CFG

           compound_statement  ::=     begin optional_statement end
        """
        # begin
        self.match(TokenCode.tc_BEGIN)

        # if we had had error in last function we try to recover
        if self.error:
            self.recover(NoneTerminal.nt_OPTIONAL_STATEMENT_FIRST)

        # begin optional_statement
        self.optional_statement()

        # if we had had error in last function we try to recover
        if self.error:
            self.recover(NoneTerminal.nt_OPTIONAL_STATEMENT_FOLLOW)

        # begin optional_statement end
        self.match(TokenCode.tc_END)
    def optional_statement(self):
        """ implements the CFG

           optional_statement   ::=     statement_list
                               |       ϵ
        """
        self.statement_list()

        # if we had had error in last function we try to recover
        if self.error:
            self.recover(NoneTerminal.nt_STATEMENT_LIST_FOLLOW)
    def statement_list(self):
        """ implements the CFG

           statement_list   ::=     statement statement_list_marked
        """
        # statement
        self.statement()

        # if we had had error in last function we try to recover
        if self.error:
            self.recover(NoneTerminal.nt_STATEMENT_FOLLOW)


        self.statement_list_marked()

        # if we had had error in last function we try to recover
        if self.error:
            self.recover(NoneTerminal.nt_STATEMENT_LIST_MARKED_FOLLOW)
    def statement_list_marked(self):
        """ implements the CFG

           statement_list_marked   ::=     ; statement statement_list_marked
                                   |       ϵ
        """
        current_token_code = self.get_token_code()

        # ;
        if current_token_code == TokenCode.tc_SEMICOL:
            self.match(TokenCode.tc_SEMICOL)

            # ; statement
            self.statement()

            # if we had had error in last function we try to recover
            if self.error:
                self.recover(NoneTerminal.nt_STATEMENT_FOLLOW)

            # ; statement statement_list_marked
            self.statement_list_marked()

            # if we had had error in last function we try to recover
            if self.error:
                self.recover(NoneTerminal.nt_STATEMENT_LIST_MARKED_FOLLOW)
        # ϵ
        else:
            pass
    def statement(self):
        """ inplements the CFG

           statement   ::=     id statement_marked
                       |       compound_statement
                       |       if expression then statement else statement
                       |       while expression do statement
        """
        current_token_code = self.get_token_code()

        # id
        if current_token_code == TokenCode.tc_ID:
            entry = self.token.symbol_table_entry
            self.match(TokenCode.tc_ID)

            # id statement_marked
            result_entry = self.statement_marked(entry)

            # if we had had error in last function we try to recover
            if self.error:
                self.recover(NoneTerminal.nt_STATEMENT_MARKED_FOLLOW)

        # compound_statement
        elif current_token_code == TokenCode.tc_BEGIN:
            self.compound_statement()

            # if we had had error in last function we try to recover
            if self.error:
                self.recover(NoneTerminal.nt_COMPOUND_STATEMENT_FOLLOW)

        # if
        elif current_token_code == TokenCode.tc_IF:
            self.match(TokenCode.tc_IF)

            # if expression
            next = self.new_label()
            false = self.new_label()
            expression = self.expression()
            false_entry = self.scanner.symbol_table.lookup("0")
            self.code.generate(CodeOp.cd_EQ, expression, false_entry, false)

            # if we had had error in last function we try to recover
            if self.error:
                self.recover(NoneTerminal.nt_EXPRESSION_FOLLOW)

            # if expression then
            self.match(TokenCode.tc_THEN)

            # if we had had error in last function we try to recover
            if self.error:
                self.recover(NoneTerminal.nt_STATEMENT_FIRST)

            # if expression then statement
            self.statement()
            self.code.generate(CodeOp.cd_GOTO, None, None, next)
            self.code.generate(CodeOp.cd_LABEL, None, None, false)

            # if we had had error in last function we try to recover
            if self.error:
                self.recover(NoneTerminal.nt_STATEMENT_FOLLOW)

            # if expression then statement else
            self.match(TokenCode.tc_ELSE)

            # if we had had error in last function we try to recover
            if self.error:
                self.recover(NoneTerminal.nt_STATEMENT_FIRST)

            # if expression then statement else statement
            self.statement()
            self.code.generate(CodeOp.cd_LABEL, None, None, next)

            # if we had had error in last function we try to recover
            if self.error:
                self.recover(NoneTerminal.nt_STATEMENT_FOLLOW)

        # while
        elif current_token_code == TokenCode.tc_WHILE:
            self.match(TokenCode.tc_WHILE)

            # while expression
            begin = self.new_label()
            next = self.new_label()
            false_entry = self.scanner.symbol_table.lookup("0")
            self.code.generate(CodeOp.cd_LABEL, None, None, begin)
            expression = self.expression()
            self.code.generate(CodeOp.cd_EQ, expression, false_entry, next)

            # if we had had error in last function we try to recover
            if self.error:
                self.recover(NoneTerminal.nt_EXPRESSION_FOLLOW)

            # while expression do
            self.match(TokenCode.tc_DO)

            # if we had had error in last function we try to recover
            if self.error:
                self.recover(NoneTerminal.nt_STATEMENT_FIRST)

            # while expression do statement
            self.statement()

            self.code.generate(CodeOp.cd_GOTO, None, None, begin)
            self.code.generate(CodeOp.cd_LABEL, None, None, next)

            # if we had had error in last function we try to recover
            if self.error:
                self.recover(NoneTerminal.nt_STATEMENT_FOLLOW)

        # error
        else:
            self.match(TokenCode.tc_STATEMENT)
    def statement_marked(self, entry):
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
                self.recover(NoneTerminal.nt_EXPRESSION_FOLLOW)

            # [ expression ]
            self.match(TokenCode.tc_RBRACK)

            if not self.error:

                # [ expression ] assignop
                self.match(TokenCode.tc_ASSIGNOP)

            # if we had had error in last function we try to recover
            if self.error:
                self.recover(NoneTerminal.nt_EXPRESSION_FIRST)

            # [ expression ] assignop expression
            self.expression()

            # if we had had error in last function we try to recover
            if self.error:
                self.recover(NoneTerminal.nt_EXPRESSION_FOLLOW)

        # :=
        elif current_token_code == TokenCode.tc_ASSIGNOP:
            self.match(TokenCode.tc_ASSIGNOP)

            # := expression
            result_entry = self.expression()

            self.code.generate(CodeOp.cd_ASSIGN, result_entry, None, entry)

            # if we had had error in last function we try to recover
            if self.error:
                self.recover(NoneTerminal.nt_EXPRESSION_FOLLOW)

        # (
        elif current_token_code == TokenCode.tc_LPAREN:
            self.match(TokenCode.tc_LPAREN)

            # ( expression_list
            entry_list = []
            self.expression_list(entry_list)
            for e in entry_list:
                self.code.generate(CodeOp.cd_APARAM, None, None, e)
            self.code.generate(CodeOp.cd_CALL, entry, None, None)

            # if we had had error in last function we try to recover
            if self.error:
                self.recover(NoneTerminal.nt_EXPRESSION_LIST_FOLLOW)

            # ( expression_list )
            self.match(TokenCode.tc_RPAREN)

        # ϵ
        else:
            pass
    def expression_list(self, entry_list=None):
        """ implements the CFG

           expression_list     ::=     expression expression_list_marked
        """
        # expression
        entry = self.expression()
        if not entry_list == None:
            entry_list.append(entry)


        # if we had had error in last function we try to recover
        if self.error:
            self.recover(NoneTerminal.nt_EXPRESSION_FOLLOW)

        self.expression_list_marked(entry_list)

        # if we had had error in last function we try to recover
        if self.error:
            self.recover(NoneTerminal.nt_EXPRESSION_LIST_MARKED_FOLLOW)
    def expression_list_marked(self, entry_list):
        """ inplements the CFG

           expression_list_marked      ::=     , expression expression_list_marked
                                       |       ϵ
        """
        current_token_code = self.get_token_code()

        # ,
        if current_token_code == TokenCode.tc_COMMA:
            self.match(TokenCode.tc_COMMA)

            # , expression
            entry = self.expression()
            if not entry_list == None:
                entry_list.append(entry)

            # if we had had error in last function we try to recover
            if self.error:
                self.recover(NoneTerminal.nt_EXPRESSION_FOLLOW)

            # , expression expression_list_marked
            self.expression_list_marked(entry_list)

            # if we had had error in last function we try to recover
            if self.error:
                self.recover(NoneTerminal.nt_EXPRESSION_LIST_MARKED_FOLLOW)

        # ϵ
        else:
            pass
    def expression(self):
        """ implements the CFG

           expression      ::=     simple_expression1 expression_marked
        """
        # simple_expression
        entry = self.simple_expression()

        # if we had had error in last function we try to recover
        if self.error:
            self.recover(NoneTerminal.nt_SIMPLE_EXPRESSION_FOLLOW)

        # simple_expression expression_marked
        result_entry = self.expression_marked(entry)

        # if we had had error in last function we try to recover
        if self.error:
            self.recover(NoneTerminal.nt_EXPRESSION_MARKED_FOLLOW)

        return result_entry
    def expression_marked(self, entry):
        """ implements the CFG

           expression_marked   ;;=     relop simple_expression1
                               |       ϵ
        """
        current_token_code = self.get_token_code()

        # relop
        if current_token_code == TokenCode.tc_RELOP:
            op = self.convert_optype_to_opcode(self.get_op_type())
            self.match(TokenCode.tc_RELOP)

            # relop simple_expression
            entry2 = self.simple_expression()
            result_entry = self.new_temp()
            true = self.new_label()
            next = self.new_label()
            false_entry = self.scanner.symbol_table.lookup("0")
            true_entry = self.scanner.symbol_table.lookup("1")
            self.code.generate(op,entry, entry2, true)
            self.code.generate(CodeOp.cd_ASSIGN,false_entry, None, result_entry)
            self.code.generate(CodeOp.cd_GOTO, None, None, next)
            self.code.generate(CodeOp.cd_LABEL, None, None, true)
            self.code.generate(CodeOp.cd_ASSIGN, true_entry, None, result_entry)
            self.code.generate(CodeOp.cd_LABEL, None, None, next)

            # if we had had error in last function we try to recover
            if self.error:
                self.recover(NoneTerminal.nt_SIMPLE_EXPRESSION_FOLLOW)

        # ϵ
        else:
            result_entry = entry

        return result_entry
    def simple_expression(self):
        """ implements the CFG

           simple_expresson    ::=     term simple_expression_marked
                               |       sign term simple_expression_marked
        """
        current_token_code = self.get_token_code()
        result_entry = None

        # sign
        if current_token_code == TokenCode.tc_ADDOP:
            self.sign()

            # if we had had error in last function we try to recover
            if self.error:
                self.recover(NoneTerminal.nt_SIGN_FOLLOW)

            # sign term
            entry = self.term()
            new_temp = self.new_temp()
            self.code.generate(CodeOp.cd_UMINUS, entry, None, new_temp)

            # if we had had error in last function we try to recover
            if self.error:
                self.recover(NoneTerminal.nt_TERM_FOLLOW)

            # sign term simple_expression_marked
            result_entry = self.simple_expression_marked(new_temp)

            # if we had had error in last function we try to recover
            if self.error:
                self.recover(NoneTerminal.nt_SIMPLE_EXPRESSION_MARKED_FOLLOW)

        # term
        elif current_token_code == TokenCode.tc_ID or\
             current_token_code == TokenCode.tc_NUMBER or\
             current_token_code == TokenCode.tc_LPAREN or\
             current_token_code == TokenCode.tc_NOT:

            entry = self.term()

            # if we had had error in last function we try to recover
            if self.error:
                self.recover(NoneTerminal.nt_TERM_FOLLOW)

            # term simple_expression_marked
            result_entry = self.simple_expression_marked(entry)

            # if we had had error in last function we try to recover
            if self.error:
                self.recover(NoneTerminal.nt_SIMPLE_EXPRESSION_MARKED_FOLLOW)

        # error
        else:
            self.match(TokenCode.tc_SIMPLE_EXPRESSION)

        return result_entry
    def simple_expression_marked(self, entry):
        """ implements the CFG

           simple_expression_marked    ::=     addop term simple_expression_marked
                                       |       ϵ

        return true if input is according to grammar, false otherwise
        """
        current_token_code = self.get_token_code()
        result_entry = None

        # addop
        if current_token_code == TokenCode.tc_ADDOP:
            op =  self.convert_optype_to_opcode(self.get_op_type())
            self.match(TokenCode.tc_ADDOP)

            # addop term
            entry2 = self.term()
            new_temp = self.new_temp()
            self.code.generate(op, entry, entry2, new_temp)

            # if we had had error in last function we try to recover
            if self.error:
                self.recover(NoneTerminal.nt_TERM_FOLLOW)

            # addop term simple_expression_marked
            result_entry =  self.simple_expression_marked(new_temp)

            # if we had had error in last function we try to recover
            if self.error:
                self.recover(NoneTerminal.nt_SIMPLE_EXPRESSION_MARKED_FOLLOW)

        # ϵ
        else:
            result_entry = entry

        return result_entry
    def term(self):
        """ implements the CFG

           term    ::=     factor term_marked
        """
        # factor
        entry = self.factor()

        # if we had had error in last function we try to recover
        if self.error:
            self.recover(NoneTerminal.nt_FACTOR_FOLLOW)

        # factor term_marked
        result_entry = self.term_marked(entry)

        # if we had had error in last function we try to recover
        if self.error:
            self.recover(NoneTerminal.nt_TERM_MARKED_FOLLOW)

        return result_entry
    def term_marked(self, entry):
        """ implements the CFG

           term_marked    ::=     mulop factor factor term_marked
                           |      ϵ
        """
        current_token_code = self.get_token_code()

        # mulop
        if current_token_code == TokenCode.tc_MULOP:
            op = self.convert_optype_to_opcode(self.get_op_type())
            self.match(TokenCode.tc_MULOP)

            # mulop factor
            entry2 = self.factor()
            new_temp = self.new_temp()
            self.code.generate(op, entry, entry2, new_temp)

            # if we had had error in last function we try to recover
            if self.error:
                self.recover(NoneTerminal.nt_FACTOR_FOLLOW)

            # mulop factor term_marked
            result_entry = self.term_marked(new_temp)

            # if we had had error in last function we try to recover
            if self.error:
                self.recover(NoneTerminal.nt_TERM_MARKED_FOLLOW)

        # ϵ
        else:
            result_entry = entry
        return result_entry
    def factor(self):
        """ implements the CFG

           factor  ::=     id factor_marked
                   |       num
                   |       ( expression )
                   |       not factor

        return true if input is according to grammar, false otherwise
        """
        current_token_code = self.get_token_code()
        result_entry = None

        # id
        if current_token_code == TokenCode.tc_ID:
            entry = self.token.symbol_table_entry
            self.match(TokenCode.tc_ID)

            # id factor_marked
            result_entry = self.factor_marked(entry)

            # if we had had error in last function we try to recover
            if self.error:
                self.recover(NoneTerminal.nt_FACTOR_MARKED_FOLLOW)

        # num
        elif current_token_code == TokenCode.tc_NUMBER:
            result_entry = self.token.symbol_table_entry
            self.match(TokenCode.tc_NUMBER)
            return result_entry

        # (
        elif current_token_code == TokenCode.tc_LPAREN:
            self.match(TokenCode.tc_LPAREN)

            # ( expression
            result_entry = self.expression()

            # if we had had error in last function we try to recover
            if self.error:
                self.recover(NoneTerminal.nt_EXPRESSION_FOLLOW)

            # ( expression )
            self.match(TokenCode.tc_RPAREN)

        # not
        elif current_token_code == TokenCode.tc_NOT:
            self.match(TokenCode.tc_NOT)

            # not factor
            entry = self.factor()
            result_entry = self.new_temp()
            self.code.generate(CodeOp.cd_NOT, entry, None, result_entry)

            # if we had had error in last function we try to recover
            if self.error:
                self.recover(NoneTerminal.nt_FACTOR_FOLLOW)

        # error
        else:
            self.match(TokenCode.tc_FACTOR)
        return result_entry
    def factor_marked(self, entry):
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
            entry_list = []
            self.expression_list(entry_list)
            for e in entry_list:
                self.code.generate(CodeOp.cd_APARAM, None, None, e)
            self.code.generate(CodeOp.cd_CALL, entry, None, None)

            if self.error:
                self.recover(NoneTerminal.nt_EXPRESSION_LIST_FOLLOW)

            # ( expression_list )
            self.match(TokenCode.tc_RPAREN)
            result_entry = entry

        # [
        elif current_token_code == TokenCode.tc_LBRACK:
            self.match(TokenCode.tc_LBRACK)

            # [ expression
            result_entry = self.expression()

            # if we had had error in last function we try to recover
            if self.error:
                self.recover(NoneTerminal.nt_EXPRESSION_FOLLOW)

            # [ expression ]
            self.match(TokenCode.tc_RBRACK)

        # ϵ
        else:
            result_entry = entry
        return result_entry
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
    def testProgramCorrect(self):
        self.filename = "pas_syntax_ok"
        self.parser = PascalParser("test_files/"+self.filename)
        self.parser.program()
        print self.parser

    def testProgramError(self):
        self.filename = "pas_syntax_err"
        self.parser = PascalParser("test_files/"+self.filename)
        self.parser.program()
        print self.parser

    def testProgramCode(self):
        self.filename = "code"
        self.parser = PascalParser("test_files/"+self.filename)
        self.parser.program()
        print self.parser

    def testProgramCodeIf(self):
        self.filename = "pas_code_if"
        self.parser = PascalParser("test_files/"+self.filename)
        self.parser.program()
        print self.parser

    def testProgramCodeWhile(self):
        self.filename = "pas_code_while"
        self.parser = PascalParser("test_files/"+self.filename)
        self.parser.program()
        print self.parser

    def testProgramCodeAnd(self):
        self.filename = "pas_code_and"
        self.parser = PascalParser("test_files/"+self.filename)
        self.parser.program()
        print self.parser

    def testProgramCodeFact(self):
        self.filename = "pas_code_fact"
        self.parser = PascalParser("test_files/"+self.filename)
        self.parser.program()
        print self.parser

    def testProgramCodeFunc(self):
        self.filename = "pas_code_func"
        self.parser = PascalParser("test_files/"+self.filename)
        self.parser.program()
        print self.parser

    def print_out(self):
        self.parser.code.print_out(self.filename)
