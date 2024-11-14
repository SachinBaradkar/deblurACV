import streamlit as st
import numpy as np
import cv2
from scipy.signal import wiener
from io import BytesIO
from PIL import Image

# Define the Wiener filter processing function
def apply_wiener_filter(image, kernel_size=5):
    # Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Apply Wiener filter
    filtered_image = wiener(gray_image, (kernel_size, kernel_size))
    # Convert the output back to uint8 type for display
    filtered_image = np.clip(filtered_image, 0, 255).astype(np.uint8)
    return filtered_image

# Streamlit app code
def main():
    # Custom CSS for styling
    st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(to right, #ffecd2, #fcb69f);  /* Soft gradient background */
            font-family: 'Arial', sans-serif;
        }
        .stButton > button {
            background-color: #4CAF50;
            color: white;
            border-radius: 8px;
            padding: 10px 24px;
            font-size: 16px;
        }
        .stButton > button:hover {
            background-color: #45a049;
        }
        .stSlider > div > div > div {
            border-radius: 8px;
        }
        .stImage > img {
            border: 2px solid #ddd;
            padding: 5px;
            border-radius: 10px;
        }
        .footer {
            text-align: center;
            color: gray;
            margin-top: 50px;
        }
        /* Style for text to make it visible */
        h1, h2, h3, h4, p {
            color: #333333;  /* Dark text color for better contrast */
        }
        .stText {
            color: #333333;
        }
        .stMarkdown {
            color: #333333;
        }
        /* Custom style for download button */
        .stDownloadButton > button {
            background-color: #007BFF;  /* Blue color for the button */
            color: white;
            border-radius: 8px;
            padding: 10px 24px;
            font-size: 16px;
        }
        .stDownloadButton > button:hover {
            background-color: #0056b3;  /* Darker blue on hover */
        }
    </style>
    """, unsafe_allow_html=True)

    # Custom header
    st.markdown("<h1 style='text-align: center; color: #4CAF50;'>Clarify</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 18px; color: #333333;'>Upload an image or capture one to apply the Wiener deblurring filter.</p>", unsafe_allow_html=True)
    
    # Instructions section
    st.write("""
        ### How to Use:
        1. You can either upload an image from your device or take a picture using your camera.
        2. Once the image is uploaded or captured, adjust the kernel size to apply the Wiener filter. Wiener filter deblurs and sharpens image.
        3. After deblurring, download the improved image.
    """)

    # Initialize the session state to control the camera opening
    if 'open_camera' not in st.session_state:
        st.session_state.open_camera = False

    # Place both buttons vertically instead of using columns
    st.subheader("1. Upload Image or Capture")
    image_file = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])
    st.button("Take image through Camera", on_click=lambda: st.session_state.update({"open_camera": True}))

    # Show the camera input only if the session state flag is True
    camera_image = None
    if st.session_state.open_camera:
        camera_image = st.camera_input("Take a picture")

    # Process the image if either an uploaded file or a camera capture is available
    if image_file is not None or camera_image is not None:
        if image_file is not None:
            # Read the uploaded image
            image = Image.open(image_file)
        else:
            # Read the captured image from the camera
            image = Image.open(camera_image)

        # Convert the image to an array
        image = np.array(image)

        st.image(image, caption="Original Image", use_column_width=True)

        # Apply Wiener filter
        kernel_size = st.slider("Kernel Size for Wiener Filter", 3, 15, 5, step=2)
        deblurred_image = apply_wiener_filter(image, kernel_size)

        # Show the deblurred image
        st.image(deblurred_image, caption="Deblurred Image", use_column_width=True)

        # Download button for the deblurred image
        result = Image.fromarray(deblurred_image)
        buf = BytesIO()
        result.save(buf, format="PNG")
        byte_im = buf.getvalue()
        
        st.download_button(
            label="Download Deblurred Image",
            data=byte_im,
            file_name="deblurred_image.png",
            mime="image/png"
        )

    
if __name__ == "__main__":
    main()
