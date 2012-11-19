__author__ = 'palleymundsson'

from plex import *
import PascalLexer
import OpType

class PascalParser:
    def __init__(self):
        lexicon = PascalLexer.getLexer()

        filename = "test_files/pascal_lex1.txt"
        f = open(filename, "r")
        self.scanner = Scanner(lexicon, f, filename)
        self.token = self.scanner.read()


    def sign(self):
        if self.token[0][3] == OpType.op_PLUS:
            return True
        elif self.token[0]