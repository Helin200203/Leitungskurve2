import streamlit as st
from PIL import Image
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import read_data  # Ihr eigenes Modul
import leistungskurve_2 as ls2d
from person import Person
from ekgdata import EKGTest

# Laden der Aktivitätsdaten
activity_data = pd.read_csv('activity.csv')

# Berechnungen
mean_power = activity_data['PowerOriginal'].mean()
max_power = activity_data['PowerOriginal'].max()

# Initialisierung von Session State Variablen
if 'current_user' not in st.session_state:
    st.session_state.current_user = 'None'

if 'picture_path' not in st.session_state:
    st.session_state.picture_path = 'data/pictures/none.jpg'

person_names = read_data.get_person_list()

# Anzeige der Leistungsdaten
st.title('Aktivitätsanalyse')
st.write(f"Durchschnittliche Leistung: {mean_power:.2f} W")
st.write(f"Maximale Leistung: {max_power:.2f} W")

# Interaktiver Plot
st.subheader('Leistung und Herzfrequenz über die Zeit')

fig = go.Figure()

fig.add_trace(go.Scatter(x=activity_data.index, y=activity_data['PowerOriginal'],
                         mode='lines', name='Leistung', line=dict(color='blue')))
fig.add_trace(go.Scatter(x=activity_data.index, y=activity_data['HeartRate'],
                         mode='lines', name='Herzfrequenz', line=dict(color='red')))

fig.update_layout(title='Leistung und Herzfrequenz über die Zeit',
                  xaxis_title='Zeit (s)',
                  yaxis_title='Wert',
                  legend=dict(x=0, y=1),
                  template='plotly_white')

st.plotly_chart(fig, use_container_width=True)

# EKG App
st.write("# EKG APP")

col1, col2 = st.columns(2)

with col1:
    st.write("## Versuchsperson auswählen")
    st.session_state.current_user = st.selectbox(
        'Versuchsperson',
        options=person_names, key="sbVersuchsperson")

with col2:
    st.write("## Bild der Versuchsperson")
    if st.session_state.current_user in person_names:
        person_data = read_data.find_person_data_by_name(st.session_state.current_user)
        st.session_state.picture_path = person_data["picture_path"]
        person_id = person_data["id"]
    else:
        person_data = None
        person_id = None

    image = Image.open("./" + st.session_state.picture_path)
    st.image(image, caption=st.session_state.current_user)

if person_id:
    person = Person.lade_nach_id(person_id)
    if person:
        st.write(f"Name: {person.firstname} {person.lastname}")
        st.write(f"Alter: {person.berechne_alter()}")
        st.write(f"Maximale Herzfrequenz: {person.berechne_max_herzfrequenz()}")

        test_dates = [test['date'] for test in person.ekg_tests]
        if test_dates:
            selected_date = st.selectbox("EKG-Test Datum auswählen", test_dates)
            selected_test = next(test for test in person.ekg_tests if test['date'] == selected_date)
            test_id = selected_test['id']
            ekg_test = EKGTest.lade_nach_id(test_id)
            if ekg_test:
                st.write(f"Datum des Tests: {ekg_test.datum}")
                ekg_test.finde_peaks()

                # EKG-Daten anzeigen
                st.write("EKG-Daten erfolgreich geladen:")
                ekg_data = pd.read_csv(ekg_test.ergebnis_pfad, delim_whitespace=True, names=['Time', 'Amplitude'])
                st.table(ekg_data.head())

                # Peaks in einer Tabelle anzeigen
                st.write("Gefundene Peaks:")
                if ekg_test.peaks:
                    peaks_df = pd.DataFrame(ekg_test.peaks, columns=['Peak Position'])
                    st.table(peaks_df)
                else:
                    st.write("Keine Peaks gefunden.")
                
                # Durchschnittspuls berechnen und anzeigen
                try:
                    avg_hr = ekg_test.schaetze_hr()
                    st.write(f"Geschätzte Herzfrequenz: {avg_hr}")
                except Exception as e:
                    st.error(f"Fehler bei der Schätzung der Herzfrequenz. Überprüfen Sie die Peaks. {e}")
                
                # EKG-Daten plotten
                st.write("EKG-Daten Plot:")
                ekg_test.plot_zeitreihe()
            else:
                st.error("Fehler beim Laden des EKG-Tests.")
        else:
            st.warning("Keine EKG-Tests für diese Person gefunden.")
    else:
        st.error("Person nicht gefunden. Bitte geben Sie eine gültige ID ein.")

# Herzfrequenz-Zonen
st.title('Herzfrequenz-Zonen Analyse')
max_heart_rate = st.number_input('Maximale Herzfrequenz', min_value=100, max_value=220, value=190, step=1)
zone_times, avg_power = read_data.calculate_zones(max_heart_rate, activity_data['HeartRate'], activity_data['PowerOriginal'])

# Zeit in Herzfrequenz-Zonen als Tabelle darstellen
st.subheader('Zeit in Herzfrequenz-Zonen')
zone_times_df = pd.DataFrame(list(zone_times.items()), columns=['Zone', 'Zeit (s)'])
st.table(zone_times_df)

# Durchschnittliche Leistung in den Zonen als Tabelle darstellen
st.subheader('Durchschnittliche Leistung in den Zonen')
avg_power_df = pd.DataFrame(list(avg_power.items()), columns=['Zone', 'Durchschnittliche Leistung (W)'])
st.table(avg_power_df)

# Leistungskurve 2 Aufgaben:
st.subheader("Daten in Tabellendarstellung")
result_df = ls2d.calculate_duration_above_threshold(activity_data)
st.dataframe(result_df)

st.subheader("Daten in Diagrammdarstellung")
fig = px.line(result_df, y='Threshold', x='Max Duration', title='Dauer pro Threshold', labels={'Threshold': 'Threshold in Watt', 'Max Duration': 'Durations in Seconds'})
st.plotly_chart(fig)

# Style-Anpassungen
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
