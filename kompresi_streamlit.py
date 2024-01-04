import streamlit as st
from PIL import Image
import io
import base64


def compress_image(image, quality=50):
    img = Image.open(image)
    img = img.convert("RGB")
    img_io = io.BytesIO()
    img.save(img_io, format='JPEG', quality=quality)
    return img_io


st.title('Aplikasi Kompresi Gambar')

uploaded_file = st.file_uploader("Unggah Gambar", type=['jpg', 'jpeg', 'png'])

if uploaded_file is not None:
    st.image(uploaded_file, caption='Gambar Asli', use_column_width=True)

    quality = st.slider('Pilih Kualitas Kompresi (0 - 100)', 0, 100, 50)
    if st.button('Kompresi'):
        compressed_img = compress_image(uploaded_file, quality)
        st.image(compressed_img, caption='Gambar Setelah Kompresi',
                 use_column_width=True)

        # Tambahkan tombol untuk mengunduh gambar yang telah dikompresi
        compressed_img.seek(0)  # Reset posisi pointer ke awal file
        img_bytes = compressed_img.getvalue()
        encoded = base64.b64encode(img_bytes).decode()
        href = f'<a href="data:image/png;base64,{encoded}" download="compressed_image.png">Download Gambar yang Telah Dikompresi</a>'
        st.markdown(href, unsafe_allow_html=True)
