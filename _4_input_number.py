# _4_input_number.py
from flask import session
from utils import split_numbers, generate_double_numbers, generate_6_glub

# ✅ จัดการเลขที่กรอก และระบบเบิ้ล/6กลับ เพื่อเสริ่มตรง UI

# ✅ คืนค่าเลขที่แสดง + สถานะเบิ้ล/6กลับ

def get_number_input():
    numbers = session.get("numbers", [])
    double_mode = session.get("double_mode", False)
    glub_mode = session.get("glub_mode", False)
    return numbers, double_mode, glub_mode

# ✅ กรอกเลข + ตัดเลขอัตโนมัติ

def process_number_input(raw_input):
    bet_type = session.get("bet_type", "2 ตัว")
    double_mode = session.get("double_mode", False)
    glub_mode = session.get("glub_mode", False)

    numbers = []

    if double_mode:
        digits = 2 if bet_type == "2 ตัว" else 3
        numbers = generate_double_numbers(digits)
    else:
        step = 2 if bet_type == "2 ตัว" else 3
        base_numbers = split_numbers(raw_input, step)

        if glub_mode and bet_type == "6 กลับ":
            glub_set = set()
            for num in base_numbers:
                glub_set.update(generate_6_glub(num))
            numbers = sorted(glub_set)
        else:
            numbers = base_numbers

    session["numbers"] = numbers

# ✅ ลบเลขทีละตัวตาม index

def delete_number(idx):
    numbers = session.get("numbers", [])
    if 0 <= idx < len(numbers):
        numbers.pop(idx)
        session["numbers"] = numbers

# ✅ toggle เบิ้ล/6กลับ

def toggle_double():
    session["double_mode"] = not session.get("double_mode", False)


def toggle_glub():
    session["glub_mode"] = not session.get("glub_mode", False)
