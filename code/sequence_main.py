# This program runs the popular board game of Sequence.
# The code is based on the pre-poke-framework from UAlberta CMPUT 174 Fall 2020.
# This program is for personal use only. Sequence(R) is property of Jax Ltd.

import os
import pygame


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
    suits = ['H', 'D', 'S', 'C']
    nums = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    images = {}
    for suit in suits:
        for num in nums:
            key = num + suit
            path = os.path.join("card_images", "{}.png".format(key))
            image = pygame.image.load(path)
            images[key] = image
    images['W'] = pygame.image.load(os.path.join("card_images", "W2.png"))
    return images

# User-defined classes


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

        pass

    def create_board(self):
        board_color = pygame.Color((100, 70, 40))
        board_size = [1200, 800]
        board_pos = [0, 0]
        for axis in range(len(board_size)):
            board_pos[axis] = (self.surface.get_size()[axis] - board_size[axis]) // 2
        board = Board(board_pos, board_size, board_color, self.images_dict, self.surface)
        return board


class Board:
    # This class represents the Sequence Board.

    def __init__(self, position, size, color, images, surface):
        self.rect = pygame.Rect(position, size)
        self.size = 10
        self.color = color
        self.surface = surface
        self.images = images
        self.tiles = self.create_tiles()

    def draw(self):
        pygame.draw.rect(self.surface, self.color, self.rect)
        for row in self.tiles:
            for tile in row:
                tile.draw()

    def create_tiles(self):
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

    def create_tile(self, card, i, j):
        gap_size = 5
        image_width = (self.rect.width - gap_size * (self.size + 1)) // self.size
        image_height = (self.rect.height - gap_size * (self.size + 1)) // self.size
        image = self.images[card]
        x = j * (image_width + gap_size) + self.rect.left + gap_size
        y = i * (image_height + gap_size) + self.rect.top + gap_size
        image = pygame.transform.rotate(image, 90)
        image = pygame.transform.scale(image, (image_width, image_height))
        return Tile(card, image, (x, y), (image_width, image_height), self.surface)


class Tile:
    # This class represents a Tile.

    def __init__(self, card, image, position, size, surface):
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
        self.surface.blit(self.image, self.pos)
        if self.is_highlighted:
            pygame.draw.rect(self.surface, pygame.Color('yellow'), self.rect, width=3)
        if self.color is not None:
            pygame.draw.circle(self.surface, self.color, self.centre, 25)


main()
