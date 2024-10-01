import pygame
import random
import time
import copy
import os
import sys

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Define constants
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 400
CUP_WIDTH, CUP_HEIGHT = 120, 160
WHITE = (255, 255, 255)
RED = (95, 10, 10)
BLACK = (0, 0, 0)
BG_COL = WHITE
FPS = 60
marble_show_speed = 1
cup_switch_speed = 1
n_moves_scramble = 3

# Load cup and marble images
cup_image = pygame.image.load('images/cup.png')
cup_image = pygame.transform.scale(cup_image, (CUP_WIDTH, CUP_HEIGHT))
marble_image = pygame.image.load('images/marble.png')
marble_image = pygame.transform.scale(marble_image, (40, 40))


#sounds
correct_sound = pygame.mixer.Sound(os.path.join('sounds', 'correct_sound.mp3'))
worng_sound = pygame.mixer.Sound(os.path.join('sounds', 'wrong_sound.mp3'))
intro_sound = pygame.mixer.Sound(os.path.join('sounds', 'happy-intro.mp3'))
sh_sound = pygame.mixer.Sound(os.path.join('sounds', 'sh.mp3'))
click_sound = pygame.mixer.Sound(os.path.join('sounds', 'click.mp3'))
guitar_sound = pygame.mixer.Sound(os.path.join('sounds', 'guitar-riff.mp3'))
#sh_sound.set_volume(.2)





