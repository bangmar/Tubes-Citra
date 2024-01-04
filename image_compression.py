import cv2
import io
import base64
import numpy as np

def image_compression(images, quality=50):
    compressed_images = []

    # perulangan untuk setiap gambar
    for image in images:
        # kompresi gambar
        _, buf = cv2.imencode(".jpg", image, [int(cv2.IMWRITE_JPEG_QUALITY), quality])

        # konversi bytes ke gambar
        compressed_image = cv2.imdecode(np.frombuffer(buf, dtype=np.uint8), cv2.IMREAD_COLOR)

        # tambahkan gambar ke list
        compressed_images.append(compressed_image)

    return compressed_images

