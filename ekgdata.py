import json
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from scipy.signal import find_peaks

class EKGTest:
    def __init__(self, id, datum, ergebnis_pfad):
        self.id = id
        self.datum = datum
        self.ergebnis_pfad = ergebnis_pfad
        self.peaks = []

    @staticmethod
    def lade_nach_id(test_id):
        with open('data/person_db.json', 'r') as file:
            daten = json.load(file)
        for person in daten:
            for test in person['ekg_tests']:
                if test['id'] == test_id:
                    return EKGTest(test['id'], test['date'], test['result_link'])
        return None

    def finde_peaks(self):
        daten = np.loadtxt(self.ergebnis_pfad)
        self.peaks, _ = find_peaks(daten, height=0)

    def schaetze_hr(self):
        if not self.peaks:
            self.finde_peaks()
        if len(self.peaks) > 1:
            dauer = len(self.peaks)
            herzfrequenz = (len(self.peaks) / dauer) * 60
            return herzfrequenz
        return None

    def plot_zeitreihe(self):
        daten = np.loadtxt(self.ergebnis_pfad)
        plt.figure(figsize=(10, 5))
        plt.plot(daten, label='EKG-Daten')
        if self.peaks.size > 0:
            plt.plot(self.peaks, daten[self.peaks], 'ro', label='Peaks')
        plt.title('EKG-Daten')
        plt.xlabel('Zeit')
        plt.ylabel('Amplitude')
        plt.legend()
        st.pyplot(plt)
