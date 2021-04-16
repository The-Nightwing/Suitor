from django.shortcuts import render
from django.db import connection
import pandas as pd
from pathlib import Path
import os
from django.shortcuts import HttpResponse
from main.helpers import *
from main.data import *
from django.shortcuts import redirect
from django.http import HttpResponseRedirect

def index(request):
    return render(request,'main/index.html',{})

def login(request):
    return render(request,'main/login.html',{})
#
def loginaccess(request):
   
    if request.POST['username'][0]=='Y':
        writeinfile(request.POST['username'])
        if user_data[request.POST['username']]==request.POST['password']:
            return render(request,'main/paralegal.html',{})
    
    elif request.POST['username'][0]=='I':
        writeinfile(request.POST['username'])
        
        if user_data[request.POST['username']]==request.POST['password']:
            return render(request, 'main/customer.html',{})
    
    elif request.POST['username'][0]=='A':
        writeinfile(request.POST['username'])
        if user_data[request.POST['username']]==request.POST['password']:
            return render(request, 'main/Lawyer.html',{})

    elif request.POST['username'][0]=='O':
        writeinfile(request.POST['username'])
        if user_data[request.POST['username']]==request.POST['password']:
            return render(request, 'main/other_staff.html',{})

    elif request.POST['username']=='Harvey':
        if request.POST['password']=='Specter':
            return render(request,'main/managing_partner.html',{})

    return render(request,'main/user1.html',{})

def paralegal(request):
    
    if request.POST.get("q1"):
        with connection.cursor() as cursor:
            query = """CREATE OR REPLACE VIEW myDetails AS SELECT * FROM Lawyer 
            WHERE userID = "{}";"""

            query = query.format(readfile())
            cursor.execute(query)
            
            cursor.execute("select * from myDetails;")
            data = cursor.fetchall()
        context={}
        columns = ['userID','firstName','middleName','lastName','dateOfBirth','gender','charges','casesWon','casesLost','casesSettled','experience','emailID','phoneNumber','positionAtFirm','avgTimePerCase','streetName','city','pincode','state','specialization','clientRating']

        obj = getdf(context, columns, data)
        return render(request, 'data.html', {'table': obj})
    #query2
    elif request.POST.get("q2"):
        context = {}
        with connection.cursor() as cursor:
            query = "create or replace VIEW myEvents AS select * from Calendar where userID = '{}';"
            query = query.format(readfile())
        
            cursor.execute(query)
            cursor.execute("select * from myEvents;")
            data = cursor.fetchall()
        columns=['userID','when','description']

        obj = getdf(context, columns, data)

        return render(request, 'data.html', {'table': obj})

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

        return render(request, 'data.html', {'table': obj})

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
        return render(request, 'data.html', {'table': obj})

    return render(request,'main/user1.html',{})

