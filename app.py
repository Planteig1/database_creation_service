import sqlite3
import pandas
import os

# Get file paths from environment variables
filepath_rooms = os.getenv("FILEPATH_ROOMS", "/Users/planteig/Desktop/international_names_with_rooms_1000.xlsx")
filepath_drinks = os.getenv("FILEPATH_DRINKS", "/Users/planteig/Desktop/drinks_menu_with_sales.xlsx")

def create_guest_table():
    # Create the table
    with sqlite3.connect("/app/data/guests.db") as conn:
        cur = conn.cursor()
        cur.execute(""" CREATE TABLE IF NOT EXISTS guests
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
        data.to_sql("guests", conn, if_exists="append", index=False)
        conn.commit()


def create_drinks_table():
    #Create the table
    with sqlite3.connect("/app/data/drinks.db") as conn:
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

def create_booking_table():
    # Get the list of guest id's from the other database
    with sqlite3.connect("/app/data/guests.db") as conn:
        cur = conn.cursor()
        guest_id = pandas.read_sql(" SELECT id FROM guests", conn)
        guest_id.columns = ["guest_id"]



    #Create the table
    with sqlite3.connect("/app/data/bookings.db") as conn:
        cur = conn.cursor()
        cur.execute(""" CREATE TABLE IF NOT EXISTS bookings
                    (
                    booking_id INTEGER PRIMARY KEY,
                    days_rented INTEGER,
                    season TEXT,
                    price INTEGER,
                    room_type TEXT,
                    guest_id INTEGER
                    )""")
        #Get the data
        data = pandas.read_excel(filepath_rooms, usecols=["Days Rented", "Season", "Price","Room Type"])

        #Format the columns name
        data.columns = ["room_type", "days_rented", "season", "price"]

        #Merge the data 
        data["guest_id"] = guest_id["guest_id"]
    

        #Insert the data
        data.to_sql("bookings", conn, if_exists="append", index=False)
        conn.commit()

create_guest_table()
create_drinks_table()
create_booking_table()


#Change path to make i accessable in the volume
#"/Users/planteig/Desktop/international_names_with_rooms_1000.xlsx"