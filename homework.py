from typing import Union, List, Tuple
from dataclasses import asdict, dataclass

@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    messages = ('Тип тренировки: {training_type}; '
                'Длительность: {duration:.3f} ч.; '
                'Дистанция: {distance:.3f} км; '
                'Ср. скорость: {speed:.3f} км/ч; '
                'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        return self.messages.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_HOUR: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError("Вы не переопределили метод")

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__, self.duration,
                           self.get_distance(), self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def get_spent_calories(self) -> float:
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT) * self.weight / self.M_IN_KM
                * self.duration * self.MIN_IN_HOUR)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    weight_multiplier: float = 0.035
    second_weight_multiplier: float = 0.029
    m_in_sec: float = 0.278
    centim_in_m: float = 100

    def __init__(self, action: int, duration: float,
                 weight: float, height: int) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return ((self.weight_multiplier * self.weight + ((self.get_mean_speed()
                 * self.m_in_sec)**2
                 / (self.height / self.centim_in_m))
                 * self.second_weight_multiplier * self.weight)
                * (self.duration * self.MIN_IN_HOUR))


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    speed_multiplier: float = 1.1
    second_speed_multiplier: int = 2

    def __init__(self, action: int, duration: float, weight: float,
                 length_pool: int, count_pool) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + self.speed_multiplier)
                * self.second_speed_multiplier
                * self.weight * self.duration)


def read_package(workout_type: str, data: list[Union[int, float]]) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_dict: dict = {'SWM': Swimming,
                          'RUN': Running,
                          'WLK': SportsWalking}
    if workout_type in workout_dict:
        return workout_dict[workout_type](*data)
    else:
        raise NotImplementedError("Этой тренировки нет в словаре")


def main(training: Training) -> None:
    """Главная функция."""
    info_message: str = training.show_training_info()
    print(info_message.get_message())


if __name__ == '__main__':
    packages: list[Tuple[str, List[int]]] = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)