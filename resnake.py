import turtle
import time
import random
from threading import Thread
import sys

score = 0

class Game:

    def __init__(self):

        self.screen = turtle.Screen()

        self.screen.title("Snake game")
        self.screen.setup(700, 500)
        self.screen.bgcolor("cyan")
        self.speed = 2.5
        self.length = 0

        self.end_code = False

        self.started = False
        self.in_quit_mode = False
        self.food_exists = False

        self.snake = turtle.Turtle()
        self.snake.shape("square")
        self.snake.setheading(90)
        self.snake.color("Green")

        self.segments = []

        self.game_end = turtle.Turtle()
        self.game_end.hideturtle()
        self.game_end.penup()

        self.screen._root.resizable(False, False)

        self.score_turtle = turtle.Turtle()
        self.score_turtle.penup()
        self.score_turtle.hideturtle()
        self.score_turtle.goto(-340, 200)

        self.snake.penup()
        self.screen.onkey(self.up, "Up")
        self.screen.onkey(self.down, "Down")
        self.screen.onkey(self.left, "Left")
        self.screen.onkey(self.right, "Right")
        self.screen.onkey(self.retry, "space")

        movement = Thread(target=self.continous_move)
        movement.start()

        food = Thread(target=self.make_food)
        food.start()

        snakseze = Thread(target=self.snakesize)
        snakseze.start()

        focol = Thread(target=self.collision_f)
        focol.start()

        followsnek = Thread(target=self.follow_snake_segments)
        followsnek.start()

        self.screen.listen()
        print("workey!")
        self.screen.mainloop()
        
        self.end_code = True
        sys.exit()

    def make_food(self):
        while True:
            if self.food_exists == False:
                time.sleep(2)
                food_x = 0
                food_y = 0
                self.food = turtle.Turtle()
                self.food.shape("circle")
                self.food.speed(0)
                minus_or_plus = random.randint(0, 3)

                if minus_or_plus == 0:
                    food_x = random.randint(100, 340) * -1
                    food_y = random.randint(100, 250) * -1
                elif minus_or_plus == 1:
                    food_x = random.randint(100, 340) 
                    food_y = random.randint(100, 240)
                elif minus_or_plus == 2:
                    food_x = random.randint(100, 340) * -1
                    food_y = random.randint(100, 240)
                elif minus_or_plus == 3:
                    food_x = random.randint(100, 340)
                    food_y = random.randint(100, 240) * -1

                self.food.hideturtle()
                self.food.color("red")
                self.food.penup()
                self.food.goto(food_x, food_y)
                self.food.showturtle()
                self.food_exists = True

                if self.end_code:
                    exit()
            time.sleep(0.1)

    def up(self):
        self.snake.setheading(90)
        self.started = True
    
    def down(self):
        self.snake.setheading(270)
        self.started = True
    
    def left(self):
        self.snake.setheading(180)
        self.started = True

    def right(self):
        self.snake.setheading(360)
        self.started = True

    def retry(self):
        self.started = False
        self.snake.goto(0, 0)
        self.in_quit_mode = False
        global score
        score = 0
        self.speed = 2.5
        if self.food_exists:
            self.food.reset()
            self.food.hideturtle()
            self.food_exists == False
        
        if self.end_code:
            exit()

        self.score_turtle.clear()
        self.game_end.clear()
        self.score_turtle.write(f"Score: {score}", font=15)

    def collision_b(self):
        if self.snake.xcor() >= 350 or self.snake.xcor() <= -350 or self.snake.ycor() >= 250 or self.snake.ycor() <= -250:
            self.started = False
            self.in_quit_mode = True
            self.game_end.write("Game over!", font=10, align="center")

            if self.end_code:
                exit()

    def collision_f(self):
        if self.food_exists:
            if self.snake.xcor() - self.food.xcor() < 15 and self.snake.xcor() - self.food.xcor() > -15:
                if self.snake.ycor() - self.food.ycor() < 15 and self.snake.ycor() - self.food.ycor() > -15:
                    self.food.reset()
                    self.food.hideturtle()
                    self.food_exists = False
                    global score
                    score += 10
                    self.score_turtle.clear()
                    self.score_turtle.write(f"Score: {score}", font = 15)
                    self.speed += 0.1
                    print(self.speed)
                    print(score)

    def continous_move(self):
        while True:
            if self.started == True and self.in_quit_mode == False:
                self.snake.forward(self.speed)
                self.collision_b()
                self.collision_f()

                if self.end_code:
                    exit()
    
    def follow_snake_segments(self):
        if self.segments:
            while True:
                global score

                snake_x = self.snake.xcor()
                snake_y = self.snake.ycor()

                index = 0
                scores = score/10

                if scores == len(self.segments):
                    pass
                else:
                    new = turtle.Turtle(self.snake.xcor() - len(self.segements), self.snake.ycor())
                    self.segments.append(new)
                    new.penup()
                    new.speed("fastest")
                    new.shape("square")
                    new.color("orange")
                
                for seg in self.segments:
                    index += 1
                    time.sleep(index/2)
                    seg.forward(self.speed)
                    seg.setheading(seg.towards(self.snake))
                
                if self.end_code:
                    exit()
                
                time.sleep(0.1)
        
    def snakesize(self):
        while True:
            global score
            self.length = score/10
            time.sleep(0.1)

            if self.end_code:
               exit()

game = Game()