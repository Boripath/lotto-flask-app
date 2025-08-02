# _2_pricerate.py
from flask import session

# ✅ แสดงอัตราจ่ายที่เลือก [70, 90] สำหรับบิล

DEFAULT_RATE = 90  # เริ่ม 90 บาท

# ✅ คืนค่า rate ที่เลือก ปัจจุบัน

def get_pricerate():
    rate = session.get("pricerate")
    if rate not in [70, 90]:
        rate = DEFAULT_RATE
        session["pricerate"] = rate
    return rate
