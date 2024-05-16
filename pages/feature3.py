import streamlit as st
from PIL import Image

def main():
    st.title("Image Uploader")

    uploaded_images = st.file_uploader("Choose image(s) to upload...", accept_multiple_files=True, type=["jpg", "jpeg", "png", "mp4","gif","mov","avi","wmv","webm"])
 
    if uploaded_images is not None:
        for uploaded_image in uploaded_images:
            image = Image.open(uploaded_image)
            st.image(image, caption="Uploaded Image", use_column_width=True)
            st.success("File uploaded successfully!")

    
    st.markdown("---")
    st.write("Disclaimer: This site may collect metadata from uploaded images, including location data.")
    st.write("Please be cautious while uploading images containing sensitive information.")
 

if __name__ == "__main__":
    main()
