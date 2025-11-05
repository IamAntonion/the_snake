from random import randint

import pygame

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
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Базовый класс игровых объектов."""

    def __init__(self) -> None:
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = None

    def draw(self) -> None:
        """Отрисовать объект."""
        pass


class Apple(GameObject):
    """Класс игрового объекта Apple, наследуемого от GameObject."""

    def __init__(self) -> None:
        super().__init__()
        self.body_color = APPLE_COLOR
        self.randomize_position()

    def randomize_position(self) -> None:
        """Сгенерировать случайное положение."""
        x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE

        self.position = x, y

    # Метод draw класса Apple
    def draw(self) -> None:
        """Отрисовать яблоко."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс игрового объекта Snake, наследуемого от GameObject."""

    def __init__(self) -> None:
        super().__init__()
        self.reset()

    def update_direction(self) -> None:
        """Поменять направление движения."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self) -> None:
        """Передвинуть змею относительно направления direction."""
        head_position = self.get_head_position()

        # Координата = координата головы + размер ячейки
        # * направление (по оси 1, против -1)
        dx = head_position[0] + GRID_SIZE * self.direction[0]
        dy = head_position[1] + GRID_SIZE * self.direction[1]

        # Проверяем, зашла ли змея за экран
        if dx < 0:
            dx = SCREEN_WIDTH - GRID_SIZE
        if dx > SCREEN_WIDTH - GRID_SIZE:
            dx = 0
        if dy < 0:
            dy = SCREEN_HEIGHT - GRID_SIZE
        if dy > SCREEN_HEIGHT - GRID_SIZE:
            dy = 0

        new_head_position = (dx, dy)

        # Добавляем новую позицию головы
        self.positions.insert(0, new_head_position)

        if len(self.positions) > self.length:
            self.last = self.positions.pop()

    def draw(self) -> None:
        """Отрисовать змею."""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self) -> tuple:
        """Вернуть позицию головы."""
        return self.positions[0]

    def reset(self) -> None:
        """Отрисовать змею."""
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.last = None


def handle_keys(game_object) -> None:
    """Обработать event и установить направление движения."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT
            game_object.update_direction()


def main() -> None:
    """Запустить программу."""
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    apple = Apple()
    snake = Snake()

    while True:
        clock.tick(SPEED)

        # Тут опишите основную логику игры.
        handle_keys(snake)
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()

        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()

        apple.draw()
        snake.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