def customer(request):
    print(request.POST)
    #query1
    if request.POST.get("q1"):
        with connection.cursor() as cursor:
            query="""create or replace view myDetailsClient as
            select * from IndividualClients
            where userID = "{}";"""
            query = query.format(readfile())
            cursor.execute(query)
            cursor.execute("select * from myDetailsClient;")
            data = cursor.fetchall()
        context={}

        columns = ['userID','firstName','middleName','lastName','dateOfBirth','budget','emailID','phoneNumber','streetName','city','pincode','state','isClient']
        getdf(context, columns, data)
        return render(request, 'data.html')
    #query2
    elif request.POST.get("q2"):
        context = {}
        with connection.cursor() as cursor:
            query = """CREATE OR REPLACE VIEW myEventsClient AS
            select * from Calendar
            where userID = "{}";"""

            query = query.format(readfile())
            
            print(query)
            cursor.execute(query)
            cursor.execute("select * from myEventsClient;")
            data = cursor.fetchall()
        columns=['userID','when','description']

        obj = getdf(context, columns, data)

        return render(request, 'data.html', {'table': obj})

    elif request.POST.get("q3"):
        context = {}
        with connection.cursor() as cursor:
            query = """create or replace view allMyCasesClient as 
            select h.caseID, c.plaintiff, c.lastDateOfActivity, c.flair, c.dateOfFiling, c.duration, c.status, l.userID as LawyerID, l.firstName as LFirstName, l.lastName as LLastName, l.emailID as LEmailID, l.positionAtFirm, l.specialization, l.city as LCity, o.oppositionID, o.firstName as OFirstName, o.lastName as OLastName from Lawyer l, Handles h, LegalCases c, HasA ch, IndividualClients ic, Opposition o, Against a
            where l.userID = h.userID and h.caseID = c.caseID and ch.userID = ic.userID and a.oppositionID = o.oppositionID and a.caseID = c.caseID;
            """            
            cursor.execute(query)
            cursor.execute("select * from allMyCasesClient;")
            data = cursor.fetchall()

        columns = ['caseID', 'plaintiff', 'lastDateOfActivity', 'flair', 'dateOfFiling', 'duration', 'status', 'userID']

        obj = getdf(context,columns,data)

        return render(request, 'data.html', {'table': obj})

    elif request.POST.get("q4"):
        context = {}
        with connection.cursor() as cursor:
            query = """create or replace view myBillsClient as 
            select f.transactionID, f.dateOfPayment, f.description, f.amount, c.caseID, c.flair, c.status from FinancialTransactions f, Invest i, HasA h, LegalCases c
            where f.transactionID = i.transactionid and i.caseID = h.caseID and h.caseID = c.caseID and h.userID = "{}";"""           
            query = query.format(readfile())
            cursor.execute(query)
            cursor.execute("select * from myBillsClient;")
            data = cursor.fetchall()

        columns = ['transactionID', 'dateOfPayment', 'description', 'amount', 'caseID', 'flair', 'status']

        obj = getdf(context, columns, data)
        return render(request, 'data.html', {'table': obj})

    elif request.POST.get("q5"):
        return render(request,'main/form_lawyer.html',{})

    return render(request,'main/user1.html',{})

def user_search_lawyer_query(request):
    specialization = request.POST['specialization']
    clientRating = request.POST['clientRating']
    experience = request.POST['Experience']
    avgtime = request.POST['avgTimePerCase']


    context = {}
    with connection.cursor() as cursor:
        query = """Create or Replace view BestSuitedLawyer as select Lawyer.firstname, Lawyer.lastname, Lawyer.userID from Lawyer 
        where specialization="{}" and experience >= {} and avgTimePerCase <= {} and charges <= 30000 and clientRating >= {} and casesWon div casesLost >= 0;
        """            
        query = query.format(specialization,experience,avgtime,clientRating)
        print(query)
        cursor.execute(query)
        cursor.execute("select * from BestSuitedLawyer;")
        data = cursor.fetchall()

    columns = ['firstName','lastName','userID']

    obj = getdf(context,columns,data)

    return render(request, 'data.html', {'table': obj})

