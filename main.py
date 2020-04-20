import os
import random

from flask import Flask, render_template, redirect, request, make_response, session
from flask_login import LoginManager, login_user, logout_user, login_required

from data import db_session
from data.login_form import LoginForm
from data.register import RegisterForm
from data.db_session import global_init
from data.users import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


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
count = 0


def main():
    @app.route('/')
    def index():
        return render_template('index.html', player1_field=fields[0],
                               player2_field=fields[1], info=info)

    db_session.global_init("db/seabattle.sqlite")

    @login_manager.user_loader
    def load_user(user_id):
        session = db_session.create_session()
        return session.query(User).get(user_id)

    @app.route('/register', methods=['GET', 'POST'])
    def reqister():
        form = RegisterForm()
        if form.validate_on_submit():
            if form.password.data != form.password_again.data:
                return render_template('register.html',
                                       form=form,
                                       message="Пароли не совпадают")
            session = db_session.create_session()
            if session.query(User).filter(User.email == form.email.data).first():
                return render_template('register.html',
                                       form=form,
                                       message="Такой пользователь уже есть")
            user = User(
                nickname=form.nickname.data,
                email=form.email.data,
            )
            user.set_password(form.password.data)
            session.add(user)
            session.commit()
            return redirect('/login')
        return render_template('register.html', form=form)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            session = db_session.create_session()
            user = session.query(User).filter(User.email == form.email.data).first()
            if user and user.check_password(form.password.data):
                login_user(user, remember=form.remember_me.data)
                return redirect("/")
            return render_template('login.html',
                                   message="Неправильный логин или пароль",
                                   form=form)
        return render_template('login.html', form=form)

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect("/")

    @app.route('/button/<button_id>')
    @login_required
    def buttons(button_id):

        if button_id != 'start':
            letters_id = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8, 'j': 9}
            field_id, y, x = int(button_id[1]) - 1, int(''.join(button_id[3:])) - 1, letters_id[button_id[2]]
            cords = field_id, y, x
            button_id = list(button_id)
            button_id[3] = ''.join(button_id[3:])
            cell = fields[field_id][y][x]

        global game_status
        global info
        if game_status == statuses[0]:
            if button_id == 'start':
                info = "Ваш ход"
                game_status = statuses[1]

            elif button_id[1] == '1':
                if cell == ' ':
                    fields[field_id][y][x] = '[ ]'
                elif cell == '[ ]':
                    fields[field_id][y][x] = ' '

            elif button_id[1] == '2':
                info = 'Вы не можете стрелять по вражескому полю на этапе подготовки'
                print('Вы не можете стрелять по вражескому полю на этапе подготовки')
        elif game_status == statuses[1]:
            if button_id[1] == '1':
                info = 'Вы не можете стрелять по своему полю!'
                print('Вы не можете стрелять по своему полю!')

            elif button_id[1] == '2':
                shot(cell, cords)

        return redirect('/')

    random_placement(1)


def shot(cell, cord):
    global info, count
    field_id, y, x = cord
    if cell == '[ ]':
        fields[field_id][y][x] = '[X]'
        count += 1
        if check_nearby_cells([field_id, y, x]) == 0:
            mark_destroyed_ship([field_id, y, x])
            print(count)
            if count == 20:
                info = "ВЫ ВЫИГРАЛИ"
            else:
                info = 'Вражеский корабль потоплен!'
            print('Вражеский корабль потоплен!')
        else:
            if count == 20:
                info = "ВЫ ВЫИГРАЛИ"
            else:
                info = 'Вражеский корабль подбит!'

            print('Вражеский корабль подбит!')

    elif cell == ' ':
        fields[field_id][y][x] = ' • '
        info = 'Мимо'
        print('Мимо')

    # elif cell == '[X]' or cell == ' • ':
        # info = 'Вы уже стреляли в эту клетку'
        # print('Вы уже стреляли в эту клетку')


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


def check_nearby_cells(cord):
    location_horizontal = define_plane(cord)

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

    if location_horizontal:
        x += 1
    else:
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

    result = None
    for i in range(-1, 2):
        if y == 0 and i == -1 or y == 9 and i == 1:
            continue
        for j in range(-1, 2):
            if x == 0 and j == -1 or x == 9 and j == 1:
                continue
            elif fields[field_id][y + i][x + j] in ['[ ]', '[X]']:
                if result is not None:
                    result = None
                elif i == 0 and j in [-1, 1]:
                    result = True
                elif j == 0 and i in [-1, 1]:
                    result = False
                elif i in [-1, 1] and j in [-1, 1]:
                    result = None

    return result


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

