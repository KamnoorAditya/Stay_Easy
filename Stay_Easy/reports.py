
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
def revenue_report():
    conn=database.connect()
    cur=conn.cursor()
    cur.execute("SELECT * FROM bookings")
    bookings=cur.fetchall()
    conn.close()
    room_types=["standard","deluxe","suite"]
    for room_type in room_types:
        completed_stays=0
        room_revenue=0
        gst_collected=0
        cancellation_amount=0
        for booking in bookings:
            if booking[3].lower()!=room_type:
                continue
            if booking[8]=="CHECKED_OUT":
                completed_stays+=1
                for room in records:
                    if room.room_no==booking[2]:
                        bill=calculate_prices(room,booking[4],booking[5],booking[6],bool(booking[7]),0)
                        gst_collected+=bill["gst"]
                        room_revenue+=booking[9]-bill["gst"]
                        break
            elif booking[8]=="CANCELLED":
                cancellation_amount+=booking[9]-booking[10]
        print("--------------------")
        print("Room Type:",room_type)
        print("Completed Stays:",completed_stays)
        print("Room Revenue:",round(room_revenue,2))
        print("GST Collected:",round(gst_collected,2))
        print("Amount Kept From Cancellations:",round(cancellation_amount,2))
def export_bookings():
    conn=database.connect()
    cur=conn.cursor()
    cur.execute("SELECT * FROM bookings")
    bookings=cur.fetchall()
    conn.close()
    with open("bookings_export.csv","w",newline="") as file:
        writer=csv.writer(file)
        writer.writerow(["booking_id","mobile","room_no","room_type","check_in","check_out","guest_count","breakfast","status","total_amount","refund_amount"])
        writer.writerows(bookings)
    print("Bookings exported successfully!")