def lawyer(request):
    if request.POST.get("q1"):
        context = {}
        with connection.cursor() as cursor:
            query = """
            CREATE OR REPLACE VIEW LawyerEvents AS
            select * from Calendar
            where userID = "{}";
            """

            query = query.format(readfile())
            cursor.execute(query)
            cursor.execute("select * from LawyerEvents;")
            data = cursor.fetchall()

        columns = ['userID','when','description']

        obj = getdf(context,columns,data)

        return render(request, 'data.html', {'table': obj})

    if request.POST.get("q2"):
        context = {}
        with connection.cursor() as cursor:
            query = """
            CREATE OR REPLACE VIEW LawyerCases AS
            select LegalCases.caseID, plaintiff, lastDateOfActivity, flair, dateOfFiling, duration, LegalCases.status 
            from Handles inner join LegalCases 
            on LegalCases.caseID=Handles.caseID and Handles.userID="{}";
            """
            query = query.format(readfile())
            cursor.execute(query)
            cursor.execute("select * from LawyerCases;")
            data = cursor.fetchall()

        columns = ['caseID', 'plaintiff', 'lastDateOfActivity', 'flair', 'dateOfFiling', 'duration', 'status']

        obj = getdf(context,columns,data)

        return render(request, 'data.html', {'table': obj})

    if request.POST.get("q3"):
        context = {}
        with connection.cursor() as cursor:
            query = """
            create or replace view LawyerDeets as 
            select * from Lawyer where userId="{}";
            """
            query = query.format(readfile())
            cursor.execute(query)
            cursor.execute("select * from LawyerDeets;")
            data = cursor.fetchall()

        columns = ['userID','firstName','middleName','lastName','dateOfBirth','gender','charges','casesWon','casesLost','casesSettled','experience','emailID','phoneNumber','positionAtFirm','avgTimePerCase','streetName','city','pincode','state','specialization','clientRating']

        obj = getdf(context,columns,data)

        return render(request, 'data.html', {'table': obj})

    if request.POST.get("q4"):
        context = {}
        with connection.cursor() as cursor:
            query = """
            create or replace view otherlawyers as
            select firstname, lastname, emailId, specialization, experience, casesLost, casesSettled, avgTimePerCase, clientRating from Lawyer where userId="{}";
            """
            query = query.format(readfile())
            cursor.execute(query)
            cursor.execute("select * from otherlawyers;")
            data = cursor.fetchall()

        columns = ['firstname', 'lastname', 'emailId', 'specialization', 'experience', 'casesLost', 'casesSettled', 'avgTimePerCase', 'clientRating']
        obj = getdf(context,columns,data)

        return render(request, 'data.html', {'table': obj})

    if request.POST.get("q5"):
        context = {}
        with connection.cursor() as cursor:
            query = """
            create or replace view visibleDocs as 
            select d.docID, d.createdOn, d.dateLastModified, d.type, c.caseID, c.lastdateofactivity, c.flair, c.status, c.plaintiff from LegalDocuments d, LegalCases c
            where d.caseID = c.caseID and d.visibility = 1;
            """
            
            cursor.execute(query)
            cursor.execute("select * from visibleDocs;")
            data = cursor.fetchall()

        columns = ['docID', 'createdOn', 'dateLastModified', 'type', 'caseID', 'lastdateofactivity', 'flair', 'status', 'plaintiff']
        obj = getdf(context,columns,data)

        return render(request, 'data.html', {'table': obj})

    if request.POST.get("q6"):
        context = {}
        with connection.cursor() as cursor:
            query = """
            CREATE OR REPLACE VIEW IndividualsAsClients AS
            select * from IndividualClients where userID in (
            select HasA.userID 
            from Handles inner join Lawyer 
            on Handles.userID=Lawyer.userID and Lawyer.userID="{}" 
            inner join HasA 
            on HasA.caseID=Handles.caseID);
            """
            
            query = query.format(readfile())
            cursor.execute(query)
            cursor.execute("select * from IndividualAsClients;")
            data = cursor.fetchall()

        columns = ['userID','firstName','middleName','lastName','dateOfBirth','budget','emailID','phoneNumber','streetName','city','pincode','state','isClient']
        obj = getdf(context,columns,data)

        return render(request, 'data.html', {'table': obj})

    if request.POST.get("q7"):
        context = {}
        with connection.cursor() as cursor:
            query = """ 
            update Lawyer
            set casesWon=casesWon+1
            where userID="{}";
            """            
            # query=query.format(user)
            # cursor.execute(query)
            # cursor.execute("select * from BestSuitedLawyer;")
        return HttpResponseRedirect('login')

    return render(request,'main/user1.html',{})


