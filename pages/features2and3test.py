# Feature 2 & 3: File Uploader and Metadata Extraction with Folium Map Integration
import streamlit as st
from PIL import Image
from PIL.ExifTags import TAGS
import folium
from streamlit_folium import st_folium

def dms_to_decimal(degrees, minutes, seconds, direction):
    # Convert degrees, minutes, seconds to decimal degrees with proper sign (based on direction)
    decimal_degrees = degrees + (minutes / 60.0) + (seconds / 3600.0)
    if direction in ['S', 'W']:
        decimal_degrees = -decimal_degrees  # Apply negative sign for South and West directions
    return decimal_degrees

def get_exif_data(image):
    exif_data = image._getexif()
    if exif_data is not None:
        exif = {TAGS[k]: v for k, v in exif_data.items() if k in TAGS and TAGS[k] != 'MakerNote'}
        return exif
    return None

def main():
    st.title("Image Uploader, Metadata Extractor & Folium Map")

    uploaded_images = st.file_uploader("Choose image(s) to upload...", accept_multiple_files=True, type=["jpg", "jpeg", "png", "mp4","gif","mov","avi","wmv","webm"])

    if uploaded_images is not None:
        for uploaded_image in uploaded_images:
            image = Image.open(uploaded_image)
            st.image(image, caption="Uploaded Image", use_column_width=True)

            # Extract metadata for location
            exif_data = get_exif_data(image)
            if exif_data is not None and 'GPSInfo' in exif_data:
                gps_info = exif_data['GPSInfo']
                if gps_info is not None:
                    # Extract GPS coordinates (degrees, minutes, seconds, direction)
                    latitude = dms_to_decimal(gps_info[2][0], gps_info[2][1], gps_info[2][2], gps_info[1])  # Latitude
                    longitude = dms_to_decimal(gps_info[4][0], gps_info[4][1], gps_info[4][2], gps_info[3])  # Longitude
                    st.write(f"Approximate Location: Latitude: {latitude:.6f}, Longitude: {longitude:.6f}")

                    # Create Folium Map centered at extracted coordinates
                    m = folium.Map(location=[latitude, longitude], zoom_start=15)
                    folium.Marker([latitude, longitude], popup='Pothole Location').add_to(m)  # Add marker at the location
                    st.write("Map showing approximate location:")
                    st_folium(m)

    st.markdown("---")
    st.write("Disclaimer: This site may collect metadata from uploaded images, including location data.")
    st.write("Please be cautious while uploading images containing sensitive information.")

if __name__ == "__main__":
    main()
