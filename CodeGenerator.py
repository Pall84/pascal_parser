# -*- coding: utf-8 -*-
__author__ = 'palleymundsson'
from Enums import *

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

    def __str__(self):
        buffer = ""
        self.label_before = False
        for q in self.quadrople_list:
            if q.op:
                if q.op == CodeOp.cd_LABEL:
                    buffer += (str(q.result)+":").rjust(10)
                    self.label_before = True
                elif self.label_before:
                    self.label_before = False
                    buffer += str(q.op).rjust(10)

                    if q.arg1:
                        buffer += str(q.arg1).rjust(10)
                    else:
                        buffer += " ".rjust(10)

                    if q.arg2:
                        buffer += str(q.arg2).rjust(10)
                    else:
                        buffer += " ".rjust(10)

                    if q.result:
                        buffer += str(q.result).rjust(10)
                    else:
                        buffer += " ".rjust(10)

                    buffer += "\n"
                else:
                    buffer += str(q.op).rjust(20)

                    if q.arg1:
                        buffer += str(q.arg1).rjust(10)
                    else:
                        buffer += " ".rjust(10)

                    if q.arg2:
                        buffer += str(q.arg2).rjust(10)
                    else:
                        buffer += " ".rjust(10)

                    if q.result:
                        buffer += str(q.result).rjust(10)
                    else:
                        buffer += " ".rjust(10)

                    buffer += "\n"

        return buffer

    def new_temp(self):
        """ generates new temporal variable. """
        temp = 't%i' % self.temp_index
        self.temp_index += 1
        return temp

    def new_label(self):
        """ generates new label. """
        label = 'lab%i' % self.label_index
        self.label_index += 1
        return label

    def generate(self, op, arg1, arg2, result):
        quadruple = Quadruple(op, arg1, arg2, result)
        self.quadrople_list.append(quadruple)

    def print_out(self, filename):
        file = open("output/"+filename, "w")
        file.write(self.__str__())
        file.close()


