from Grammar import Grammar


class Parser:
    def __init__(self, grammar):
        self.grammar = grammar
        self.states = []

    def goto(self, production):
        pass

    def closure(self, production):
        pass

    def canonnicalCollection(self):
        pass


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
                pass
            else:
                break


gr = Grammar("Data/g1.in")
g = Parser(gr)
g.run()
