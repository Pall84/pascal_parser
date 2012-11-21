# -*- coding: utf-8 -*-
__author__ = 'Palli'

import Token


class SourceLine:
    def __init__(self):
        self.line = ""
        self.lineNr = 1
        self.errors = []
        self.number_of_errors = 0

    def addToken(self, token ):
        word = token.str
        if token.line > self.lineNr:
            print (str(self.lineNr).rjust(3) + ': ' + self.line).strip('\n')
            for error in self.errors:
                print error
            self.lineNr = token.line
            for i in range(token.col-1):
                word = " " + word
            self.line = token.str
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
        print 'Number of errors: %i' %self.number_of_errors


    def addError(self, error, spaces):
        self.number_of_errors += 1
        for i in range(spaces+5):
            error = " " + error
        self.errors.append(error)