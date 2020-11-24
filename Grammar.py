import os
import sys


class Grammar:
    def __init__(self, file_name):
        self.non_terminal = []
        self.terminal = []
        self.production = {}
        self.file = file_name
        self.read_grammar()

    def read_grammar(self):
        file = open(os.path.join(sys.path[0], self.file), 'r')
        file_content = []
        for line in file:
            # we don't need the new line or any spaces
            file_content.append(line.replace("\n", ""))
        self.non_terminal = file_content[0].split(',')
        self.terminal = file_content[1].split(',')
        for i in range(2, len(file_content)):
            symbol = file_content[i].split('->')[0]
            productions = file_content[i].split('->')[1]
            productions = productions.split("|")
            self.production[symbol] = productions


    def get_terminals(self):
        return self.terminal

    def get_non_terminals(self):
        return self.non_terminal

    def get_production(self):
        return self.production


# g = Grammar("Data/g1.in")
