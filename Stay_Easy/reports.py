
import csv
from datetime import datetime,timedelta
import database
from room_manager import records
from costs import calculate_prices

def view_booking_details(booking_id):
    conn=database.connect()
    cur=conn.cursor()
    cur.execute("SELECT * FROM bookings WHERE booking_id=?",(booking_id,))
    booking=cur.fetchone()
    if booking is None:
        conn.close()
        print("Booking not found")
        return
    cur.execute("SELECT * FROM guests WHERE mobile=?",(booking[1],))
    guest=cur.fetchone()
    conn.close()
    if guest is None:
        print("Guest details not found")
        return
    print("Booking ID:",booking[0])
    print("Guest Name:",guest[1])
    print("Mobile:",guest[0])
    print("Email:",guest[2])
    print("Room Number:",booking[2])
    print("Room Type:",booking[3])
    print("Check-in:",booking[4])
    print("Check-out:",booking[5])
    print("Guest Count:",booking[6])
    print("Breakfast:",booking[7])
    print("Status:",booking[8])
    print("Total Amount:",booking[9])
    print("Refund Amount:",booking[10])
def guest_history(mobile):
    conn=database.connect()
    cur=conn.cursor()
    cur.execute("SELECT * FROM guests WHERE mobile=?",(mobile,))
    guest=cur.fetchone()
    if guest is None:
        conn.close()
        print("Guest not found")
        return
    cur.execute("SELECT * FROM bookings WHERE mobile=?",(mobile,))
    bookings=cur.fetchall()
    conn.close()
    print("Guest Name:",guest[1])
    print("Mobile:",guest[0])
    print("Email:",guest[2])
    if len(bookings)==0:
        print("No bookings found")
        return
    for booking in bookings:
        print("--------------------")
        print("Booking ID:",booking[0])
        print("Room:",booking[2])
        print("Room Type:",booking[3])
        print("Check-in:",booking[4])
        print("Check-out:",booking[5])
        print("Guest Count:",booking[6])
        print("Breakfast:",booking[7])
        print("Status:",booking[8])
        print("Amount:",booking[9])
        print("Refund:",booking[10])
def occupancy_report(start_date,end_date):
    try:
        start=datetime.strptime(start_date,"%d-%m-%Y").date()
        end=datetime.strptime(end_date,"%d-%m-%Y").date()
    except ValueError:
        print("Invalid date format")
        return
    if end<=start:
        print("End date must be after start date")
        return
    conn=database.connect()
    cur=conn.cursor()
    cur.execute("SELECT room_no,check_in,check_out FROM bookings WHERE status IN ('CONFIRMED','CHECKED_IN')")
    bookings=cur.fetchall()
    conn.close()
    total_rooms=len(records)
    current=start
    total_occupancy=0
    total_nights=(end-start).days
    while current<end:
        occupied=0
        for booking in bookings:
            check_in=datetime.strptime(booking[1],"%d-%m-%Y").date()
            check_out=datetime.strptime(booking[2],"%d-%m-%Y").date()
            if check_in<=current and current<check_out:
                occupied+=1
        if total_rooms>0:
            percentage=(occupied/total_rooms)*100
        else:
            percentage=0
        print(current.strftime("%d-%m-%Y"))
        print("Occupied Rooms:",occupied)
        print("Total Rooms:",total_rooms)
        print("Occupancy:",round(percentage,2),"%")
        total_occupancy+=percentage
        current+=timedelta(days=1)
    if total_nights>0:
        average=total_occupancy/total_nights
        print("Average Occupancy:",round(average,2),"%")
