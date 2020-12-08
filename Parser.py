from Grammar import Grammar


class Parser:
    def __init__(self, grammar):
        self.grammar = grammar
        self.states = []
        self.C = []

    def goto(self, state, symbol):
        sym_index = state.split("->")[1].find(symbol) + len(state.split("->")[0]) + 2
        if state[sym_index - 1] is '.':
            state = state.replace('.', '')
            state = state.replace(symbol, symbol + '.')
            if state[1] is '.':
                state = state.replace('.', '', 1)
        return self.closure(state)

    def closure(self, production):
        state = [production]
        point_index = production.find('.')
        if point_index != len(production) - 1:
            symbol = production[point_index + 1]
            if symbol in self.grammar.get_non_terminals():
                for i in self.grammar.get_production()[symbol]:
                    state.append(symbol + "->." + i)
        if state[len(state) - 1] is '.':
            return []
        return state

    def ColCan(self):
        s0 = self.closure(self.grammar.get_initial_state() + "'->." + self.grammar.get_initial_state())
        self.C.append(s0)
        while True:
            isChanged = False
            for state in self.C:
                for i in state:
                    for symbol in i.split("->")[1]:
                        if symbol is not '.':
                            if self.goto(i, symbol) is not []:
                                if self.unique_state(state, self.goto(i, symbol)):
                                    self.C.append(self.goto(i, symbol))
                                    isChanged = True
            if not isChanged:
                self.print_C()
                break

    def unique_state(self, state, list):
        aux = False
        for x in list:
            for s in self.C:
                if x in s:
                    return False
        return True

    def print_C(self):
        for state in self.C:
            s = "s" + str(self.C.index(state)) + "= "
            for i in state:
                s += i + " , "
            print(s)

    def menu(self):
        s = "0. Exit \n"
        s += "1. Set of non_terminals \n"
        s += "2. Set of terminals \n"
        s += "3. Set of productions \n"
        s += "4. Production for a given non_terminal \n"
        s += "5. Parse \n"
        return s

    def run(self):
        while True:
            print(self.menu())
            print("Enter command: ")
            command = int(input())
            if command == 1:
                print(str(self.grammar.get_non_terminals()) + "\n")
            elif command == 2:
                print(str(self.grammar.get_terminals()) + "\n")
            elif command == 3:
                for key in self.grammar.production.keys():
                    prod = str(key) + " -> "
                    for value in self.grammar.production[key]:
                        prod += value + " | "
                    print(prod)
                print("\n")
            elif command == 4:
                print("Enter non-terminal: ")
                non_term = input()
                prod = non_term + " -> "
                for value in self.grammar.production[non_term]:
                    prod += value + " | "
                print(prod + "\n")
            elif command == 5:
                self.ColCan()
            else:
                break


gr = Grammar("Data/g1.in")
g = Parser(gr)
g.run()
