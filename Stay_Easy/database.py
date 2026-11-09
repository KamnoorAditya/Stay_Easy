
import sqlite3
db_name="stayeasy.db"
def connect():
    return sqlite3.connect(db_name)
def create_tables():
    conn=connect()
    cur=conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS guests(
            mobile TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS bookings(
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
            FOREIGN KEY (mobile) REFERENCES guests(mobile)
        )
    """)
    conn.commit()
    conn.close()
def get_guest(mobile):
    conn=connect()
    cur=conn.cursor()
    cur.execute("SELECT * FROM guests WHERE mobile=?",(mobile,))
    guest=cur.fetchone()
    conn.close()
    return guest
def insert_guest(mobile,name,email):
    conn=connect()
    cur=conn.cursor()
    cur.execute("INSERT INTO guests(mobile,name,email) VALUES(?,?,?)",(mobile,name,email))
    conn.commit()
    conn.close()
def update_guest(mobile,name,email):
    conn=connect()
    cur=conn.cursor()
    cur.execute("UPDATE guests SET name=?,email=? WHERE mobile=?",(name,email,mobile))
    conn.commit()
    conn.close()
def get_booking(booking_id):
    conn=connect()
    cur=conn.cursor()
    cur.execute("SELECT * FROM bookings WHERE booking_id=?",(booking_id,))
    booking=cur.fetchone()
    conn.close()
    return booking
def insert_booking(mobile,room_no,room_type,check_in,check_out,guest_count,breakfast,status,total_amount,refund_amount=0):
    conn=connect()
    cur=conn.cursor()
    cur.execute("INSERT INTO bookings(mobile,room_no,room_type,check_in,check_out,guest_count,breakfast,status,total_amount,refund_amount) VALUES(?,?,?,?,?,?,?,?,?,?)",(mobile,room_no,room_type,check_in,check_out,guest_count,breakfast,status,total_amount,refund_amount))
    cur.execute("SELECT MAX(booking_id) FROM bookings")
    booking_id=cur.fetchone()[0]
    conn.commit()
    conn.close()
    return booking_id
def update_booking_status(booking_id,status):
    conn=connect()
    cur=conn.cursor()
    cur.execute("UPDATE bookings SET status=? WHERE booking_id=?",(status,booking_id))
    conn.commit()
    conn.close()
def update_refund(booking_id,refund_amount):
    conn=connect()
    cur=conn.cursor()
    cur.execute("UPDATE bookings SET refund_amount=? WHERE booking_id=?",(refund_amount,booking_id))
    conn.commit()
    conn.close()
def get_guest_bookings(mobile):
    conn=connect()
    cur=conn.cursor()
    cur.execute("SELECT * FROM bookings WHERE mobile=?",(mobile,))
    bookings=cur.fetchall()
    conn.close()
    return bookings
#DOne
