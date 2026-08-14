import streamlit.components.v1 as components

def show_map(latitude, longitude):
    url = f"https://www.google.com/maps?q={latitude},{longitude}&output=embed"

    components.iframe(
        url,
        width=700,
        height=450
    )