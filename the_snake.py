from random import choice, randint
import pygame

# Инициализация PyGame:
pygame.init()

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
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self, position=(0, 0), body_color=(0, 0, 0)):
        """Инициализация игрового объекта с заданными позицией и цветом."""
        self.position = position
        self.body_color = body_color

    def draw(self, surface):
        """
        Метод для отрисовки объекта.
        Предназначен для переопределения в дочерних классах.
        """
        pass


class Apple(GameObject):
    """Класс для яблока, наследуется от GameObject."""

    def __init__(self, position=(0, 0), body_color=APPLE_COLOR):
        """Инициализация яблока с заданными позицией и цветом."""
        super().__init__(position, body_color)

    def randomize_position(self):
        """Устанавливает случайное положение яблока на игровом поле."""
        self.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                         randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

    def draw(self, surface):
        """Отрисовывает яблоко на игровой поверхности."""
        rect = pygame.Rect((self.position[0], self.position[1]),
                           (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс для змейки, наследуется от GameObject."""

    def __init__(self, position=(0, 0), body_color=SNAKE_COLOR):
        """Инициализация змейки с заданными позицией и цветом."""
        super().__init__(position, body_color)
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.length = 1
        self.last = None

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """
        Обновляет позицию змейки, добавляя новую голову в начало списка
        positions и удаляя последний элемент.
        """
        head_position = self.get_head_position()
        new_position = (
            (head_position[0] + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH,
            (head_position[1] + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT
        )
        if new_position in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new_position)
            if len(self.positions) > self.length:
                self.last = self.positions.pop()

    def draw(self, surface):
        """Отрисовывает змейку на экране."""
        for position in self.positions:
            rect = pygame.Rect((position[0], position[1]),
                               (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, BORDER_COLOR, rect, 1)
        if self.last:
            rect = pygame.Rect((self.last[0], self.last[1]),
                               (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, rect)

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.length = 1
        self.positions = [self.position]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.last = None


def handle_keys(snake):
    """
    Обрабатывает нажатия клавиш, чтобы изменить направление
    движения змейки.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != DOWN:
                snake.next_direction = UP
            elif event.key == pygame.K_DOWN and snake.direction != UP:
                snake.next_direction = DOWN
            elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                snake.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                snake.next_direction = RIGHT


def main():
    """
    Основная функция игры. Создает экземпляры классов Snake и Apple
    и запускает игровой цикл.
    """
    snake = Snake((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), SNAKE_COLOR)
    apple = Apple(body_color=APPLE_COLOR)
    apple.randomize_position()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()
        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw(screen)
        apple.draw(screen)
        pygame.display.update()


if __name__ == '__main__':
    main()
