import os

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


def main():
    @app.route('/')
    def index():
        return render_template('index.html', player1_field=fields[0],
                               player2_field=fields[1])

    @app.route('/button/<button_id>')
    def buttons(button_id):
        letters_id = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8, 'j': 9}
        button_id = list(button_id)
        button_id[3] = ''.join(button_id[3:])
        cell = fields[int(button_id[1]) - 1][int(button_id[3]) - 1][letters_id[button_id[2]]]

        if button_id[1] == '1':
            print('Вы не можете стрелять по своему полю!')
            fields[int(button_id[1]) - 1][int(button_id[3]) - 1][letters_id[button_id[2]]] = '[ ]'
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
            elif cell == '[X]' or cell == ' . ':
                print('Вы уже стреляли в эту клетку')

        return redirect('/')


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

