
from datetime import datetime
import database
from models import Guest,Booking
from costs import calculate_prices
from room_manager import availability
from validation import validate_name,validate_mobile,validate_email
from exceptions import Room_Unavailable_Exception,Invalid_Date,Booking_Not_Found,Invalid_Guest_Details,Invalid_Booking_Status
def create_booking(name,mobile,email,room_type,guest_count,check_in,check_out,breakfast=False):
    if not validate_name(name):
        raise Invalid_Guest_Details("Invalid name")
    if not validate_mobile(mobile):
        raise Invalid_Guest_Details("Invalid mobile number")
    if not validate_email(email):
        raise Invalid_Guest_Details("Invalid email")
    if guest_count<=0:
        raise Invalid_Guest_Details("Guest count must be positive")
    try:
        check_in_date=datetime.strptime(check_in,"%d-%m-%Y").date()
        check_out_date=datetime.strptime(check_out,"%d-%m-%Y").date()
    except ValueError:
        raise Invalid_Date("Invalid date format")
    today=datetime.today().date()
    if check_in_date<today:
        raise Invalid_Date("Check-in cannot be in the past")
    if (check_in_date-today).days>180:
        raise Invalid_Date("Check-in cannot be more than 180 days ahead")
    nights=(check_out_date-check_in_date).days
    if nights<1 or nights>30:
        raise Invalid_Date("Stay must be between 1 and 30 nights")
    room_type=room_type.strip().lower()
    if room_type not in ["standard","deluxe","suite"]:
        raise ValueError("Invalid room type")
    room=availability(room_type,guest_count,check_in,check_out)
    if room is None:
        raise Room_Unavailable_Exception("No suitable room is available")
    guest_data=database.get_guest(mobile)
    completed_stays=0
    if guest_data is not None:
        conn=database.connect()
        cur=conn.cursor()
        cur.execute("SELECT COUNT(*) FROM bookings WHERE mobile=? AND status='CHECKED_OUT'",(mobile,))
        completed_stays=cur.fetchone()[0]
        conn.close()
    guest=Guest(name,mobile,email)
    bill=calculate_prices(room,check_in,check_out,guest_count,breakfast,completed_stays)
    conn=database.connect()
    cur=conn.cursor()
    
    try:
        if guest_data is None:
            cur.execute("INSERT INTO guests(mobile,name,email) VALUES(?,?,?)",(guest.phone,guest.name,guest.email))
        else:
            cur.execute("UPDATE guests SET name=?,email=? WHERE mobile=?",(guest.name,guest.email,guest.phone))
        cur.execute("INSERT INTO bookings(mobile,room_no,room_type,check_in,check_out,guest_count,breakfast,status,total_amount,refund_amount) VALUES(?,?,?,?,?,?,?,?,?,?)",(guest.phone,room.room_no,room_type,check_in,check_out,guest_count,int(breakfast),"CONFIRMED",bill["total"],0))
        cur.execute("SELECT MAX(booking_id) FROM bookings")
        booking_id=cur.fetchone()[0]
        conn.commit()
    except Exception:
        conn.rollback()
        conn.close()
        raise
    conn.close()
    booking_object=Booking(booking_id,guest,room,check_in,check_out,guest_count,breakfast)
    print("Booking created successfully!")
    print("Booking ID:",booking_object.booking_id)
    print("Guest:",booking_object.guest)
    print("Room:",booking_object.room)
    print("Total Amount:",bill["total"])
    return booking_id
def check_in(booking_id):
    booking=database.get_booking(booking_id)
    if booking is None:
        raise Booking_Not_Found("Booking not found")
    if booking[8]!="CONFIRMED":
        raise Invalid_Booking_Status("Only confirmed bookings can be checked in")
    today=datetime.today().date()
    booking_date=datetime.strptime(booking[4],"%d-%m-%Y").date()
    if today!=booking_date:
        raise Invalid_Date("Check-in is allowed only on the check-in date")
    database.update_booking_status(booking_id,"CHECKED_IN")
    print("Guest checked in successfully!")
def check_out(booking_id):
    booking=database.get_booking(booking_id)
    if booking is None:
        raise Booking_Not_Found("Booking not found")
    if booking[8]!="CHECKED_IN":
        raise Invalid_Booking_Status("Guest must be checked in before checkout")
    database.update_booking_status(booking_id,"CHECKED_OUT")
    print("Guest checked out successfully!")
def cancel_booking(booking_id):
    booking=database.get_booking(booking_id)
    if booking is None:
        raise Booking_Not_Found("Booking not found")
    if booking[8]!="CONFIRMED":
        raise Invalid_Booking_Status("Only confirmed bookings can be cancelled")
    today=datetime.today().date()
    check_in_date=datetime.strptime(booking[4],"%d-%m-%Y").date()
    days_left=(check_in_date-today).days
    if days_left>=7:
        refund=booking[9]
    elif days_left>=2:
        refund=booking[9]*0.50
    else:
        refund=0
    amount_kept=booking[9]-refund
    conn=database.connect()
    cur=conn.cursor()
    try:
        cur.execute("UPDATE bookings SET refund_amount=?,status='CANCELLED' WHERE booking_id=?",(refund,booking_id))
        conn.commit()
    except Exception:
        conn.rollback()
        conn.close()
        raise
    conn.close()
    print("Booking cancelled successfully!")
    print("Original Amount:",booking[9])
    print("Refund Amount:",refund)
    print("Amount Kept by Hotel:",amount_kept)
