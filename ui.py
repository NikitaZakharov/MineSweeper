import pygame as pg

import constants as consts


class GUI(object):
    """
    `GUI` instance implements methods to represent field on the interface
    """

    def __init__(self, screen=None, basic_font=None):
        self.screen = screen or pg.display.set_mode((consts.WINDOW_WIDTH, consts.WINDOW_HEIGHT))
        self.basic_font = basic_font or pg.font.SysFont(consts.FONT_TYPE, consts.FONT_SIZE)

    def init(self):
        pg.display.set_caption('MineSweeper')
        self.screen.fill(consts.BG_COLOR)
        pg.draw.rect(
            self.screen,
            consts.FIELD_COLOR,
            (consts.FIELD_TOP_LEFT_XY, consts.FIELD_DOWN_RIGHT_XY)
        )

    def draw_field(self):
        for box_x in range(consts.FIELD_WIDTH):
            for box_y in range(consts.FIELD_HEIGHT):
                left, top = self.get_left_top_xy(box_x, box_y)
                pg.draw.rect(self.screen, consts.BOX_COLOR_REV, (left, top, consts.BOX_SIZE, consts.BOX_SIZE))

    @classmethod
    def get_left_top_xy(cls, box_x, box_y):
        """
        Get top left cords for drawing mine boxes
        """
        left = consts.PADDING_SIZE + box_x * (consts.BOX_SIZE + consts.BORDER_SIZE)
        top = consts.PADDING_SIZE + box_y * (consts.BOX_SIZE + consts.BORDER_SIZE)
        return left, top

    def update(self, field):
        """
        Draw updated field
        """
        self.draw_field()
        self.draw_mine_numbers(field)
        self.draw_covers(field)

    def draw_covers(self, field):
        # uses revealed_boxed consts.FIELD_WIDTH x consts.FIELD_HEIGHT data structure to determine whether
        # to draw box covering mine/number
        # draw consts.RED cover instead of gray cover over marked mines

        for box_x in range(field.width):
            for box_y in range(field.height):
                if not field.box_is_checked(box_x, box_y):
                    x, y = self.get_left_top_xy(box_x, box_y)
                    if field.box_is_marked_as_mine(box_x, box_y):
                        pg.draw.rect(self.screen, consts.MINE_MARK_COV, (x, y, consts.BOX_SIZE, consts.BOX_SIZE))
                    else:
                        pg.draw.rect(self.screen, consts.BOX_COLOR_COV, (x, y, consts.BOX_SIZE, consts.BOX_SIZE))

    @classmethod
    def draw_text(cls, text, font, color, surface, x, y):
        """
        Easy text drawing
        """
        text_obj = font.render(text, True, color)
        text_rect = text_obj.get_rect()
        text_rect.centerx = x
        text_rect.centery = y
        surface.blit(text_obj, text_rect)

    @classmethod
    def get_center_xy(cls, box_x, box_y):
        center_x = consts.PADDING_SIZE + consts.BOX_SIZE / 2 + box_x * (consts.BOX_SIZE + consts.BORDER_SIZE)
        center_y = consts.PADDING_SIZE + consts.BOX_SIZE / 2 + box_y * (consts.BOX_SIZE + consts.BORDER_SIZE)
        return center_x, center_y

    @classmethod
    def get_box_xy(cls, field, x, y):
        """
        Get cords of box at mouse cords
        """

        for box_x in range(field.width):
            for box_y in range(field.height):
                left, top = cls.get_left_top_xy(box_x, box_y)
                box_rect = pg.Rect(left, top, consts.BOX_SIZE, consts.BOX_SIZE)
                if x is not None and y is not None and box_rect.collidepoint(x, y):
                    return box_x, box_y
        return None, None

    def highlight_box(self, box_x, box_y):
        """
        Highlight box with border on mouse hover
        """
        left, top = self.get_left_top_xy(box_x, box_y)
        pg.draw.rect(self.screen, consts.HI_LITE_COLOR, (left, top, consts.BOX_SIZE, consts.BOX_SIZE), 4)

    def draw_mine_numbers(self, field):
        """
        Draw mines and number on the GUI using `field` object
        """

        half = int(consts.BOX_SIZE * 0.5)
        quarter = int(consts.BOX_SIZE * 0.25)
        eighth = int(consts.BOX_SIZE * 0.125)

        for box_x in range(field.width):
            for box_y in range(field.height):
                left, top = self.get_left_top_xy(box_x, box_y)
                center_x, center_y = self.get_center_xy(box_x, box_y)
                if field.box_is_mine(box_x, box_y):
                    # draw mine
                    pg.draw.circle(self.screen, consts.MINE_COLOR, (left + half, top + half), quarter)
                    pg.draw.circle(self.screen, consts.WHITE, (left + half, top + half), eighth)
                    pg.draw.line(self.screen, consts.MINE_COLOR, (left + eighth, top + half),
                                 (left + half + quarter + eighth, top + half))
                    pg.draw.line(self.screen, consts.MINE_COLOR, (left + half, top + eighth),
                                 (left + half, top + half + quarter + eighth))
                    pg.draw.line(self.screen, consts.MINE_COLOR, (left + quarter, top + quarter),
                                 (left + half + quarter, top + half + quarter))
                    pg.draw.line(self.screen, consts.MINE_COLOR, (left + quarter, top + half + quarter),
                                 (left + half + quarter, top + quarter))
                else:
                    # draw mines count in box
                    mines_count = field.adjacent_mines_count(box_x, box_y)
                    if mines_count != 0:
                        if mines_count in range(1, 3):
                            color = consts.TEXT_COLOR_1
                        else:
                            color = consts.TEXT_COLOR_2
                        self.draw_text(str(mines_count), self.basic_font, color, self.screen, center_x, center_y)

    def background_animate(self, field, r, g, b):
        """
        Animates background with color blinking
        """
        screen = self.screen.copy()
        surface = pg.Surface(self.screen.get_size())
        surface = surface.convert_alpha()
        speed = 20

        for i in range(5):
            for start, end, step in ((0, 255, 1), (255, 0, -1)):
                for alpha in range(start, end, speed * step):  # animation loop
                    surface.fill((r, g, b, alpha))
                    self.screen.blit(screen, (0, 0))
                    self.screen.blit(surface, (0, 0))
                    pg.draw.rect(self.screen, consts.FIELD_COLOR, (
                        consts.PADDING_SIZE - 5, consts.PADDING_SIZE - 5,
                        (consts.BOX_SIZE + consts.BORDER_SIZE) * consts.FIELD_WIDTH + 5,
                        (consts.BOX_SIZE + consts.BORDER_SIZE) * consts.FIELD_HEIGHT + 5))
                    self.update(field)
                    pg.display.update()

    def lose(self, field):
        """
        Show lose animation
        """
        self.background_animate(field, *consts.RED)

    def win(self, field):
        """
        Show win animation
        """
        self.background_animate(field, *consts.BLUE)
