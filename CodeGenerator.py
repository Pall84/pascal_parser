# -*- coding: utf-8 -*-
__author__ = 'palleymundsson'
from Lexical import SymbolTableEntry

# CodeOp m op; /* operator */
# SymbolTableEntry* m arg1; /* arg1 is in symbol table */
# SymbolTableEntry* m arg2; /* arg2 is in symbol table */
# SymbolTableEntry* m result;/* result is in symbol table */

class Quadruple:
    def __init__(self, op="", arg1="", arg2="", result=""):
        self.op = op
        self.arg1 = arg1
        self.arg2 = arg2
        self.result = result

class QuadrupleList():
    def __init__(self):
        self.quadruple_list = []

class Code:
    def __init__(self):
        self.temp_index = 1
        self.label_index = 1
        self.quadrople_list = []

    def new_temp(self):
        temp = 't%i' % self.temp_index
        symbol_table_entry = SymbolTableEntry()
        symbol_table_entry.lexeme = temp
        self.temp_index += 1
        return symbol_table_entry

    def new_label(self):
        label = 't%i' % self.label_index
        symbol_table_entry = SymbolTableEntry()
        symbol_table_entry.lexeme = label
        self.temp_index += 1
        return symbol_table_entry

    def generate(self, op, arg1, arg2, result):
        quadruple = Quadruple(op, arg1, arg2, result)
        self.quadrople_list.append(quadruple)

    def __str__(self):
        buffer = "Op".rjust(10) + "Arg1".rjust(10) + "Arg2".rjust(10) + "Result".rjust(10) + "\n"
        for q in self.quadrople_list:
            buffer += str(q.op).rjust(10) + str(q.arg1).rjust(10) + str(q.arg2).rjust(10) + str(q.result).rjust(10) + "\n"

        return buffer
