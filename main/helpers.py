from django.shortcuts import render
from django.db import connection
import pandas as pd
from pathlib import Path
import os
from django.shortcuts import HttpResponse


def getdf(context, columns, data):
    for c in columns:
        context[c] = []
            
    for d in data:
        for i in range(len(columns)):
            context[columns[i]].append(d[i])
    BASE_DIR = Path(__file__).resolve().parent.parent

    df = pd.DataFrame.from_dict(context)
    df.to_csv(os.path.join(BASE_DIR,'use.csv'),index=False)

    df = pd.read_csv(os.path.join(BASE_DIR,'use.csv'))
    obj = df.to_html()

    return obj