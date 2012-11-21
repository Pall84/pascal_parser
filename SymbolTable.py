__author__ = 'Palli'

class SymbolTable:
    def __init__(self):
        self.symbolTableEntries = []
        self.insert(0)
        self.insert(1)

    def insert(self, lexeme):
        if not self.lookup(lexeme):
            symbol_table_entry = SymbolTableEntry()
            symbol_table_entry.lexeme = lexeme
            self.symbolTableEntries.append(symbol_table_entry)
            return symbol_table_entry
        return None

    def lookup(self, lexeme):
        for symbol_table_entry in self.symbolTableEntries:
            if symbol_table_entry.lexeme == lexeme:
                return symbol_table_entry

        return None

    def __str__(self):
        header = 'Entry'.rjust(6) + 'Lexeme'.rjust(15) + '\n'
        body = ""
        index = 0
        for entry in self.symbolTableEntries:
            body += str(index).rjust(6) + str(entry.lexeme).rjust(15) + '\n'
            index +=1

        return header + body




class SymbolTableEntry:
    def __init__(self):
        self.lexeme = None

