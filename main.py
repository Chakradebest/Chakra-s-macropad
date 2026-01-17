import board
import busio
from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners.keypad import MCP23017
from kmk.modules.encoder import RotaryEncoder
from kmk.extensions.RGB import RGB
from kmk.extensions.display import Display, SSD1306

keyboard = KMKKeyboard()

# 1. Setup I2C for the Screen and the U2 Chip
i2c = busio.I2C(board.SCL, board.SDA)

# 2. Buttons (connected to the U2 Expander)
keyboard.matrix = MCP23017(
    address=0x20,
    pins=[0, 1, 2, 3, 4, 5],
)

# 3. Rotaryencoder Knobs (SW13 and SW14) (for color grading etc...)
encoder_handler = RotaryEncoder()
encoder_handler.pins = (
    (board.D2, board.D3, None), # SW13
    (board.D10, board.D9, None), # SW14
)
keyboard.modules.append(encoder_handler)

# 4. RGB Lights (D1 and D4)
rgb = RGB(pixel_pin=board.D1, num_pixels=2, val=150)
keyboard.extensions.append(rgb)

# 5. OLED Screen
display = Display(display_type=SSD1306, width=128, height=64, i2c=i2c)
keyboard.extensions.append(display)

# 6. What the buttons do (Keymap)
keyboard.keymap = [[KC.A, KC.B, KC.C, KC.D, KC.E, KC.F]]

# 7. What the knobs do
encoder_handler.map = [
    ((KC.VOLD, KC.VOLU),), # Knob 1: Volume
    ((KC.LEFT, KC.RGHT),), # Knob 2: Color Grade (Arrows)
]

if __name__ == '__main__':
    keyboard.go()