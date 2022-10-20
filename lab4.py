# 4 1 2 0 3

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

def is_final(state):
    for element in state[0]:
        if element == -1:
            return False
    return True



def possible_values(state, x):
    n = len(state[0])
    queens = state[0]
    if queens[x] != -1:  # daca exista deja o regina pe acea linie
        return []

    # toate coloanele pe care se poate pune ceva
    domain = list(i for i in range(n))

    # sa nu existe blocaj pe coloana
    for possible_occupied_Y in queens:
        if possible_occupied_Y in domain:
            domain.remove(possible_occupied_Y)

    # sa nu existe blocaj pe diagonale
    placed_queens = []
    for i in range(n):
        if queens[i] != -1:
            placed_queens.append((i, queens[i]))

    for possible_Y in domain:
        for queen in placed_queens:
            if abs(queen[0] - queen[1]) == abs(x - possible_Y):
                domain.remove(possible_Y)
    return domain

def transition(state, x, y):
    if state[0][x] != -1:
        print("Fatal error: there already is a piece on line X:", x)
    state[0][x] = y

def readValues():
    print("hello")
    n = int(input("n = "))
    blocksInString = str(input("coords for blocks separated by space \n"))
    tuples = blocksInString.split(" ")
    tuples = list(a for a in tuples if len(a) > 0)
    tuples = list([int(a.split(',')[0]), int(a.split(',')[1])] for a in tuples)
    return n, tuples


def main():

    n = 8
    tuples = [[1, 7], [2, 5], [6, 4]]

    state = init_state(8, tuples)
    # queen at 1,6 4,2 2,8
    state[0][0] = 5
    state[0][3] = 1
    state[0][1] = 7

    possible = possible_values(state, 5+1)
    possible = list(i+1 for i in possible)
    print(possible)

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

