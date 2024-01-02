import cv2
import streamlit as st
import numpy as np
from image_comparison import image_com

# judul web
st.title("Image Comparison")

# upload gambar
upload_file_1 = st.file_uploader("Upload Image 1", type=['png', 'jpeg', 'jpg'])
upload_file_2 = st.file_uploader("Upload Image 2", type=['png', 'jpeg', 'jpg'])

# jika gambar sudah diupload
if upload_file_1 is not None and upload_file_2 is not None:
    # baca gambar
    file_bytes_1 = np.asarray(bytearray(upload_file_1.read()), dtype=np.uint8)
    file_bytes_2 = np.asarray(bytearray(upload_file_2.read()), dtype=np.uint8)
    image_1 = cv2.imdecode(file_bytes_1, cv2.IMREAD_COLOR)
    image_2 = cv2.imdecode(file_bytes_2, cv2.IMREAD_COLOR)

    # deklarasi kolom
    col1, col2 = st.columns(2)

    # tampilkan gambar
    col1.image(image_1, caption="Image 1", use_column_width=True, channels="BGR")
    col2.image(image_2, caption="Image 2", use_column_width=True, channels="BGR")

    # ambil gambar hasil dari fungsi image_com di file image_comparison.py
    image_1, image_2, image_3, image_4 =  image_com(image_1, image_2)
    # jika tombol ditekan
    if st.button("Bandingkan"):
        # tampilkan gambar
        col1, col2 = st.columns(2)
        col1.image(image_1, caption="Original", use_column_width=True, channels="BGR")
        col2.image(image_2, caption="Modified", use_column_width=True, channels="BGR")
        col1.image(image_3, caption="Diff", use_column_width=True)
        col2.image(image_4, caption="Thresh", use_column_width=True)