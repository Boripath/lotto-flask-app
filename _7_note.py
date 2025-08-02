# _7_note.py
from flask import session

def get_memo_and_total():
    memo = session.get("memo", "")
    bills = session.get("bills", [])
    total_top = sum(float(b.get("top", 0)) for b in bills)
    total_bottom = sum(float(b.get("bottom", 0)) for b in bills)
    total_tod = sum(float(b.get("tod", 0)) for b in bills)
    total_amount = total_top + total_bottom + total_tod
    return memo, total_amount

def set_memo(text):
    session["memo"] = text  # ✅ ไม่มีปุ่ม OK แล้ว ใช้งานทันที
