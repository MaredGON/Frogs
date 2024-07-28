from abc import ABC, abstractmethod
from random import choice, uniform
from typing import List, Tuple, Dict
import asyncio


class Frog(ABC):
    """
    Абстрактный класс, представляющий жабу.

    Атрибуты:
    attack (int): Атака жабы.
    health (int): Здоровье жабы.
    armor (int): Броня жабы.
    frog_type (str): Тип жабы.
    """

    def __init__(self, attack: int = 15, health: int = 150, armor: int = 5):
        """
        Инициализация жабы.

        Args:
        attack (int): Атака жабы.
        health (int): Здоровье жабы.
        armor (int): Броня жабы.
        """
        self.attack = self.mod_attack(attack)
        self.health = self.mod_health(health)
        self.armor = self.mod_armor(armor)
        self.frog_type = "ПАПА"

    @abstractmethod
    def mod_attack(self, attack: int) -> int:
        """
        Модификация атаки.

        Args:
        attack (int): Атака жабы.

        Returns:
        int: Модифицированная атака.
        """
        raise NotImplementedError("Это абстрактный класс!")

    @abstractmethod
    def mod_health(self, health: int) -> int:
        """
        Модификация здоровья.

        Args:
        health (int): Здоровье жабы.

        Returns:
        int: Модифицированное здоровье.
        """
        raise NotImplementedError("Это абстрактный класс!")

    @abstractmethod
    def mod_armor(self, armor: int) -> int:
        """
        Модификация брони.

        Args:
        armor (int): Броня жабы.

        Returns:
        int: Модифицированная броня.
        """
        raise NotImplementedError("Это абстрактный класс!")

    def get_attack(self) -> int:
        """
        Получение текущей атаки жабы.

        Returns:
        int: Значение атаки.
        """
        return uniform(self.attack / 2, self.attack)

    def get_armor(self) -> int:
        """
        Получение текущей брони жабы.

        Returns:
        int: Значение брони.
        """
        return uniform(0, self.armor)

    def taking_damage(self, damage: int) -> None:
        """
        Применение урона к жабе.

        Args:
        damage (int): Значение урона.
        """
        self.health -= damage - self.get_armor()

    def __str__(self) -> str:
        """
        Строковое представление объекта жабы.

        Returns:
        str: Строковое описание жабы.
        """
        return f"Я жаба {self.frog_type} у меня сейчас: {self.attack} атаки, {round(self.health, 1)} здоровья, {self.armor} брони"


class AssassinFrog(Frog):
    """
    Класс, представляющий жабу Ассасин.
    """

    def __init__(self):
        super().__init__()
        self.frog_type = "Ассасин"

    def mod_attack(self, attack: int) -> int:
        return attack

    def mod_health(self, health: int) -> int:
        return health * 1.25

    def mod_armor(self, armor: int) -> int:
        return armor


class AdventurerFrog(Frog):
    def __init__(self):
        super().__init__()
        self.frog_type = "Авантюрист"

    def mod_attack(self, attack: int) -> int:
        return attack * 1.5

    def mod_health(self, health: int) -> int:
        return health

    def mod_armor(self, armor: int) -> int:
        return armor


class ArtisanFrog(Frog):
    def __init__(self):
        super().__init__()
        self.frog_type = "Ремесленник"

    def mod_attack(self, attack: int) -> int:
        return attack

    def mod_health(self, health: int) -> int:
        return health

    def mod_armor(self, armor: int) -> int:
        return armor * 2


async def random_create_frog() -> Frog:
    """
    Случайное создание жабы одного из трех типов.

    Returns:
    Frog: Случайно созданная жаба.
    """
    frog_classes = [AssassinFrog, AdventurerFrog, ArtisanFrog]
    return choice(frog_classes)()


async def fight(frog1: Frog, frog2: Frog) -> Tuple[int, str]:
    """
    Симуляция боя между двумя жабами.

    Args:
    frog1 (Frog): Первая жаба.
    frog2 (Frog): Вторая жаба.

    Returns:
    Tuple[int, str]: Результат боя (выйграшая жаба) и тип победившей жабы.
    """
    while frog1.health > 0 and frog2.health > 0:
        frog1.taking_damage(frog2.get_attack())
        if frog1.health <= 0:
            return 1, frog2.frog_type
        frog2.taking_damage(frog1.get_attack())
        if frog2.health <= 0:
            return 0, frog1.frog_type


async def battles(number_battles: int) -> Tuple[List[int], Dict[str, int]]:
    """
    Проведение боев между жабами указанное кол-во раз.

    Args:
    number_battles (int): Количество боев.

    Returns:
    Tuple[List[int], Dict[str, int]]: Результаты боев и статистика побед по классам.
    """
    battle_results = [0, 0]
    frog_wins = {"Ассасин": 0, "Авантюрист": 0, "Ремесленник": 0}
    for number_current_battle in range(number_battles):
        frog1 = await random_create_frog()
        frog2 = await random_create_frog()
        winner, winner_type = await fight(frog1, frog2)
        battle_results[winner] += 1
        frog_wins[winner_type] += 1

    return battle_results, frog_wins


async def main():
    number_battles = 100
    results = await asyncio.gather(battles(number_battles), battles(number_battles))
    total_results = [sum(x) for x in zip(*[r[0] for r in results])]
    total_wins = {key: sum(r[1][key] for r in results) for key in results[0][1]}
    text_result = (
        "=" * 30
        + "\n"
        + f"Жаба 1 победила {total_results[0]} раз\n"
        + f"Жаба 2 победила {total_results[1]} раз\n"
        + "=" * 30
        + "\n"
        + "Статистика побед по классам:\n"
        + f"Ассасин: {total_wins['Ассасин']}\n"
        + f"Авантюрист: {total_wins['Авантюрист']}\n"
        + f"Ремесленник: {total_wins['Ремесленник']}\n"
        + "=" * 30
    )
    print(text_result)


if __name__ == "__main__":
    asyncio.run(main())
