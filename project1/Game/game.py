list_1 = [' ', '|', ' ', '|', ' ']
line_1 = ['—————']
list_2 = [' ', '|', ' ', '|', ' ']
line_2 = ['—————']
list_3 = [' ', '|', ' ', '|', ' ']


def show_place():
    print(''.join(list_1))
    print(''.join(line_1))
    print(''.join(list_2))
    print(''.join(line_2))
    print(''.join(list_3))


def repeat_input_value():
    print('Введите значение от 1 до 3!')


def make_move(a, b, player):
    if a not in range(4) or b not in range(4):
        repeat_input_value()
        return False
    if a == 1:
        if b not in range(4):
            repeat_input_value(), play_game()
        else:
            list_1[0] = player if b == 1 and list_1[0] == ' ' else list_1[0]
            list_1[2] = player if b == 2 and list_1[2] == ' ' else list_1[2]
            list_1[4] = player if b == 3 and list_1[4] == ' ' else list_1[4]
    elif a == 2:
        if b not in range(4):
            repeat_input_value(), play_game()
        else:
            list_2[0] = player if b == 1 and list_2[0] == ' ' else list_2[0]
            list_2[2] = player if b == 2 and list_2[2] == ' ' else list_2[2]
            list_2[4] = player if b == 3 and list_2[4] == ' ' else list_2[4]
    elif a == 3:
        if b not in range(4):
            repeat_input_value(), play_game()
        else:
            list_3[0] = player if b == 1 and list_3[0] == ' ' else list_3[0]
            list_3[2] = player if b == 2 and list_3[2] == ' ' else list_3[2]
            list_3[4] = player if b == 3 and list_3[4] == ' ' else list_3[4]
    elif a > 3 or a < 1:
        repeat_input_value()
    check_win()
    return True


def check_win():
    combination_list = [
        [list_1[0], list_1[2], list_1[4]],
        [list_2[0], list_2[2], list_2[4]],
        [list_3[0], list_3[2], list_3[4]],
        [list_1[0], list_2[0], list_3[0]],
        [list_1[2], list_2[2], list_3[2]],
        [list_1[4], list_2[4], list_3[4]],
        [list_1[0], list_2[2], list_3[4]],
        [list_1[4], list_2[2], list_3[0]]
    ]

    for combination in combination_list:
        if combination == ['X', 'X', 'X']:
            return 'Игрок X победил!'
        if combination == ['O', 'O', 'O']:
            return 'Игрок O победил!'

    return None


def play_game():
    show_place()
    current_player = 'X'
    for _ in range(9):
        move_made = False
        while not move_made:
            a = int(input(f'Игрок {current_player}, введите строку 1-3: '))
            b = int(input(f'Игрок {current_player}, введите столбец 1-3: '))
            move_made = make_move(a, b, current_player)

        show_place()

        result = check_win()
        if result:
            print(result)
            return

        current_player = 'O' if current_player == 'X' else 'X'

    print('Ничья!')


play_game()