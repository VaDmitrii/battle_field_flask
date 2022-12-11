import json
from random import uniform
from dataclasses import dataclass
from typing import List

import marshmallow.exceptions
import marshmallow_dataclass


@dataclass
class Weapon:
    id: int
    name: str
    max_damage: float
    min_damage: float
    stamina_per_hit: int

    @property
    def get_damage(self):
        return uniform(self.min_damage, self.max_damage)


@dataclass
class Armor:
    id: int
    name: str
    defence: float
    stamina_per_turn: int


@dataclass
class EquipmentData:
    weapon_list: List[Weapon]
    armor_list: List[Armor]


class Equipment:

    def __init__(self):
        self.equipment = self._get_equipment_data()

    def get_weapon(self, weapon_name: str) -> Weapon:
        for weapon in self.equipment.weapon_list:
            if weapon.name == weapon_name:
                return weapon

    def get_armor(self, armor_name: str) -> Armor:
        for armor in self.equipment.armor_list:
            if armor.name == armor_name:
                return armor

    def get_weapon_names(self) -> List[str]:
        return [weapon.name for weapon in self.equipment.weapon_list]

    def get_armor_names(self) -> List[str]:
        return [armor.name for armor in self.equipment.armor_list]

    @staticmethod
    def _get_equipment_data():
        data_json = open('data/equipment.json', encoding='utf-8')
        equipment_data = json.load(data_json)
        equipment_schema = marshmallow_dataclass.class_schema(EquipmentData)
        try:
            return equipment_schema().load(equipment_data)
        except marshmallow.exceptions.ValidationError:
            raise ValueError
