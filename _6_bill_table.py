# _6_bill_table.py
from flask import session
from utils import format_currency

# ✅ เตรียมข้อมูลบิลทั้งหมดแบบจัดกลุ่มเพื่อแสดงผล

def get_bill_table_data():
    bills = session.get("bills", [])
    grouped = []

    for idx, bill in enumerate(bills):
        grouped.append({
            "idx": idx,
            "number": bill.get("number", ""),
            "top": bill.get("top", 0),
            "bottom": bill.get("bottom", 0),
            "tod": bill.get("tod", 0),
            "type": bill.get("type", "")
        })

    return grouped

# ✅ คำนวนยอดรวม

def calculate_total():
    bills = session.get("bills", [])
    total = 0
    for bill in bills:
        total += bill.get("top", 0)
        total += bill.get("bottom", 0)
        total += bill.get("tod", 0)
    return format_currency(total)
