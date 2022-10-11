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

# starea initiala: (0, 0, m, n, k)
# starea finala: (c1, c2, m, n, k), unde c1 == k sau c2 == k


# tranzitii valide

# c1 -> 0 - golesc primul pahar, daca c1 > 0
# c2 -> 0 - golesc al 2-lea pahar, daca c2 > 0
# c1 -> c2:
# c2 = c2 + min(n-c2, c1), c1 = c1 - min(n-c2, c1), daca c1 > 0 si c2 != n

#       conditii: c1 > 0 si min > 0 ---- min(n-c2, c1) = cantitatea transferata
#               -> min > 0 => c1 > 0 (conditie preexistenta) si n-c2 > 0 => c2 < n => c2 != n

# c1 <- c2:
# c1 = c1 + min(m-c1, c2), c2 = c2 - min(m-c1, c2), daca c2 > 0 si c1 != m


class Lab2Problem:
    def initialize(self, m, n, k):
        return [0, 0, m, n, k]

    def isFinal(self, state):
        if state[0] == state[4] or state[1] == state[4]:
            return True
        return False

    def validate(self, state, reciever_position, giver_position):
        if reciever_position > 1 or giver_position > 1 or giver_position == reciever_position:
            print("Receiver position or giver position are invalid")
            return False
        if state[giver_position] == 0:  # giver doesn't have water
            return False
        if reciever_position < 0:  # giver is spilled on the floor
            return True

        receiver_current_quantity = state[reciever_position]
        receiver_max_quantity = state[reciever_position + 2]

        if receiver_max_quantity != receiver_current_quantity:
            return True

    def transition(self, state, reciever_position, giver_position):
        if reciever_position < 0:
            state[giver_position] = 0
        else:
            receiver_current_quantity = state[reciever_position]
            receiver_max_quantity = state[reciever_position + 2]

            giver_current_quantity = state[giver_position]
            giver_max_quantity = state[giver_position + 2]

            transferred_quantity = min(receiver_max_quantity - receiver_current_quantity, giver_current_quantity)
            state[reciever_position] += transferred_quantity
            state[giver_position] -= transferred_quantity
        return state


solver = Lab2Problem()

state = [1, 4, 3, 6, 2]
print("is final:", solver.isFinal(state))
# print("is emptying glass 1 ok", solver.validate(state, -1, 0))
# print("is emptying glass 2 ok", solver.validate(state,-1,1))
state = solver.transition(state, 0, 1)
print("glass1 <- glass2: ", state)
print(state)
state = solver.transition(state, 1, 0)
print("glass1 -> glass2: ", state)

