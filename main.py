import os
import random

from flask import Flask, render_template, redirect

from data.db_session import global_init

app = Flask(__name__)

fields = [
    [[' ', ' ', '[ ]', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
     [' ', ' ', ' ', ' ', '[ ]', ' ', ' ', ' ', ' ', ' '],
     [' ', ' ', ' ', ' ', ' ', ' ', '[ ]', ' ', ' ', ' '],
     ['[ ]', ' ', ' ', ' ', '[ ]', ' ', '[ ]', ' ', ' ', '[ ]'],
     ['[ ]', ' ', ' ', ' ', '[ ]', ' ', '[ ]', ' ', ' ', ' '],
     ['[ ]', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
     ['[ ]', ' ', ' ', '[ ]', ' ', ' ', ' ', '[ ]', ' ', ' '],
     [' ', ' ', ' ', '[ ]', ' ', ' ', ' ', '[ ]', ' ', ' '],
     [' ', '[ ]', ' ', '[ ]', ' ', ' ', ' ', ' ', ' ', ' '],
     [' ', '[ ]', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '[ ]']],

    [[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
     [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
     [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
     [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
     [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
     [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
     [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
     [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
     [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
     [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']]]
statuses = ['preparation', 'game is on', 'game over']
game_status = 'preparation'
info = 'Разместите корабли'



def main():
    @app.route('/')
    def index():
        return render_template('index.html', player1_field=fields[0],
                               player2_field=fields[1], info=info)

    @app.route('/button/<button_id>')
    def buttons(button_id):

        if button_id != 'start':
            letters_id = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8, 'j': 9}
            field_id, y, x = int(button_id[1]) - 1, int(''.join(button_id[3:])) - 1, letters_id[button_id[2]]
            cords = field_id, y, x
            button_id = list(button_id)
            button_id[3] = ''.join(button_id[3:])
            cell = fields[field_id][y][x]

        global game_status, info

        if game_status == statuses[0]:
            if button_id == 'start' and check_player_ship_arrangement(0) is True:
                game_status = statuses[1]
                info = 'Игра началась!'

            elif button_id[1] == '1':
                if cell == ' ':
                    fields[field_id][y][x] = '[ ]'
                elif cell == '[ ]':
                    fields[field_id][y][x] = ' '

            elif button_id[1] == '2':
                info = 'Вы не можете стрелять по вражескому полю на этапе подготовки!'

        elif game_status == statuses[1]:
            if check_count_ships(0) == 0:
                info = 'Вы проиграли'
                game_status = statuses[2]

            elif check_count_ships(1) == 0:
                info = 'Вы победили'
                game_status = statuses[2]

            elif button_id[1] == '1':
                info = 'Вы не можете стрелять по своему полю!'

            elif button_id[1] == '2':
                shot(cell, cords)

        elif game_status == statuses[2]:
            info = 'Игра окончена'

        return redirect('/')

    random_placement(1)


def shot(cell, cord):
    global info
    field_id, y, x = cord

    if cell == '[ ]':
        fields[field_id][y][x] = '[X]'

        if check_whole_sections(cord, define_plane(cord)) == 0:
            mark_destroyed_ship(cord)
            info = 'Вражеский корабль потоплен!'
        else:
            info = 'Вражеский корабль подбит!'

    elif cell == ' ':
        fields[field_id][y][x] = ' • '
        info = 'Мимо'

    elif cell == '[X]' or cell == ' • ':
        info = 'Вы уже стреляли в эту клетку'


def check_count_ships(player_id):
    ships_count = 0

    for i in fields[player_id]:
        for j in i:
            if j == '[ ]':
                ships_count += 1

    return ships_count


def check_player_ship_arrangement(field_id):
    global info

    ships = []
    ships_cords = []

    for i in range(len(fields[field_id])):
        for j in range(len(fields[field_id])):
            cord = [field_id, i, j]
            ship_plane = define_plane(cord)

            if ship_plane is None:
                info = 'В расстановке кораблей обнаружена ошибка!'
                return False
            elif (j, i) in ships_cords:
                continue
            elif fields[field_id][i][j] == '[ ]':
                ship_size = identify_ship(cord, ship_plane)
                ships.append(ship_size)
                ships_cords.extend(identify_ship_cords(cord, ship_plane, ship_size))

    ships.sort()

    if len(ships_cords) == 20 and ships == [1, 1, 1, 1, 2, 2, 2, 3, 3, 4]:
        return True
    info = 'В расстановке кораблей обнаружена ошибка!'
    return False


def identify_ship(cord, ship_plane):
    field_id, y, x = cord

    ship_size = 0

    while x <= 9 and y <= 9 and fields[field_id][y][x] == '[ ]':
        if ship_plane:
            if x <= 9 and fields[field_id][y][x] == '[ ]':
                ship_size += 1
                x += 1
        elif not ship_plane:
            if y <= 9 and fields[field_id][y][x] == '[ ]':
                ship_size += 1
                y += 1

    return ship_size


def identify_ship_cords(cord, ship_plane, ship_size):
    field_id, y, x = cord

    cords = []

    for i in range(ship_size):
        if ship_plane:
            cords.append((x + i, y))
        elif not ship_plane:
            cords.append((x, y + i))

    return cords


def place_ship(x, y, hor, length, field):
    for i in range(length):
        if hor:
            fields[field][y][x + i] = '[ ]'
        else:
            fields[field][y + i][x] = '[ ]'


def can_place_ship(x, y, hor, length, field):
    if hor:
        for j in range(y - 1, y + 2):
            for i in range(x - 1, x + length + 1):
                if 0 <= i < 10 and 0 <= j < 10:
                    if fields[field][j][i] == '[ ]':
                        return False
    else:
        for j in range(y - 1, y + length + 1):
            for i in range(x - 1, x + 2):
                if 0 <= i < 10 and 0 <= j < 10:
                    if fields[field][j][i] == '[ ]':
                        return False
    return True


def random_placement(field):
    available_ships = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
    for _ in range(10):
        index = random.choice(range(len(available_ships)))
        length = available_ships.pop(index)
        hor = random.randint(0, 1)
        x = random.randint(0, 9 - length * hor)
        y = random.randint(0, 9 - length * (1 - hor))
        while not can_place_ship(x, y, hor, length, field):
            hor = random.randint(0, 1)
            x = random.randint(0, 9 - length * hor)
            y = random.randint(0, 9 - length * (1 - hor))
        place_ship(x, y, hor, length, field)


def check_whole_sections(cord, location_horizontal):
    field_id, y, x = cord
    whole_sections = 0

    while x != -1:
        if fields[field_id][y][x] == '[ ]':
            whole_sections += 1
        elif fields[field_id][y][x] not in ['[ ]', '[X]']:
            break
        if location_horizontal:
            x -= 1
        else:
            y -= 1

    if location_horizontal and x != 9:
        x += 1
    elif not location_horizontal and y != 9:
        y += 1

    while x != 10:
        if fields[field_id][y][x] == '[ ]':
            whole_sections += 1
        elif fields[field_id][y][x] not in ['[ ]', '[X]']:
            break
        if location_horizontal:
            x += 1
        else:
            y += 1

    else:
        return 0

    return whole_sections


def define_plane(cord):
    field_id, y, x = cord

    if x != 0 and fields[field_id][y][x - 1] in ['[ ]', '[X]'] or \
            x != 9 and fields[field_id][y][x + 1] in ['[ ]', '[X]']:
        return True
    elif y != 0 and fields[field_id][y - 1][x] in ['[ ]', '[X]'] or \
            y != 9 and fields[field_id][y + 1][x] in ['[ ]', '[X]']:
        return False
    else:
        return True


def mark_destroyed_ship(cord):
    location_horizontal = define_plane(cord)
    field_id, y, x = cord

    while x != -1:
        if fields[field_id][y][x] == '[X]':
            set_dots([field_id, y, x])
        elif fields[field_id][y][x] not in ['[ ]', '[X]']:
            break
        if location_horizontal:
            x -= 1
        else:
            y -= 1

    if location_horizontal:
        x += 1
    else:
        y += 1

    while x != 10:
        if fields[field_id][y][x] == '[X]':
            set_dots([field_id, y, x])
        elif fields[field_id][y][x] not in ['[ ]', '[X]']:
            break
        if location_horizontal:
            x += 1
        else:
            y += 1


def set_dots(cord):
    field_id, y, x = cord

    for i in range(-1, 2):
        if (y == 0 and i == -1) or (y == 9 and i == 1):
            continue
        for j in range(-1, 2):
            if (x == 0 and j == -1) or (x == 9 and j == 1):
                continue
            elif fields[field_id][y + i][x + j] == ' ':
                fields[field_id][y + i][x + j] = ' • '


if __name__ == '__main__':
    main()
    global_init('db/seabattle.sqlite')
    port = int(os.environ.get('PORT', 7000))
    app.run('0.0.0.0', port)

