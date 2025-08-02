# _8_summary_footer.py
from flask import session

# ✅ จัดการล้างตาราง และเตรียมข้อมูลสำหรับบันทึกโพย

# ✅ ล้างบิลทั้งหมด + ข้อมูลกรอกเลข/ราคา/memo

def clear_all_data():
    session["bills"] = []
    session["numbers"] = []
    session["price_top"] = 0
    session["price_bottom"] = 0
    session["price_tod"] = 0
    session["memo"] = ""

# ✅ เตรียมข้อมูลโพยที่จะบันทึก บันทึกตามระเวลา

def get_all_bills():
    return session.get("bills", [])

# ✅ คืนค่าข้อความ memo ปัจจุบ

def get_current_memo():
    return session.get("memo", "")
