# -*- coding: utf-8 -*-
__author__ = 'Palli'

import PascalParser


#test sign
def testSign():
    filename = "test_files/sign"
    parser = PascalParser.PascalParser(filename)
    sign = parser.sign()
    if not sign[0]:
        print "sign error"
        print sign[1]

def testType():
    filename = "test_files/type"
    parser = PascalParser.PascalParser(filename)
    sign = parser.type()
    if not sign[0]:
        print "sign error"
        print sign[1]

def testProgramCorrect():
    filename = "test_files/pas_syntax_ok"
    parser = PascalParser.PascalParser(filename)
    sign = parser.program()
    if not sign[0]:
        print "sign error"
        print sign[1]

def testProgramError():
    filename = "test_files/pas_syntax_err"
    parser = PascalParser.PascalParser(filename)
    sign = parser.program()
    if not sign[0]:
        print "sign error"
        print sign[1]


#testSign()
#testType()
#testProgramCorrect()
testProgramError()