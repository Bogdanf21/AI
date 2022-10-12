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
    def __init__(self, m, n, k):
        self.m = m
        self.n = n
        self.k = k

    def initialize(self, m, n, k):
        return [0, 0, m, n, k]

    def isFinal(self, state):
        if state[0] == state[4] or state[1] == state[4]:
            return True
        return False

    def validate(self, state, new_state):
        if state[0] == new_state[0] and state[1] == new_state[1]:
            # nothing changed (spilling an empty glass, pouring from an empty glass, pouring to a full glass etc)
            return False
        return True

    def possibleMoves(self, state):
        state1 = state.copy()
        state2 = state.copy()
        state3 = state.copy()
        state4 = state.copy()
        state5 = state.copy()
        state6 = state.copy()
        # spill c1
        state1[0] = 0
        # spill c2
        state2[1] = 0
        # c1 <- c2
        transferred_value1 = min(state3[2] - state3[0], state3[1])
        state3[1] = state3[1] - transferred_value1
        state3[0] = state3[0] + transferred_value1
        # c2 <- c1
        transferred_value2 = min(state4[3] - state4[1], state4[0])
        state4[1] = state4[1] + transferred_value2
        state4[0] = state4[0] - transferred_value2
        # fill c1
        state5[0] = state5[2]
        # fill c2
        state6[1] = state6[3]

        return [state1, state2, state3, state4, state5, state6]

    def __trace_back(self, parent_map, head):
        path = []
        while head != (0, 0):
            # print(head)
            path.append(head)
            head = parent_map[head]
        path = path[::-1]
        return path

    def bfs(self):
        is_solvable = False
        print("##### BFS SOLUTION #####")
        queue = [self.initialize(self.m, self.n, self.k)]
        parent = {(0, 0): (0, 0)}
        visited = {}
        path = []
        previous_transition = transition = queue[0]

        while len(queue) > 0:
            transition = queue.pop(0)
            if (transition[0], transition[1]) in visited:
                continue

            path.append((transition[0], transition[1]))
            visited[(transition[0], transition[1])] = 1

            if self.isFinal(transition):
                is_solvable = True
                solution = self.__trace_back(parent, (transition[0], transition[1]))
                for i in solution:
                    print(i)
                break

            for possible_next_transition in self.possibleMoves(transition):
                if self.validate(transition, possible_next_transition):
                    queue.append(possible_next_transition)
                    if (possible_next_transition[0], possible_next_transition[1]) not in parent.keys():
                        parent[(possible_next_transition[0], possible_next_transition[1])] = (
                            transition[0], transition[1])

        if not is_solvable:
            print("No solution found")

    def bkt(self):
        print("##### BACKTRACKING SOLUTION #####")
        state = self.initialize(self.m, self.n, self.k)
        self.__runbkt(state, {}, {})

    def __runbkt(self, state, visited, parent_map):
        if self.isFinal(state):
            solution = self.__trace_back(parent_map, (state[0], state[1]))
            for i in solution:
                print(i)
            print("\n")
            return True
        else:
            for possible_next_transition in self.possibleMoves(state):
                if self.validate(state, possible_next_transition) and \
                        (possible_next_transition[0], possible_next_transition[1]) not in visited:
                    visited[(possible_next_transition[0], possible_next_transition[1])] = 1
                    parent_map[(possible_next_transition[0], possible_next_transition[1])] = (state[0], state[1])
                    return self.__runbkt(possible_next_transition, visited, parent_map)

    def __hill_climbing_heuristic(self, state):
        return abs(state[0] - state[4]) + abs(state[1] - state[4])

    def hillclimb(self):
        is_solvable = False
        steps = 0
        print("##### HillClimb SOLUTION #####")
        initial_state = self.initialize(self.m, self.n, self.k)
        queue = [initial_state]
        parent = {(initial_state[0], initial_state[1]): (initial_state[0], initial_state[1])}
        parent_heuristic_value = self.__hill_climbing_heuristic(initial_state)
        visited = {}
        path = []

        while len(queue) > 0:
            steps += 1
            transition = queue.pop(0)
            parent_heuristic_value = self.__hill_climbing_heuristic(transition)

            if (transition[0], transition[1]) in visited:
                continue

            path.append((transition[0], transition[1]))
            visited[(transition[0], transition[1])] = 1

            if self.isFinal(transition):
                is_solvable = True
                solution = self.__trace_back(parent, (transition[0], transition[1]))
                for i in solution:
                    print(i)
                print("Steps: ", steps)
                break


            transitions = self.possibleMoves(transition)
            transitions = list(t for t in transitions if self.__hill_climbing_heuristic(t) <= parent_heuristic_value)
            transitions.sort(key=self.__hill_climbing_heuristic, reverse=True)

            for possible_next_transition in transitions:
                if self.validate(transition, possible_next_transition):
                    queue.append(possible_next_transition)
                    if (possible_next_transition[0], possible_next_transition[1]) not in parent.keys():
                        parent[(possible_next_transition[0], possible_next_transition[1])] = (
                        transition[0], transition[1])

        if not is_solvable:
            print("No solution found")


