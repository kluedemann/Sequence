# This program runs the popular board game of Sequence.
# The objective of the game align chips in rows of 5 horizontally, vertically, or diagonally.
# Players take turns playing cards and placing chips in the corresponding locations on the board.
# The first team to reach the required number of Sequences wins the game.
# The code is based on the pre-poke-framework from UAlberta CMPUT 174 Fall 2020.
# This program is for personal use only. Sequence(R) is property of Jax Ltd.

import os
import pygame
import random


# User-defined functions

def main():
    # initialize all pygame modules (some need initialization)
    pygame.init()
    # create a pygame display window
    pygame.display.set_mode((1920, 1020), flags=pygame.RESIZABLE)
    # set the title of the display window
    pygame.display.set_caption('Sequence')
    # get the display surface
    w_surface = pygame.display.get_surface()
    # create a game object
    game = Game(w_surface)
    # start the main game loop by calling the play method on the game object
    game.play()
    # quit pygame and clean up the pygame window
    pygame.quit()


def load_images():
    # Load the images associated with each card.
    # Returns - dict; the images associated with a str card ID (unscaled)
    suits = ['H', 'D', 'S', 'C']
    nums = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    images = {}
    for suit in suits:
        for num in nums:
            key = num + suit
            path = os.path.join("card_images", "{}.png".format(key))
            image = pygame.image.load(path)
            images[key] = image
    images['W'] = pygame.image.load(os.path.join("card_images", "W.png"))
    images['back'] = pygame.image.load(os.path.join("card_images", "card_back.png"))
    return images

# User-defined classes


def setup_deck():
    # Setup and return the deck.
    # returns - list; the cards in the deck

    deck = []
    suits = ['H', 'D', 'S', 'C']
    nums = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    for suit in suits:
        for num in nums:
            deck.append(num + suit)
    deck *= 2
    random.shuffle(deck)
    return deck


class Game:
    # An object in this class represents a complete game.

    def __init__(self, surface):
        # Initialize a Game.
        # - self is the Game to initialize
        # - surface is the display window surface object

        # === objects that are part of every game that we will discuss
        self.surface = surface
        self.bg_color = pygame.Color((0, 75, 0))

        self.FPS = 60
        self.game_Clock = pygame.time.Clock()
        self.close_clicked = False
        self.continue_game = True

        # === game specific objects
        self.images_dict = load_images()
        self.board = self.create_board()
        self.num_players = 2
        self.num_teams = self.get_num_teams()
        self.deck = setup_deck()
        self.num_cards = self.get_num_cards()
        self.hands = self.setup_hands()
        self.num_sequences = [0, 0, 0]
        self.turn_num = 0
        self.colors = [pygame.Color('blue'), pygame.Color('green'), pygame.Color('red')]

        print(self.num_players, self.num_teams, self.num_cards)
        print(self.deck)
        print(self.hands)

    def play(self):
        # Play the game until the player presses the close box.
        # - self is the Game that should be continued or not.

        while not self.close_clicked:  # until player clicks close box
            # play frame
            self.handle_events()
            self.draw()
            if self.continue_game:
                self.update()
                self.decide_continue()
            self.game_Clock.tick(self.FPS)  # run at most with FPS Frames Per Second

    def handle_events(self):
        # Handle each user event by changing the game state appropriately.
        # - self is the Game whose events will be handled

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.close_clicked = True
            elif event.type == pygame.MOUSEBUTTONUP and self.continue_game:
                self.handle_mouse_up(event)
            elif event.type == pygame.MOUSEMOTION and self.continue_game:
                self.handle_mouse_motion(event)

    def draw(self):
        # Draw all game objects.
        # - self is the Game to draw

        self.surface.fill(self.bg_color)  # clear the display surface first
        self.board.draw()
        pygame.display.update()  # make the updated surface appear on the display

    def update(self):
        # Update the game objects for the next frame.
        # - self is the Game to update

        pass

    def decide_continue(self):
        # Check and remember if the game should continue
        # - self is the Game to check

        for num in self.num_sequences:
            if num >= 3:
                self.continue_game = False
                print("Game Over!")

    def create_board(self):
        # Create the Board object.
        # self - Game; the Game object
        # returns - Board; the Sequence Board
        board_color = pygame.Color((100, 70, 40))
        board_size = [1200, 800]
        board_pos = [0, 0]
        for axis in range(len(board_size)):
            board_pos[axis] = (self.surface.get_size()[axis] - board_size[axis]) // 2
        board = Board(board_pos, board_size, board_color, self.images_dict, self.surface)
        return board

    def handle_mouse_up(self, event):
        # Handle mouse up events.
        # self - Game; the Game object
        # event - pygame.Event; the event to be handled

        current_hand = self.hands[self.turn_num % self.num_players]
        current_color = self.colors[self.turn_num % self.num_teams]
        has_moved = self.board.select(event.pos, current_color, current_hand)
        self.num_sequences[self.turn_num % self.num_teams] = self.board.check_sequences(current_color)
        if has_moved:
            self.turn_num += 1
        print(self.num_sequences, self.turn_num)

    def handle_mouse_motion(self, event):
        # Handle mouse motion events.
        # self - Game; the Game object
        # event - pygame.Event; the event to be handled

        pass

    def get_num_teams(self):
        # Determine the number of teams given the number of players.
        # self - Game; the Game object
        # returns - int; the number of teams

        if self.num_players % 3 == 0:
            return 3
        elif self.num_players % 2 == 0:
            return 2
        else:
            print("Number of players must be divisible by 2 or 3.")

    def setup_hands(self):
        # Setup the hands of cards for each player
        # self - Game; the Game object
        # returns - list; a 2D list of str of the card IDs for each player

        hands = []
        for i in range(self.num_cards):
            for player_ind in range(self.num_players):
                if i == 0:
                    hands.append([])
                hands[player_ind].append(self.deck.pop(0))
        return hands

    def get_num_cards(self):
        # Return the number of cards dealt to each player given the number of players.
        # self - Game; the Game object
        # returns - int; the number of cards for each player

        num_cards_dict = {
            2: 7,
            3: 6,
            4: 6,
            6: 5,
            8: 4,
            9: 4,
            10: 3,
            12: 3
        }
        return num_cards_dict.get(self.num_players)


