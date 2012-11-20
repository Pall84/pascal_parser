__author__ = 'Palli'

import TokenCode
import DataType
import OpType

class Token:
    def __init__(self, token_code, data_type, op_type, line, col, str):
        self.token_code = token_code
        self.data_type = data_type
        self.op_type = op_type
        self.line = line
        self.col = col
        self.str = str