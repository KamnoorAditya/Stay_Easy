import csv
records=[]
room_set=set()
with open("rooms.csv","r") as file:
    reader=csv.reader(file)
    next(reader)
    for line in file:
        flag=False
        try:
            parts=line.split(",")
            room_no=int(parts[0])
            room_type=str(parts[1]).lower()
            floor=int(parts[2])
            if room_no=="":
                print("Room number is empty:")
                continue
            if room_no in room_set:
                print("Duplicate room number,room numbers must be unique")
                continue
            if room_type not in ["standard","deluxe","suite"]:
                print("Invalid room type ")
                continue
            if floor<0:
                print("Floor number cannot be negative")
                continue
            flag=True
            if flag:
                room_set.add(room_no)
                records.append([floor,room_type,room_no])
        except Exception as e:
            print("Invalid Room entries in room csv")
    for r in records:
        print(r)
            

            
        