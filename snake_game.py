import pygame
import time
import random

# Oyun penceresi boyutları
DIS_WIDTH = 800
DIS_HEIGHT = 600

# Renkler
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)

class Snake:
    def __init__(self):
        self.snake_block = 10
        self.snake_speed = 15
        self.snake_list = []
        self.length_of_snake = 1
        self.x1 = DIS_WIDTH / 2
        self.y1 = DIS_HEIGHT / 2
        self.x1_change = 0
        self.y1_change = 0

    def draw(self, display):
        for segment in self.snake_list:
            pygame.draw.rect(display, BLACK, [segment[0], segment[1], self.snake_block, self.snake_block])

    def update(self):
        self.x1 += self.x1_change
        self.y1 += self.y1_change
        head = [self.x1, self.y1]
        self.snake_list.append(head)
        if len(self.snake_list) > self.length_of_snake:
            del self.snake_list[0]

    def check_collision(self):
        if (self.x1 >= DIS_WIDTH or self.x1 < 0 or 
            self.y1 >= DIS_HEIGHT or self.y1 < 0):
            return True
        for segment in self.snake_list[:-1]:
            if segment == [self.x1, self.y1]:
                return True
        return False

    def grow(self):
        self.length_of_snake += 1

    def change_direction(self, direction):
        if direction == 'LEFT':
            self.x1_change = -self.snake_block
            self.y1_change = 0
        elif direction == 'RIGHT':
            self.x1_change = self.snake_block
            self.y1_change = 0
        elif direction == 'UP':
            self.y1_change = -self.snake_block
            self.x1_change = 0
        elif direction == 'DOWN':
            self.y1_change = self.snake_block
            self.x1_change = 0

class Food:
    def __init__(self):
        self.x = round(random.randrange(0, DIS_WIDTH - 10) / 10.0) * 10.0
        self.y = round(random.randrange(0, DIS_HEIGHT - 10) / 10.0) * 10.0

    def draw(self, display):
        pygame.draw.rect(display, GREEN, [self.x, self.y, 10, 10])

    def randomize(self):
        self.x = round(random.randrange(0, DIS_WIDTH - 10) / 10.0) * 10.0
        self.y = round(random.randrange(0, DIS_HEIGHT - 10) / 10.0) * 10.0

class Game:
    def __init__(self):
        pygame.init()
        self.display = pygame.display.set_mode((DIS_WIDTH, DIS_HEIGHT))
        pygame.display.set_caption('Yılan Oyunu')
        self.clock = pygame.time.Clock()
        self.snake = Snake()
        self.food = Food()
        self.font_style = pygame.font.SysFont(None, 50)
        self.score_font = pygame.font.SysFont(None, 35)
        self.game_over = False

    def display_score(self):
        value = self.score_font.render("Puan: " + str(self.snake.length_of_snake - 1), True, WHITE)
        self.display.blit(value, [0, 0])

    def message(self, msg, color):
        mesg = self.font_style.render(msg, True, color)
        self.display.blit(mesg, [DIS_WIDTH / 6, DIS_HEIGHT / 3])

    def game_loop(self):
        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.snake.change_direction('LEFT')
                    elif event.key == pygame.K_RIGHT:
                        self.snake.change_direction('RIGHT')
                    elif event.key == pygame.K_UP:
                        self.snake.change_direction('UP')
                    elif event.key == pygame.K_DOWN:
                        self.snake.change_direction('DOWN')

            if self.snake.check_collision():
                self.message("Kaybettiniz! Q-Quit veya C-Play Again", RED)
                self.display_score()
                pygame.display.update()
                time.sleep(2)
                self.game_over = True

            self.snake.update()
            if self.snake.x1 == self.food.x and self.snake.y1 == self.food.y:
                self.food.randomize()
                self.snake.grow()

            self.display.fill(BLUE)
            self.food.draw(self.display)
            self.snake.draw(self.display)
            self.display_score()
            pygame.display.update()
            self.clock.tick(self.snake.snake_speed)

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.game_loop()
