from django.shortcuts import render
from django.db import connection
import pandas as pd
from pathlib import Path
import os
from django.shortcuts import HttpResponse
from main.helpers import *
# Create your views here.

def index(request):
    return render(request,'main/index.html',{})

def login(request):
    return render(request,'main/login.html',{})
#
def loginaccess(request):
    print(request.POST)
    if request.POST['username']=='paralegal':
        return render(request,'main/paralegal.html',{})
    
    elif request.POST['username']=='customer':
        return render(request, 'main/customer.html',{})

    return render(request,'main/user1.html',{})

def paralegal(request):
    print(request.POST)
    #query1
    if request.POST.get("q1"):
        with connection.cursor() as cursor:
            query = """CREATE OR REPLACE VIEW myDetails AS SELECT * FROM Lawyer 
            WHERE userID = "{}";"""
            query = query.format("A21s9n5a5A")
            cursor.execute()
            
            cursor.execute("select * from myDetails;")
            data = cursor.fetchall()
        context={}
        columns = ['userID','firstName','middleName','lastName','dateOfBirth','gender','charges','casesWon','casesLost','casesSettled','experience','emailID','phoneNumber','positionAtFirm','avgTimePerCase','streetName','city','pincode','state','specialization','clientRating']

        obj = getdf(context, columns, data)
        return render(request, 'main/table.html', {'table': obj})
    #query2
    elif request.POST.get("q2"):
        context = {}
        with connection.cursor() as cursor:
            query = "create or replace VIEW myEvents AS select * from Calendar where userID = '{}';"
            query = query.format("A21s9n5a5A")
            
            print(query)
            cursor.execute(query)
            cursor.execute("select * from myEvents;")
            data = cursor.fetchall()
        columns=['userID','when','description']

        obj = getdf(context, columns, data)

        return render(request, 'main/table.html', {'table': obj})

    elif request.POST.get("q3"):
        context = {}
        with connection.cursor() as cursor:
            query = """create or replace view allCases as 
            select h.caseID, c.plaintiff, c.lastDateOfActivity, c.flair, c.dateOfFiling, c.duration, c.status, ic.userID as ClientID, ic.firstName as CFirstName, ic.lastName as CLastName, ic.emailID as CEmailID, ic.isClient, ic.city as CCity, l.userID as LawyerID, l.firstName as LFirstName, l.lastName as LLastName, l.emailID as LEmailID, l.positionAtFirm, l.specialization, l.city as LCity, o.oppositionID, o.firstName as OFirstName, o.lastName as OLastName from Lawyer l, Handles h, LegalCases c, HasA ch, IndividualClients ic, Opposition o, Against a
            where l.userID = h.userID and h.caseID = c.caseID and ch.userID = ic.userID and a.oppositionID = o.oppositionID and a.caseID = c.caseID;"""
            
            cursor.execute(query)
            cursor.execute("select * from allCases;")
            data = cursor.fetchall()

        columns = ['caseID', 'plaintiff', 'lastDateOfActivity', 'flair', 'dateOfFiling', 'duration', 'status', 'userID']

        obj = getdf(context,columns,data)

        return render(request, 'main/table.html', {'table': obj})

    elif request.POST.get("q4"):
        context = {}
        with connection.cursor() as cursor:
            query = """create or replace view allLegalDocs as 
            select d.docID, d.createdOn, d.dateLastModified, d.type, c.caseID, c.lastdateofactivity, c.flair, c.status, c.plaintiff from LegalDocuments d, LegalCases c
            where d.caseID = c.caseID and d.visibility = 1;"""            
            cursor.execute(query)
            cursor.execute("select * from allLegalDocs;")
            data = cursor.fetchall()

        columns = ['docID', 'createdOn', 'dateLastModified', 'type', 'caseID', 'lastDateofActivity', 'flair', 'status','plaintiff']

        obj = getdf(context, columns, data)
        return render(request, 'main/table.html', {'table': obj})

    return render(request,'main/user1.html',{})


def customer(request):
    print(request.POST)
    #query1
    if request.POST.get("q1"):
        with connection.cursor() as cursor:
            query="""create or replace view myDetailsClient as
            select * from IndividualClients
            where userID = "{}";"""
            query = query.format("I21p5a6t2C")
            cursor.execute(query)
            cursor.execute("select * from myDetailsClient;")
            data = cursor.fetchall()
        context={}

        columns = ['userID','firstName','middleName','lastName','dateOfBirth','budget','emailID','phoneNumber','streetName','city','pincode','state','isClient']
        obj = getdf(context, columns, data)
        return render(request, 'main/table.html', {'table': obj})
    #query2
    elif request.POST.get("q2"):
        context = {}
        with connection.cursor() as cursor:
            query = """CREATE OR REPLACE VIEW myEventsClient AS
            select * from calendar
            where userID = "{}";"""

            query = query.format("I21p5a6t2C")
            
            print(query)
            cursor.execute(query)
            cursor.execute("select * from myEventsClient;")
            data = cursor.fetchall()
        columns=['userID','when','description']

        obj = getdf(context, columns, data)

        return render(request, 'main/table.html', {'table': obj})

    elif request.POST.get("q3"):
        context = {}
        with connection.cursor() as cursor:
            query = """create or replace view allMyCasesClient as 
            select h.caseID, c.plaintiff, c.lastDateOfActivity, c.flair, c.dateOfFiling, c.duration, c.status, l.userID as LawyerID, l.firstName as LFirstName, l.lastName as LLastName, l.emailID as LEmailID, l.positionAtFirm, l.specialization, l.city as LCity, o.oppositionID, o.firstName as OFirstName, o.lastName as OLastName from lawyer l, handles h, legalcases c, hasa ch, individualclients ic, opposition o, against a
            where l.userID = h.userID and h.caseID = c.caseID and ch.userID = ic.userID and a.oppositionID = o.oppositionID and a.caseID = c.caseID;
            """            
            cursor.execute(query)
            cursor.execute("select * from allCasesClient;")
            data = cursor.fetchall()

        columns = ['caseID', 'plaintiff', 'lastDateOfActivity', 'flair', 'dateOfFiling', 'duration', 'status', 'userID']

        obj = getdf(context,columns,data)

        return render(request, 'main/table.html', {'table': obj})

    elif request.POST.get("q4"):
        context = {}
        with connection.cursor() as cursor:
            query = """create or replace view myBillsClient as 
            select f.transactionID, f.dateOfPayment, f.description, f.amount, c.caseID, c.flair, c.status from FinancialTransactions f, Invest i, HasA h, LegalCases c
            where f.transactionID = i.transactionid and i.caseID = h.caseID and h.caseID = c.caseID and h.userID = "{}";"""           
            query = query.format("I21p5a6t2C")
            cursor.execute(query)
            cursor.execute("select * from myBillsClient;")
            data = cursor.fetchall()

        columns = ['transactionID', 'dateOfPayment', 'description', 'amount', 'caseID', 'flair', 'status']

        obj = getdf(context, columns, data)
        return render(request, 'main/table.html', {'table': obj})

    return render(request,'main/user1.html',{})