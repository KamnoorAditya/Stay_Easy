
from datetime import datetime,timedelta
from exceptions import Invalid_Date,Invalid_Guest_Details
def calculate_prices(room,check_in,check_out,guest_count,breakfast=False,completed_stays=0):
    try:
        check_in=datetime.strptime(check_in,"%d-%m-%Y").date()
        check_out=datetime.strptime(check_out,"%d-%m-%Y").date()
    except ValueError:
        raise Invalid_Date("Invalid date format")
    if check_out<=check_in:
        raise Invalid_Date("Check-out must be after check-in")
    if guest_count<=0 or guest_count>room.max_guests():
        raise Invalid_Guest_Details("Invalid guest count")
    total_nights=(check_out-check_in).days
    room_charges=0
    breakfast_charge=0
    weekend_charges=0
    extra_guest_charge=0
    gst_amount=0
    current_day=check_in
    for i in range(total_nights):
        day=current_day.strftime("%A")
        daily_rates=room.base_rates()
        if day=="Friday" or day=="Saturday":
            weekend=daily_rates*0.2
        else:
            weekend=0
        extra_guest=0
        if guest_count>2:
            extra_guest=(guest_count-2)*room.extra_guest_charge()
        breakfast_amount=0
        if not room.breakfast_included() and breakfast:
            breakfast_amount=guest_count*room.breakfast_charges()
        nightly_tariff=daily_rates+weekend+extra_guest
        if nightly_tariff>7500:
            gst=nightly_tariff*0.18
        else:
            gst=nightly_tariff*0.12
        room_charges+=daily_rates
        weekend_charges+=weekend
        extra_guest_charge+=extra_guest
        breakfast_charge+=breakfast_amount
        gst_amount+=gst
        current_day+=timedelta(days=1)
    long_stay_discount=0
    if total_nights>=7:
        long_stay_discount=room_charges*0.10
    loyalty_discount=0
    if completed_stays>=3:
        loyalty_discount=room_charges*0.05
    total=room_charges+extra_guest_charge+weekend_charges+breakfast_charge-loyalty_discount-long_stay_discount+gst_amount
    return {
        "Nights":total_nights,
        "room_charges":room_charges,
        "weekend_charges":weekend_charges,
        "extra_guest_charges":extra_guest_charge,
        "Breakfast_charge":breakfast_charge,
        "gst":gst_amount,
        "loyalty_discount":loyalty_discount,
        "long_stay_discount":long_stay_discount,
        "total":total
    }
