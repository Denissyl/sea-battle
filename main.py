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
        print(button_id)
        cell = fields[int(button_id[1]) - 1][int(button_id[3]) - 1][letters_id[button_id[2]]]

        if button_id[1] == '1':
            print('Вы не можете стрелять по своему полю!')
            fields[int(button_id[1]) - 1][int(button_id[3]) - 1][letters_id[button_id[2]]] = '[ ]'
        elif button_id[1] == '2':
            if cell == '[ ]':
                fields[int(button_id[1]) - 1][int(button_id[3]) - 1][letters_id[button_id[2]]] = '[X]'
                print('Вражеский корабль подбит!')
            elif cell == ' ':
                fields[int(button_id[1]) - 1][int(button_id[3]) - 1][letters_id[button_id[2]]] = ' . '
                print('Мимо')
            elif cell == '[X]' or cell == ' . ':
                print('Вы уже стреляли в эту клетку')

        return redirect('/')


if __name__ == '__main__':
    main()
    global_init('db/seabattle.sqlite')
    port = int(os.environ.get('PORT', 7000))
    app.run('0.0.0.0', port)

