import csv
import pandas as pd
import django
django.setup()
from helpmefind.models import cities 

with open("C:/Users/Admin/OneDrive - St. Clair College/Documents/DAB/DAB304 Lecture/Healthcare Group Project/helpme/fileUpload/docList.csv", 'r') as file:
        reader = csv.DictReader(file)
        unique_cities = set()
        for row in reader:
            unique_cities.add(row["City/Town"])
        for symp in unique_cities:
            cities.objects.create(
                city=symp)
        
