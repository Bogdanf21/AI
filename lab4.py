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

    # # sa nu existe regine pe coloana
    # for possible_occupied_Y in queens:
    #     if possible_occupied_Y in domain:
    #         domain.remove(possible_occupied_Y)
    #
    # # sa nu existe regine pe diagonale
    # placed_queens = []
    # for i in range(n):
    #     if queens[i] != -1:
    #         placed_queens.append((i, queens[i]))
    # domain = list(y for y in domain if not intersects_with_any_queen_on_diagonal(placed_queens, x, y))

    # sa nu existe blocaje
    domain = list(y for y in domain if [x, y] not in state[1])

    return domain


def intersects_with_any_queen_on_diagonal(placed_queens, x, y):
    for queen in placed_queens:
        if queen[0] - queen[1] == x - y or queen[0] + queen[1] == x + y:
            return True
    return False


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
    blocksInString = str(input("coords for blocks separated by space \n"))
    tuples = blocksInString.split(" ")
    tuples = list(a for a in tuples if len(a) > 0)
    tuples = list([int(a.split(',')[0]), int(a.split(',')[1])] for a in tuples)
    return n, tuples


def forward_check(state, x):
    if x == len(state[0]):
        if has_all_queens_placed(state):
            print(state[0])
        else:
            return
    else:
        for y in domain_of(state, x):
            new_state = transition(state, x, y)
            forward_check(new_state, x + 1)


def main():
    n = 8
    blocks = [[1, 1], [2, 2], [4, 3]]

    state = init_state(4, blocks)

    forward_check(state, 0)
    # state[0][0] = 5
    # state[0][1] = 7
    # state[0][3] = 1
    # for i in range(n):
    #     print(possible_values(state, i))


main()

# def validate(state, coord_tuple):
#     n = len(state[0])
#     queens = state[0]
#     pieceX = coord_tuple[0]
#     pieceY = coord_tuple[1]
#     # daca exista pe linia X
#     if queens[pieceX] != -1:
#         return False
#     # daca exista pe coloana Y
#     for value in queens:
#         if value == pieceY:
#             return False
#             # daca exista pe diagonale
#     placed_queens = []
#     for i in range(n):
#         if queens[i] != -1:
#             placed_queens.append((i, queens[i]))
#     abs_value = abs(pieceX - pieceY)
#     for queen in placed_queens:
#         if abs(queen[0] - queen[1]) == abs_value:
#             return False
#     # daca pui pe blocaj
#     if (pieceX, pieceY) in state[1]:
#         return False
#     return True
