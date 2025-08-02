# _3_bet_type.py
from flask import session

# ✅ แสดงประเภทการแทง: ["2 ตัว", "3 ตัว", "6 กลับ", "วิ่ง", "รูด", "19 ประตู"]

BET_TYPES = ["2 ตัว", "3 ตัว", "6 กลับ", "วิ่ง", "รูด", "19 ประตู"]
DEFAULT_BET_TYPE = "2 ตัว"

# ✅ คืนค่าประเภทการแทงปัจจุบัน

def get_bet_type():
    bet_type = session.get("bet_type")
    if bet_type not in BET_TYPES:
        bet_type = DEFAULT_BET_TYPE
        session["bet_type"] = bet_type
    return bet_type
