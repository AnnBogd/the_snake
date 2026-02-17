"""Основной файл игры 'Змейка'.

Здесь описаны классы игровых объектов и сам игровой цикл.
"""
from random import choice, randint

import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
SCREEN_CENTER = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

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
SPEED = 10

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Базовый класс, от которого наследуются игровые объекты."""

    def __init__(self, body_color=BOARD_BACKGROUND_COLOR,
                 border_color=BORDER_COLOR):
        """Инициализировать базовые атрибуты класса - цвет и позиция."""
        self.position = SCREEN_CENTER
        self.body_color = body_color
        self.border_color = border_color

    def draw(self):
        """Отрисовать объекты на игровом поле.

        Заготовка. Будет переопределен в дочерних классах.
        """
        raise NotImplementedError(
            'Необходимо переопределить метод в дочернем классе')

    def draw_cell(self, position):
        """Отрисовать одну клетку."""
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, self.border_color, rect, 1)


class Snake(GameObject):
    """Класс, который описывает змейку и её поведение"""

    def __init__(self, body_color=SNAKE_COLOR, border_color=BORDER_COLOR):
        """Инициализировать атрибуты объекта змейка.

        Цвет по умолчанию зеленый, позиция - в центре экрана.
        """
        super().__init__(body_color, border_color)
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None

    def update_direction(self):
        """Обновить направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Обновить позицию змейки."""
        head_x, head_y = self.get_head_position()
        self.positions.insert(
            0,
            ((head_x + GRID_SIZE * self.direction[0]) % SCREEN_WIDTH,
             (head_y + GRID_SIZE * self.direction[1]) % SCREEN_HEIGHT))
        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self):
        """Отрисовать змейку."""
        for position in self.positions:
            self.draw_cell(position)

    def get_head_position(self):
        """Вернуть позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбросить змейку в начальное состояние"""
        self.length = 1
        self.positions = [self.position]
        self.direction = choice([RIGHT, LEFT, UP, DOWN])
        self.next_direction = None


class Apple(GameObject):
    """Класс, который описывает яблоко и действия с ним"""

    def __init__(self, body_color=APPLE_COLOR, border_color=BORDER_COLOR,
                 occupied_spots=(SCREEN_CENTER, )):
        """Инициализировать атрибуты объекта яблоко.

        Цвет по умолчанию красный.
        Позиция устанавливается методом randomize_position.
        """
        super().__init__(body_color, border_color)
        self.randomize_position(occupied_spots)

    def randomize_position(self, occupied_spots):
        """Задать координаты для появления яблока.

        Координаты выбираются случайным образом. Избегаем клеток змейки.
        """
        while True:
            x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
            y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            if (x, y) not in occupied_spots:
                self.position = (x, y)
                break

    def draw(self):
        """Отрисовать объект яблоко."""
        self.draw_cell(self.position)


def handle_keys(game_object):
    """Обработать нажатие клавиш для изменения направления змейки."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Запустить основной цикл игры."""
    # Инициализация PyGame:
    pg.init()
    apple = Apple()
    snake = Snake()

    while True:
        snake.move()
        handle_keys(snake)
        snake.update_direction()
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)
        elif snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            apple.randomize_position(snake.positions)
        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()
        pg.display.update()
        clock.tick(SPEED)


if __name__ == '__main__':
    main()
