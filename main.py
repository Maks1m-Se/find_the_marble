import pygame
import random
import time
import copy
import sys

# Initialize pygame
pygame.init()

# Define constants
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 400
CUP_WIDTH, CUP_HEIGHT = 120, 160
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 60
marble_show_speed = 1
cup_switch_speed = 1

# Load cup and marble images
cup_image = pygame.image.load('cup.png')
cup_image = pygame.transform.scale(cup_image, (CUP_WIDTH, CUP_HEIGHT))
marble_image = pygame.image.load('marble.png')
marble_image = pygame.transform.scale(marble_image, (40, 40))





# Define cup positions and text
cup_positions = [
    [100, 200],
    [250, 200],
    [400, 200]
]
text_pos = (SCREEN_WIDTH // 2 , 100)
font = pygame.font.SysFont('Arial', 30, bold=True)
text_surface = font.render('FIND THE MARBLE!', True, (0, 0, 0))



# Setup the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("FIND THE MARBLE!")
screen.blit(text_surface, text_surface.get_rect(center=(text_pos)))

clock = pygame.time.Clock()

def show_where_marble(marble_position=None):
    global marble_show_speed
    """Show the position of the marble"""
    print('Show where marble')

    new_cup_positions = copy.deepcopy(cup_positions)

    go_up = True
    go_down = False

    for i in range(0, 1000):
        if go_up and i % 11 == 0:
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

        screen.fill(WHITE)

        screen.blit(marble_image, (cup_positions[marble_position][0] + CUP_WIDTH // 2 - 20, 200 + CUP_HEIGHT - 40))

        screen.blit(cup_image, new_cup_positions[0])
        screen.blit(cup_image, new_cup_positions[1])
        screen.blit(cup_image, new_cup_positions[2])
        screen.blit(text_surface, text_surface.get_rect(center=(text_pos)))
        
        pygame.display.flip()
        # print('new_cup_positions', new_cup_positions)
        # print('cup_positions', cup_positions)

def draw_scene(marble_position=None, reveal=False):
    """Draws the cups and, if revealed, the marble under one of the cups."""
    print('Draw scene')

    screen.fill(WHITE)
    for i, pos in enumerate(cup_positions):
        screen.blit(cup_image, pos)
        screen.blit(text_surface, text_surface.get_rect(center=(text_pos)))
        if reveal and i == marble_position:
            show_where_marble(marble_position)
    pygame.display.flip()



def scramble_cups(cup_order, marble_position):
    """Scramble the cups with an animation."""
    print('Scramble cups')

    num_moves = 3
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

        for i in range(0, 2000):
            #cup1
            if move_cup1 and new_cup_positions[idx1][0] < pos2[0]:
                if i % 4 == 0:
                    new_cup_positions[idx1][0] += cup_switch_speed         
            elif move_cup1 and new_cup_positions[idx1][0] > pos2[0]:
                if i % 4 == 0:
                    new_cup_positions[idx1][0] -= cup_switch_speed 
            else:
                 move_cup1 = False
                 print('ERROR switch cup1')
                 print('new_cup_positions', new_cup_positions)
                 print('cup_positions', cup_positions)
                 break
            #cup2
            if move_cup2 and new_cup_positions[idx2][0] < pos1[0]:
                if i % 4 == 0:
                    new_cup_positions[idx2][0] += cup_switch_speed         
            elif move_cup2 and new_cup_positions[idx2][0] > pos1[0]:
                if i % 4 == 0:
                    new_cup_positions[idx2][0] -= cup_switch_speed 
            else:
                 move_cup2 = False
                 print('ERROR switch cup2')
                 print('new_cup_positions', new_cup_positions)
                 print('cup_positions', cup_positions)
                 break
       
            # Draw the cups
            screen.fill(WHITE)
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
    global marble_position, text_surface
    running = True

    while running:

        # Initial setup: shuffle cups and hide marble
        
        cup_order = [0, 1, 2]  # Keep track of the cup order
        draw_scene()

        pygame.time.delay(100)  # Short pause before scrambling
        
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
            print("You guessed correctly!\n")
            text_surface = font.render('Correct', True, (0, 155, 0))
        else:
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
