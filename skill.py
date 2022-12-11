from abc import ABC, abstractmethod


class Skill(ABC):
    user = None
    target = None

    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def damage(self):
        pass

    @property
    @abstractmethod
    def stamina(self):
        pass

    @abstractmethod
    def skill_effect(self):
        pass

    def _is_stamina_enough(self):
        self.user.stamina - self.stamina >= 0

    def use(self, user, target) -> str:
        self.user = user
        self.target = target

        if self._is_stamina_enough():
            return f"{self.user.name} попытался использовать {self.name}, но у него не хватило выносливости."
        return self.skill_effect()


class BatKick(Skill):
    name: str = 'Бэтпинок'
    damage: int = 10
    stamina: int = 5

    def skill_effect(self) -> str:
        self.target.get_damage(damage=self.damage)
        if self.user.stamina - self.stamina > 0:
            self.user.stamina -= self.stamina
        else:
            self.user.stamina = 0
        self.user.is_skill_used = True

        return f'{self.user.name} использует {self.name} и наносит {round(self.damage, 1)} урона сопернику.'


class LaserEyes(Skill):
    name: str = 'Лазеры из глаз'
    damage: int = 15
    stamina: int = 8

    def skill_effect(self) -> str:
        self.target.get_damage(damage=self.damage)
        if self.user.stamina - self.stamina > 0:
            self.user.stamina -= self.stamina
        else:
            self.user.stamina = 0
        self.user.is_skill_used = True

        return f'{self.user.name} использует {self.name} и наносит {round(self.damage, 1)} урона сопернику.'


class FuryClaws(Skill):
    name: str = 'Когти ярости'
    damage: int = 12
    stamina: int = 6

    def skill_effect(self) -> str:
        self.target.get_damage(damage=self.damage)
        if self.user.stamina - self.stamina > 0:
            self.user.stamina -= self.stamina
        else:
            self.user.stamina = 0
        self.user.is_skill_used = True

        return f'{self.user.name} использует {self.name} и наносит {round(self.damage, 1)} урона сопернику.'
