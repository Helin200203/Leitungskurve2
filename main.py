import json
import numpy as np
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from ekgdata import EKGTest
from person import Person
from PIL import Image
import plotly.graph_objects as go
from plotly.subplots import make_subplots

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
ekg_dates = [ekg["date"] for ekg in ekg_data]
st.session_state.current_date = st.selectbox(
    'Experimentauswahl', options=ekg_dates, key="sbExperimentauswahl", on_change=callback_function
)

selected_ekg_data = next(ekg for ekg in ekg_data if ekg["date"] == st.session_state.current_date)
ekg = EKGTest(selected_ekg_data["id"], selected_ekg_data["date"], selected_ekg_data["result_link"])

ekg.ergebnis = EKGTest.estimate_hr_dataset(ekg.ergebnis)
# Erstellen eines DataFrames

# Dateiname
datei_name = 'ekg_ergebnis.txt'

# Speichern des DataFrames in eine Textdateie
ekg.ergebnis.to_csv(datei_name, index=False, sep='\t')

print(f"Das Array wurde erfolgreich in {datei_name} gespeichert.")

# Create subplots
fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.1,
                    subplot_titles=("EKG Signal", "Heart Rate"))

# Plot EKG Signal
fig.add_trace(go.Scatter(x=ekg.ergebnis['Time'], y=ekg.ergebnis['Amplitude'], mode='lines', name='EKG in mV'), row=1, col=1)

# Plot Peaks
fig.add_trace(go.Scatter(x=ekg.ergebnis['Time'], y=ekg.ergebnis['Peaks'], mode='markers', name='Peaks', marker=dict(color='red')), row=1, col=1)

#Komischerweise funktioniert es leider nicht, sodass die x-Achse bei dm oberen Graph, der länge des unteren Graphes entspricht.
# Ich habe hierfür mit Matthias zusammengearbeitet, aber wir sind nicht auf das richtige Ergebnis gekommen
# bei ihm funktioniert es aber bei mir nicht, was die Sache noch komischer macht.
fig.add_trace(go.Scatter(x=ekg.ergebnis.index, y=ekg.ergebnis["HeartRate"], mode='markers', name='Heart Rate', marker=dict(color='blue')),
              row=2, col=1)

peak_indices = ekg.ergebnis.dropna(subset=["HeartRate"]).index 
# Plot Heart Rate (interpolated over entire series)
fig.add_trace(go.Scatter(x=peak_indices, y=ekg.ergebnis.loc[peak_indices, "HeartRate"], mode='lines', name='Heart Rate', marker=dict(color='blue'), line=dict(color='green')), row=2, col=1)

# Update Layout
fig.update_layout(height=600, width=800, title_text="EKG Signal and Heart Rate")
fig.update_xaxes(title_text="Time", row=2, col=1)
fig.update_yaxes(title_text="EKG in mV", row=1, col=1)
fig.update_yaxes(title_text="Heart Rate", row=2, col=1)

st.plotly_chart(fig, use_container_width=True)

st.write("## Parameter")
st.write("Durchschnittswert in mV", ekg.ergebnis["Amplitude"].mean())

    
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
