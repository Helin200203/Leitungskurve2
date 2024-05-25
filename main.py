import streamlit as st
from PIL import Image
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import read_data  # Ihr eigenes Modul
import leistungskurve_2 as ls2d

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

# Herzfrequenz-Zonen
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

#Leistungskurve 2 Aufgaben:
st.subheader("Daten in Tabellendarstellung")
result_df = ls2d.calculate_duration_above_threshold(activity_data)
st.dataframe(result_df)

st.subheader("Daten in Diagrammdarstellung")
fig = px.line(result_df, y='Threshold', x='Max Duration', title='Dauer pro Threshold', labels={'Threshold': 'Threshold in Watt', 'Max Duration': 'Durations in Seconds'})
st.plotly_chart(fig)


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