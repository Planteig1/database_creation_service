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
                    room_number,
                    guest_id INTEGER,
                    number_of_guests INTEGER,
                    start_date DATE,
                    end_DATE DATE
                    )""")
        
def create_bill_table():
    #Create the table
    with sqlite3.connect("/app/data/bills.db") as conn:
        cur = conn.cursor()
        cur.execute(""" CREATE TABLE IF NOT EXISTS bills
                    (
                    guest_id INTEGER, 
                    item TEXT,
                    price INTEGER,
                    paid_status BOOLEAN,
                    bill_id INTEGER PRIMARY KEY
                    )
                    """)
        # No initial data is needed - Commit the table
        conn.commit()


def create_rooms_table():
    #Create the table
    with sqlite3.connect("/app/data/rooms.db") as conn:
        cur = conn.cursor()
        cur.execute(""" CREATE TABLE IF NOT EXISTS rooms
                    (
                    room_number INTEGER PRIMARY KEY,
                    room_type TEXT,
                    availability BOOLEAN,
                    cleaned_status BOOLEAN
                    )
                    """)
        # Self made data on the amount of rooms.
        rooms = [
            {"room_type": "Spa Executive", "amount": 3},
            {"room_type": "Grand Lit", "amount": 6},
            {"room_type": "Standard Single", "amount": 20},
            {"room_type": "LOFT Suite", "amount": 4},
            {"room_type": "Suite", "amount": 5},
            {"room_type": "Standard Double", "amount": 15},
            {"room_type": "Junior Suite", "amount": 7},
            {"room_type": "Superior Double", "amount": 2}
]


        # Iteriate through each roomtype and create the right amount of rooms
        for room in rooms:
            current_room_type = room["room_type"]
            amount = room["amount"]
            for amount in range(amount):
                cur.execute(" INSERT INTO rooms (room_type, availability, cleaned_status) VALUES (?,?,?)", (current_room_type, True, True))
        conn.commit()


def create_rooms_price_table():
    with sqlite3.connect("/app/data/datarooms.db") as conn:
        cur = conn.cursor()
        #Create the table with all the data - used to 
        cur.execute(""" CREATE TABLE IF NOT EXISTS datarooms
                    (
                    days_rented INTEGER,
                    season TEXT,
                    price INTEGER,
                    room_type TEXT
                    )
                    """)
        conn.commit()
        
        #Get the data
        data = pandas.read_excel(filepath_rooms, usecols=["Days Rented", "Season", "Price","Room Type"])

        #Format the column names
        data.columns = ["room_type", "days_rented", "season","price"] 
             

        #Insert the data
        data.to_sql("datarooms", conn, if_exists="append", index=False)
        conn.commit()

        # Create the table with calculated data
        cur.execute(""" CREATE TABLE IF NOT EXISTS rooms_pricing
                        (
                        room_type TEXT,
                        season TEXT,
                        daily_price INTEGER
                        )
                        """)
        conn.commit()

        # Run calculations on the dataset and insert the calculated data
        cur.execute("SELECT room_type, season, SUM(price) / SUM(days_rented) AS daily_price FROM datarooms GROUP BY room_type, season")
        result = cur.fetchall()
        #Insert the data into the pricing table
        cur.executemany(""" INSERT INTO rooms_pricing (room_type, season, daily_price) VALUES (?,?,?)""",result)
        conn.commit()


# Run all of the create database functions. 

create_guest_table()
create_drinks_table()
create_booking_table()
create_bill_table()
create_rooms_table()
create_rooms_price_table()