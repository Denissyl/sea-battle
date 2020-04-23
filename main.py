import os
import random

from flask import Flask, render_template, redirect, request, make_response, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

from data import db_session
from data.login_form import LoginForm
from data.register import RegisterForm
from data.db_session import global_init, create_session
from data.fields import Fields
from data.users import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)

fields = [
    [[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
     [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
     [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
     [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
     [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
     [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
     [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
     [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
     [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
     [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']],

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
global_init('db/seabattle.sqlite')
session = create_session()
game = Fields()
game.player1_field_isfilled = True
game.player1_field = str(fields[0])
game.player2_field = str(fields[1])
game.player2_field_isfilled = True
game.player1_id = 0
game.player2_id = 1
session.add(game)
session.commit()
info1 = 'Разместите корабли'
info2 = ' '
info3 = ' '

turn = None


def main():
    @app.route('/')
    def index():
        return render_template('index.html', player1_field=fields[0],
                               player2_field=fields[1], info1=info1, info2=info2, info3=info3)

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
        global game_status, info1, info2, info3, turn

        if button_id != 'start':

            letters_id = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8, 'j': 9}
            field_id, y, x = int(button_id[1]) - 1, int(''.join(button_id[3:])) - 1, letters_id[button_id[2]]
            cords = field_id, y, x
            button_id = list(button_id)
            button_id[3] = ''.join(button_id[3:])
            cell = fields[field_id][y][x]

        if game_status == statuses[0]:
            if button_id == 'start' and check_player_ship_arrangement(0) is True:
                game_status = statuses[1]
                info1 = 'Игра началась!'
                info2 = ' '
                info3 = ' '
                turn = 'player1'

            elif button_id[1] == '1':
                if cell == ' ':
                    fields[field_id][y][x] = '[ ]'
                elif cell == '[ ]':
                    fields[field_id][y][x] = ' '

            elif button_id[1] == '2':
                info3 = 'Вы не можете стрелять по вражескому полю на этапе подготовки!'

        elif game_status == statuses[1]:
            if check_count_ships(0) == 0:
                info1 = 'Вы проиграли'
                game_status = statuses[2]

            elif check_count_ships(1) == 0:
                info1 = 'Вы победили'
                game_status = statuses[2]

            elif button_id[1] == '1':
                info2 = 'Вы не можете стрелять по своему полю!'

            elif button_id[1] == '2':
                shot(cell, cords)

                if turn == 'ai':
                    ai_shot(0)

        elif game_status == statuses[2]:
            info1 = 'Игра окончена'

        return redirect('/')

    random_placement(1)


def shot(cell, cord):
    global info3, turn
    field_id, y, x = cord

    if cell == '[ ]':
        fields[field_id][y][x] = '[X]'

        if check_whole_sections(cord) == 0:
            mark_destroyed_ship(cord)
            info3 = 'Вражеский корабль потоплен!'
        else:
            info3 = 'Вражеский корабль подбит!'

    elif cell == ' ':
        fields[field_id][y][x] = ' • '
        info3 = 'Мимо'
        turn = 'ai'

    elif cell == '[X]' or cell == ' • ':
        info3 = 'Вы уже стреляли в эту клетку'

    if cell in ['[ ]', ' ']:
        if field_id == 0:
            game.player1_field = str(fields[0])
        else:
            game.player2_field = str(fields[1])
        session.add(game)
        session.commit()


def ai_shot(enemy_field_id, retry=False):
    if not retry:
        for i in range(len(fields[enemy_field_id])):
            for j in range(len(fields[enemy_field_id][i])):
                cord = enemy_field_id, i, j
                if fields[enemy_field_id][i][j] == '[X]' and check_whole_sections(cord) and \
                        check_place_for_shot(cord):

                    possible_ship_cords = determine_possible_ship_cords((enemy_field_id, i, j))

                    target_y, target_x = random.choice(possible_ship_cords)
                    target_cords = enemy_field_id, target_y, target_x

                    check_shot_ai(target_cords)
                    return

    target_y, target_x = random.choice(range(10)), random.choice(range(10))
    cord = enemy_field_id, target_y, target_x

    check_shot_ai(cord)


def check_shot_ai(cord):
    global info2, turn
    field_id, y, x = cord
    cell = fields[field_id][y][x]

    if cell in ['[X]', ' • ']:
        ai_shot(field_id, True)

    elif cell == ' ':
        fields[field_id][y][x] = ' • '
        info2 = 'Противник промахнулся'
        turn = 'player1'

    elif cell == '[ ]':
        target_cord = field_id, y, x

        fields[field_id][y][x] = '[X]'
        if check_whole_sections(target_cord) == 0:
            mark_destroyed_ship(cord)
            info2 = 'Противник потопил ваш корабль'
        else:
            info2 = 'Прямое попадание по вашему кораблю'
        ai_shot(0)


def determine_possible_ship_cords(cord):
    field_id, y, x = cord
    cord_mod = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    possible_ship_cords = []

    for mod in cord_mod:
        if y + mod[0] in range(10) and x + mod[1] in range(10) and fields[field_id][y + mod[0]][x + mod[1]] == '[X]' \
                and fields[field_id][y - mod[0]][x - mod[1]] != '[X]':
            return [(y - mod[0], x - mod[1])]
        elif y + mod[0] in range(10) and x + mod[1] in range(10) and \
                fields[field_id][y + mod[0]][x + mod[1]] in ['[ ]', ' ']:
            possible_ship_cords.append((y + mod[0], x + mod[1]))

    return possible_ship_cords


def check_place_for_shot(cord):
    ship_plane = define_plane(cord)
    field_id, y, x = cord

    if ship_plane and fields[field_id][y][x - 1] in ['[X]', ' • '] and fields[field_id][y][x + 1] in ['[X]', ' • '] or \
            not ship_plane and fields[field_id][y - 1][x] in ['[X]', ' • '] and \
            fields[field_id][y + 1][x] in ['[X]', ' • ']:
        return False
    return True


def check_count_ships(player_id):
    ships_count = 0

    for i in fields[player_id]:
        for j in i:
            if j == '[ ]':
                ships_count += 1

    return ships_count


def check_player_ship_arrangement(field_id):
    global info2

    ships = []
    ships_cords = []

    for i in range(len(fields[field_id])):
        for j in range(len(fields[field_id])):
            cord = [field_id, i, j]
            ship_plane = define_plane(cord)

            if ship_plane is None:
                info2 = 'В расстановке кораблей обнаружена ошибка!'
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
    info2 = 'В расстановке кораблей обнаружена ошибка!'
    return False


def identify_ship(cord):
    ship_plane = define_plane(cord)
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


def identify_ship_cords(cord, ship_size):
    ship_plane = define_plane(cord)
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
    if field == 0:
        game.player1_field = str(fields[0])
    else:
        game.player2_field = str(fields[1])
    session.add(game)
    session.commit()


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


def check_whole_sections(cord):
    global fields

    ship_plane = define_plane(cord)
    field_id, y, x = cord
    whole_sections = 0

    while x != -1 and y != -1:
        if fields[field_id][y][x] == '[ ]':
            whole_sections += 1
        elif fields[field_id][y][x] not in ['[ ]', '[X]']:
            break
        if ship_plane:
            x -= 1
        else:
            y -= 1

    if ship_plane and x != 9:
        x += 1
    elif not ship_plane and y != 9:
        y += 1

    while x != 10 and y != 10:
        if fields[field_id][y][x] == '[ ]':
            whole_sections += 1
        elif fields[field_id][y][x] not in ['[ ]', '[X]']:
            break
        if ship_plane:
            x += 1
        else:
            y += 1

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
    ship_plane = define_plane(cord)
    field_id, y, x = cord

    while x != -1 and y != -1:
        if fields[field_id][y][x] == '[X]':
            set_dots([field_id, y, x])
        elif fields[field_id][y][x] not in ['[ ]', '[X]']:
            break
        if ship_plane:
            x -= 1
        else:
            y -= 1

    if ship_plane:
        x += 1
    else:
        y += 1

    while x != 10 and y != 10:
        if fields[field_id][y][x] == '[X]':
            set_dots([field_id, y, x])
        elif fields[field_id][y][x] not in ['[ ]', '[X]']:
            break
        if ship_plane:
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

