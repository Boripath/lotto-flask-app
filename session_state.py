from flask import session

# ✅ สร้างและจัดการข้อมูลใน session สำหรับบิล, ตัวเลข, ราคา, งวด

def init_session():
    session.setdefault("draw_date", None)
    session.setdefault("pricerate", 90)
    session.setdefault("bet_type", "2 ตัว")
    session.setdefault("numbers", [])
    session.setdefault("price_top", 0)
    session.setdefault("price_bottom", 0)
    session.setdefault("price_tod", 0)
    session.setdefault("bills", [])
    session.setdefault("memo", "")

# ✅ จัดการเลขที่กรอก (ตัดอัตโนมัติ)
def process_numbers(raw_input):
    cleaned = ''.join(c for c in raw_input if c.isdigit())
    bet_type = session.get("bet_type", "2 ตัว")
    numbers = []

    step = 2 if bet_type == "2 ตัว" else 3
    for i in range(0, len(cleaned), step):
        part = cleaned[i:i+step]
        if len(part) == step:
            numbers.append(part)

    session["numbers"] = numbers

# ✅ ลบเลขตาม index

def delete_number(idx):
    numbers = session.get("numbers", [])
    if 0 <= idx < len(numbers):
        numbers.pop(idx)
        session["numbers"] = numbers

# ✅ เพิ่มบิลใหม่เข้า session

def add_bill(price_top, price_bottom, price_tod):
    bet_type = session.get("bet_type")
    numbers = session.get("numbers", [])

    bills = session.get("bills", [])
    for number in numbers:
        bill = {
            "draw_date": session.get("draw_date"),
            "type": bet_type,
            "number": number,
            "top": price_top,
            "bottom": price_bottom,
            "tod": price_tod
        }
        bills.append(bill)

    session["bills"] = bills
    clear_input_only()

# ✅ ลบบิลตาม index

def delete_bill(idx):
    bills = session.get("bills", [])
    if 0 <= idx < len(bills):
        bills.pop(idx)
        session["bills"] = bills

# ✅ ดึงข้อมูลทั้งหมดของบิล

def get_bills():
    return session.get("bills", [])

# ✅ ล้างข้อมูลทั้งหมด (หลังบันทึกโพย)

def clear_all():
    session["numbers"] = []
    session["bills"] = []
    session["price_top"] = 0
    session["price_bottom"] = 0
    session["price_tod"] = 0
    session["memo"] = ""

# ✅ ล้างเฉพาะช่อง input (หลังเพิ่มบิล)
def clear_input_only():
    session["numbers"] = []
    session["price_top"] = 0
    session["price_bottom"] = 0
    session["price_tod"] = 0

# ✅ ดึงเลขที่กรอกไว้

def get_numbers():
    return session.get("numbers", [])
