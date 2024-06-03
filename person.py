import json
from datetime import datetime

class Person:
    def __init__(self, id, date_of_birth, firstname, lastname, picture_path, ekg_tests):
        self.id = id
        self.date_of_birth = date_of_birth
        self.firstname = firstname
        self.lastname = lastname
        self.picture_path = picture_path
        self.ekg_tests = ekg_tests

    @staticmethod
    def lade_nach_id(person_id):
        with open('data/person_db.json', 'r') as file:
            daten = json.load(file)
        for person in daten:
            if person['id'] == person_id:
                return Person(
                    person['id'], person['date_of_birth'], person['firstname'],
                    person['lastname'], person['picture_path'], person['ekg_tests']
                )
        return None

    def berechne_alter(self):
        heute = datetime.today()
        return heute.year - self.date_of_birth

    def berechne_max_herzfrequenz(self):
        return 220 - self.berechne_alter()
