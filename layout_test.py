from inky.auto import auto
inky_display = auto()
inky_display.set_border(inky_display.WHITE)

from PIL import Image, ImageFont, ImageDraw

img = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT))
draw = ImageDraw.Draw(img)

path = str(input("Image path: "))
img = Image.open(path)
inky_display.h_flip = True
inky_display.v_flip = True
inky_display.set_image(img)
inky_display.show()
