import cv2
import streamlit as st
import numpy as np
from image_comparison import image_comparison
from image_compression import image_compression
import io
import base64
from zipfile import ZipFile
import io as BytesIO
import base64
from base64 import b64encode
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

    if "button_clicked" not in st.session_state:
        st.session_state.button_clicked = False
    
    def callback():
        st.session_state.button_clicked = True
    

    if(st.button("Bandingkan", on_click=callback) or st.session_state.button_clicked):
        # ambil gambar hasil dari fungsi image_com di file image_comparison.py
        image_1_cmp, image_2_cmp, image_3_cmp, image_4_cmp = image_comparison(image_1, image_2)
        col1, col2 = st.columns(2)
        col1.image(image_1_cmp, caption="Original", use_column_width=True, channels="BGR")
        col2.image(image_2_cmp, caption="Modified", use_column_width=True, channels="BGR")
        col1.image(image_3_cmp, caption="Diff", use_column_width=True)
        col2.image(image_4_cmp, caption="Thresh", use_column_width=True)

        # masukan kualiats kompresi
        quality = st.slider('Pilih Kualitas Kompresi (0 - 100)', 0, 100, 50)
        # jika tombol kompresi ditekan
        if st.button("Kompresi"):
            # ambil gambar hasil dari fungsi image_com di file image_compression.py
            compressed_images = image_compression([image_1_cmp, image_2_cmp, image_3_cmp, image_4_cmp], quality=quality)
            # munculkan gambar hasil kompresi
            col1, col2 = st.columns(2)
            for idx, compressed_image in enumerate(compressed_images):
                if idx % 2 == 0:
                    col1.image(compressed_image, caption=f"Compressed Image {idx+1}", use_column_width=True, channels="BGR")
                else:
                    col2.image(compressed_image, caption=f"Compressed Image {idx+1}", use_column_width=True, channels="BGR")

            # deklarasi baris dan kolom
            rows = 2
            cols = 2
            # gabungkan gambar
            image_height, image_width, _ = compressed_images[0].shape
            combined_image = np.zeros((rows * image_height, cols * image_width, 3), dtype=np.uint8)
            # perulanagn untuk menggabungkan gambar
            for i in range(rows):
                for j in range(cols):
                    combined_image[i * image_height : (i + 1) * image_height,
                        j * image_width : (j + 1) * image_width, :] = compressed_images[i * cols + j]
            # membuat numpy array menjadi bytes
            image_bytes = cv2.imencode('.jpg', combined_image)[1].tobytes()
            # membuat tombol download
            st.markdown(
                f'<a href="data:image/jpeg;base64,{b64encode(image_bytes).decode()}" download="hasil_kompresi.jpg">Download Hasil Kompresi</a>',
                unsafe_allow_html=True,
            )


        



