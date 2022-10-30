def read_game():
    game_values = []
    moves_name = []
    players_name = []
    index = 0
    with open('resources/lab5.txt') as f:
        lines = f.readlines()
        for line in lines:
            values = list(l[:-1] if l[len(l) - 1] == '\n' else l for l in line.split(" ") if len(l) > 0)
            game_value_line = []
            if values[0][0].isdigit():
                for value in values:
                    numbers = value.split("/")
                    game_value_line.append([int(numbers[0]), int(numbers[1])])
                game_values.append(game_value_line)
            else:
                players_name.append(values.pop(0))
                moves_name.append(values)

    return players_name, moves_name, game_values


def main():
    players_name, moves_name, moves_value = read_game()
    print(players_name)
    print(moves_name)
    print(moves_value)
    print(moves_value[0][0])


main()
