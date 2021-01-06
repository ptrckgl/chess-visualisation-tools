import random
import pygame
pygame.init()


# --- Classes ---


class button():
    def __init__(self, x, y, w, h, ic, ac):
        """Initialise the button."""
        self.x = x  # Distance from left border
        self.y = y  # Distance from top border
        self.w = w  # Width
        self.h = h  # Height
        self.ic = ic  # Inactive colour
        self.ac = ac  # Active colour
        self.colour = self.ic  # Initialising the colour to inactive

    def draw(self, surface, text='', outline=None, font_size=24):
        """Draws a button on the screen, (if outline is not none, it's a colour)"""

        # If user wants an outline
        if outline:
            pygame.draw.rect(surface, outline, (self.x - 2, self.y - 2, self.w + 4, self.h + 4), 0)

        pygame.draw.rect(surface, self.colour, (self.x, self.y, self.w, self.h), 0)

        if text != '':
            small_text = pygame.font.Font(BASE_FONT, font_size)
            text_surface, text_rect = text_objects(text, small_text, WHITE)
            text_rect.center = (self.x + self.w // 2, self.y + self.h // 2)
            surface.blit(text_surface, text_rect)

    def is_over(self, pos):
        """Returns true if the mouse is hovering over the button"""
        # 'pos' is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.w:
            if pos[1] > self.y and pos[1] < self.y + self.h:
                return True
        return False

    def update_colour(self, pos):
        """Updates the colour of the button."""
        if self.is_over(pos):
            self.colour = self.ac
        else:
            self.colour = self.ic


# --- Functions ---


def text_objects(text, font, colour):
    """Somehow creates the text"""
    text_surface = font.render(text, True, colour)
    return text_surface, text_surface.get_rect()


def exit_game():
    """A function to exit the game."""
    pygame.quit()
    quit()


def add_time_1():
    """Adds one second to the timer."""
    global TIMER
    if TIMER < MAX_TIME:
        TIMER += 1


def add_time_5():
    """Adds five seconds to the timer."""
    global TIMER
    if TIMER < MAX_TIME - 5:
        TIMER += 5
    else:
        TIMER = MAX_TIME


def minus_time_1():
    """Subtracts one second from the timer."""
    global TIMER
    if TIMER > MIN_TIME:
        TIMER -= 1


def minus_time_5():
    """Subtracts five seconds from the timer."""
    global TIMER
    if TIMER > MIN_TIME + 5:
        TIMER -= 5
    else:
        TIMER = MIN_TIME


def increment_score():
    global SCORE, SQUARE_CHOSEN
    SCORE += 1
    SQUARE_CHOSEN = False  # So new one can be chosen


def decrement_score():
    global SCORE
    SCORE -= 1
    # Note, new square only chosen when the choice was correct


def update_timer():
    """Updates the timer during the game."""
    global TIMER
    current_time = pygame.time.get_ticks()
    TIMER = 3 + STARTING_TIME - (current_time - STARTED_TIME) // 1000


def redraw_window():
    """Draws the window after every frame."""
    BUTTON_EXIT.draw(GAME_DISPLAY, 'Exit')
    BUTTON_TIMER.draw(GAME_DISPLAY, f'Time: {TIMER}')
    BUTTON_SCORE.draw(GAME_DISPLAY, f'Score: {SCORE}')
    BUTTON_BLACK_SQUARE.draw(GAME_DISPLAY)
    BUTTON_WHITE_SQUARE.draw(GAME_DISPLAY)

    if not GAME_STARTED:
        BUTTON_START.draw(GAME_DISPLAY, 'Start')
        BUTTON_PLUS1.draw(GAME_DISPLAY, '+')
        BUTTON_PLUS5.draw(GAME_DISPLAY, '+')
        BUTTON_MINUS1.draw(GAME_DISPLAY, '-')
        BUTTON_MINUS5.draw(GAME_DISPLAY, '-')
        BUTTON_TEXT1.draw(GAME_DISPLAY, '1', font_size=20)
        BUTTON_TEXT5.draw(GAME_DISPLAY, '5', font_size=20)
        BUTTON_SQUARE.draw(GAME_DISPLAY)


def start_game():
    """Starts the game."""
    global GAME_STARTED, STARTED_TIME, STARTING_TIME
    GAME_STARTED = True
    STARTING_TIME = TIMER
    STARTED_TIME = pygame.time.get_ticks()

    # Overwrite previous buttons to 'hide' them :)
    BUTTON_PLUSMINUS.draw(GAME_DISPLAY)
    BUTTON_START_OVERWRITE.draw(GAME_DISPLAY)
    pygame.display.update()


def get_random_square():
    """Generates a random square."""
    global SQUARE_CHOSEN
    square = random.randint(0, 63)
    square_name = get_square_notation(square)
    print(f"Index: {square}, Squarename: {square_name}")
    BUTTON_SQUARE.draw(GAME_DISPLAY, square_name)
    SQUARE_CHOSEN = True
    return square


def get_square_notation(index):
    """The way the squares are in this program starts from top left and goes down, then right."""
    file_vals = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    rank_vals = ['1', '2', '3', '4', '5', '6', '7', '8']
    # Note - the rank values only need to be accurate relating to square colour :)

    # Getting the correct column
    file_num, rank_num = get_file_rank(index)

    return f"{file_vals[file_num]}{rank_vals[rank_num]}"


def get_file_rank(index):
    """Returns the file and rank based off the index from 0 to 63 provided."""
    # Starts from a1 and goes up, then right towards h8
    file_num = 0
    rank_num = index
    while rank_num > 7:
        rank_num -= 8
        file_num += 1

    return (file_num, rank_num)


def get_square_colour(index):
    """Gets the colour and returns it based off the index passed in."""
    file_num, rank_num = get_file_rank(index)
    if file_num % 2 == 0:
        if rank_num % 2 == 0:
            colour = 'B'
        else:
            colour = 'W'
    else:
        if rank_num % 2 == 0:
            colour = 'W'
        else:
            colour = 'B'
    return colour


def reset():
    """Resets global variables upon restarting the game."""
    global TIMER, SCORE, GAME_STARTED, SQUARE_CHOSEN
    TIMER = 30
    SCORE = 0
    GAME_STARTED = False
    SQUARE_CHOSEN = False
    BUTTON_RESET_COVER.draw(GAME_DISPLAY)
    pygame.display.update()


def main():
    """The main function."""
    pygame.display.set_caption('Square Colour Trainer')
    GAME_DISPLAY.fill(BLUE)
    clock = pygame.time.Clock()
    game_playing = True
    game_over = False

    while game_playing:
        while not game_over:
            redraw_window()
            pygame.display.update()
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                    pygame.quit()
                    quit()

                pos = pygame.mouse.get_pos()
                left_click = pygame.mouse.get_pressed()[0]

                if event.type == pygame.MOUSEBUTTONDOWN and left_click == 1:
                    if BUTTON_EXIT.is_over(pos):
                        exit_game()
                    elif not GAME_STARTED:
                        if BUTTON_START.is_over(pos):
                            start_game()
                        if BUTTON_PLUS1.is_over(pos):
                            add_time_1()
                        elif BUTTON_MINUS1.is_over(pos):
                            minus_time_1()
                        elif BUTTON_PLUS5.is_over(pos):
                            add_time_5()
                        elif BUTTON_MINUS5.is_over(pos):
                            minus_time_5()
                    elif SQUARE_CHOSEN:
                        square_colour = get_square_colour(square_index)
                        if BUTTON_BLACK_SQUARE.is_over(pos):
                            increment_score() if square_colour == 'B' else decrement_score()
                        elif BUTTON_WHITE_SQUARE.is_over(pos):
                            increment_score() if square_colour == 'W' else decrement_score()

                # Updating the colour of a button if it is hovered over
                if event.type == pygame.MOUSEMOTION:
                    BUTTON_EXIT.update_colour(pos)
                    BUTTON_PLUS1.update_colour(pos)
                    BUTTON_PLUS5.update_colour(pos)
                    BUTTON_MINUS1.update_colour(pos)
                    BUTTON_MINUS5.update_colour(pos)
                    if not GAME_STARTED:
                        BUTTON_START.update_colour(pos)

            if GAME_STARTED:
                # Simple timer functionality
                current_time = pygame.time.get_ticks()

                if current_time - STARTED_TIME < 1000:
                    BUTTON_SQUARE.draw(GAME_DISPLAY, '3')
                    pygame.display.update()
                elif current_time - STARTED_TIME < 2000:
                    BUTTON_SQUARE.draw(GAME_DISPLAY, '2')
                    pygame.display.update()
                elif current_time - STARTED_TIME < 3000:
                    BUTTON_SQUARE.draw(GAME_DISPLAY, '1')
                    pygame.display.update()
                elif not SQUARE_CHOSEN:
                    square_index = get_random_square()
                    pygame.display.update()

                if current_time - STARTED_TIME > 3000:
                    update_timer()

            if TIMER == 0:
                game_over = True
                BUTTON_TIMER.draw(GAME_DISPLAY, f'Time: {TIMER}')
                pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_playing = False
                pygame.quit()
                quit()

            BUTTON_RESET.draw(GAME_DISPLAY, 'Reset')
            BUTTON_EXIT.draw(GAME_DISPLAY, 'Exit')
            pygame.display.update()

            pos = pygame.mouse.get_pos()
            left_click = pygame.mouse.get_pressed()[0]

            if event.type == pygame.MOUSEBUTTONDOWN and left_click == 1:
                if BUTTON_RESET.is_over(pos):
                    reset()
                    game_over = False
                if BUTTON_EXIT.is_over(pos):
                    exit_game()

            if event.type == pygame.MOUSEMOTION:
                BUTTON_RESET.update_colour(pos)
                BUTTON_EXIT.update_colour(pos)


# --- Global Variables ---


WIDTH = 400
HEIGHT = 160
GAME_DISPLAY = pygame.display.set_mode((WIDTH, HEIGHT))
BASE_FONT = 'freesansbold.ttf'
TIMER = 30  # The time to play the game
STARTING_TIME = 30  # Will change to what user sets it upon starting anyway
MAX_TIME = 99  # In seconds
MIN_TIME = 1
SCORE = 0
GAME_STARTED = False
STARTED_TIME = 0
SQUARE_CHOSEN = False

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (205, 25, 25)
GREEN = (33, 145, 29)
AQUA = (13, 201, 107)
DARK_AQUA = (48, 144, 96)
ORANGE = (252, 136, 21)
BLUE = (61, 106, 229)
PURPLE = (72, 63, 202)
PINK = (234, 61, 240)

BUTTON_START = button(0, 0, 120, 40, GREEN, ORANGE)
BUTTON_START_OVERWRITE = button(0, 0, 120, 40, BLUE, BLUE)
BUTTON_EXIT = button(0, 40, 120, 40, RED, ORANGE)
BUTTON_TIMER = button(128, 0, 110, 80, BLUE, BLUE)
BUTTON_PLUS1 = button(250, 0, 30, 30, AQUA, DARK_AQUA)
BUTTON_PLUS5 = button(285, 0, 30, 30, AQUA, DARK_AQUA)
BUTTON_MINUS1 = button(250, 50, 30, 30, AQUA, DARK_AQUA)
BUTTON_MINUS5 = button(285, 50, 30, 30, AQUA, DARK_AQUA)
BUTTON_PLUSMINUS = button(250, 0, 70, 80, BLUE, BLUE)
BUTTON_TEXT1 = button(254, 30, 20, 20, BLUE, BLUE)
BUTTON_TEXT5 = button(289, 30, 20, 20, BLUE, BLUE)
BUTTON_SCORE = button(0, 80, 120, 80, BLUE, BLUE)
BUTTON_SQUARE = button(320, 0, 80, 80, ORANGE, ORANGE)
BUTTON_RESET = button(320, 80, 80, 80, DARK_AQUA, ORANGE)
BUTTON_RESET_COVER = button(320, 80, 80, 80, BLUE, BLUE)
BUTTON_BLACK_SQUARE = button(170, 90, 60, 60, BLACK, BLACK)
BUTTON_WHITE_SQUARE = button(250, 90, 60, 60, WHITE, WHITE)


if __name__ == '__main__':
    main()
