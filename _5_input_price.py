from flask import session

def get_price_inputs():
    top = session.get("price_top", 0)
    bottom = session.get("price_bottom", 0)
    tod = session.get("price_tod", 0)
    return top, bottom, tod

def set_price_inputs(top, bottom, tod):
    session["price_top"] = top
    session["price_bottom"] = bottom
    session["price_tod"] = tod

def submit_bill():
    bet_type = session.get("bet_type", "2 ตัว")
    numbers = session.get("numbers", [])
    top = float(session.get("price_top", 0))
    bottom = float(session.get("price_bottom", 0))
    tod = float(session.get("price_tod", 0))

    bill = {
        "type": bet_type,
        "numbers": numbers.copy(),  # ✅ เก็บเลขทุกตัวในบิล
        "top": top,
        "bottom": bottom,
        "tod": tod
    }

    bills = session.get("bills", [])
    bills.append(bill)
    session["bills"] = bills

    # ✅ เคลียร์ input
    session["numbers"] = []
    session["price_top"] = 0
    session["price_bottom"] = 0
    session["price_tod"] = 0
