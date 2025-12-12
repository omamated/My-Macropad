import board
from kmk.kmk_keyboard import KMKKeyboard
from kmk.scanners import DiodeOrientation
from kmk.keys import KC
from kmk.modules.encoder import EncoderHandler
from kmk.extensions.display import Display, TextEntry, ImageEntry
from kmk.extensions.display.ssd1306 import SSD1306

# Create keyboard instance
keyboard = KMKKeyboard()

# Add encoder module
encoder_handler = EncoderHandler()
keyboard.modules.append(encoder_handler)

# Define the matrix for your 6 buttons (3 columns × 2 rows)
keyboard.col_pins = (board.GPIO2, board.GPIO4, board.GPIO3)  # Column_1, Column_2, Column_3
keyboard.row_pins = (board.GPIO0, board.GPIO1)                # Row_1, Row_2
keyboard.diode_orientation = DiodeOrientation.COL2ROW

# Define rotary encoder pins (A, B, Switch)
encoder_handler.pins = (
    (board.GPIO28, board.GPIO27, board.GPIO26),  # A, B, S1 (switch)
)

# OLED Display setup (I2C on GPIO6/SDA and GPIO7/SCL)
i2c_bus = board.I2C()
driver = SSD1306(
    i2c=i2c_bus,
    device_address=0x3C,
)

display = Display(
    display=driver,
    width=128,
    height=32,
)

# Smiley face (16x16 bitmap)
smiley_face = [
    0b00000111, 0b11100000,
    0b00011000, 0b00011000,
    0b00100000, 0b00000100,
    0b01000000, 0b00000010,
    0b10000000, 0b00000001,
    0b10011001, 0b10011001,
    0b10011001, 0b10011001,
    0b10000000, 0b00000001,
    0b10000000, 0b00000001,
    0b10010000, 0b00001001,
    0b10001000, 0b00010001,
    0b01000100, 0b00100010,
    0b00100011, 0b11000100,
    0b00011000, 0b00011000,
    0b00000111, 0b11100000,
    0b00000000, 0b00000000,
]

display.entries = [
    ImageEntry(image=smiley_face, x=0, y=0, width=16, height=16),
    TextEntry(text='Macro Pad', x=20, y=0),
    TextEntry(text='Ready!', x=20, y=16),
]

keyboard.extensions.append(display)

# Keymap definition
# Physical layout:
# Row 1: [Copy]      [Paste]       [Undo]
# Row 2: [Alt-Tab]   [Ctrl+PrtScn] [Win+L]
keyboard.keymap = [
    [
        KC.LCTL(KC.C),           # Key 1: Copy (Ctrl+C)
        KC.LCTL(KC.V),           # Key 2: Paste (Ctrl+V)
        KC.LCTL(KC.Z),           # Key 3: Undo (Ctrl+Z)
        KC.LALT(KC.TAB),         # Key 4: Alt+Tab
        KC.LCTL(KC.PSCR),        # Key 5: Ctrl+Print Screen
        KC.LGUI(KC.L),           # Key 6: Win+L (Lock Windows)
    ]
]

# Encoder map (clockwise, counter-clockwise, press)
encoder_handler.map = [
    ((KC.VOLU, KC.VOLD, KC.MUTE),),  # Volume up, down, mute on press
]

# Start the keyboard
if __name__ == '__main__':
    keyboard.go()