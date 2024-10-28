import sqlite3
import pandas

filepath_rooms = "/Users/planteig/Desktop/international_names_with_rooms_1000.xlsx"
filepath_drinks = "/Users/planteig/Desktop/drinks_menu_with_sales.xlsx"

def create_guest_table():
    # Create the table
    with sqlite3.connect("guest.db") as conn:
        cur = conn.cursor()
        cur.execute(""" CREATE TABLE IF NOT EXISTS guest
                (
                    id INTEGER PRIMARY KEY,
                    first_name TEXT,
                    last_name TEXT,
                    country TEXT
                )""")
        conn.commit()
        # Get the data
        data = pandas.read_excel(filepath_rooms, usecols=["First Name", "Family Name", "Country"])
        #Format the columns name
        data.columns = ["first_name","last_name","country"]
        
        #Insert data
        data.to_sql("guest", conn, if_exists="append", index=False)
        conn.commit()


def create_drinks_table():
    #Create the table
    with sqlite3.connect("drinks.db") as conn:
        cur = conn.cursor()
        cur.execute(""" CREATE TABLE IF NOT EXISTS drinks
                (
                name TEXT,
                category TEXT,
                price NUMBER,
                units_sold NUMBER
                )""")
        #Get the data
        data = pandas.read_excel(filepath_drinks, usecols=["Drink Name","Category","Price (DKK)", "Units Sold"])
        #Format the columns name 
        data.columns = ["name","category","price","units_sold"]
        #Insert the data
        data.to_sql("drinks", conn, if_exists="append", index=False)
        conn.commit()




    

create_guest_table()
create_drinks_table()


#Change path to make i accessable in the volume
"/Users/planteig/Desktop/international_names_with_rooms_1000.xlsx"