class Board:
    # This class represents the Sequence Board.

    def __init__(self, position, size, color, images, surface):
        # Initialize the Board.
        # self - Board; the Board to initialize
        # position - list; the x and y coordinates of the top-left corner of the Board
        # size - list; the width and height of the Board
        # color - pygame.Color; the color of the Board
        # images - dict; the images associated with each card
        # surface - pygame.Surface; the Game window

        self.rect = pygame.Rect(position, size)
        self.size = 10
        self.color = color
        self.surface = surface
        self.images = images
        self.tiles = self.create_tiles()

    def draw(self):
        # Draw the Board to the screen.
        # self - Board; the Board to draw

        pygame.draw.rect(self.surface, self.color, self.rect)
        for row in self.tiles:
            for tile in row:
                tile.draw()

    def create_tiles(self):
        # Create the Tiles on the Board from a file.
        # self - Board; the Board object

        filename = "board1.txt"
        with open(filename, 'r') as in_file:
            content = in_file.read()
        lines = content.splitlines()
        tiles = []
        for i, line in enumerate(lines):
            cards = line.split(' ')
            row = []
            for j, card in enumerate(cards):
                tile = self.create_tile(card, i, j)
                row.append(tile)
            tiles.append(row)
        return tiles

    def create_tile(self, card, row_ind, col_ind):
        # Initialize the Tiles on the Board.
        # self - Board; the Board object
        # card - str; the ID of the card of the Tile
        # row_ind - int; the row index of the Tile
        # col_ind - int; the column index of the Tile
        # return - Tile; the new Tile object

        gap_size = 5
        image_width = (self.rect.width - gap_size * (self.size + 1)) // self.size
        image_height = (self.rect.height - gap_size * (self.size + 1)) // self.size
        image = self.images[card]
        x = col_ind * (image_width + gap_size) + self.rect.left + gap_size
        y = row_ind * (image_height + gap_size) + self.rect.top + gap_size
        image = pygame.transform.rotate(image, 90)
        image = pygame.transform.scale(image, (image_width, image_height))
        return Tile(card, image, (x, y), (image_width, image_height), self.surface)

    def select(self, position, color, cards):
        # Attempt to play a piece on a Tile on the Board.
        # self - Board; the Board to select
        # color - pygame.Color; the color of the team playing
        # cards - list; the hand of the player playing

        for row in self.tiles:
            for tile in row:
                if tile.select(position, color, cards):
                    return True
        return False

    def check_sequences(self, color):
        # Count the sequences for a given team on the Board.
        # self - Board; the Board to check
        # color - pygame.Color; the color of the team to check
        # returns - int; number of valid sequences

        sequences = 0
        for row_ind in range(self.size):
            for col_ind in range(self.size):
                sequences += self.check_sequence(row_ind, col_ind, color)
        return sequences

    def check_sequence(self, row_ind, col_ind, color):
        # Count the sequences starting from the given Tile.
        # self - Board; the Board to check
        # row_ind - int; the row index of the Tile checked
        # col_ind - int; the column index of the Tile checked
        # color - pygame.Color; the color of the team to check
        # returns - int; the number of sequences formed from this Tile

        right = self.check_right(row_ind, col_ind, color)
        down = self.check_down(row_ind, col_ind, color)
        down_right = self.check_down_right(row_ind, col_ind, color)
        down_left = self.check_down_left(row_ind, col_ind, color)
        directions = [right, down, down_right, down_left]
        count = 0
        for direction in directions:
            if direction == 5 or direction == 10:
                count += 1
        return count

    def check_right(self, row_ind, col_ind, color):
        # Count the length of the series to the right of the Tile.
        # self - Board; the Board to check
        # row_ind - int; the row index of the Tile checked
        # col_ind - int; the column index of the Tile checked
        # color - pygame.Color; the color of the team to check
        # returns - int; the length of the series

        if 0 <= col_ind < self.size:
            if self.tiles[row_ind][col_ind].matches(color):
                return 1 + self.check_right(row_ind, col_ind + 1, color)
        return 0

    def check_down(self, row_ind, col_ind, color):
        # Count the length of the series downward from the Tile.
        # self - Board; the Board to check
        # row_ind - int; the row index of the Tile checked
        # col_ind - int; the column index of the Tile checked
        # color - pygame.Color; the color of the team to check
        # returns - int; the length of the series

        if 0 <= row_ind < self.size:
            if self.tiles[row_ind][col_ind].matches(color):
                return 1 + self.check_down(row_ind + 1, col_ind, color)
        return 0

    def check_down_right(self, row_ind, col_ind, color):
        # Count the length of the series downward and to the right of the Tile.
        # self - Board; the Board to check
        # row_ind - int; the row index of the Tile checked
        # col_ind - int; the column index of the Tile checked
        # color - pygame.Color; the color of the team to check
        # returns - int; the length of the series

        if 0 <= row_ind < self.size and 0 <= col_ind < self.size:
            if self.tiles[row_ind][col_ind].matches(color):
                return 1 + self.check_down_right(row_ind + 1, col_ind + 1, color)
        return 0

    def check_down_left(self, row_ind, col_ind, color):
        # Count the length of the series downward and to the left of the Tile.
        # self - Board; the Board to check
        # row_ind - int; the row index of the Tile checked
        # col_ind - int; the column index of the Tile checked
        # color - pygame.Color; the color of the team to check
        # returns - int; the length of the series

        if 0 <= row_ind < self.size and 0 <= col_ind < self.size:
            if self.tiles[row_ind][col_ind].matches(color):
                return 1 + self.check_down_left(row_ind + 1, col_ind - 1, color)
        return 0


