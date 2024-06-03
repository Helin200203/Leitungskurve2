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
    def load_person_data(file_path="data/person_db.json"):
        """Eine Funktion, die weiß, wo die Personendatenbank ist, und ein Wörterbuch mit den Personen zurückgibt."""
        with open(file_path, "r") as file:
            person_data = json.load(file)
        return person_data


    @staticmethod
    def get_person_list(person_data):
        """Eine Funktion, die eine Liste von Personen zurückgibt."""
        list_of_names = []
        for eintrag in person_data:
            list_of_names.append(eintrag["lastname"] + ", " +  eintrag["firstname"])
        return list_of_names
    @staticmethod
    def find_person_data_by_name(suchstring):
        """Eine Funktion, der Nachname, Vorname als ein String übergeben wird und die die Person als Dictionary zurückgibt."""
        person_data = Person.load_person_data()
        
        if suchstring == "None":
            return {}

        try:
            lastname, firstname = suchstring.split(", ")
        except ValueError:
            return {}

        for eintrag in person_data:
            if eintrag["lastname"] == lastname and eintrag["firstname"] == firstname:
                return eintrag
            
            else:
                return {}

    def berechne_alter(self):
        heute = datetime.today()
        return heute.year - self.date_of_birth

    def berechne_max_herzfrequenz(self):
        return 220 - self.berechne_alter()

    @staticmethod
    def lade_nach_id(id):
        person_data=Person.load_person_data()
        for person in person_data:
            if person['id'] == id:
                return Person(
                    person['id'], person['date_of_birth'], person['firstname'],
                    person['lastname'], person['picture_path'], person['ekg_tests']
                )
        else:
            return {}
        
if __name__ == "__main__":
    print("Starting tests...")
    persons = Person.load_person_data()
    person_names = Person.get_person_list(persons)
    print(person_names)
    print(Person.find_person_data_by_name("Huber, Julian"))