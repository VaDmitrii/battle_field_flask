class BaseSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Arena(metaclass=BaseSingleton):
    STAMINA_PER_ROUND = 3
    hero = None
    enemy = None
    game_is_running = False
    surrender_status = False

    def start_game(self, hero, enemy):

        self.hero = hero
        self.enemy = enemy
        self.game_is_running = True

    def _check_heroes_hp(self) -> str:

        result = None
        if self.surrender_status or self.hero.hp <= 0:
            result = f'{self.hero.name} пал смертью храбрых'
        elif self.enemy.hp <= 0:
            result = f'{self.hero.name} выиграл битву!'
        elif self.hero.hp <= 0 and self.enemy.hp <= 0:
            result = 'Ничья'
        return result

    def _stamina_regeneration(self):
        hero_add_stamina = self.STAMINA_PER_ROUND * self.hero.unit_class.stamina
        enemy_add_stamina = self.STAMINA_PER_ROUND * self.enemy.unit_class.stamina

        if self.hero.stamina + hero_add_stamina < self.hero.unit_class.max_stamina:
            self.hero.stamina += hero_add_stamina
        if self.enemy.stamina + enemy_add_stamina < self.enemy.unit_class.max_stamina:
            self.enemy.stamina += enemy_add_stamina

    def next_turn(self):
        result = self._check_heroes_hp()

        if result is None and self.game_is_running:
            self._stamina_regeneration()
            result = self.enemy.hit(target=self.hero)
        else:
            self._end_game()

        return result

    def _end_game(self) -> str:
        result = self._check_heroes_hp()

        self._instances = {}
        self.game_is_running = False

        return result

    def hero_hit(self):
        result = f"{self.hero.hit(target=self.enemy)}" \
                 f"{self.next_turn()}"

        return result

    def hero_use_skill(self):
        result = f"{self.hero.use_skill(target=self.enemy)}" \
                 f"{self.next_turn()}"

        return result
