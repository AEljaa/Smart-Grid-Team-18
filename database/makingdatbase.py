import sqlite3
from datetime import date, timedelta
from ..server.flaskBackendServer import *

def creation():
    #connect to it
    db = sqlite3.connect("SPdatabase.db")
    cursor = db.cursor()

    #create tables
    cursor.execute(""" CREATE TABLE IF NOT EXISTS History_table (
    Date VARCHAR(20) NOT NULL,
    Tick INTEGER NOT NULL,
    BuyPrice  INTEGER NOT NULL,
    Demand REAL NOT NULL,
    SellPrice INTEGER NOT NULL,
    PRIMARY KEY (Date,Tick));
    """)

    cursor.execute("""CREATE TABLE IF NOT EXITS Action_table(
    FOREIGN KEY (Date) REFRENCES History_table(Date) ON DELETE CASCADE,
    FOREIGN KEY (Tick) REFRENCES History_table(Tick) ON DELETE CASCADE,
    Met VARCHAR(1) NOT NULL,
    bySolar VARCHAR(1),
    byStored VARCHAR(1),
    byBought VARCHAR(1),
    ChangeinMoney  INTEGER NOT NULL);
    """)
    #save the database
    print("saving")
    db.commit()

    #dis-connect from the database
    print("closing")
    db.close()

    print("Table created")

def showmeall():

    print("Running showmeall")

    # connect to the database
    db = sqlite3.connect("SPdatabase.db")
    cursor = db.cursor()

    # show the entries in the histriy table
    print("HISTROY")
    cursor.execute("SELECT * FROM History_table")
    results = cursor.fetchall()
    for i in results:
        print(i)


    # show the entries in the users table
    print("Actions")
    cursor.execute("SELECT * FROM Action_table")
    results = cursor.fetchall()
    for i in results:
        print(i)
     #save the database
    print("saving")
    db.commit()

    #dis-connect from the database
    print("closing")
    db.close()
def deletedatabase():

    print("Running deletedatabase")
    
    # connect to the database
    db = sqlite3.connect("SPdatabase.db")
    cursor = db.cursor()

    cursor.execute('''DROP TABLE IF EXISTS History_table;''')
    cursor.execute('''DROP TABLE IF EXISTS Action_table;''')
    print("Tables deleted")

     #save the database
    print("saving")
    db.commit()

    #dis-connect from the database
    print("closing")
    db.close()
def addnewtick():
    try:
            # connect to the database
        db = sqlite3.connect("SPdatabase.db")
        cursor = db.cursor()

        date=input("enter date")
        tick=input("enter tick")
        buyprice=input("buy price")
        demand=input("demand")
        sellprice=input("sellproce")
        mycommand= "INSERT INTO History_table (Date,Tick,BuyPrice,Demand,SellPrice) VALUES(?,?,?,?,?)"
        cursor.execute(mycommand, (date,tick,buyprice, demand,sellprice))
        
        met= input("mwt?")
        bysolar=input("solar?")
        bystored=input("by stoed?")
        bybought=input("by bought?")
        Changeinmoney=input("change in money?")
        mycommand= "INSERT INTO Action_table (Date,Tick,Met,bySolar,byStored,byBought,ChangeinMoney) VALUES(?,?,?,?,?,?,?)"
        cursor.execute(mycommand, (date.today(),tick,met, bysolar,bystored,bybought,Changeinmoney))
        
        #save the database
        print("saving")
        db.commit()

        #dis-connect from the database
        print("closing")
        db.close() 
    except:
        print("sorry that was already been inputterd")

def loadinhistory(buyHist, demandHist, sellHist, tick):
    try:
         # connect to the database
        db = sqlite3.connect("SPdatabase.db")
        cursor = db.cursor()

        for i in range (0, len(buyHist)):
            mycommand= "INSERT INTO History_table (Date,Tick,BuyPrice,Demand,SellPrice) VALUES(?,?,?,?,?)"
            cursor.execute(mycommand, (((date.now() - timedelta(1)).strftime('%Y-%m-%d')),tick[i],buyHist[i], demandHist[i],sellHist[i]))
      #save the database
        print("saving")
        db.commit()

        #dis-connect from the database
        print("closing")
        db.close() 
    except:
        print("sorry that was already been inputterd")

if __name__ == "__main__":
    creation()
    buyHist, demandHist, sellHist, tick = cleanData(get_yesterday_data)
    loadinhistory(buyHist, demandHist, sellHist, tick)
    #buyHist, demandHist, sellHist, tick

