# metoda de ordonare a tranzitiei pt backtracking
# BFS are nevoie de celelalte stari vizitate -> instanta cat mai mica
# nu stiu daca are solutii -> m si n au divizor comun k



# (c1, c2, m, n, k) unde:

# c1 - cati litri sunt la un anumit moment in paharul c1
# c2 - cati litri sunt la un anumit moment in paharul c2
# m - nr maxim de litri ce poate tine paharul c1
# n - nr maxim de litri ce poate tine paharul c2
# k - numarul de litri la care dorim sa ajungem in unul din pahare


# c1, c2, m, n, k
# tranzitii valide

# c1 -> 0 - golesc primul pahar
# c2 -> 0 - golesc al 2-lea pahar

# c1 -> m - c1, daca c2 >= m - c1
# c1 +> c1 + c2, daca c2 < m - c1

# c2 -> n - c2, daca c1 >= n - c2
# c2 -> n - c2, daca c2 < n - c2

# starea initiala: (0, 0, m, n, k)
# starea finala: (c1, c2, m, n, k), unde c1 == k sau c2 == k

class Lab2Problem:
    def initialize(self, m, n, k):
        return [0, 0, m, n, k]

    def isFinal(self, state):
        if state[0] == state[4] or state[1] == state[4]:
            return True
        return False

    def validate(self, state, c1, c2):
        #hello
        print("HELLO")

    def isPossible(self, state):
        print("TODO")


