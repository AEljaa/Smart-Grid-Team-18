import sqlite3

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

    # show the entries in the users table
    print("HISTROY")
    cursor.execute("SELECT * FROM History_table")
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
    print("Tables deleted")

     #save the database
    print("saving")
    db.commit()

    #dis-connect from the database
    print("closing")
    db.close()
def addtick():
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
    addtick()
    showmeall()
    deletedatabase()
    showmeall()