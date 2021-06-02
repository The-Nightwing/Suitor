import os
import mysql.connector

os.system('cls')
print('Welcome to Suitor')
user = input("Enter Username: ")
password = input("Enter Password: ")

mydb = mysql.connector.connect(
    host="suitor.czjiaq8hoddl.us-east-2.rds.amazonaws.com",
    user=user,
    password=password,
    database='suitor'
    )

while True:

    cursor = mydb.cursor()
    cursor.execute("Select * from Against;")
    data  = cursor.fetchall()
    for d in data:
        print(d)
    
    print("Want to continue as the same user? Press 1, to change user 2, else 3")
    c = int(input())
    if c==1:
        continue
    elif c==2:
        user = input()
        password = input()
        mydb.disconnect()
        mydb = mysql.connector.connect(
        host="suitor.czjiaq8hoddl.us-east-2.rds.amazonaws.com",
        user=user,
        password=password,
        database='suitor'
        )
        continue
    else:
        mydb.disconnect()
        exit()