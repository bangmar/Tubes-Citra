from PIL import Image

filepath = "first.png"

picture = Image.open(filepath)

picture.save("compressed.png", "PNG", optimize=True, quality=50)