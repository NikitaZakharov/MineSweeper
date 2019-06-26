# by zah.nik

# imports
import sys

import pygame as pg
from pygame import locals as pg_consts

from field import Field
from ui import GUI
import constants as consts


# initialize all imported `pygame` modules
pg.init()


class MineSweeper(object):
    """
    Class that supports `run()` method to start the game
    """

    def __init__(self, field=None, gui=None, clock=None):
        # `Field()` object contains methods for business logic for Mine Sweeper game
        self.field = field or Field()
        # `GUI()` object contains methods for building interface
        self.gui = gui or GUI()
        # `Clock()` object helps to track time
        self.clock = clock or pg.time.Clock()

        # responsible for the main game loop
        self.running = True

        # current mouse position
        self._mouse_x = None
        self._mouse_y = None

        # flags to handle some actions
        self._mouse_clicked = False
        self._space_pressed = False

        # initialize game with randomly filled field and creating interface to interact with the field
        self.init()

    def init(self):
        """
        Initialize UI and randomly fill field with mines and numbers
        """
        self.gui.init()
        self.field.init()

    @classmethod
    def terminate(cls):
        """
        Method to exit the game
        """
        pg.quit()
        sys.exit()

    @classmethod
    def handle_quit(cls):
        """
        Handle exit events like Esc-key press and terminate the game
        """
        quit_events = pg.event.get(pg_consts.QUIT)
        key_up_events = pg.event.get(pg_consts.KEYUP)

        if quit_events or (key_up_events and key_up_events[0].key == pg_consts.K_ESCAPE):
            cls.terminate()

    def run(self):
        """
        Main game loop
        """
        while self.running:

            # re-init gui every tick to remove extra highlights from around boxes
            self.gui.init()

            # reset flags
            self._mouse_clicked = False
            self._space_pressed = False

            # check for exit events
            self.handle_quit()

            # draw field with mines and number
            self.gui.update(self.field)

            # event handling loop
            for event in pg.event.get():
                if event.type == pg_consts.QUIT or (event.type == pg_consts.KEYUP and event.key == pg_consts.K_ESCAPE):
                    self.terminate()
                elif event.type == pg_consts.MOUSEMOTION:
                    self._mouse_x, self._mouse_y = event.pos
                elif event.type == pg_consts.MOUSEBUTTONDOWN:
                    self._mouse_x, self._mouse_y = event.pos
                    self._mouse_clicked = True
                elif event.type == pg_consts.KEYDOWN:
                    if event.key == pg_consts.K_SPACE:
                        self._space_pressed = True
                elif event.type == pg_consts.KEYUP:
                    if event.key == pg_consts.K_SPACE:
                        self._space_pressed = False

            # determine boxes at clicked areas
            box_x, box_y = self.gui.get_box_xy(self.field, self._mouse_x, self._mouse_y)

            # mouse not over a box in field
            if (box_x, box_y) != (None, None):

                # highlight unrevealed box
                if not self.field.box_is_checked(box_x, box_y):
                    self.gui.highlight_box(box_x, box_y)

                    # mark mines
                    if self._space_pressed:
                        self.field.mark_mine(box_x, box_y)

                    # reveal clicked boxes
                    if self._mouse_clicked:
                        self.field.reveal_box(box_x, box_y)

                        # when 0 is revealed, show relevant boxes
                        if self.field.box_is_empty(box_x, box_y):
                            self.field.show_numbers(box_x, box_y)

                        # when mine is revealed, show mines
                        if self.field.box_is_mine(box_x, box_y):
                            self.field.reveal_mines()
                            self.gui.lose(self.field)
                            self.clock.tick(consts.FPS)
                            self.field.init()

            # check whether player has won
            if self.field.solved():
                self.gui.win(self.field)
                self.clock.tick(consts.FPS)
                self.field.init()

            # wait clock tick
            pg.display.update()
            self.clock.tick(consts.FPS)


# run game
if __name__ == '__main__':
    game = MineSweeper()
    game.run()
