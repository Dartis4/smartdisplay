import os
from PIL import Image, ImageFont, ImageDraw
import weather_data_management as data

try:
    from inky.auto import auto
except ImportError:
    exit("This script requires the inky module\nInstall with: sudo pip install inky")

PATH = os.path.dirname(__file__)
FONT_FACE = "Verdana.ttf"

# Set up the display
try:
    inky_display = auto(ask_user=True, verbose=True)
except TypeError:
    raise TypeError("You need to update the Inky library to >= v1.1.0")


def generate_font(font_face, size):
    return ImageFont.truetype(os.path.join(PATH, font_face), size)


font = generate_font(FONT_FACE, 22)

img = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT))
draw = ImageDraw.Draw(img)

message = "Welcome!"
w, h = font.getsize(message)
x = (inky_display.WIDTH / 2) - (w / 2)
y = (inky_display.HEIGHT / 2) - (h / 2)

draw.text((x, y), message, inky_display.RED, font)
inky_display.set_image(img)
inky_display.show()
