import tkinter #importing a library
import random
import os


#defining constants
ROWS=25
COLS=25
TILE_SIZE=25
WINDOW_WIDTH=TILE_SIZE*COLS
WINDOW_HEIGHT=TILE_SIZE*ROWS
HIGH_SCORE_FILE = "highscore.txt"


def load_high_score():
    if os.path.exists(HIGH_SCORE_FILE):
        try:
            with open(HIGH_SCORE_FILE, "r") as file:
                return int(file.read().strip())
        except ValueError:
            return 0
    return 0

def save_high_score(score):
    with open(HIGH_SCORE_FILE, "w") as file:
        file.write(str(score))





class Tile:
    def __init__(self,x,y,color):
        self.x=x
        self.y=y
        self.color=color

#game window
window=tkinter.Tk()
window.title("SNAKE GAME")
window.resizable(width=False, height=False)


#canvas
canvas=tkinter.Canvas(window, bg="lime green", width=WINDOW_WIDTH, height=WINDOW_HEIGHT, borderwidth=0, highlightthickness=0 )
canvas.pack()
canvas.update()

high_score = load_high_score()

#initializing the game
def  reset_game():
    global snake, food, snake_body, velocityX, velocityY, game_over, score
    snake = Tile(5 * TILE_SIZE, 5 * TILE_SIZE, color="red")
    food = Tile(10 * TILE_SIZE, 10 * TILE_SIZE, color="purple")
    snake_body = []  # multiple snake tiles which act as the body
    velocityX = 0
    velocityY = 0
    game_over = False
    score = 0
reset_game()


def change_direction(event):
#print event
   print(event.keysym)
   global velocityX,velocityY
   if (event.keysym == "Up" and velocityY !=1):
       velocityX=0
       velocityY=-1
   elif (event.keysym == "Down" and velocityY !=-1):
       velocityX=0
       velocityY=1
   elif (event.keysym == "Left" and velocityX !=1):
        velocityY=0
        velocityX=-1
   elif (event.keysym == "Right"and velocityX !=-1):
        velocityY=0
        velocityX=1

def move_snake():
    global game_over, food, score, high_score

    if game_over:
        return

    #wall collision
    if (snake.x < 0 or snake.x >= WINDOW_WIDTH or snake.y < 0 or snake.y >= WINDOW_HEIGHT):
        game_over = True
        return
    #self collision
    for tile in snake_body:
        if (snake.x == tile.x and snake.y == tile.y):
            game_over = True
            return

    # food collision
    if snake.x==food.x and snake.y==food.y:
        snake_body.append(Tile(food.x,food.y, "red"))
        food.x=random.randint(0,COLS-1)*TILE_SIZE
        food.y=random.randint(0,ROWS-1)*TILE_SIZE
        score+=1
      #high score
    if score > high_score:
        high_score=score
        save_high_score(high_score)

        #update snake body
    for i in range(len (snake_body)-1,0,-1): #move rest of body first
            snake_body[i].x=snake_body[i-1].x
            snake_body[i].y=snake_body[i-1].y

    if len (snake_body)>0: #move body segment to snake's current position
                snake_body[0].x=snake.x
                snake_body[0].y=snake.y


    snake.x+=+velocityX*TILE_SIZE #move the head
    snake.y+=+velocityY*TILE_SIZE

def draw_snake(): #function for snake
    global snake
    move_snake()
    canvas.delete("all") #erases all previous snakes

    if game_over:
        # game over screen
        canvas.create_text(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 10, text=f"GAME OVER", fill="white",
                           font="Arial 20 bold")
        canvas.create_text(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 20, text=f"Score: {score}", fill="white",
                           font="Arial 16 bold")
        canvas.create_text(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 50, text="Press 'Space' to Restart", fill="white",
                           font="Arial 12")
    else:
      # drawing the food
      canvas.create_rectangle(food.x, food.y, food.x + TILE_SIZE, food.y + TILE_SIZE, fill="purple")

      #drawing the snake
      canvas.create_rectangle(snake.x,snake.y,snake.x + TILE_SIZE,snake.y + TILE_SIZE,fill="red")

      #adding body to draw function
    for tile in snake_body:
        canvas.create_rectangle(tile.x,tile.y,tile.x + TILE_SIZE,tile.y + TILE_SIZE,fill="red")

    #scoreboard
    canvas.create_text(110, 15, text=f"Score: {score}  |  High Score: {high_score}", fill="white", font="Arial 12 bold")


    window.after(150, draw_snake) #after every 100ms draw the snake

def restart_game(event):
    if game_over:
        reset_game()


window.bind("<KeyPress>", change_direction)
window.bind("<space>", restart_game)

#starting the game
draw_snake() #calling the function
window.mainloop()



