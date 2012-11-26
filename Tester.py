__author__ = 'Palli'

from Lexical import PascalScannerTester
from Parser import  PascalParserTester

#lex_tester = PascalScannerTester()

tester = PascalParserTester()

tester.testProgramCorrect()
tester.print_out()

#tester.testProgramError()

tester.testProgramCodeIf()
tester.print_out()

tester.testProgramCodeWhile()
tester.print_out()

tester.testProgramCodeAnd()
tester.print_out()

tester.testProgramCodeFact()
tester.print_out()

tester.testProgramCodeFunc()
tester.print_out()

