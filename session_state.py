from flask import session

def init_session():
    session.setdefault("draw_date", "")
    session.setdefault("pricerate", 90)
    session.setdefault("bet_type", "2 ตัว")
    session.setdefault("numbers", [])
    session.setdefault("price_top", 0)
    session.setdefault("price_bottom", 0)
    session.setdefault("price_tod", 0)
    session.setdefault("bills", [])
    session.setdefault("memo", "")
    session.setdefault("double_mode", False)

def clear_input_only():
    session["numbers"] = []
    session["price_top"] = 0
    session["price_bottom"] = 0
    session["price_tod"] = 0

def get_bills():
    return session.get("bills", [])

def delete_bill(idx):
    bills = session.get("bills", [])
    if 0 <= idx < len(bills):
        bills.pop(idx)
        session["bills"] = bills

def edit_bill(idx):
    bills = session.get("bills", [])
    if 0 <= idx < len(bills):
        bill = bills.pop(idx)
        session["bills"] = bills

        # ✅ ดึงข้อมูลทั้งหมดกลับไป input
        session["bet_type"] = bill.get("type", "2 ตัว")

        if "numbers" in bill:
            # ✅ บิลใหม่: มีหลายเลข
            session["numbers"] = bill["numbers"]
        else:
            # ✅ บิลเก่า: มีเลขเดียว
            number = bill.get("number", "")
            session["numbers"] = [number] if number else []

        session["price_top"] = float(bill.get("top", 0))
        session["price_bottom"] = float(bill.get("bottom", 0))
        session["price_tod"] = float(bill.get("tod", 0))