def otherstaff(request):
    if request.POST.get("q1"):
        with connection.cursor() as cursor:
            query="""create or replace view myDetailsStaff as
            select * from OtherStaff
            where userID = "{}";
            """
            
            query = query.format(readfile())
            cursor.execute(query)
            cursor.execute("select * from myDetailsStaff;")
            data = cursor.fetchall()

        context={}

        columns = ['userID','firstName','middleName','lastName','dateOfBirth','gender','salary','experience','emailID','phoneNumber','positionAtFirm','streetName','city','pincode','state']
        getdf(context, columns, data)
        return render(request, 'data.html')
        
    elif request.POST.get("q2"):
        with connection.cursor() as cursor:
            query="""CREATE OR REPLACE VIEW myEventsStaff AS
            select * from Calendar
            where userID = "{}";
            """
            query = query.format(readfile())
            cursor.execute(query)
            cursor.execute("select * from myEventsStaff;")
            data = cursor.fetchall()
        context={}

        columns = ['userID','when','description']
        getdf(context, columns, data)

        return render(request, 'data.html')

    elif request.POST.get("q3"):
        with connection.cursor() as cursor:
            query="""CREATE OR REPLACE VIEW allFinancialTrans AS
            select * from FinancialTransactions ;
            """
            cursor.execute(query)
            cursor.execute("select * from allFinancialTrans;")
            data = cursor.fetchall()

        context={}

        columns = ['transactionID','dateOfPayment','description','amount','type']
        getdf(context, columns, data)

        return render(request, 'data.html')


def managing_partner(request):
    if request.POST.get("q1"):
        with connection.cursor() as cursor:
            query="""create or replace view myManagingPartner as
            select * from OtherStaff
            where userID = "O21a0b2d6K";
            """
            cursor.execute(query)
            cursor.execute("select * from myManagingPartner;")
            data = cursor.fetchall()

        context={}

        columns = ['userID','firstName','middleName','lastName','dateOfBirth','gender','salary','experience','emailID','phoneNumber','positionAtFirm','streetName','city','pincode','state']
        getdf(context, columns, data)

        return render(request, 'data.html')


    if request.POST.get("q2"):
        with connection.cursor() as cursor:
            query="""CREATE OR REPLACE VIEW myEventsManagement AS
            select * from Calendar
            where userID = "O21a0b2d6K";
            """
            cursor.execute(query)
            cursor.execute("select * from myEventsManagement;")
            data = cursor.fetchall()

        context={}

        columns = ['userID','when','description']
        getdf(context, columns, data)

        return render(request, 'data.html')


    if request.POST.get("q3"):
        with connection.cursor() as cursor:
            query="""CREATE OR REPLACE VIEW allFinancialTrans AS
            select * from FinancialTransactions ;
            """
            cursor.execute(query)
            cursor.execute("select * from allFinancialTrans;")
            data = cursor.fetchall()

        context={}

        columns = ['transactionID','dateOfPayment','description','amount','type']
        getdf(context, columns, data)

        return render(request, 'data.html')


    if request.POST.get("q4"):
        with connection.cursor() as cursor:
            query="""CREATE OR REPLACE VIEW ChooseLawyerRatio AS
            Select *  From Lawyer where round(casesWon/casesLost) in
            (Select max(Ratio) from
            (select userID, round(casesWon/casesLost) as Ratio from Lawyer) as latest);
            """
            cursor.execute(query)
            cursor.execute("select * from ChooseLawyerRatio;")
            data = cursor.fetchall()

        context={}

        columns = ['userID','firstName','middleName','lastName','dateOfBirth','gender','charges','casesWon','casesLost','casesSettled','experience','emailID','phoneNumber','positionAtFirm','avgTimePerCase','streetName','city','pincode','state','specialization','clientRating']
        getdf(context, columns, data)

        return render(request, 'data.html')


    if request.POST.get("q5"):
        with connection.cursor() as cursor:
            query="""
            CREATE OR REPLACE VIEW ChooseLawyerRating AS
            Select Distinct userID, firstName, lastName From Lawyer  where clientRating in 
            (Select max(clientRating) from Lawyer) 
            limit 1;
            """
            cursor.execute(query)
            cursor.execute("select * from ChooseLawyerRating;")
            data = cursor.fetchall()

        context={}

        columns = ['userID','firstName','lastName']
        getdf(context, columns, data)

        return render(request, 'data.html')