# _5_input_price.py
from flask import session

def get_price_inputs():
    return session.get("price_top", 0), session.get("price_bottom", 0), session.get("price_tod", 0)

def set_price_inputs(top, bottom, tod):
    session["price_top"] = top
    session["price_bottom"] = bottom
    session["price_tod"] = tod

def submit_bill():
    numbers = session.get("numbers", [])
    bet_type = session.get("bet_type", "2 ตัว")
    top = session.get("price_top", 0)
    bottom = session.get("price_bottom", 0)
    tod = session.get("price_tod", 0)

    bills = session.get("bills", [])
    for number in numbers:
        bills.append({
            "type": bet_type,
            "number": number,
            "top": top,
            "bottom": bottom,
            "tod": tod
        })

    session["bills"] = bills
    # ล้าง input
    session["numbers"] = []
    session["price_top"] = 0
    session["price_bottom"] = 0
    session["price_tod"] = 0
