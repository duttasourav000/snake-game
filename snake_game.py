import pygame
import random

# game paramertes
BLOCK_WIDTH = 10
GAME_HEIGHT = 500
GAME_WIDTH  = 500

# colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

# block class which is used to build snake and food
# the minimum width of any object and steps size per frame are of size BLOCK_WIDTH
class Block:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.rect = pygame.Rect(self.x, self.y, BLOCK_WIDTH , BLOCK_WIDTH)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

# snake class which is an array of blocks
# returns whether the snake is dead or not and the total score of the snake
class Snake:

    # initialize the snake with a length and optional x, y
    def __init__(self, length = 10, x = -1, y = -1):
        self.color = WHITE
        self.score = 0
        self.body = []
        self.direction = 0

        if x == -1:
            x = GAME_WIDTH / 2
        if y == -1:
            y = GAME_HEIGHT / 2

        # initializes the snake's body position
        for i in range(length):
            self.body.append(Block(x, y, self.color))
            y += BLOCK_WIDTH

        # reverses the list so that head is the last object in the list
        self.body = self.body[::-1]

    def draw(self, screen):
        for block in self.body:
            block.draw(screen)

    # updates snake and food for next frame according to direction
    def update(self, direction, food):
        # updates direction based on current key event
        # does not allow to turn 180 degrees
        if direction != -1:
            if direction == 0:
                if self.direction != 180:
                    self.direction = direction
            elif direction == 90:
                if self.direction != 270:
                    self.direction = direction
            elif direction == 180:
                if self.direction != 0:
                    self.direction = direction
            elif direction == 270:
                if self.direction != 90:
                    self.direction = direction
            else:        
                raise ValueError("Unsupported operation")

        # get the head of the snake and append the new head based on the direction
        x = self.body[-1].x
        y = self.body[-1].y
        isDead = False
        score = 0

        if self.direction == 0:
            self.body.append(Block(x, y - BLOCK_WIDTH, self.color))
        elif self.direction == 90:
            self.body.append(Block(x - BLOCK_WIDTH, y, self.color))
        elif self.direction == 180:
            self.body.append(Block(x, y + BLOCK_WIDTH, self.color))
        elif self.direction == 270:
            self.body.append(Block(x + BLOCK_WIDTH, y, self.color))

        # check collision with food
        hasCollidedWithFood = self.body[-1].rect.colliderect(food.body.rect)
        # set a score if collided with food
        if hasCollidedWithFood:
            score = 1
            # reset food to place it at new position
            food.reset()
        else:
            # delete the last block of snake in case no food is consumes in this step
            # otherwise the snake will keep growing
            del self.body[0]

        # check for snake collision with itself, head with rest of the body
        hasCollidedWithItself = False
        for block in self.body[0:-1]:
            if self.body[-1].rect.colliderect(block.rect):
                hasCollidedWithItself = True
                break

        # increase the total score
        self.score += score

        # check if snake has gone out if the screen bounds
        hasCollidedWithWall = x < 0 or y < 0 or x >= GAME_WIDTH or y >= GAME_WIDTH

        return hasCollidedWithItself or hasCollidedWithWall, self.score

# food class which stores the properties of food
class Food:

    def __init__(self):
        self.color = GREEN
        x, y = self.__getPosition()
        self.body = Block(x, y, self.color)

    # returns a random position for the food
    # the logic can be updated to take the snake's body positions and no initialize food with those positions
    def __getPosition(self):
        x = random.randint(0, GAME_WIDTH // BLOCK_WIDTH - 1) * BLOCK_WIDTH
        y = random.randint(0, GAME_HEIGHT // BLOCK_WIDTH - 1) * BLOCK_WIDTH

        return x, y

    # sets new positions for the food object
    def reset(self):
        x, y = self.__getPosition()
        self.body = Block(x, y, self.color)

    def draw(self, screen):
        self.body.draw(screen)

# game class which initializes the game objects, updates and draws them
class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = Food()
        self.isDead = False
        self.score = 0
        print ("Game intialized")

    # draws the game screen
    def __draw(self, screen, score):
        self.snake.draw(screen)
        self.food.draw(screen)
        text = pygame.font.Font(None, 30).render("Score: " + str(score), True, WHITE)
        screen.blit(text, (5,5))

    # draws the game over screen
    def __drawEnd(self, screen, score):        
        text = pygame.font.Font(None, 30).render("Score: " + str(score), True, WHITE)
        screen.blit(text, (GAME_WIDTH // 2 - 25, GAME_HEIGHT // 2))

        text = pygame.font.Font(None, 30).render("Game over", True, WHITE)
        screen.blit(text, (GAME_WIDTH // 2 - 40, GAME_HEIGHT // 2 - 20))

    # updates the game state
    def update(self, screen, direction):
        if not self.isDead:
            self.isDead, self.score = self.snake.update(direction, self.food)

        if self.isDead:
            self.__drawEnd(screen, self.score)
        else:
            self.__draw(screen, self.score)

# initialize pygame
pygame.init()
screen=pygame.display.set_mode([GAME_WIDTH, GAME_HEIGHT])
pygame.display.set_caption('Snake')
clock = pygame.time.Clock()

# initialize the game
game  = Game()
stop = False

while not stop:
    # run while loop 15 times per second
    clock.tick(15)
    direction = -1

    # color the screen to erase previous objects
    screen.fill(BLACK)

    # iterate over the events captured by pygame
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            stop = True
            break
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                stop = True
                break
            elif event.key == pygame.K_DOWN:
                direction = 180
            elif event.key == pygame.K_UP:
                direction = 0
            elif event.key == pygame.K_LEFT:
                direction = 90
            elif event.key == pygame.K_RIGHT:
                direction = 270

    # update game every iteration
    if not stop:
        game.update(screen, direction)
        pygame.display.flip()

pygame.quit()
