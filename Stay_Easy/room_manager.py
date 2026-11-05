import csv
from datetime import datetime,date
from .models import StandardRoom,Deluxe,Suite
import sqlite3
conn=sqlite3.connect("stayeasy.db")
cur=conn.cursor()
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
                print("Duplicate room number,room numbers must be unique")
                continue
            if room_type not in ["standard","deluxe","suite"]:
                print("Invalid room type ")
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
            room.room_type=room_type
            room_set.add(room_no)
            records.append(room)
        except:
            print("Invalid CSV Entry")
            print("Invalid Room entries in room csv")
print("rooms at our stay")
for r in records:
    print(r)


def availability(room_type,guest_count,check_in,check_out):
    if guest_count<=0:
        print("Guest count cannot be zero or lesser")
        return None
    check_out=datetime.strptime(check_out,"%d-%m-%Y").date()
    check_in=datetime.strptime(check_in,"%d-%m-%Y").date()
    if check_out<=check_in:
        print("CHeck out must be after check in")
        return None
    cur.execute("""SELECT room_no,check_in,check_out FROM bookings WHERE status IN ('CONFIRMED','CHECKED_IN')""")
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
            if(available[j].room_no>available[j+1].room_no):
                available[j],available[j+1]=available[j+1],available[j]
    if len(available)>0:
        return available[0]
    return None
room=availability("deluxe",3,"10-11-2026","15-11-2026")
if room is None:
    print("No rooms are available")
else:
    print("room available",room)
    
        
        

            

            
        