
import sys
import database
from exceptions import Hotel_Exception
if len(sys.argv)>1:
    database.db_name=sys.argv[1]
database.create_tables()
import booking
import reports
import room_manager
def main():
    print("Welcome to StayEasy Hotel Reservation System")
    while True:
        print("\n1. Search room availability\n2. Create booking\n3. Check in\n4. Check out\n5. Cancel booking\n6. View booking details\n7. Guest stay history\n8. Occupancy report\n9. Revenue report\n10. Export all bookings\n11. Exit")
        choice=input("Enter your choice: ")
        try:
            if choice=="1":
                room_type=input("Enter room type: ").lower()
                guest_count=int(input("Enter number of guests: "))
                check_in=input("Enter check-in date (DD-MM-YYYY): ")
                check_out=input("Enter check-out date (DD-MM-YYYY): ")
                room=room_manager.availability(room_type,guest_count,check_in,check_out)
                if room is None:
                    print("No room available")
                else:
                    print("Available room:",room)
            elif choice=="2":
                name=input("Enter guest name: ")
                mobile=input("Enter mobile number: ")
                email=input("Enter email: ")
                room_type=input("Enter room type: ")
                guest_count=int(input("Enter number of guests: "))
                check_in=input("Enter check-in date (DD-MM-YYYY): ")
                check_out=input("Enter check-out date (DD-MM-YYYY): ")
                breakfast=False
                if room_type.lower()=="standard":
                    answer=input("Do you want breakfast? (yes/no): ").lower()
                    if answer=="yes":
                        breakfast=True
                booking.create_booking(name,mobile,email,room_type,guest_count,check_in,check_out,breakfast)
            elif choice=="3":
                booking_id=int(input("Enter booking ID: "))
                booking.check_in(booking_id)
            elif choice=="4":
                booking_id=int(input("Enter booking ID: "))
                booking.check_out(booking_id)
            elif choice=="5":
                booking_id=int(input("Enter booking ID: "))
                booking.cancel_booking(booking_id)
            elif choice=="6":
                booking_id=int(input("Enter booking ID: "))
                reports.view_booking_details(booking_id)
            elif choice=="7":
                mobile=input("Enter guest mobile number: ")
                reports.guest_history(mobile)
            elif choice=="8":
                start_date=input("Enter start date (DD-MM-YYYY): ")
                end_date=input("Enter end date (DD-MM-YYYY): ")
                reports.occupancy_report(start_date,end_date)
            elif choice=="9":
                reports.revenue_report()
            elif choice=="10":
                reports.export_bookings()
            elif choice=="11":
                print("Thank you for using StayEasy!")
                break
            else:
                print("Invalid choice")
        except Hotel_Exception as e:
            print("Hotel Error:",e)
        except ValueError as e:
            print("Input Error:",e)
        except Exception as e:
            print("Error:",e)
main()
# TEST CHANGE