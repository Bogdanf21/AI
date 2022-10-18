import sys
from collections import deque
from email.policy import default


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
        previous_transition = transition = queue[0]

        while len(queue) > 0:
            transition = queue.pop(0)
            if (transition[0], transition[1]) in visited:
                continue

            visited[(transition[0], transition[1])] = 1

            if self.isFinal(transition):
                is_solvable = True
                solution = self.__trace_back(parent, (transition[0], transition[1]))
                for i in solution:
                    print(i)
                break

            for possible_next_transition in self.possibleMoves(transition):
                if self.validate(transition, possible_next_transition):  # adaug doar tranzitiile valide
                    if self.isFinal(possible_next_transition):
                        parent[(possible_next_transition[0], possible_next_transition[1])] = (
                            transition[0], transition[1])
                        is_solvable = True
                        solution = self.__trace_back(parent, (possible_next_transition[0], possible_next_transition[1]))
                        for i in solution:
                            print(i)
                        break
                    queue.append(possible_next_transition)
                    if (possible_next_transition[0], possible_next_transition[1]) not in parent.keys():
                        parent[(possible_next_transition[0], possible_next_transition[1])] = (
                            transition[0], transition[1])
            if is_solvable:
                break

        if not is_solvable:
            print("No solution found")

    def bktt(self):
        is_solvable = False
        print("##### BackTracking SOLUTION #####")
        queue = deque([self.initialize(self.m, self.n, self.k)])
        parent = {(0, 0): (0, 0)}
        visited = {}

        previous_transition = transition = queue[0]

        while len(queue) > 0:
            transition = queue.popleft()
            if (transition[0], transition[1]) in visited:
                continue

            visited[(transition[0], transition[1])] = 1

            if self.isFinal(transition):
                is_solvable = True
                solution = self.__trace_back(parent, (transition[0], transition[1]))
                for i in solution:
                    print(i)

            for possible_next_transition in self.possibleMoves(transition):
                if self.validate(transition, possible_next_transition):
                    if self.isFinal(possible_next_transition):
                        parent[(possible_next_transition[0], possible_next_transition[1])] = (
                            transition[0], transition[1])
                        is_solvable = True
                        solution = self.__trace_back(parent, (possible_next_transition[0], possible_next_transition[1]))
                        for i in solution:
                            print(i)
                    else:
                        queue.appendleft(possible_next_transition)
                        if (possible_next_transition[0], possible_next_transition[1]) not in parent.keys():
                            parent[(possible_next_transition[0], possible_next_transition[1])] = (
                                transition[0], transition[1])

        if not is_solvable:
            print("No solution found")

    def __hill_climb_heuristic(self, state):
        return abs(state[0] - state[4]) + abs(state[1] - state[4])

    def __a_star_heuristic(self, state):
        if abs(state[0] - state[4]) + abs(state[1] - state[4]) == 0:
            return sys.maxsize
        return abs(state[0] - state[4]) + abs(state[1] - state[4])

    def hillclimb(self):
        is_solvable = False
        steps = 0
        print("##### HillClimb SOLUTION #####")
        initial_state = self.initialize(self.m, self.n, self.k)
        transition = initial_state
        parent = {(initial_state[0], initial_state[1]): (initial_state[0], initial_state[1])}
        visited = {}

        while True:
            parent_heuristic_value = self.__hill_climb_heuristic(transition)

            if (transition[0], transition[1]) in visited:
                continue

            visited[(transition[0], transition[1])] = 1

            if self.isFinal(transition):
                is_solvable = True
                solution = self.__trace_back(parent, (transition[0], transition[1]))
                for i in solution:
                    print(i)
                break

            transitions = self.possibleMoves(transition)
            transitions = list(t for t in transitions if self.__hill_climb_heuristic(t) <= parent_heuristic_value)
            transitions.sort(key=self.__hill_climb_heuristic)
            heuristics = list(self.__hill_climb_heuristic(t) for t in transitions)

            possible_next_transition = None

            for t in transitions:
                if (t[0], t[1]) not in visited:
                    possible_next_transition = t
                    break

            if possible_next_transition is None:
                break

            parent[(possible_next_transition[0], possible_next_transition[1])] = (
                transition[0], transition[1])
            parent_heuristic_value = self.__hill_climb_heuristic(transition)
            transition = possible_next_transition

        if not is_solvable:
            print("No solution found")

    def a_star(self):
        is_solvable = False
        print("##### A* SOLUTION #####")
        queue = [self.initialize(self.m, self.n, self.k)]
        parent = {(0, 0): (0, 0)}
        visited = {}
        previous_transition = transition = queue[0]

        while len(queue) > 0:
            transition = queue.pop(0)
            if (transition[0], transition[1]) in visited:
                continue

            visited[(transition[0], transition[1])] = 1

            if self.isFinal(transition):
                is_solvable = True
                solution = self.__trace_back(parent, (transition[0], transition[1]))
                for i in solution:
                    print(i)

            for possible_next_transition in self.possibleMoves(transition):
                if self.validate(transition, possible_next_transition):  # adaug doar tranzitiile valide
                    if self.isFinal(possible_next_transition):
                        parent[(possible_next_transition[0], possible_next_transition[1])] = (
                            transition[0], transition[1])
                        is_solvable = True
                        solution = self.__trace_back(parent, (possible_next_transition[0], possible_next_transition[1]))
                        print("--Solution--")
                        for i in solution:
                            print(i)
                        print("\n")
                        break

                    queue.append(possible_next_transition)
                    if (possible_next_transition[0], possible_next_transition[1]) not in parent.keys():
                        parent[(possible_next_transition[0], possible_next_transition[1])] = (
                            transition[0], transition[1])

            queue.sort(key=self.__hill_climb_heuristic, reverse=True)

        if not is_solvable:
            print("No solution found")


def menu():
    continuee = True
    m = int(input("Enter m:"))
    n = int(input("Enter n:"))
    k = int(input("Enter k:"))

    while continuee:


        print("Choose the strategy you want")

        print("1.bkt")
        print("2.bfs")
        print("3.hillclimbing")
        print("4.A*")
        option = int(input("number:"))

        solver = Lab2Problem(m, n, k)

        match option:
            case 1:
                solver.bktt()
            case 2:
                solver.bfs()
            case 3:
                solver.hillclimb()
            case 4:
                solver.a_star()

            case _:
                print("enter a valid option")

        var = input("Want to try again?(y/n)")

        if var == 'n':
            continuee = False


menu()