# Define cup positions and text
cup_positions = [
    [100, 200],
    [250, 200],
    [400, 200]
]
text_pos = (SCREEN_WIDTH // 2 , 50)
font = pygame.font.SysFont('Arial', 50, bold=True)
font2= pygame.font.SysFont('Arial', 20, bold=True) 
text_surface = font.render('FIND THE MARBLE!', True, (0, 0, 0))



# Setup the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("FIND THE MARBLE!")
screen.blit(text_surface, text_surface.get_rect(center=(text_pos)))

clock = pygame.time.Clock()






def show_where_marble(marble_position=None):
    global marble_show_speed, BG_COL
    """Show the position of the marble"""
    print('Show where marble')

    new_cup_positions = copy.deepcopy(cup_positions)

    go_up = True
    go_down = False

    for i in range(0, 1000):
        if go_up and i % 12 == 0:
            new_cup_positions[marble_position][1] -= marble_show_speed
        if go_down and i % 6 == 0:
            new_cup_positions[marble_position][1] += marble_show_speed
        if new_cup_positions[marble_position][1] <= 155:
                go_up = False
                go_down = True
        if new_cup_positions[marble_position][1] > 200:
                go_up = False
                go_down = False
                break

        screen.fill(BG_COL)

        screen.blit(marble_image, (cup_positions[marble_position][0] + CUP_WIDTH // 2 - 20, 200 + CUP_HEIGHT - 40))

        screen.blit(cup_image, new_cup_positions[0])
        screen.blit(cup_image, new_cup_positions[1])
        screen.blit(cup_image, new_cup_positions[2])
        screen.blit(text_surface, text_surface.get_rect(center=(text_pos)))
        
        pygame.display.flip()
        # print('new_cup_positions', new_cup_positions)
        # print('cup_positions', cup_positions)

def draw_scene(marble_position=None, reveal=False):
    global BG_COL
    """Draws the cups and, if revealed, the marble under one of the cups."""
    print('Draw scene')

    screen.fill(BG_COL)
    for i, pos in enumerate(cup_positions):
        screen.blit(cup_image, pos)
        screen.blit(text_surface, text_surface.get_rect(center=(text_pos)))
        if reveal and i == marble_position:
            show_where_marble(marble_position)
    pygame.display.flip()



def scramble_cups(cup_order, marble_position):
    global BG_COL
    """Scramble the cups with an animation."""
    print('Scramble cups')

    num_moves = n_moves_scramble + random.choice([-1, 0, 1])
    print('number scramble moves: ', num_moves)

    for n in range(1, num_moves+1):
        print('Move: ', n, '/', num_moves)
        # Randomly swap two cups
        idx1, idx2 = random.sample(range(3), 2)
        print('Cups swapping: ', idx1, idx2)

        new_cup_positions = copy.deepcopy(cup_positions)
        #print('new_cup_positions', new_cup_positions)
        #print('cup_positions', cup_positions)
        pos1 = cup_positions[idx1]
        pos2 = cup_positions[idx2]

        move_cup1 = True
        move_cup2 = True

        sh_sound.play()

        for i in range(0, 2000):
            #cup1
            if move_cup1 and new_cup_positions[idx1][0] < pos2[0]:
                if i % 2 == 0:
                    new_cup_positions[idx1][0] += cup_switch_speed         
            elif move_cup1 and new_cup_positions[idx1][0] > pos2[0]:
                if i % 2 == 0:
                    new_cup_positions[idx1][0] -= cup_switch_speed 
            else:
                 move_cup1 = False
                 print('ERROR switch cup1')
                 print('new_cup_positions', new_cup_positions)
                 print('cup_positions', cup_positions)
                 break
            #cup2
            if move_cup2 and new_cup_positions[idx2][0] < pos1[0]:
                if i % 2 == 0:
                    new_cup_positions[idx2][0] += cup_switch_speed         
            elif move_cup2 and new_cup_positions[idx2][0] > pos1[0]:
                if i % 2 == 0:
                    new_cup_positions[idx2][0] -= cup_switch_speed 
            else:
                 move_cup2 = False
                 print('ERROR switch cup2')
                 print('new_cup_positions', new_cup_positions)
                 print('cup_positions', cup_positions)
                 break
       
            # Draw the cups
            screen.fill(BG_COL)
            screen.blit(cup_image, new_cup_positions[0])
            screen.blit(cup_image, new_cup_positions[1])
            screen.blit(cup_image, new_cup_positions[2])
            screen.blit(text_surface, text_surface.get_rect(center=(text_pos)))
            pygame.display.flip()

        cup_order[idx1], cup_order[idx2] = cup_order[idx2], cup_order[idx1]
        marble_position = idx1 if marble_position == idx2 else (idx2 if marble_position == idx1 else marble_position)
        draw_scene()

        print('Marble Pos:', marble_position)

        # Pause to create the animation effect
        pygame.time.delay(100)
    
    return marble_position

marble_position = random.randint(0, 2)

def main():
    global marble_position, text_surface, cup_switch_speed, n_moves_scramble
    
    

    ####### Initail button Difficulty ###

    #easy
    easy_button_surface = pygame.Surface((100, 30))
    easy_text = font2.render("EASY", True, (0, 0, 0))
    easy_rect = easy_text.get_rect(center=(easy_button_surface.get_width()/2, easy_button_surface.get_height()/2))
    easy_button_rect = pygame.Rect(100, 125, 150, 50)
    #medium
    medium_button_surface = pygame.Surface((100, 30))
    medium_text = font2.render("MEDIUM", True, (0, 0, 0))
    medium_rect = medium_text.get_rect(center=(medium_button_surface.get_width()/2, medium_button_surface.get_height()/2))
    medium_button_rect = pygame.Rect(210, 125, 150, 50)
    #hard
    hard_button_surface = pygame.Surface((100, 30))
    hard_text = font2.render("HARD", True, (0, 0, 0))
    hard_rect = hard_text.get_rect(center=(hard_button_surface.get_width()/2, hard_button_surface.get_height()/2))
    hard_button_rect = pygame.Rect(320, 125, 150, 50)
    #insane
    insane_button_surface = pygame.Surface((100, 30))
    insane_text = font2.render("INSANE", True, (100, 0, 0))
    insane_rect = insane_text.get_rect(center=(insane_button_surface.get_width()/2, insane_button_surface.get_height()/2))
    insane_button_rect = pygame.Rect(430, 125, 150, 50)


    intro_sound.play()

    run_difficulty = True
    while run_difficulty:
        global BG_COL
        # Set the frame rate
        clock.tick(60)
        
        

        # Get events from the event queue
        for event in pygame.event.get():
            # Check for the quit event
            if event.type == pygame.QUIT:
                # Quit the game
                pygame.quit()
                sys.exit()

            # Check for the mouse button down event
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Call the on_mouse_button_down() function
                if easy_button_rect.collidepoint(event.pos):
                    print("EASY")
                    click_sound.play()
                    cup_switch_speed = 1
                    n_moves_scramble = 3
                    run_difficulty = False
                elif medium_button_rect.collidepoint(event.pos):
                    print("MEDIUM")
                    click_sound.play()
                    cup_switch_speed = 2
                    n_moves_scramble = 4
                    run_difficulty = False
                elif hard_button_rect.collidepoint(event.pos):
                    print("HARD")
                    click_sound.play()
                    cup_switch_speed = 2
                    n_moves_scramble = 7
                    run_difficulty = False
                elif insane_button_rect.collidepoint(event.pos):
                    print("INSANE")
                    click_sound.play()
                    guitar_sound.play()
                    BG_COL = RED
                    cup_switch_speed = 3
                    n_moves_scramble = 9
                    run_difficulty = False

            # Check if the mouse is over the button. This will create the button hover effect
            if easy_button_rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(easy_button_surface, (127, 255, 212), (1, 1, 100, 30))
            else:
                pygame.draw.rect(easy_button_surface, (255, 255, 255), (1, 1, 100, 30))

            if medium_button_rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(medium_button_surface, (127, 255, 212), (1, 1, 100, 30))
            else:
                pygame.draw.rect(medium_button_surface, (255, 255, 255), (1, 1, 100, 30))

            if hard_button_rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(hard_button_surface, (127, 255, 212), (1, 1, 100, 30))
            else:
                pygame.draw.rect(hard_button_surface, (255, 255, 255), (1, 1, 100, 30))

            if insane_button_rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(insane_button_surface, 'red2', (1, 1, 100, 30))
            else:
                pygame.draw.rect(insane_button_surface, 'darksalmon', (1, 1, 100, 30))


        # Fill the display with color
        screen.fill(BG_COL)

        # Shwo the button text
        easy_button_surface.blit(easy_text, easy_rect)
        medium_button_surface.blit(medium_text, medium_rect)
        hard_button_surface.blit(hard_text, hard_rect)
        insane_button_surface.blit(insane_text, insane_rect)

        # Draw the button on the screen
        screen.blit(easy_button_surface, (easy_button_rect.x, easy_button_rect.y))
        screen.blit(medium_button_surface, (medium_button_rect.x, medium_button_rect.y))
        screen.blit(hard_button_surface, (hard_button_rect.x, hard_button_rect.y))
        screen.blit(insane_button_surface, (insane_button_rect.x, insane_button_rect.y))

        for i, pos in enumerate(cup_positions):
            screen.blit(cup_image, pos)
            screen.blit(text_surface, text_surface.get_rect(center=(text_pos)))

        # Update the game state
        pygame.display.update()
        if not run_difficulty:
            pygame.time.delay(2000)
        ####### Initail button Difficulty ###





    
    running = True
    while running:
        # Initial setup: shuffle cups and hide marble
        
        cup_order = [0, 1, 2]  # Keep track of the cup order
        draw_scene()

        pygame.time.delay(500)  # Short pause before scrambling
        
        # Scramble cups with animation
        show_where_marble(marble_position)
        print('Marble Pos:', marble_position)
        print('Guess!')
        text_surface = font.render('Guess...', True, (0, 0, 0))
        marble_position = scramble_cups(cup_order, marble_position)
        print('Marble Pos:', marble_position)
        
        # Wait for player input
        guess = None
        while guess is None:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    for i, pos in enumerate(cup_positions):
                        if pos[0] < mouse_x < pos[0] + CUP_WIDTH and pos[1] < mouse_y < pos[1] + CUP_HEIGHT:
                            guess = i
                            click_sound.play()
            if running == False:
                break
            
        if running == False:
                break
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break

        
        pygame.time.delay(100)

        # Check if the player guessed correctly
        if guess == marble_position:
            correct_sound.play()
            print("You guessed correctly!\n")
            text_surface = font.render('Correct', True, (0, 155, 0))
        else:
            worng_sound.play()
            print("You guessed wrong!\n")
            text_surface = font.render('Wrong', True, (200, 0, 0))

        # Reveal the marble
        draw_scene(marble_position, reveal=True)

        # Pause before the next round
        pygame.time.delay(1000)

    print('exit')
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
