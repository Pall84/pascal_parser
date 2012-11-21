# -*- coding: utf-8 -*-
__author__ = 'Palli'

import Token


class SourceLine:
    def __init__(self):
        self.line = ""
        self.lineNr = 1
        self.errors = []

    def addToken(self, token ):
        if token.line > self.lineNr:
            print (str(self.lineNr).rjust(3) + ': ' + self.line).strip('\n')
            for error in self.errors:
                print error
            self.lineNr = token.line
            for i in range(token.col-1):
                token.str = " " + token.str
            self.line = token.str
            self.errors = []
        else:
            #print '%s : %s' %(len(self.line), token.col)
            for i in range(token.col- len(self.line)):
                token.str = " " + token.str

            self.line += token.str

    def printing(self):
        print (str(self.lineNr).rjust(3) + ': ' + self.line).strip('\n')
        for error in self.errors:
            print error

    def addError(self, error):
        error.rjust()
        self.errors.append(error)
        for error in self.errors:
            print error

    def addError(self, error, spaces):
        for i in range(spaces+5):
            error = " " + error
        self.errors.append(error)