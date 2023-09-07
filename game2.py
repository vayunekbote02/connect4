from ursina import *
import random

# Initialize the game window
app = Ursina()

# Create the game objects
snake = Entity(model='quad', color=color.green, scale=(1,1))
food = Entity(model='quad', color=color.red, scale=(1,1))

# Set the initial position of the snake and food
snake_position = (0, 0)
food_position = (random.randint(-4, 4), random.randint(-4, 4))

# Define the movement of the snake
def update():
    global snake_position, food_position
    
    # Move the snake in the current direction
    if held_keys['a']:
        snake_position = (snake_position[0]-1, snake_position[1])
    if held_keys['d']:
        snake_position = (snake_position[0]+1, snake_position[1])
    if held_keys['w']:
        snake_position = (snake_position[0], snake_position[1]+1)
    if held_keys['s']:
        snake_position = (snake_position[0], snake_position[1]-1)
        
    # Check if the snake has collided with the food
    if snake_position == food_position:
        food_position = (random.randint(-4, 4), random.randint(-4, 4))
        
    # Update the positions of the snake and food
    snake.position = (snake_position[0], snake_position[1], 0)
    food.position = (food_position[0], food_position[1], 0)

# Run the game
app.run()
