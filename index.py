import cv2
import streamlit as st
import numpy as np
from image_comparison import image_comparison
from image_compression import image_compression
import io
import base64
from zipfile import ZipFile
# judul web
st.title("Image Comparison")

# upload gambar
upload_file_1 = st.file_uploader("Upload Image 1", type=['png', 'jpeg', 'jpg'])
upload_file_2 = st.file_uploader("Upload Image 2", type=['png', 'jpeg', 'jpg'])


# fungsi untuk mengubah gambar menjadi bytes
def image_to_bytes(compressed_image):
    _, buffer = cv2.imencode('.png', cv2.cvtColor(compressed_image, 1))
    
    img_byte_array = io.BytesIO(buffer.tobytes())
    
    return img_byte_array.getvalue()


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

    bandingkan_button_clicked = False
    kompresi_button_clicked = False

    # bandingkan_button_clicked = st.button("Bandingkan")

    if 'image_state' not in st.session_state:
        st.session_state.image_state = {
            'image_1_cmp': None,
            'image_2_cmp': None,
            'image_3_cmp': None,
            'image_4_cmp': None
        }

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

            # membuat zip file
            zip_file_name = "hasil_images.zip"
            with st.spinner("Creating ZIP file..."):
                with ZipFile(zip_file_name, "w") as zip_file:
                    for idx, compressed_image in enumerate(compressed_images):
                        image_bytes = image_to_bytes(compressed_image)
                        zip_file.writestr(f"Compressed_Image_{idx+1}.png", image_bytes)

            # membuka zip file
            with open(zip_file_name, "rb") as zip_file:
                zip_data = zip_file.read()

            # membuat tombol download
            download_button = st.download_button(
                label="Download Hasil Kompresi",
                key='download_button',
                data=zip_data,
                file_name=zip_file_name,
                mime="application/zip",
            )


        



