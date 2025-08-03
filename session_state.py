# session_state.py
from flask import session

def init_session():
    session.setdefault("bills", [])
    session.setdefault("bet_type", "2 ตัว")
    session.setdefault("numbers", [])
    session.setdefault("price_top", 0)
    session.setdefault("price_bottom", 0)
    session.setdefault("price_tod", 0)
    session.setdefault("memo", "")

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
        # คืนค่าข้อมูลบิลนั้นกลับไปยัง input
        session["bet_type"] = bill.get("type", "2 ตัว")
        session["numbers"] = [bill.get("number", "")]
        session["price_top"] = float(bill.get("top", 0))
        session["price_bottom"] = float(bill.get("bottom", 0))
        session["price_tod"] = float(bill.get("tod", 0))
