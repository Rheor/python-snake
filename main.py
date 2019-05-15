import os
import sys
import time
import random
from pynput import keyboard

def random_pos(height, width):
    return [int(random.uniform(0,height)), int(random.uniform(0, width))]


def on_press(snake_game):
    def func(key):
        try:
            print("alphanumeric key {} pressed".format(key.char))
        except AttributeError:
            if key is keyboard.Key.up:
                snake_game.move_snake("up")
            if key is keyboard.Key.down:
                snake_game.move_snake("down")
            if key is keyboard.Key.left:
                snake_game.move_snake("left")
            if key is keyboard.Key.right:
                snake_game.move_snake("right")
    return func

def on_release(key):
    pass


class SnakeGame:

    count_eaten = -1

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.direction = None
        self._clear_game()
        self._pop_snake()        
        self._pop_food()
        
        listener = keyboard.Listener(
            on_press=on_press(self),
            on_release=on_release)
        listener.start()

    def _clear_game(self):
        self.game_array = []
        for i in range(self.height):
            self.game_array.append([" " for y in range(self.width)])
    
    def _pop_snake(self):
        rand_pos = random_pos(self.width, self.height)
        self.snake = [rand_pos]

    def move_snake(self, direction=None):

        if direction is not None:
            self.direction = direction

        dx, dy = 0, 0 
        if self.direction == "up":
            dy = -1
        if self.direction == "down":
            dy = 1
        if self.direction == "right":
            dx = 1
        if self.direction == "left":
            dx = -1

        self.count_eaten += -1

        inserted_eaten = False

        if self.count_eaten == 0:
            self.snake.insert(1, self.last_food)
            self.count_eaten = -1
            inserted_eaten = True
        
        top = self.snake[0].copy()
        for i in range(0, len(self.snake)):
            if i == 0:
                self.snake[i][0] += dy
                self.snake[i][1] += dx
            if i != 0 and not inserted_eaten:
                old_value = self.snake[i].copy()
                self.snake[i] = top.copy()
                top = old_value.copy()

        if self.snake[0] == self.food:
            self.last_food = self.food
            self.count_eaten = 1
            self._pop_food()
        
        if self.snake[0][0] < 0 or self.snake[0][1] < 0:
            print("Game over: out of arena")
            sys.exit(0)    

        if self.snake[0] in self.snake[1:]:
            print("Game over: Head eats tail, ouch")         
            sys.exit(0)            

        os.system("clear")
        print(self)
    
    def _pop_food(self):
        in_snake = True
        rand_food = []
        while in_snake:
            rand_food = random_pos(self.width, self.height)
            in_snake = rand_food in self.snake
        self.food = rand_food

    def _compute_score(self):
        return "Score: {0}".format(str(len(self.snake)*50)) \
                            .rjust(self.width, "-") \
                            .ljust(self.width*2, "-")

    def __str__(self):
        self._clear_game()
        
        self.game_array[self.food[0]][self.food[1]] = "f"    
   
        try: 
            for cell in self.snake:
                self.game_array[cell[0]][cell[1]] = "*"
        except IndexError:
            print("Game over: out of arena")
            sys.exit(0)        

        vertical_border = [" -" for i in range(self.width-1)]
        vertical_border.append("\n")
        game_str = "".join(vertical_border) 
        for i in range(self.height):
            game_str += "|"
            game_str += " ".join(self.game_array[i])
            game_str += "|\n"
        game_str += "".join(vertical_border) + "\n"
        game_str += self._compute_score()
        return game_str


sn = SnakeGame(20, 20)

while True:
    sn.move_snake()
    time.sleep(0.5)

