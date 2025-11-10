# the_snake.py

"""
Модуль the_snake.py.

Данный модуль содержит логику игрового персонажа Sneak
и подбираемого объекта Apple.
"""

from random import choice, randint

import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

MOVE_DIRECTION = {
    # Случаи при нажатии на клавишу K_UP
    (pg.K_UP, UP): UP,
    (pg.K_UP, LEFT): UP,
    (pg.K_UP, RIGHT): UP,

    (pg.K_DOWN, DOWN): DOWN,
    (pg.K_DOWN, LEFT): DOWN,
    (pg.K_DOWN, RIGHT): DOWN,

    (pg.K_LEFT, LEFT): LEFT,
    (pg.K_LEFT, UP): LEFT,
    (pg.K_LEFT, DOWN): LEFT,

    (pg.K_RIGHT, RIGHT): RIGHT,
    (pg.K_RIGHT, UP): RIGHT,
    (pg.K_RIGHT, DOWN): RIGHT
}

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0x0, 0x0, 0x0)

# Цвет границы ячейки
BORDER_COLOR = (0x5D, 0xD8, 0xE4)

# Цвет яблока
APPLE_COLOR = (0xFF, 0x0, 0x0)

# Цвет змейки
SNAKE_COLOR = (0x0, 0xFF, 0x0)

# Скорость движения змейки:
SPEED = 5

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


class GameObject:
    """Базовый класс игровых объектов."""

    def __init__(self,
                 color: tuple[int, int, int] = (0x0, 0x0, 0x0)
                 ) -> None:
        """
        Инициализатор класса GameObject.
        Задает начальную позицию в центре экрана.
        Задает начальный цвет как (0x0, 0x0, 0x0).

        Args:
            color (tuple[int, int, int]): Цвет объекта.
        """
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = color

    def _draw_cell(self,
                   position: tuple[int, int] | None = None,
                   color: tuple[int, int, int] | None = None
                   ) -> None:
        """
        Отрисовать одну ячейку на поле.

        Args:
            position (tuple[int, int] | None): Позиция объекта.
            color (tuple[int, int, int] | None): Цвет объекта.
        """
        position = position or self.position
        color = color or self.body_color

        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)

    def draw(self) -> None:
        """Отрисовать объект."""
        raise NotImplementedError('Этот метод должен быть реализован '
                                  'в подклассе.')


class Apple(GameObject):
    """Класс игрового объекта Apple, наследуемого от GameObject."""

    def __init__(self,
                 color: tuple[int, int, int] = APPLE_COLOR,
                 occupied_count: list[tuple[int, int]] | None = None
                 ) -> None:
        """
        Создать объект Apple, наследуемый от GameObject.

        Args:
            color (tuple[int, int, int]): Цвет Apple
            occupied_count (list[tuple[int, int]] | None):
                Список занятых ячеек.
        """
        super().__init__(color)

        occupied_count = occupied_count or []

        self.randomize_position(occupied_count)

    def randomize_position(self,
                           occupied_count: list[tuple[int, int]] | None = None
                           ) -> None:
        """
        Сгенерировать случайное положение.

        Args:
            occupied_count (list[tuple[int, int]] | None):
                Список занятых ячеек.
        """
        occupied_count = occupied_count or []

        x_position = int()
        y_position = int()

        while True:
            x_position = randint(0, GRID_WIDTH - 1) * GRID_SIZE
            y_position = randint(0, GRID_HEIGHT - 1) * GRID_SIZE

            if (x_position, y_position) not in occupied_count:
                break

        self.position = x_position, y_position

    def draw(self) -> None:
        """Отрисовать яблоко."""
        self._draw_cell()


