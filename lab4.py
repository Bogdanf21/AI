# 4 1 2 0 3
from collections import deque


# Reprezentarea pentru regine :
# daca exista regina pe casuta cu coordonatele (X,Y) in vector v[X-1] = Y-1, -1 gol

# ([regine],[blocaje])

# blocajele sunt o lista de tuple

def init_state(n, blocks):
    regine = [-1] * n
    for element in blocks:
        element[0] -= 1
        element[1] -= 1
    return (regine, blocks)


# functioneaza pentru ca putem avea o singura regina pe linie
# blocks va fi vector de tuple, avand structura (X-1,Y-1) unde un blocaj 

def has_all_queens_placed(state):
    for element in state[0]:
        if element == -1:
            return False
    return True


def intersects_with_queen(possible_queen, queen):
    possible_x = possible_queen[0]
    possible_y = possible_queen[1]
    x = queen[0]
    y = queen[1]

    if x == possible_x or y == possible_y or \
            x - y == possible_x - possible_y or x + y == possible_x + possible_y:
        return True
    return False


def intersects_with_any_queen(possible_queen, queens):
    for x in range(len(queens)):
        if queens[x] != -1 and intersects_with_queen(possible_queen, [x, queens[x]]):
            return True
    return False


def domain_of(state, x):
    n = len(state[0])
    queens = state[0]
    if queens[x] != -1:  # daca exista deja o regina pe acea linie
        return []

    # toate coloanele pe care se poate pune ceva
    domain = list(i for i in range(n))

    # filtrare
    domain = list(y for y in domain if not intersects_with_any_queen([x, y], queens))

    # sa nu existe blocaje
    domain = list(y for y in domain if [x, y] not in state[1])

    return domain


def possible_moves(state):
    next_states = []
    for x in range(len(state[0])):
        domain_of_x = domain_of(state, x)
        for y in domain_of_x:
            new_state = transition(state.copy(), x, y)
            next_states.append(new_state)

    return possible_moves


def transition(state, x, y):
    if state[0][x] != -1:
        print("Fatal error: there already is a piece on line X:", x)
    queens = state[0].copy()
    queens[x] = y
    return (queens, state[1])


def readValues():
    print("hello")
    n = int(input("n = "))
    blocksInString = str(input("coords for blocks separated by space: \n"))
    tuples = blocksInString.split(" ")
    tuples = list(a for a in tuples if len(a) > 0)
    tuples = list([int(a.split(',')[0]), int(a.split(',')[1])] for a in tuples)
    return n, tuples


def fwd_check(n, blocks):
    state = init_state(n, blocks)
    forward_check(state, 0, domain_of(state, 0))


def forward_check(state, x, domain_of_x):
    for y in domain_of_x:
        possible_queen = [x, y]
        new_state = transition(state, x, y)
        if x == len(state[0]) - 1:
            if has_all_queens_placed(new_state):
                print_solution(new_state[0])
            continue

        # vad daca voi pune o regina pe x, y daca domeniul este nul pentru x+1. Daca este nu mai parcurg
        domain_of_next_x = list(forward_y for forward_y in domain_of(state, x + 1) if
                                not intersects_with_queen(possible_queen, [x + 1, forward_y]))
        if len(domain_of_next_x) > 0:
            forward_check(new_state, x + 1, domain_of_next_x)


def mrv(state, x, domain_of_x):
    next_states = []
    for y in domain_of_x:
        possible_queen = [x, y]
        new_state = transition(state, x, y)
        # vad daca am pus toate reginele, printez daca e o solutie viabila
        if x == len(state[0]) - 1:
            if has_all_queens_placed(new_state):
                print_solution(new_state[0])
            continue

        # vad daca voi pune o regina pe x, y daca domeniul este nul pentru x+1. Daca nu este, il adaug in lista
        domain_of_next_x = list(forward_y for forward_y in domain_of(state, x + 1) if
                                not intersects_with_queen(possible_queen, [x + 1, forward_y]))

        if len(domain_of_next_x) > 0:
            next_states.append([new_state, domain_of_next_x])

    if len(next_states):
        # sortam lista si alegem doar tranzitia cu cel mai mic domeniu.
        # In cazul special in care exista mai multe minime, le vom pargurge pe ambele
        next_states.sort(key=lambda i: len(i[1]))
        lowest_domain_count = len(next_states[0][1])
        next_states = list(next_state for next_state in next_states if len(next_state[1]) == lowest_domain_count)
        for next_state in next_states:
            lowest_values_left_transition = next_state[0]
            lowest_values_left_transition_domain = next_state[1]
            mrv(lowest_values_left_transition, x + 1, lowest_values_left_transition_domain)

def print_solution(queens):
    solution = []
    for i in range(len(queens)):
        solution.append((i+1, queens[i] + 1))
    print(solution)

def main():
    # n = 4
    # blocks = [[1, 1], [2, 2], [4, 3]]
    n, blocks = readValues()
    state = init_state(n, blocks)
    # Forward check
    print("Forward check solution: ")
    forward_check(state, 0, domain_of(state, 0))
    # MRV
    print("MRV:")
    mrv(state, 0, domain_of(state, 0))

    # state[0][0] = 5
    # state[0][1] = 7
    # state[0][3] = 1
    # for i in range(n):
    #     print(possible_values(state, i))


main()