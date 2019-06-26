FPS = 30
# box width and height in pixels
BOX_SIZE = 30
# border for box in pixels
BORDER_SIZE = 5
# field size in boxs count
FIELD_WIDTH = 15
FIELD_HEIGHT = 15

# padding from field to the window edges
PADDING_SIZE = 35

# calculate window size
WINDOW_WIDTH = (BOX_SIZE + BORDER_SIZE) * FIELD_WIDTH + PADDING_SIZE * 2
WINDOW_HEIGHT = (BOX_SIZE + BORDER_SIZE) * FIELD_HEIGHT + PADDING_SIZE * 2

# calculate positions of corners on window
FIELD_TOP_LEFT_XY = PADDING_SIZE - BORDER_SIZE, PADDING_SIZE - BORDER_SIZE
FIELD_DOWN_RIGHT_XY = WINDOW_WIDTH - PADDING_SIZE * 2 + BORDER_SIZE, WINDOW_HEIGHT - PADDING_SIZE * 2 + BORDER_SIZE

# total mines to generate on the field
MINES_TOTAL = 30

# assign colors
LIGHT_GRAY = (225, 225, 225)
DARK_GRAY = (160, 160, 160)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 128, 0)

# set up major colors
BG_COLOR = WHITE
FIELD_COLOR = BLACK
BOX_COLOR_COV = DARK_GRAY  # covered box color
BOX_COLOR_REV = LIGHT_GRAY  # revealed box color
MINE_COLOR = BLACK
TEXT_COLOR_1 = BLUE
TEXT_COLOR_2 = RED
HI_LITE_COLOR = GREEN
MINE_MARK_COV = RED

# set up font
FONT_TYPE = 'Courier New'
FONT_SIZE = 20
