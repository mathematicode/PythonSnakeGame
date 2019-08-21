import turtle
import time
import random as rand
import numpy as np
import random

# Set up screen
win = turtle.Screen()
win.title("Wormy Game")
win.bgcolor("green")
win.setup(width=500, height=500)
win.tracer(0) # Turns off screen updates
width_dim = 230
heigh_dim = 230

win.score=0

# Set up border
border = turtle.Turtle()
border.penup()
border.goto(width_dim, heigh_dim)
border.pencolor('black')
border.pendown()
# Draw
border.right(90)
count = 0
while count != 4:
    border.forward(width_dim*2)
    border.right(90)
    count = count + 1
border.hideturtle()

# Create worm head
head = turtle.Turtle()
head_width = 1
head.turtlesize(head_width,head_width)
head.speed(0)
head.shape("square")
head.color("pink")
head.penup()
head.goto(0,0)
head.direction = "stop"

# NOTE: Delay doesn't work well it's a small value
win.delay=0.1

# Create list of segments
segments = [head]

# Create food
food = turtle.Turtle()
food.speed(0)
food.shape("square")
food.color("black")
food.penup()
food.goto(0,100)

# Create turtle to write on the screen
write_turtle = turtle.Turtle()
write_turtle.penup()

# Functions

def move():
    # Move each segment

    # Stop at 0 so that we don't get an error with
    # i-1 being out of bounds
    # print("length of segments", len(segments))
    for i in range(len(segments)-1, 0, -1):
        current_segment = segments[i]
        next_segment = segments[i-1]
        current_segment.goto(next_segment.xcor(), next_segment.ycor())

    # Move the head
    if head.direction == "up":
        y = head.ycor()
        head.sety(y + 20)
    if head.direction == "down":
        y = head.ycor()
        head.sety(y - 20)
    if head.direction == "left":
        x = head.xcor()
        head.setx(x - 20)
    if head.direction == "right":
        x = head.xcor()
        head.setx(x + 20)

def go_up():
    # These if statements make sure the snake can only go forward, left, or right
    # from it's current direction
    if head.direction != "down":
        head.direction="up"

def go_down():
    if head.direction != "up":
        head.direction="down"

def go_left():
    if head.direction != "right":
        head.direction="left"

def go_right():
    if head.direction != "left":
        head.direction="right"

def grow():
    new_segment = turtle.Turtle()
    new_segment.turtlesize(head_width,head_width)
    new_segment.speed(0)
    new_segment.shape("square")
    new_segment.color("blue")
    new_segment.penup()
    # Send new segment to end of snake
    last_seg = segments[len(segments)-1]
    new_segment.goto(last_seg.xcor(), last_seg.ycor())
    segments.append(new_segment)

# Determines if snake head is touching another segment. Returns 0 for false, 1 for true
def isTouchingItself():
    # Stop at 1 as we don't want to iterate over the head. The head touching itself should be allowed!
    for i in range(len(segments)-1, 1, -1):
        current_segment = segments[i]
        if (current_segment.xcor() == head.xcor()) and (current_segment.ycor() == head.ycor()):
            return 1
    return 0

# Shift food to a random position on the screen
def repositionFood():
    # width_dim and height_dim have -10 because the screen width and height needs to be -10 to be a
    # multiple of 20
    food.goto(rand.randint(0, (width_dim - 10)/20) * 20, rand.randint(0, (heigh_dim - 10)/20) * 20)

win.delay_count=0

def changeSpeed():
    win.delay_count = win.delay_count + 1
    delay_factor = 1.4 * win.delay_count
    # Make snake go from slow to fast
    if win.delay > 0.15:
        win.delay = win.delay / delay_factor
    # Make snake go from fast to slow
    else:
        win.delay = win.delay * delay_factor
        
def incrementScore():
    win.score = win.score + 1

# Keyboard bindings
win.listen()
win.onkeypress(go_up, "w")
win.onkeypress(go_down, "s")
win.onkeypress(go_left, "a")
win.onkeypress(go_right, "d")

# Main loop
while isTouchingItself() != 1:
    # Make sure to call move before doing the delay. This makes the game much smoother asn easier
    # to code

    move()

    if isTouchingItself() == 1:
        break

    # Check if the head is touching the food
    if (head.xcor() == food.xcor()) and (head.ycor() == food.ycor()):
        grow()
        repositionFood()
        changeSpeed()
        incrementScore()

    write_turtle.clear()
    write_turtle.goto(-width_dim + 50, heigh_dim - 25)
    write_turtle.pencolor("black")
    write_turtle.write("SCORE:"+str(win.score), align="center", font=("Arial", 15, "normal"))
    write_turtle.hideturtle()

    # If statements to check if the snake is going off screen. If it does, make it come out
    # of the opposite screen edge
    size=20 # size of one square of the snake
    if head.ycor() > heigh_dim:
        head.goto(head.xcor() , -heigh_dim + size/2)
    if head.ycor() < -heigh_dim:
        head.goto(head.xcor() , heigh_dim - size/2)
    if head.xcor() > width_dim:
        head.goto(-width_dim + size/2, head.ycor())
    if head.xcor() < -width_dim:
        head.goto(width_dim - size/2, head.ycor())

    time.sleep(win.delay)

    win.update()


write_turtle.goto(0, 50)
write_turtle.pencolor("black")
write_turtle.write("GAME OVER :p", align="center", font=("Arial", 20, "normal"))
write_turtle.hideturtle()

win.mainloop()
