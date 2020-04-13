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

    [[' ', ' ', ' ', '[ ]', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', '[ ]', ' ', '[ ]', ' '],
    ['[ ]', ' ', ' ', ' ', ' ', ' ', '[ ]', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', '[ ]', ' ', ' ', '[ ]', ' ', ' ', ' ', ' ', ' '],
    [' ', '[ ]', ' ', ' ', '[ ]', ' ', '[ ]', ' ', ' ', ' '],
    [' ', '[ ]', ' ', ' ', ' ', ' ', '[ ]', ' ', ' ', '[ ]'],
    [' ', '[ ]', ' ', '[ ]', ' ', ' ', '[ ]', ' ', ' ', ' '],
    [' ', ' ', ' ', '[ ]', ' ', ' ', ' ', ' ', ' ', '[ ]'],
    [' ', ' ', ' ', '[ ]', ' ', ' ', ' ', ' ', ' ', '[ ]']]]
statuses = ['preparation', 'game is on', 'game over']
game_status = 'preparation'


def main():
    @app.route('/')
    def index():
        return render_template('index.html', player1_field=fields[0],
                               player2_field=fields[1])

    @app.route('/button/<button_id>')
    def buttons(button_id):
        if button_id != 'start':
            letters_id = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8, 'j': 9}
            button_id = list(button_id)
            button_id[3] = ''.join(button_id[3:])
            cell = fields[int(button_id[1]) - 1][int(button_id[3]) - 1][letters_id[button_id[2]]]

        global game_status

        if game_status == statuses[0]:
            if button_id == 'start':
                game_status = statuses[1]

            elif button_id[1] == '1':
                if fields[int(button_id[1]) - 1][int(button_id[3]) - 1][letters_id[button_id[2]]] == ' ':
                    fields[int(button_id[1]) - 1][int(button_id[3]) - 1][letters_id[button_id[2]]] = '[ ]'
                elif fields[int(button_id[1]) - 1][int(button_id[3]) - 1][letters_id[button_id[2]]] == '[ ]':
                    fields[int(button_id[1]) - 1][int(button_id[3]) - 1][letters_id[button_id[2]]] = ' '

            elif button_id[1] == '2':
                print('Вы не можете стрелять по вражескому полю на этапе подготовки')
        elif game_status == statuses[1]:
            if button_id[1] == '1':
                print('Вы не можете стрелять по своему полю!')

            elif button_id[1] == '2':
                if cell == '[ ]':
                    fields[int(button_id[1]) - 1][int(button_id[3]) - 1][letters_id[button_id[2]]] = '[X]'
                    if check_nearby_cells([int(button_id[1]) - 1, int(button_id[3]) - 1, letters_id[button_id[2]]]) == 0:
                        print('Вражеский корабль потоплен!')
                    else:
                        print('Вражеский корабль подбит!')

                elif cell == ' ':
                    fields[int(button_id[1]) - 1][int(button_id[3]) - 1][letters_id[button_id[2]]] = ' • '
                    print('Мимо')

                elif cell == '[X]' or cell == ' • ':
                    print('Вы уже стреляли в эту клетку')

        return redirect('/')


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
                if fields[field][j][i] == '[ ]' or not (-1 <= i <= 10 and -1 <= j <= 10):
                    return False
    else:
        for j in range(y - 1, y + length + 1):
            for i in range(x - 1, x + 2):
                if fields[field][j][i] == '[ ]' or not (-1 <= i <= 10 and -1 <= j <= 10):
                    return False
    return True


def random_placement(field):
    available_ships = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
    for _ in range(10):
        index = random.choice(range(len(available_ships)))
        length = available_ships.pop(index)
        x = random.randint(0, 9)
        y = random.randint(0, 9)
        hor = random.randint(0, 1)
        while not can_place_ship(x, y, hor, length, field):
            x = random.randint(0, 9)
            y = random.randint(0, 9)
            hor = random.randint(0, 1)
        place_ship(x, y, hor, length, field)


def check_nearby_cells(cord):
    field_id, y, x = cord
    location_horizontal = None

    if y != 9:
        if fields[field_id][y + 1][x] in ['[ ]', '[X]']:
            location_horizontal = False
    if y != 0:
        if fields[field_id][y - 1][x] in ['[ ]', '[X]']:
            location_horizontal = False
    if x != 9:
        if fields[field_id][y][x + 1] in ['[ ]', '[X]']:
            location_horizontal = True
    if x != 0:
        if fields[field_id][y][x - 1] in ['[ ]', '[X]']:
            location_horizontal = True

    whole_sections = 0

    if location_horizontal:
        while x != -1:
            if fields[field_id][y][x] == '[ ]':
                whole_sections += 1
            elif fields[field_id][y][x] not in ['[ ]', '[X]']:
                break
            x -= 1
        x += 1
        while x != 10:
            if fields[field_id][y][x] == '[ ]':
                whole_sections += 1
            elif fields[field_id][y][x] not in ['[ ]', '[X]']:
                break
            x += 1

    elif not location_horizontal:
        while y != -1:
            if fields[field_id][y][x] == '[ ]':
                whole_sections += 1
            elif fields[field_id][y][x] not in ['[ ]', '[X]']:
                break
            y -= 1
        y += 1
        while y != 10:
            if fields[field_id][y][x] == '[ ]':
                whole_sections += 1
            elif fields[field_id][y][x] not in ['[ ]', '[X]']:
                break
            y += 1
    else:
        return 0

    return whole_sections


if __name__ == '__main__':
    main()
    global_init('db/seabattle.sqlite')
    port = int(os.environ.get('PORT', 7000))
    app.run('0.0.0.0', port)

