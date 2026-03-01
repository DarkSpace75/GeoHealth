import csv
import django
django.setup()
from helpmefind.models import symptoms 

with open("C:/Users/Admin/OneDrive - St. Clair College/Documents\DAB/DAB304 Lecture/Healthcare Group Project/helpme/helpmefind/SpecialitiesCountDf.csv", 'r') as file:
        reader = csv.DictReader(file)
        symps = reader.fieldnames[1:]
        for symp in symps:
            symptoms.objects.create(
                symptom=symp)
        