solver = Lab2Problem(4, 5, 3)
solver.bkt()
solver.bfs()
solver.hillclimb()
# 4
# 4
# 3
# 4
# 3
# 3
# 2
# 3
# 4
# 2
# 3
# 3
# 2

# statee = [8, 5, 8, 4, 2]
# possible = solver.possibleMoves(statee)
# print("possible moves:", possible)
# print("valid moves:")
# for move in possible:
#     if (solver.validate(statee, move)):
#         print(move)

# print("is final:", solver.isFinal(statee))
# print("is emptying glass 1 ok", solver.validate(statee, 0, 4))
# print("is emptying glass 2 ok", solver.validate(statee, 0, 0))
# print("glass1 <- glass2: ", solver.validate(statee, 3, 2))
# print("glass1 -> glass2: ", solver.validate(statee, 1, 5))
# # state = solver.transition(state, 1, 0)
# print("glass1 -> glass2: ", statee)

# def validate(self, state, reciever_position, giver_position):
#     #receiver can have the values -1, 0, 1, giver 0, 1
#     if reciever_position > 1 or giver_position > 1 or giver_position == reciever_position:
#         print("Receiver position or giver position are invalid")
#         return False
#     if state[giver_position] == 0:  # giver doesn't have water
#         return False
#     if reciever_position < 0:  # giver is spilled on the floor
#         return True
#
#     receiver_current_quantity = state[reciever_position]
#     receiver_max_quantity = state[reciever_position + 2]
#
#     if receiver_max_quantity != receiver_current_quantity:
#         return True

# def transition(self, state, reciever_position, giver_position):
#     if reciever_position < 0:
#         state[giver_position] = 0
#     else:
#         receiver_current_quantity = state[reciever_position]
#         receiver_max_quantity = state[reciever_position + 2]
#
#         giver_current_quantity = state[giver_position]
#         giver_max_quantity = state[giver_position + 2]
#
#         transferred_quantity = min(receiver_max_quantity - receiver_current_quantity, giver_current_quantity)
#         state[reciever_position] += transferred_quantity
#         state[giver_position] -= transferred_quantity
#     return state


# def validate2(self, state, cup1_new_value, cup2_new_value):
#     if cup1_new_value < 0 or cup2_new_value < 0:
#         return False
#     cup1_current_value = state[0]
#     cup2_current_value = state[1]
#
#     if cup1_new_value == 0 and cup1_current_value != 0 and cup2_new_value == state[1]:  # cup1 was spilled and
#         # cup2 stayed the same
#         return True
#
#     if cup1_new_value == cup1_current_value and cup2_new_value == 0 and cup2_current_value != 0:
#         #  cup1 stayed the same
#         #  and cup2 was spilled
#         return True
#
#     cup1_max_value = state[2]
#
#     cup2_max_value = state[3]
#
#     # c1 to c2:
#     transferred_value1 = min(cup2_max_value - cup2_current_value, cup1_current_value)
#     if cup2_new_value == cup2_current_value + transferred_value1 and \
#             cup1_new_value == cup1_current_value - transferred_value1 and \
#             transferred_value1 > 0:  # check if the move is redundant or not
#         return True
#
#     # c2 to c1
#     transferred_value2 = min(cup1_max_value - cup1_current_value, cup2_current_value)
#     if cup1_new_value == cup1_current_value + transferred_value2 and \
#             cup2_new_value == cup2_current_value - transferred_value2 and \
#             transferred_value2 > 0:
#         return True
#     return False
