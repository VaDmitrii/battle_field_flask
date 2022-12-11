from abc import ABC, abstractmethod
from random import randint
from typing import Optional

from classes import UnitClass
from equipment import Weapon, Armor


class BaseUnit(ABC):
    """
    Базовый класс юнита
    """

    def __init__(self, name: str, unit_class: UnitClass):
        """
        При инициализации класса Unit используем свойства класса UnitClass
        """
        self.name = name
        self.unit_class = unit_class
        self.hp = unit_class.max_health
        self.stamina = unit_class.max_stamina
        self.weapon = None
        self.armor = None
        self._is_skill_used = False

    @property
    def health_points(self):
        return round(self.hp, 1)

    @property
    def stamina_points(self):
        return round(self.stamina, 1)

    def equip_weapon(self, weapon: Weapon):
        self.weapon = weapon
        return f"{self.name} экипирован оружием {self.weapon.name}"

    def equip_armor(self, armor: Armor):
        self.armor = armor
        return f"{self.name} экипирован броней {self.armor.name}"

    def _count_damage(self, target) -> int:
        """
        Функция расчета количества урона и уменьшения остатка стамины
        """
        if target.stamina < target.armor.stamina_per_turn:
            target_armor = 0
        else:
            target_armor = target.armor.defence * target.unit_class.armor
            if target.stamina - target.armor.stamina_per_turn > 0:
                target.stamina -= target.armor.stamina_per_turn
            else:
                target.stamina = 0

        unit_attack = self.weapon.get_damage * self.unit_class.attack
        damage = unit_attack - target_armor
        if self.stamina - self.weapon.stamina_per_hit > 0:
            self.stamina -= self.weapon.stamina_per_hit
        else:
            self.stamina = 0

        target.get_damage(damage)

        return round(damage, 1)

    def get_damage(self, damage: int) -> Optional[float]:
        """
        Функция получения урона
        """
        self.hp -= damage
        return round(self.hp, 1)

    @abstractmethod
    def hit(self, target) -> str:
        pass

    def use_skill(self, target) -> str:
        """
        Использование супер-навыка
        """
        if self._is_skill_used:
            return 'Навык уже был использован'
        self._is_skill_used = True
        return self.unit_class.skill.use(user=self, target=target)


class HeroUnit(BaseUnit):

    def hit(self, target: BaseUnit) -> str:
        """
        Функция нанесения удара игроком
        """
        if self.stamina_points < self.weapon.stamina_per_hit:
            return f"{self.name} попытался использовать {self.weapon.name}, но у него не хватило выносливости."

        damage = round(self._count_damage(target=target), 1)

        if damage <= 0:
            return f"{self.name} используя {self.weapon.name} наносит удар," \
                   f" но {target.armor.name} cоперника его останавливает."

        return f"{self.name} используя {self.weapon.name} пробивает" \
               f" {target.armor.name} соперника и наносит {damage} урона."


class EnemyUnit(BaseUnit):

    def hit(self, target: BaseUnit) -> str:
        """
        Функция нанесения удара противником
        """
        if randint(0, 100) <= 10 and not self._is_skill_used:
            self.use_skill(target=target)
        else:
            if self.stamina_points < self.weapon.stamina_per_hit:
                return f"{self.name} попытался использовать {self.weapon.name}, но у него не хватило выносливости."

            damage = round(self._count_damage(target=target), 1)

            if damage <= 0:
                return f"{self.name} используя {self.weapon.name} наносит удар," \
                       f" но Ваш(а) {target.armor.name} его останавливает."

            return f"{self.name} используя {self.weapon.name} пробивает" \
                   f" {target.armor.name} и наносит Вам {damage} урона."
