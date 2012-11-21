__author__ = 'Palli'

class SymbolTable:
    def __init__(self):
        self.symbolTableEntries = []

    def insert(self, lexeme):
        if not self.lookup(lexeme):
            symbol_table_entry = SymbolTableEntry
            symbol_table_entry.lexeme = lexeme
            self.symbolTableEntries.append(symbol_table_entry)
            return symbol_table_entry
        return None

    def lookup(self, lexeme):
        for symbol_table_entry in self.symbolTableEntries:
            if symbol_table_entry.lexeme == lexeme:
                return symbol_table_entry

        return None



class SymbolTableEntry:
    def __init__(self):
        self.lexeme = None