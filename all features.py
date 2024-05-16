import streamlit as st
from PIL import Image
from PIL.ExifTags import TAGS
import folium
from streamlit_folium import st_folium
import openai
import os

# Set up the OpenAI API key
openai.api_key = os.getenv("API_Key")

def dms_to_decimal(degrees, minutes, seconds, direction):
    decimal_degrees = degrees + (minutes / 60.0) + (seconds / 3600.0)
    if direction in ['S', 'W']:
        decimal_degrees = -decimal_degrees
    return decimal_degrees

def get_exif_data(image):
    exif_data = image._getexif()
    if exif_data is not None:
        exif = {TAGS[k]: v for k, v in exif_data.items() if k in TAGS and TAGS[k] != 'MakerNote'}
        return exif
    return None

def query_openai_about_image(image_description):
    response = openai.ChatCompletion.create(
        model="gpt-4.5-turbo",
        messages=[{"role": "user", "content": f"Describe this image: {image_description}"}],
        max_tokens=300
    )
    return response.choices[0].message['content']

def main():
    st.title("Image Uploader, Metadata Extractor & Folium Map with AI Insights")

    uploaded_images = st.file_uploader("Choose image(s) to upload...", accept_multiple_files=True, type=["jpg", "jpeg", "png"])
    if uploaded_images is not None:
        for uploaded_image in uploaded_images:
            image = Image.open(uploaded_image)
            st.image(image, caption="Uploaded Image", use_column_width=True)

            exif_data = get_exif_data(image)
            if exif_data is not None and 'GPSInfo' in exif_data:
                gps_info = exif_data['GPSInfo']
                if gps_info:
                    latitude = dms_to_decimal(gps_info[2][0], gps_info[2][1], gps_info[2][2], gps_info[1])
                    longitude = dms_to_decimal(gps_info[4][0], gps_info[4][1], gps_info[4][2], gps_info[3])
                    st.write(f"Approximate Location: Latitude: {latitude:.6f}, Longitude: {longitude:.6f}")

                    m = folium.Map(location=[latitude, longitude], zoom_start=15)
                    folium.Marker([latitude, longitude], popup='Image Location').add_to(m)
                    st.write("Map showing approximate location:")
                    st_folium(m, width=725, height=500)

            # Get image description and query OpenAI
            image_description = "An example description based on what you know or infer about the image."
            openai_response = query_openai_about_image(image_description)
            st.write("Insights from AI:")
            st.write(openai_response)

    st.markdown("---")
    st.write("Disclaimer: This site may collect metadata from uploaded images, including location data.")
    st.write("Please be cautious while uploading images containing sensitive information.")

if __name__ == "__main__":
    main()
