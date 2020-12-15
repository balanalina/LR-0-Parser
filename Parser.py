from Grammar import Grammar


class Parser:
    def __init__(self, grammar):
        self.grammar = grammar
        self.states = []
        self.C = []
        self.table = {}

    def goto(self, state, symbol_index):
        if symbol_index == -1:
            return []
        symbol = state[symbol_index]
        if state[symbol_index - 1] != '.' and state[len(state) - 1] is not '.':
            return []
        if state[symbol_index - 1] is '.':
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
        if len(state) == 1 and state[0][len(state[0]) - 1] is '.':
            return [production]
        return state

    def ColCan(self):
        s0 = self.closure(self.grammar.get_initial_state() + "'->." + self.grammar.get_initial_state())
        self.C.append(s0)
        while True:
            isChanged = False
            for state in self.C:
                for i in state:
                    for ind in range(len(i.split("->")[1])):
                        index = ind + len(i.split("->")[0]) + 2
                        if i[index] is not '.':
                            if self.goto(i, index):
                                if self.goto(i, index) not in self.C:
                                    self.C.append(self.goto(i, index))
                                    isChanged = True
            if not isChanged:
                self.print_C()
                self.createTable()
                break

    def checkReduce(self, s, i):
        s = s[1]
        state = self.C[int(s)][0]
        state = state.replace('.','')
        index = self.grammar.get_reduce_states().index(state)
        if index == 0:
            self.table[(i, "action")] = "accept"
        else:
            self.table[(i,"action")] = "reduce"+str(index)


    def createTable(self):
        for i in range(0, len(self.C)):
            self.table[(i, "action")] = None
        for state in self.C:
            for i in state:
                for ind in range(len(i.split("->")[1])):
                    index = ind + len(i.split("->")[0]) + 2
                    if i[index] is not '.':
                        if self.goto(i, index):
                            self.table[tuple((self.C.index(state), i[index]))] = "s" + str(
                                self.C.index(self.goto(i, index)))
                        else:
                            self.table[tuple((self.C.index(state), i[index]))] = None  # self.goto(i, index)
        for i in range(0, len(self.C)):
            resulting_states = []
            for j in self.table.keys():
                if j[0] == i and j[1] != "action":
                    resulting_states.append(self.table[j])
            for check in resulting_states:
                if "s" + str(i) != check:
                    self.table[(i, "action")] = "shift"
                    break
            if self.table[(i, "action")] != "shift":
                if resulting_states.count(resulting_states[0]) == len(resulting_states):
                    # self.table[(i, "action")] = "reduce"
                    self.checkReduce(resulting_states[0],i)
                    for j in self.table.keys():
                        if j[0] == i and j[1] != "action":
                            self.table[j] = None
        for i in range(0, len(self.C)):
            if self.table[(i, "action")] is None:
                self.table[(i, "action")] == "error"

    def print_C(self):
        for state in self.C:
            s = "s" + str(self.C.index(state)) + "={ "
            for i in state:
                s += "\n" + i

            print(s + " }\n")

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
                print(self.table)
            else:
                break


gr = Grammar("Data/g1.in")
g = Parser(gr)
g.run()
