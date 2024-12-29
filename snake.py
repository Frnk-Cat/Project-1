from tkinter import *
import random

# Constants
GAME_WIDTH = 600
GAME_HEIGHT = 400
SPEED = 100
SPACE_SIZE = 20
BODY_PARTS = 3
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "white"

# Snake Class
class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = [[0, 0] for _ in range(BODY_PARTS)]
        self.squares = []
        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)

# Food Class
class Food:
    def __init__(self):
        x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE
        self.coordinates = [x, y]
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")

# Functions
def next_turn(snake, food):
    if not paused:
        x, y = snake.coordinates[0]

        if direction == "up":
            y -= SPACE_SIZE
        elif direction == "down":
            y += SPACE_SIZE
        elif direction == "left":
            x -= SPACE_SIZE
        elif direction == "right":
            x += SPACE_SIZE

        snake.coordinates.insert(0, (x, y))
        square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
        snake.squares.insert(0, square)

        if x == food.coordinates[0] and y == food.coordinates[1]:
            global score
            score += 1
            label.config(text=f"Score: {score}")
            canvas.delete("food")
            food = Food()
        else:
            del snake.coordinates[-1]
            canvas.delete(snake.squares[-1])
            del snake.squares[-1]

        if check_collisions(snake):
            game_over()
        else:
            window.after(SPEED, next_turn, snake, food)

def change_direction(new_direction):
    global direction
    if new_direction == "left" and direction != "right":
        direction = new_direction
    elif new_direction == "right" and direction != "left":
        direction = new_direction
    elif new_direction == "up" and direction != "down":
        direction = new_direction
    elif new_direction == "down" and direction != "up":
        direction = new_direction

def check_collisions(snake):
    x, y = snake.coordinates[0]
    if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
        return True
    for part in snake.coordinates[1:]:
        if x == part[0] and y == part[1]:
            return True
    return False

def game_over():
    global game_running
    game_running = False
    canvas.delete(ALL)
    canvas.create_text(
        canvas.winfo_width() / 2, 
        canvas.winfo_height() / 2,
        font=('consolas', 40), 
        text="GAME OVER", 
        fill="red", 
        tag="gameover"
    )
    retry_button.place(x=(GAME_WIDTH // 2) - 50, y=(GAME_HEIGHT // 2) + 50)

def start_game():
    global snake, food, score, direction, game_running, paused
    canvas.delete(ALL)  # Clear the canvas
    snake = Snake()
    food = Food()
    score = 0
    direction = "down"
    game_running = True
    paused = False
    label.config(text=f"Score: {score}")
    retry_button.place_forget()  # Hide the retry button
    next_turn(snake, food)

def toggle_pause(event=None):
    global paused
    paused = not paused
    if paused:
        label.config(text="Paused")
    else:
        label.config(text=f"Score: {score}")
        next_turn(snake, food)

# Main Program
window = Tk()
window.title("Snake Game")
window.resizable(False, False)

score = 0
direction = "down"
game_running = True
paused = False

label = Label(window, text=f"Score: {score}", font=('consolas', 20))
label.pack()

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

window.update()

# Center the window
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = (screen_width // 2) - (GAME_WIDTH // 2)
y = (screen_height // 2) - (GAME_HEIGHT // 2)
window.geometry(f"{GAME_WIDTH}x{GAME_HEIGHT}+{x}+{y}")

# Retry Button
retry_button = Button(window, text="Retry", font=('consolas', 15), command=start_game)
retry_button.place_forget()  # Hide initially

# Bind keys
window.bind('<Left>', lambda event: change_direction("left"))
window.bind('<Right>', lambda event: change_direction("right"))
window.bind('<Up>', lambda event: change_direction("up"))
window.bind('<Down>', lambda event: change_direction("down"))
window.bind('p', toggle_pause)  # Bind P key to pause/resume

# Start the game
start_game()

window.mainloop()
