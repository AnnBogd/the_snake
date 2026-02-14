"""Основной файл игры 'Змейка'.

Здесь описаны классы игровых объектов и сам игровой цикл.
"""
from random import choice, randint

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
class GameObject():
    """Базовый класс, от которого наследуются игровые объекты."""

    def __init__(self, body_color: tuple, position=None):
        """Инициализировать базовые атрибуты класса - цвет и позиция."""
        self.body_color = body_color
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    def draw(self):
        """Заготовка метода для отрисовки объекта на игровом поле.

        Будет переопределен в дочерних классах
        """
        pass


class Snake(GameObject):
    """Класс, который описывает змейку и её поведение"""

    def __init__(self, body_color=(0, 255, 0), position=None):
        """Инициализировать атрибуты объекта змейка."""
        self.length = 1
        super().__init__(body_color, position)
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = self.positions[-1]

    def update_direction(self):
        """Обновить направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self, is_apple_eaten):
        """Обновить позицию змейки."""
        head = self.get_head_position()
        self.positions.insert(
            0,
            ((head[0] + GRID_SIZE * self.direction[0]) % SCREEN_WIDTH,
             (head[1] + GRID_SIZE * self.direction[1]) % SCREEN_HEIGHT))
        if not is_apple_eaten:
            self.last = self.positions.pop()
        else:
            self.last = None

    def draw(self):
        """Отрисовать змейку."""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Вернуть позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбросить змейку в начальное состояние"""
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = None
        self.last = self.positions[-1]


class Apple(GameObject):
    """Класс, который описывает яблоко и действия с ним"""

    def __init__(self, body_color=(255, 0, 0)):
        """Инициализировать атрибуты объекта яблоко.

        Цвет по умолчанию красный.
        Позиция устанавливается методом randomize_position.
        """
        super().__init__(body_color)
        self.position = self.randomize_position()

    def randomize_position(self):
        """Задать координаты для появления яблока.

        Координаты выбираются случайным образом.
        """
        x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        return x, y

    def draw(self):
        """Отрисовать объект яблоко."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


def handle_keys(game_object):
    """Обработать нажатие клавиш для изменения направления змейки."""
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


# Основной цикл недоделан - змея не увеличивается после первого яблока
# нет обработки столкновений с собой

def main():
    """Запустить основной цикл игры."""
    # Инициализация PyGame:
    pygame.init()
    apple = Apple()
    snake = Snake()
    is_apple_eaten = False

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        if snake.positions[0] == apple.position:
            snake.length += 1
            apple = Apple()
            is_apple_eaten = True
        else:
            is_apple_eaten = False
        snake.move(is_apple_eaten)
        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()
        pygame.display.update()

if __name__ == '__main__':
    main()