class Snake(GameObject):
    """Класс игрового объекта Snake, наследуемого от GameObject."""

    def __init__(self,
                 color: tuple[int, int, int] = SNAKE_COLOR
                 ) -> None:
        """
        Создать объект Sneak, наследуемый от GameObject.

        Args:
            color (tuple[int, int, int]): Цвет Snake.
        """
        super().__init__(color)
        self.reset()

    def update_direction(self,
                         direction: tuple[int, int] | None) -> None:
        """
        Поменять направление движения.

        Args:
            next_direction (tupl[int, int] | None): Направление.
        """
        if direction is None:
            return

        self.direction = direction

    def move(self) -> None:
        """Передвинуть змею относительно направления direction."""
        # Парсим координаты головы
        head_x, head_y = self.get_head_position()
        # Парсим направление головы
        axies_x, axies_y = self.direction

        # Координата = координата головы + размер ячейки
        # * направление (по оси 1, против -1)
        dx = head_x + GRID_SIZE * axies_x
        dy = head_y + GRID_SIZE * axies_y

        # Проверяем, зашла ли змея за экран
        dx = dx % SCREEN_WIDTH
        dy = dy % SCREEN_HEIGHT

        new_head_position = (dx, dy)

        # Добавляем новую позицию головы
        self.positions.insert(0, new_head_position)
        self.position = self.get_head_position()

        # Если длина змеи больше length, последний item устанавливаем
        # в self.last, для дальнейшего удаления
        snake_length = len(self.positions)
        item = self.positions.pop() if snake_length > self.length else None
        self.last = item

    def draw(self) -> None:
        """Отрисовать змею."""
        # Стираем хвост
        if self.last:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

        # Рисуем голову
        self._draw_cell()

    def get_head_position(self) -> tuple:
        """
        Вернуть позицию головы.

        Return:
            tuple: Координата головы [x, y].
        """
        return self.positions[0]

    def reset(self) -> None:
        """Отрисовать змею."""
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.length = 1
        self.positions = [self.position]
        self.last = None
        self.direction = choice((UP, DOWN, LEFT, RIGHT))


def handle_keys(game_object: Snake) -> tuple[int, int] | None:
    """
    Обработать event и установить направление движения.

    Args:
        game_object (Snake): Игровой управляемый объект.

    Returns:
        tuple[int, int] | None: Передается новое направление,
        при нажании клавишь, иначе None.
    """
    for event in pg.event.get():
        # Обработка выхода из pygame
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        # Обработка клавишь перемещения
        if event.type == pg.KEYDOWN:
            return MOVE_DIRECTION.get((event.key,
                                       game_object.direction))
    return None


def update(snake: Snake,
           apple: Apple,
           direction: tuple[int, int] | None) -> None:
    """
    Обновляем направление и положение змеи.

    Args:
        snake (Snake): Игровой объект змеи.
        apple (Apple): Игровой объект яблока.
        direction: tuple[int, int] | None: Направление движения.
    """
    # Двигаем змею после обработки клавиш
    snake.update_direction(direction)
    snake.move()

    head_pos = snake.get_head_position()

    # Проверяем змея съела яблоко
    if head_pos == apple.position:
        snake.length += 1
        apple.randomize_position(snake.positions)

    # Проверяем голова змеи находится в ячейке с телом
    if head_pos in snake.positions[1:]:
        snake.reset()
        apple.randomize_position(snake.positions)
        screen.fill(BOARD_BACKGROUND_COLOR)


def render(snake: Snake, apple: Apple) -> None:
    """
    Отрисовываем объекты.

    Args:
        snake (Snake): Игровой объект змеи
        apple (Apple): Игровой объект яблока
    """
    apple.draw()
    snake.draw()
    pg.display.update()


def main() -> None:
    """Запустить программу."""
    # Инициализация PyGame:
    pg.init()

    blue_gray = (0xAF, 0xF0, 0xF3)

    # Инициализируем игровые объекты
    snake = Snake(blue_gray)
    apple = Apple(occupied_count=snake.positions)

    while True:
        clock.tick(SPEED)

        # Обработка выхода из pygame и клавиш
        direction = handle_keys(snake)

        # Обновляем игровые объекты
        update(snake, apple, direction)

        # Отрисовываем объекты
        render(snake, apple)


if __name__ == '__main__':
    main()
