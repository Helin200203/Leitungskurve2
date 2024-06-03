import json
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
class EKGTest:
    def __init__(self, id, datum, ergebnis_pfad):
        self.id = id
        self.datum = datum
        self.ergebnis_pfad = ergebnis_pfad
        self.ergebnis = pd.read_csv(ergebnis_pfad, delim_whitespace=True, names=['Time', 'Amplitude'])

    @staticmethod
    def lade_nach_id(id, person_dict):
        
        if id == "None":
            return {}
        for eintrag in person_dict:
           print(eintrag)
           if eintrag["id"] == id:
               print()
               
               ergebnis= pd.read_csv(eintrag["ergebnis_pfad"], delim_whitespace=True, names=['Time', 'Amplitude'])
               return ergebnis
           
        else:
            return {}
    @staticmethod
    def finde_peaks(series):
        peaks = []
        for i in range(1, len(series) - 1):
            if series[i] > series[i - 1] and series[i] > series[i + 1]:
                peaks.append(i)
        return peaks

    @staticmethod
    def schaetze_hr(series):
        peaks = EKGTest.finde_peaks(series)
        if not peaks:
            raise ValueError("Keine Peaks gefunden.")
        peak_diffs = np.diff(peaks)
        return int(60 / np.mean(peak_diffs))
    
    def max_heart_rate(self, alter : int, sex : str) -> int:
        if sex == 'male':
            max_heart_rate_bpm = 223 - 0.9 * alter
        elif sex == 'female':
            max_heart_rate_bpm = 226 - 1.0 * alter
            
        else:
            raise ValueError("Ungültiger Geschlecht")
        
        return int(max_heart_rate_bpm)

    

    def plot_zeitreihe(self, ergebnis):
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=self.ergebnis['Time'], y=self.ergebnis['Amplitude']))
        return fig 
    
    
    
if __name__ == "__main__":
    print("ekg analayse")
    file = open("data/person_db.json", "r")
    person_data = json.load(file)
    ekg_dict = person_data[0]["ekg_tests"][0]
    print(ekg_dict)
    ekg = EKGTest(ekg_dict)
    print(ekg.df.head())