class Tile:
    # This class represents a Tile.

    def __init__(self, card, image, position, size, surface):
        # Initialize a Tile object.
        # self - Tile; the Tile to initialize
        # card - str; the card ID of the Tile
        # image - pygame.Surface; the image representing the Tile
        # position - list; the x and y coordinates of the top-left corner of the Tile
        # surface - pygame.Surface; the Game window

        self.card = card
        self.image = image
        self.pos = position
        self.centre = [0, 0]
        for i in range(2):
            self.centre[i] = self.pos[i] + (size[i] // 2)
        self.rect = pygame.Rect(position, size)
        self.surface = surface
        self.color = None
        self.is_highlighted = False

    def draw(self):
        # Draw the Tile to screen.
        # self - Tile; the Tile to draw

        self.surface.blit(self.image, self.pos)
        if self.is_highlighted:
            pygame.draw.rect(self.surface, pygame.Color('yellow'), self.rect, width=3)
        if self.color is not None:
            pygame.draw.circle(self.surface, self.color, self.centre, 25)

    def select(self, position, color, cards):
        # Check if the Tile can be played on. Update self.color and return True if so.
        # self - Tile; the Tile to select
        # position - list; the x and y coordinates of the mouse click
        # color - pygame.Color; the color of the team selecting the Tile
        # cards - list; the ID of the cards in the player's hand

        if self.rect.collidepoint(position[0], position[1]) and self.card != 'W':
            if self.color is None:
                if self.card in cards or 'JC' in cards or 'JD' in cards:
                    self.color = color
                    return True
            elif self.color != color:
                if 'JS' in cards or 'JH' in cards:
                    self.color = None
                    return True
        return False

    def matches(self, color):
        # Return True if the piece on this Tile matches the color.
        # self - Tile; the Tile to check
        # color - pygame.Color; the color to check for a match

        return self.color == color or self.card == 'W'


main()
