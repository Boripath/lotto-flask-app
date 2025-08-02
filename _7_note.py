# _7_note.py
from flask import session
from _6_bill_table import calculate_total

# ✅ คืนค่าบันทึกช่วยจำ + ยอดรวม

def get_memo_and_total():
    memo = session.get("memo", "")
    total = calculate_total()
    return memo, total

# ✅ เซตข้อความช่วยจำใหม่

def set_memo(text):
    session["memo"] = text
