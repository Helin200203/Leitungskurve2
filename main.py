import json
import numpy as np
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from ekgdata import EKGTest
from person import Person
from PIL import Image


def callback_function():
    print(f"The user has changed to {st.session_state.current_user}")
    print(f"The EKG date has changed to {st.session_state.ekg_date}")

@st.cache
def load_person_data():
    return Person.load_person_data()

@st.cache
def get_person_list(person_dict):
    return Person.get_person_list(person_dict)

@st.cache
def load_ekg_data(ekg_id, person_data):
    return EKGTest.lade_nach_id(ekg_id, person_data)

@st.cache
def estimate_heart_rate(ekg, threshold=350):
    return ekg.schaetze_hr(ekg.ergebnis['Amplitude'])

# Initialize session states if not already set
if 'current_user' not in st.session_state:
    st.session_state.current_user = 'None'
if 'picture_path' not in st.session_state:
    st.session_state.picture_path = 'data/pictures/none.jpg'
if 'current_date' not in st.session_state:
    st.session_state.current_date = None
if 'result' not in st.session_state:
    st.session_state.result = None

person_dict = load_person_data()
person_names = get_person_list(person_dict)

st.write("# EKG APP")

col1, col2 = st.columns(2)

with col1:
    st.write("## Versuchsperson auswählen")
    st.session_state.current_user = st.selectbox(
        'Versuchsperson', options=person_names, key="sbVersuchsperson", on_change=callback_function
    )
    current_person_dict = Person.find_person_data_by_name(st.session_state.current_user)

with col2:
    st.write("## Bild der Versuchsperson")
    if st.session_state.current_user in person_names:
        st.session_state.picture_path = current_person_dict["picture_path"]
    image = Image.open("./" + st.session_state.picture_path)
    st.image(image, caption=st.session_state.current_user)

st.write("## EKG Daten")
ekg_data = current_person_dict["ekg_tests"]
ekg_dates = [ekg["datum"] for ekg in ekg_data]
st.session_state.current_date = st.selectbox(
    'Experimentauswahl', options=ekg_dates, key="sbExperimentauswahl", on_change=callback_function
)

selected_ekg_data = next(ekg for ekg in ekg_data if ekg["datum"] == st.session_state.current_date)
ekg = EKGTest(selected_ekg_data["id"], selected_ekg_data["datum"], selected_ekg_data["ergebnis_pfad"])

if st.session_state.result is None:
    st.session_state.result = estimate_heart_rate(ekg)

result = st.session_state.result

# Plotting
fig = go.Figure()

# Plot EKG Signal
fig.add_trace(go.Scatter(x=ekg.ergebnis['Time'], y=ekg.ergebnis['Amplitude'], mode='lines', name='EKG in mV'))

# Plot Peaks
peaks = EKGTest.finde_peaks(ekg.ergebnis['Amplitude'])
fig.add_trace(go.Scatter(x=ekg.ergebnis['Time'].iloc[peaks], y=ekg.ergebnis['Amplitude'].iloc[peaks], mode='markers', name='Peaks', marker=dict(color='red')))

# Update Layout
fig.update_layout(height=600, width=800, title_text="EKG Signal and Heart Rate")
fig.update_xaxes(title_text="Time")
fig.update_yaxes(title_text="EKG in mV")
st.plotly_chart(fig, use_container_width=True)

st.write("## Parameter")
st.write("Max Heartrate", ekg.max_heart_rate(Person.calc_age(current_person_dict["date_of_birth"]), "male"))
st.write("Durchschnittswert in mV", ekg.ergebnis["Amplitude"].mean())

# Main execution
if __name__ == "__main__":
    print("EKG Analyse")
    
    # Load the person data from JSON file
    with open("data/person_db.json", "r") as file:
        person_data = json.load(file)
    
    # Access the first EKG test data for the first person in the JSON
    ekg_dict = person_data[0]["ekg_tests"][0]
    print(ekg_dict)
    
    # Create an instance of EKGTest
    ekg = EKGTest(ekg_dict["id"], ekg_dict["datum"], ekg_dict["ergebnis_pfad"])
    
    # Print the first few rows of the EKG data
    print(ekg.ergebnis.head())
    
st.markdown(
    """
    <style>
    body {
        background-color: #b0c4de;  /* Blaugrau */
        font-family: 'Arial', sans-serif;
    }
    h1, h2 {
        color: #000000;  /* Schwarz */
    }
    .stSelectbox select {
        background-color: #00008b;  /* Dunkelblau */
        color: #ffffff;  /* Weiße Schrift */
    }
    table thead th {
        background-color: #4682b4;  /* Stahlblau */
        color: white;  /* Weißer Text */
        font-size: 18px;
        font-weight: bold;
    }
    table tbody td {
        background-color: #b0c4de;  /* Blaugrauer Hintergrund */
        color: #000000;  /* Schwarzer Text */
        font-size: 16px;
    }
    .stButton button {
        background-color: #00008b;  /* Dunkelblau */
        color: white;  /* Weißer Text */
        font-size: 18px;
        font-weight: bold;
        border-radius: 8px;
    }
    .stTextInput input {
        background-color: #ffffff;  /* Weißer Hintergrund */
        color: #000000;  /* Schwarzer Text */
        font-size: 16px;
        border: 2px solid #00008b;  /* Dunkelblauer Rahmen */
        border-radius: 4px;
    }
    .stImage img {
        border: 2px solid #00008b;  /* Dunkelblauer Rahmen */
        border-radius: 8px;
    }
    .stSlider .stSliderBar {
        background-color: #00008b;  /* Dunkelblauer Hintergrund */
    }
    .stSlider .stSliderHandle {
        background-color: #4682b4;  /* Stahlblauer Griff */
    }
    </style>
    """,
    unsafe_allow_html=True
)
