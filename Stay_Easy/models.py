from abc import ABC,abstractmethod
class Room(ABC):
    def __init__(self,roll_no,floor):
        self.__room_no=roll_no
        self.__floor=floor
    @abstractmethod
    def base_rates(self):
        pass
    @abstractmethod
    def max_guests(self):
        pass
    def breakfast_included(self):
        pass
    @abstractmethod
    def extra_guest_charge(self):
        pass
    def __str__(self):
        return f"Room no :{self._room_no} Floor{self._floor}"
class StandardRoom(Room):
    def base_rates(self):
        return 2500
    def max_guests(self):
        return 2
    def breakfast_included(self):
        return False
    def extra_guest_charge(self):
        return 0
    def breakfast_charges(self):
        return 350
    def __str__(self):
        return f"Standard{super.__str__()}"
class Deluxe(Room):
    def base_rates(self):
        return 4000
    def max_guest(self):
        return 3
    def breakfast_included(self):
        return True
    def extra_guest_charge(self,guests):
        return 800

        
class Suite(Room):
    def base_rates(self):
        return 7500
    def max_guests(self):
        return 4
    def breakfast_included(self):
        return True
    def extra_guest_charge(self,guests):
        return 800
class Guest:
    
        def __init__(self,name,mobile,email):
            self._name=name
            self._mobile=mobile
            self._email=email
            @property
            def name(self):
                return self._name
            @property
            def phone(self):
                return self._mobile
            @property
            def email(self):
                return self._email
            def __str__(self):
                return self._name
class Booking:
    def __init__(self,booking_id,guest,room,check_in,check_out,guest_count,breakfast=False):
        self._booking_id=booking_id
        self._guest=guest
        self._room=room
        self._check_in=check_in
        self._check_out=check_out
        self._guest_count=guest_count
        self._status="CONFIRMED"
        self._breakfast=breakfast
        @property
        def booking_id(self):
            return self._booking_id
        @property
        def guest(self):
            return self._guest
        @property
        def room(self):
            return self._room
        @property
        def check_in(self):
            return self._check_in
        @property
        def check_out(self):
            return self._check_out
        @property
        def guest_count(self):
            return self._guest_count
        @property
        def breakafst(self):
            return self._breakfast
        @property
        def status(self):
            return self._status
        def change_status(self,new_status):
            if self._status=="CONFIRMED":
                if new_status=="CHECKED IN" or new_status=="CANCELLED":
                    self._status=new_status
                else:
                    print("Invalid Status")
            elif self._status=="CHECKED IN":
                if new_status=="CHECKED OUT":
                    self._status=new_status
                else:
                    print("Invalid status change")
            else:
                print("Status cannot be changed")
        def __str__(self):
            return f"{self.booking_id} {self.guest.name} Room {self.room.room_no} {self.check_in} to {self.check_out} {self.status}"                
                
    
            
            
     
