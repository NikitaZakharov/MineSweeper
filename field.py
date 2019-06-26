import six

import random

import constants as consts


class Field(object):
    """
    `Field` class implements methods to work with field
    """
    MINE = '[X]'
    HIDDEN = '[ ]'
    EMPTY = '[0]'

    def __init__(self, width=consts.FIELD_WIDTH, height=consts.FIELD_HEIGHT, mines_count=consts.MINES_TOTAL):
        assert mines_count < width * height, 'More mines than boxes'

        self.width = width
        self.height = height
        self.mines_count = mines_count

        self._field_matrix = self.fill_matrix_with(self.HIDDEN)
        # what boxs are revealed by user click
        self._revealed_field_matrix = self.fill_matrix_with(False)

        # cords of boxs (x, y) that user marked as mines
        self._marked_mines = []
        # cords of empty boxs (x, y). used for recursion revealing
        self._empty_boxes = []

    def init(self):
        """
        Reset field state and place mines and number
        """
        self._field_matrix = self.fill_matrix_with(self.HIDDEN)
        self._revealed_field_matrix = self.fill_matrix_with(False)
        self._marked_mines = []
        self._empty_boxes = []

        self.place_mines()
        self.place_numbers()

    def show(self):
        """
        Reveal all boxes
        """
        self._revealed_field_matrix = self.fill_matrix_with(True)

    def box_is_mine(self, x, y):
        return self._field_matrix[x][y] == self.MINE

    def box_is_checked(self, x, y):
        return self._revealed_field_matrix[x][y]

    def box_is_empty(self, x, y):
        return self._field_matrix[x][y] == self.EMPTY

    def box_is_marked_as_mine(self, x, y):
        return (x, y) in self._marked_mines

    def mark_mine(self, x, y):
        self._marked_mines.append((x, y))

    def reveal_box(self, x, y):
        self._revealed_field_matrix[x][y] = True

    def solved(self):
        """
        Check whether user won the game
        """
        for x in range(self.width):
            for y in range(self.height):
                if not self.box_is_checked(x, y) and not self.box_is_mine(x, y):
                    return False
        return True

    def adjacent_mines_count(self, x, y):
        """
        Returns number in box or 0
        """
        value = self._field_matrix[x][y]
        # `value` looks like '[2]' where 2 is adjacent mines count
        count = value[1]
        if isinstance(count, six.string_types):
            return int(count)
        return 0

    def fill_matrix_with(self, value=None):
        # returns 2-dim array with specified value
        """
        [[ . . . ], [ . . . ], ...]

        :return:
        """
        matrix = []
        for i in range(self.width):
            matrix.append([])
            for _ in range(self.height):
                matrix[i].append(value)
        return matrix

    def place_mines(self):
        """
        Randomly place `mines_count` mines
        """
        mines_cords = []
        while len(mines_cords) < self.mines_count:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            mine_cords = (x, y)
            if mine_cords not in mines_cords:
                self._field_matrix[x][y] = self.MINE
                mines_cords.append(mine_cords)

    def reveal_mines(self):
        """
        Reveal all mines if user clicked on mine box
        """
        for x in range(self.width):
            for y in range(self.height):
                if self.box_is_mine(x, y):
                    self._revealed_field_matrix[x][y] = True

    def place_numbers(self):
        # places numbers

        for x in range(self.width):
            for y in range(self.height):
                if not self.box_is_mine(x, y):
                    count = 0
                    if x != 0:
                        if self.box_is_mine(x - 1, y):
                            count += 1
                        if y != 0:
                            if self.box_is_mine(x - 1, y - 1):
                                count += 1
                        if y != self.height - 1:
                            if self.box_is_mine(x - 1, y + 1):
                                count += 1
                    if x != self.width - 1:
                        if self.box_is_mine(x + 1, y):
                            count += 1
                        if y != 0:
                            if self.box_is_mine(x + 1, y - 1):
                                count += 1
                        if y != self.height - 1:
                            if self.box_is_mine(x + 1, y + 1):
                                count += 1
                    if y != 0:
                        if self.box_is_mine(x, y - 1):
                            count += 1
                    if y != self.height - 1:
                        if self.box_is_mine(x, y + 1):
                            count += 1
                    self._field_matrix[x][y] = '[%s]' % count

    def show_numbers(self, box_x, box_y):
        """
        Recursively reveal adjacent boxes if empty box was clicked
        """

        self._revealed_field_matrix[box_x][box_y] = True
        self.reveal_adjacent_boxes(box_x, box_y)
        for x, y in self.get_adjacent_boxes_xy(box_x, box_y):
            if self.box_is_empty(x, y) and (x, y) not in self._empty_boxes:
                self._empty_boxes.append((x, y))
                self.show_numbers(x, y)

    def reveal_adjacent_boxes(self, box_x, box_y):
        """
        Reveal all adjacent boxes if empty box was clicked
        """
        if box_x != 0:
            self._revealed_field_matrix[box_x - 1][box_y] = True
            if box_y != 0:
                self._revealed_field_matrix[box_x - 1][box_y - 1] = True
            if box_y != self.height - 1:
                self._revealed_field_matrix[box_x - 1][box_y + 1] = True
        if box_x != self.width - 1:
            self._revealed_field_matrix[box_x + 1][box_y] = True
            if box_y != 0:
                self._revealed_field_matrix[box_x + 1][box_y - 1] = True
            if box_y != self.height - 1:
                self._revealed_field_matrix[box_x + 1][box_y + 1] = True
        if box_y != 0:
            self._revealed_field_matrix[box_x][box_y - 1] = True
        if box_y != self.height - 1:
            self._revealed_field_matrix[box_x][box_y + 1] = True

    def get_adjacent_boxes_xy(self, box_x, box_y):
        """
        Returns list of cords [(x, y), ...] for adjacent boxes
        """

        xy = []

        if box_x != 0:
            xy.append([box_x - 1, box_y])
            if box_y != 0:
                xy.append((box_x - 1, box_y - 1))
            if box_y != self.height - 1:
                xy.append((box_x - 1, box_y + 1))
        if box_x != self.width - 1:
            xy.append((box_x + 1, box_y))
            if box_y != 0:
                xy.append((box_x + 1, box_y - 1))
            if box_y != self.height - 1:
                xy.append((box_x + 1, box_y + 1))
        if box_y != 0:
            xy.append((box_x, box_y - 1))
        if box_y != self.height - 1:
            xy.append((box_x, box_y + 1))

        return xy

