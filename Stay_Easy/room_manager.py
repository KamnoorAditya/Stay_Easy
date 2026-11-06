
import csv
from datetime import datetime,date
import database
from models import StandardRoom,Deluxe,Suite
from exceptions import Invalid_Date
records=[]
room_set=set()
with open("rooms.csv","r") as file:
    reader=csv.reader(file)
    next(reader)
    for line in reader:
        try:
            room_no=int(line[0])
            room_type=str(line[1]).lower()
            floor=int(line[2])
            if room_no in room_set:
                print("Duplicate room number, room numbers must be unique")
                continue
            if room_type not in ["standard","deluxe","suite"]:
                print("Invalid room type")
                continue
            if floor<0:
                print("Floor number cannot be negative")
                continue
            if room_type=="deluxe":
                room=Deluxe(room_no,floor)
            elif room_type=="suite":
                room=Suite(room_no,floor)
            else:
                room=StandardRoom(room_no,floor)
            room_set.add(room_no)
            records.append(room)
        except (ValueError,IndexError):
            print("Invalid CSV entry")
print("Rooms at our stay")
for r in records:
    print(r)
def availability(room_type,guest_count,check_in,check_out):
    if guest_count<=0:
        raise ValueError("Invalid guest count")
    room_type=room_type.strip().lower()
    if room_type not in ["standard","deluxe","suite"]:
        raise ValueError("Invalid room type")
    try:
        check_in=datetime.strptime(check_in,"%d-%m-%Y").date()
        check_out=datetime.strptime(check_out,"%d-%m-%Y").date()
    except ValueError:
        raise Invalid_Date("Invalid date format")
    if check_out<=check_in:
        raise Invalid_Date("Check-out must be after check-in")
    today=date.today()
    if check_in<today:
        raise Invalid_Date("Check-in cannot be in the past")
    if (check_in-today).days>180:
        raise Invalid_Date("Check-in cannot be more than 180 days ahead")
    if (check_out-check_in).days>30:
        raise Invalid_Date("Stay cannot exceed 30 nights")
    conn=database.connect()
    cur=conn.cursor()
    cur.execute("SELECT room_no,check_in,check_out FROM bookings WHERE status IN ('CONFIRMED','CHECKED_IN')")
    bookings=cur.fetchall()
    conn.close()
    available=[]
    for room in records:
        if room.room_type!=room_type:
            continue
        if guest_count>room.max_guests():
            continue
        is_available=True
        for booking in bookings:
            if booking[0]==room.room_no:
                old_in=datetime.strptime(booking[1],"%d-%m-%Y").date()
                old_out=datetime.strptime(booking[2],"%d-%m-%Y").date()
                if check_in<old_out and check_out>old_in:
                    is_available=False
                    break
        if is_available:
            available.append(room)
    for i in range(len(available)):
        for j in range(len(available)-1-i):
            if available[j].room_no>available[j+1].room_no:
                available[j],available[j+1]=available[j+1],available[j]
    if len(available)>0:
        return available[0]
    return None
