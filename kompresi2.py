from PIL import Image
import os

image = Image.open('first.png')

width, height = image.size
new_size = (width // 2, height // 2)

# Konversi gambar ke mode RGB
image = image.convert("RGB")

resized_image = image.resize(new_size)
resized_image.save('compressed_image.jpg', optimize=True, quality=50)

original_size = os.path.getsize('first.png')
compressed_size = os.path.getsize('compressed_image.jpg')

print("Original Size: ", original_size)
print("Compressed Size: ", compressed_size)
