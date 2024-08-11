import streamlit as st
from PIL import Image
import requests
from io import BytesIO

def main():
    st.markdown("""
        <style>
        body {
            margin: 0;
            padding: 0;
            overflow: hidden;
        }
        .video-background {
            position: fixed;
            right: 0;
            bottom: 0;
            min-width: 100%;
            min-height: 100%;
            width: auto;
            height: auto;
            z-index: -1;
        }
        .stApp {
            background: transparent;
        }
        .center-button {
            display: flex;
            justify-content: center;
        }
        </style>
        <video autoplay muted loop class="video-background">
            <source src="your_video.mp4" type="video/mp4">
        </video>
    """, unsafe_allow_html=True)

    st.title("Image Compression 😊")

    # Option to upload an image or provide a URL
    option = st.selectbox("Choose an option to upload an image:", ("Upload from PC", "Provide URL"))

    if option == "Upload from PC":
        uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png", "bmp", "gif", "tiff"])
        if uploaded_file is not None:
            my_image = Image.open(uploaded_file)
            process_image(my_image, uploaded_file)
    elif option == "Provide URL":
        url = st.text_input("Enter the image URL:")
        if url:
            response = requests.get(url)
            my_image = Image.open(BytesIO(response.content))
            process_image(my_image, BytesIO(response.content))

def process_image(my_image, image_data):
    # Display original image
    st.image(my_image, caption="Original Image", use_column_width=True)

    # Original size of the image
    original_size = round(len(image_data.getvalue()) / 1024, 2)
    st.write(f"The original size of the image is: {original_size} KB")

    # Custom CSS for blue slider and centering the download button
    st.markdown("""
        <style>
        .stSlider > div > div > div > input[type=range] {
            accent-color: blue;
        }
        .center-button {
            display: flex;
            justify-content: center;
        }
        </style>
    """, unsafe_allow_html=True)

    # Compression quality slider
    quality = st.slider("Select compression quality", 0, 100, 30)

    # Compress the image
    compressed_image_io = BytesIO()
    my_image.save(compressed_image_io, format='JPEG', optimize=True, quality=quality)
    compressed_image_io.seek(0)

    # Open the compressed image
    compressed_image = Image.open(compressed_image_io)
    compressed_size = round(len(compressed_image_io.getvalue()) / 1024, 2)

    # Display the sizes
    st.write(f"The size of the compressed image is: {compressed_size} KB")

    st.image(compressed_image, caption="Compressed Image", use_column_width=True)

    # Add download button centered
    st.markdown('<div class="center-button">', unsafe_allow_html=True)
    st.download_button(
        label="Download Compressed Image",
        data=compressed_image_io,
        file_name="compressed_image.jpg",
        mime="image/jpeg"
    )
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()