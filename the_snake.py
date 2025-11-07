# the_snake.py

"""
Модуль the_snake.py

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

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

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

    def __init__(self) -> None:
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = None

    def draw(self) -> None:
        """Отрисовать объект."""
        raise NotImplementedError('Этот метод должен быть реализован '
                                  'в подклассе.')


class Apple(GameObject):
    """Класс игрового объекта Apple, наследуемого от GameObject."""

    def __init__(self) -> None:
        """Создать объект Apple, наследуемый от GameObject."""
        super().__init__()
        self.body_color = APPLE_COLOR
        self.randomize_position()

    def randomize_position(self,
                           occupied_count: list[tuple[int, int]] = []) -> None:
        """
        Сгенерировать случайное положение
        и проверить на совпадение со списком occupied_count.
        Если не передается аргумент occupied_count,
        occupied_count становится равным []
        """
        x_position = int()
        y_position = int()

        while (True):
            x_position = randint(0, GRID_WIDTH - 1) * GRID_SIZE
            y_position = randint(0, GRID_HEIGHT - 1) * GRID_SIZE

            if (x_position, y_position) not in occupied_count:
                break

        self.position = x_position, y_position

    def draw(self) -> None:
        """Отрисовать яблоко."""
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс игрового объекта Snake, наследуемого от GameObject."""

    def __init__(self) -> None:
        """Создать объект Sneak, наследуемый от GameObject."""
        super().__init__()
        self.reset()

    def update_direction(self) -> None:
        """Поменять направление движения."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

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

        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def draw(self) -> None:
        """Отрисовать змею."""
        for position in self.positions[:-1]:
            rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, self.body_color, rect)
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)

        head_rect = pg.Rect(self.get_head_position(), (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, head_rect)
        pg.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        if self.last:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self) -> tuple:
        """Вернуть позицию головы."""
        return self.positions[0]

    def reset(self) -> None:
        """Отрисовать змею."""
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.length = 1
        self.positions = [self.position]
        self.direction = choice([UP, DOWN, RIGHT, LEFT])
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.last = None


def handle_keys(game_object) -> None:
    """Обработать event и установить направление движения."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            if event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            if event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            if event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT
            game_object.update_direction()


def main() -> None:
    """Запустить программу."""
    # Инициализация PyGame:
    pg.init()

    # Инициализируем игровые объекты
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)

        handle_keys(snake)
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)

        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)

        apple.draw()
        snake.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
