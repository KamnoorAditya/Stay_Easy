import sqlite3
conn=sqlite3.connect("stayeasy.db")
cur=conn.cursor()
cur.execute(""" CREATE TABLE IF NOT EXISTS guests(
        mobile TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT NOT NULL)""")
cur.execute(""" CREATE TABLE IF NOT EXISTS bookings(
        booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
        mobile TEXT NOT NULL,
        room_no INTEGER NOT NULL,
        room_type TEXT NOT NULL,
        check_in TEXT NOT NULL,
        check_out TEXT NOT NULL,
        guest_count INTEGER NOT NULL,
        breakfast INTEGER NOT NULL,
        status TEXT NOT NULL,
        total_amount REAL NOT NULL,
        refund_amount REAL NOT NULL,
        FOREIGN KEY (mobile) REFERENCES guests(mobile))""")
conn.commit()
print("Success")