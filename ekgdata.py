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
        self.ergebnis = pd.read_csv(ergebnis_pfad, delim_whitespace=True, names=['Amplitude', 'Time'])

    @staticmethod
    def lade_nach_id(id, person_dict):
        if id == "None":
            return {}
        for eintrag in person_dict:
           if eintrag["id"] == id:
               ergebnis= pd.read_csv(eintrag["ergebnis_pfad"], delim_whitespace=True, names=['Amplitude', 'Time'])
               return ergebnis
        else:
            return {}
        

    @staticmethod
    def find_peaks(series, threshold=350):
        ekg_values = series["Amplitude"].values
        peaks = []
        for i in range(1, len(ekg_values) - 1):
            if ekg_values[i] > ekg_values[i - 1] and ekg_values[i] > ekg_values[i + 1] and ekg_values[i] > threshold:
                peaks.append(i)
        peaks_index = pd.Index(peaks, dtype=int)
        series["Peaks"] = np.nan
        series.loc[peaks_index, "Peaks"] = series.loc[peaks_index, "Amplitude"]

        return series, peaks
    
    @staticmethod
    def estimate_hr_dataset(series, threshold=350):
        series_with_peaks, peaks = EKGTest.find_peaks(series, threshold)
        series_with_peaks["HeartRate"] = np.nan
        peak_intervals = np.diff(peaks)
        sampling_rate = 1000 
        heart_rates = 60 / (peak_intervals / sampling_rate)
        for i, peak in enumerate(peaks[1:], start=1):
            series_with_peaks.at[peak, "HeartRate"] = heart_rates[i-1]      
        return series_with_peaks


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