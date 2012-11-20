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
            print str(self.lineNr) + ': ' + self.line
            for error in self.errors:
                print error
            self.lineNr = token.line
            self.line = token.str + " "
            self.errors = []
        else:
            self.line += token.str + " "

    def addError(self, error):
        error.rjust()
        self.errors.append(error)

    def addError(self, error, spaces):
        for i in range(spaces+4):
            error = " " + error
        self.errors.append(error)