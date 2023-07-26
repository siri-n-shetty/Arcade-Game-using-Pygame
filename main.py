import pygame
import time
import random

pygame.font.init()
# Initialise/importing the fonts from pygame module

WIDTH, HEIGHT = 500, 500

# Setting the pygame window 
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Interstellar Evasion")

# The background image
BG = pygame.image.load("sky.jpg")
BG = pygame.transform.scale(BG, (WIDTH, HEIGHT))    # Scaling the image

PLAYER_HEIGHT = 50
PLAYER_WIDTH = 30
PLAYER_VELOCITY = 5
# Velocity does not literally mean 'velocity', it is just the measure of pixels

STAR_WIDTH = 8
STAR_HEIGHT = 16
STAR_VEL = 3

# Setting up font style and size to display on the screen
FONT = pygame.font.SysFont("timesnewroman", 25)

# Loading the backgrounf image
def draw(player, elapsed_time, stars):   
    # passing the player so that it is visible on the screen
    # passing the elapsed_time to display time spent during one game

    # To draw the image on the screen
    WIN.blit(BG, (0,0))
    # Here, (0,0) are the coordinates of the top left corner of the screen

    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    WIN.blit(time_text, (5,5))
    # Used to display the time on the screen
    # 1 stands for Anti-Aliasing, which makes the text look better :)

    pygame.draw.rect(WIN, "red", player)
    # We are drawing a rectangle on the window WIN 
    # which is red in colour and is our player

    # We draw the stars after the player so that it appears on top of the rectangle
    for star in stars:
        pygame.draw.rect(WIN, "white", star)

    pygame.display.update()
    #Everytime we refresh/update the screen, it draws the image over the screen


# Game logic
def main():
    run = True

    # Setting up the character
    player = pygame.Rect(200, HEIGHT-PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
    # Order of specifying is x-coordinate, y-coordinate, player-width, player-height

    # To ensure that the player moves with the same spped on any computer, we set a clock
    clock = pygame.time.Clock()

    # To keep track the time spent in the game 
    start_time = time.time()        # gives current time
    elapsed_time = 0

    # Initialising the projectiles/stars that fall from above
    star_add_increment = 2000
    # The first star will be added at 2000 milliseconds
    star_count = 0

    # To store the different stars currently present o the screen, we create a list
    stars = []
    hit = False

    while run:
        star_count += clock.tick(60)
        # It basically counts the no. of millisecs since the last clock tick
        # It counts time in simpler words
        # Here, 'clock_tick' has a while loop which will run 60 times in a second. 
        # Its like setting no. of frames per second

        elapsed_time = time.time() - start_time
        # subtracts current time from start time to give the amount of time spent in the game

        # Generating the stars
        if star_count > star_add_increment:
            # Adding stars to the screen
            # It starts adding stars after 2000 ms.
            for _ in range(6):      # adding 3 stars at a time
                star_x = random.randint(0, WIDTH - STAR_WIDTH)
                star = pygame.Rect(star_x, -STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT)
                # We have used negative coordinates becaue we want 
                # the stars to be appearing from the top of the screen
                # The -ve coordinate makes sure it comes somewhere from above the screen
                # It creates an effect that stars slowly enter the screen from somewhere above

                stars.append(star)

            #To adjust the coming of  incoming stars
            star_add_increment = max((200, star_add_increment - 50))
            # After every 50ms, we see a new star coming

            star_count = 0
            # Resets the counter before the loop starts again
            
        for event in pygame.event.get():    # It checks in the 'list' of pygame events
            if event.type == pygame.QUIT:   # If user presses the 'X' button,
                run = False                 
                break
        
        # Controlling the red rectangle's movements
        keys = pygame.key.get_pressed() # importing all kinds of keys that are pressed

        if keys[pygame.K_LEFT] and (player.x - PLAYER_VELOCITY >= 0):         
            # If left arrow key is pressed
            # it also checks, if the velocity of player becomes negative it stops the movement of the player
            # this velocity becomes negative at the corner of the screen

            player.x -= PLAYER_VELOCITY
            # We subtract as when moving left-side, player is moving towards origin
            # Implicitly, its like the x-xoordinate is decreasing

        if keys[pygame.K_RIGHT] and (player.x + PLAYER_VELOCITY + PLAYER_WIDTH <= WIDTH):
            # the second condition basically stops the player at the end corner of the screen

            player.x += PLAYER_VELOCITY
            # Similar logic as left keys 
            # but here x-coordinate increases

        # Movement of stars
        for star in stars[:]:       # iterating in the copy of the stars list
            # To remove the stars that have hit the bottom of the screen or player
            star.y += STAR_VEL
            if star.y > HEIGHT:    # height of the screen
                stars.remove(star)
                # It removes the 'instance' of the star from the list
            elif (star.y + star.height >= player.y) and star.colliderect(player):
                stars.remove(star)
                hit = True
                break

        if hit:
            lost_text = FONT.render("You Lost!", 1, "white")
            # Initialise the etxt
            WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))
            # Display the text on the screen
            pygame.display.update()
            pygame.time.delay(3000)
            # Freeze the screen
            break

        draw(player, elapsed_time, stars)
        # Draws the image at every single frame/moment on the screen

    pygame.quit()                           # Window closes

# Calling the 'main' function
if __name__ == "__main__":
    main()