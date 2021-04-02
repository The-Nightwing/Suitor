from django.shortcuts import render
from django.db import connection

# Create your views here.

def index(request):
    context = {'column1':[], 'column2':[]}
    with connection.cursor() as cursor:
        cursor.execute("select * from Against;")
        data = cursor.fetchall()
        for tu in data:
            context['column1'].append([tu[0],tu[1]])
        print(data)
    return render(request,'main/index.html',context)