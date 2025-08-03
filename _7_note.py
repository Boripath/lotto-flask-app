# _7_note.py

from flask import session

def get_memo_and_total():
    """
    ดึงข้อความบันทึกช่วยจำ และยอดรวมทั้งหมดจากบิล
    """
    memo = session.get("memo", "")
    bills = session.get("bills", [])
    total = 0

    for bill in bills:
        numbers = bill.get("numbers", [])
        count = len(numbers)

        bet_type = bill.get("type", "2 ตัว")
        top = float(bill.get("top", 0))
        bottom = float(bill.get("bottom", 0))
        tod = float(bill.get("tod", 0))

        if bet_type == "2 ตัว":
            total += count * (top + bottom)
        else:  # 3 ตัว หรือ 6 กลับ
            total += count * (top + tod)

    return memo, total

def set_memo(memo_text):
    """
    เซฟข้อความบันทึกช่วยจำลง session
    """
    session["memo"] = memo_text
