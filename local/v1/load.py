import csv


# Chargement des bases de données
def load_csv(file_name):
    with open(file_name, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return list(reader)