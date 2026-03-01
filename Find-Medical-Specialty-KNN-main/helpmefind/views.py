from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse

from sklearn.metrics import confusion_matrix, classification_report
import seaborn as sns
import matplotlib.pyplot as plt

from .models import symptoms, cities

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn import preprocessing 
from django.conf import settings
import joblib

# Load pre-trained models
findSpecialist = joblib.load("C:\\Users\\parth\\Documents\\Main_pro\\Find-Medical-Specialty-KNN-main\\helpmefind\\findSpecialist.joblib")
label_encoder = joblib.load("C:\\Users\\parth\\Documents\\Main_pro\\Find-Medical-Specialty-KNN-main\\helpmefind\\findSpecialistlabel.joblib")

def Specialty(test): 
    SpecialitiesCountDf = pd.read_csv("C:\\Users\\parth\\Documents\\Main_pro\\Find-Medical-Specialty-KNN-main\\helpmefind\\SpecialitiesCountDf.csv")
    label_encoder = preprocessing.LabelEncoder() 
    SpecialitiesCountDf['Specialty'] = label_encoder.fit_transform(SpecialitiesCountDf['Specialty']) 
    y = SpecialitiesCountDf["Specialty"]
    X = SpecialitiesCountDf.drop(["Specialty"], axis=1)
    X = X.reindex(sorted(X.columns), axis=1)
    X_train, X_test, Y_train, Y_test = train_test_split(X, y, test_size=0.2)
    classifier = KNeighborsClassifier(n_neighbors=5, metric="jaccard")
    classifier.fit(X_train, Y_train)

    

    
    X_test = pd.DataFrame(test)
    X_test[X_train.columns[~X_train.columns.isin(X_test.columns)]] = 0
    X_test = X_test.reindex(sorted(X_test.columns), axis=1)
    return label_encoder.inverse_transform(classifier.predict(X_test))

def getDocList(pred, city, origin=None):
    df = pd.read_csv("C:\\Users\\parth\\Documents\\Main_pro\\Find-Medical-Specialty-KNN-main\\helpmefind\\docList.csv")
    df = df[(df["pri_spec"] == pred) & (df["City/Town"] == city)]
    df["ZIP Code"] = df["ZIP Code"].astype(str).str[:5]
    
    # Add dummy distance and duration columns
    df["Distance"] = np.nan
    df["Duration"] = np.nan
    
    df.sort_values(by=["ZIP Code"], inplace=True)
    return df

def find_doctor(request):  
    symps = symptoms.objects.all()
    listSymps = [symp.symptom for symp in symps]
    citie = cities.objects.all()
    listCity = [ci.city for ci in citie]

    if request.method == 'POST':
        listSelectedSympt = [request.POST.get(f"select{i+1}") for i in range(5)]
        test = [{key: 1 for key in listSelectedSympt}]
        X_test = pd.DataFrame(test)
        columns = np.setdiff1d(listSymps, list(X_test.columns))
        columns = [str(col) for col in columns]
        X_test[columns] = 0
        X_test.columns = X_test.columns.astype(str)
        print("Column types:", [type(col) for col in X_test.columns])
        X_test = X_test.reindex(sorted(X_test.columns), axis=1)
        pred = label_encoder.inverse_transform(findSpecialist.predict(X_test))
        city = request.POST.get("select6")
        origin = request.POST.get("zipcode")
        df = getDocList(pred[0], city, origin)
        df1 = df.head(10)
        csv_data = df.to_csv(str(settings.BASE_DIR) + "/media/fullData.csv", index=False)
        top_csv_data = df1.to_csv(str(settings.BASE_DIR) + "/media/data.csv", index=False)
        response1 = HttpResponse(csv_data, content_type='text/csv')
        response1['Content-Disposition'] = 'attachment; filename="data.csv"'
        response2 = HttpResponse(top_csv_data, content_type='text/csv')
        response2['Content-Disposition'] = 'attachment; filename="data.csv"'
        return render(request, 'index.html', {
            'listSymps': listSymps,
            'listCity': listCity,
            'pred': pred[0],
            'response2': '/media/fullData.csv',
            'response1': '/media/data.csv'
        })

    else:
        return render(request, 'index.html', {"listSymps": listSymps, "listCity": listCity})
