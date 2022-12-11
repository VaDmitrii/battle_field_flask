from dataclasses import dataclass

from skill import Skill, BatKick, LaserEyes, FuryClaws


@dataclass
class UnitClass:
    name: str
    max_health: float
    max_stamina: float
    attack: float
    stamina: float
    armor: float
    skill: Skill


Batman = UnitClass('Бэтмен', 50.0, 30.0, 0.9, 0.9, 1.5, BatKick())
Superman = UnitClass('Супермен', 65.0, 30.0, 1.5, 1.2, 1.0, LaserEyes())
Wolverine = UnitClass('Росомаха', 55.0, 25.0, 1.4, 1.5, 1.7, FuryClaws())

unit_classes = {
    Batman.name: Batman,
    Superman.name: Superman,
    Wolverine.name: Wolverine,
}
