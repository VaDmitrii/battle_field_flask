from flask import Flask, render_template, request, redirect, url_for

from arena import Arena
from classes import unit_classes
from equipment import Equipment
from unit import HeroUnit, EnemyUnit

app = Flask(__name__, template_folder='templates')

heroes = {
    'player': HeroUnit,
    'enemy': EnemyUnit
}

arena = Arena()


@app.route('/')
def start_page():
    return render_template('index.html')


@app.route("/fight/")
def start_fight():
    # TODO выполняем функцию start_game экземпляра класса арена и передаем ему необходимые аргументы
    # TODO рендерим экран боя (шаблон fight.html)
    arena.start_game(hero=heroes['player'], enemy=heroes['enemy'])
    return render_template('fight.html', heroes=heroes)


@app.route("/fight/hit")
def hit():
    if arena.game_is_running:
        result = arena.hero_hit()
    else:
        return render_template('fight.html', heroes=heroes)
    return render_template('fight.html', heroes=heroes, result=result)

    # TODO кнопка нанесения удара
    # TODO обновляем экран боя (нанесение удара) (шаблон fight.html)
    # TODO если игра идет - вызываем метод player.hit() экземпляра класса арены
    # TODO если игра не идет - пропускаем срабатывание метода (простот рендерим шаблон с текущими данными)


@app.route("/fight/use-skill")
def use_skill():
    # TODO кнопка использования скилла
    # TODO логика пркатикчески идентична предыдущему эндпоинту
    if arena.game_is_running:
        result = arena.hero_use_skill()
    else:
        result = None
    return render_template('fight.html', heroes=heroes, result=result)


@app.route("/fight/pass-turn")
def pass_turn():
    # TODO кнопка пропус хода
    # TODO логика пркатикчески идентична предыдущему эндпоинту
    # TODO однако вызываем здесь функцию следующий ход (arena.next_turn())
    if arena.game_is_running:
        result = arena.next_turn()
    else:
        result = None
    return render_template('fight.html', heroes=heroes, result=result)


@app.route("/fight/end-fight")
def end_fight():
    # TODO кнопка завершить игру - переход в главное меню
    arena.surrender_status = True
    arena._check_heroes_hp()
    return render_template("index.html", heroes=heroes)


@app.route("/choose-hero/", methods=['post', 'get'])
def choose_hero():
    # TODO кнопка выбор героя. 2 метода GET и POST
    # TODO на GET отрисовываем форму.
    # TODO на POST отправляем форму и делаем редирект на эндпоинт choose enemy
    if request.method == 'POST':
        data = request.form
        name = data['name']
        unit_class = data['unit_class']
        weapon = data['weapon']
        armor = data['armor']
        equipments = Equipment()
        hero = HeroUnit(
            name=name,
            unit_class=unit_classes[unit_class],
        )
        hero.equip_weapon(equipments.get_weapon(weapon_name=weapon))
        hero.equip_armor(equipments.get_armor(armor_name=armor))
        heroes['player'] = hero
        return redirect(url_for('choose_enemy'))
    equipments = Equipment()
    header = 'Выбор героя'
    classes = unit_classes
    weapons = equipments.get_weapon_names()
    armors = equipments.get_armor_names()
    result = {
        "header": header,
        "classes": classes,
        "weapons": weapons,
        "armors": armors
    }
    return render_template('hero_choosing.html', result=result)


@app.route("/choose-enemy/", methods=['post', 'get'])
def choose_enemy():
    # TODO кнопка выбор соперников. 2 метода GET и POST
    # TODO также на GET отрисовываем форму.
    # TODO а на POST отправляем форму и делаем редирект на начало битвы
    if request.method == 'POST':
        data = request.form
        name = data['name']
        unit_class = data['unit_class']
        weapon = data['weapon']
        armor = data['armor']
        equipments = Equipment()
        enemy = EnemyUnit(
            name=name,
            unit_class=unit_classes[unit_class],
        )
        enemy.equip_weapon(equipments.get_weapon(weapon_name=weapon))
        enemy.equip_armor(equipments.get_armor(armor_name=armor))
        heroes['enemy'] = enemy
        return redirect(url_for('start_fight'))
    equipments = Equipment()
    header = 'Выбор врага'
    classes = unit_classes
    weapons = equipments.get_weapon_names()
    armors = equipments.get_armor_names()
    result = {
        "header": header,
        "classes": classes,
        "weapons": weapons,
        "armors": armors
    }
    return render_template('hero_choosing.html', result=result)


if __name__ == "__main__":
    app.run()
