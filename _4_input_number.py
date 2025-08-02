# _4_input_number.py
from flask import session
from utils import split_numbers, generate_double_numbers, generate_6_glub, generate_triple_numbers

# คืนค่าเลขที่แสดง + สถานะเบิ้ล

def get_number_input():
    numbers = session.get("numbers", [])
    double_mode = session.get("double_mode", False)
    return numbers, double_mode

# กรอกเลข + ตัดเลขอัตโนมัติ พร้อมรองรับ 6 กลับ และตอง

def process_number_input(raw_input):
    bet_type = session.get("bet_type", "2 ตัว")
    double_mode = session.get("double_mode", False)

    numbers = []

    if double_mode:
        if bet_type == "2 ตัว":
            numbers = generate_double_numbers(2)
        elif bet_type == "3 ตัว":
            numbers = generate_triple_numbers()
        else:
            step = 3
            base_numbers = split_numbers(raw_input, step)
            glub_set = set()
            for num in base_numbers:
                glub_set.update(generate_6_glub(num))
            numbers = sorted(glub_set)
    else:
        step = 2 if bet_type == "2 ตัว" else 3
        base_numbers = split_numbers(raw_input, step)

        if bet_type == "6 กลับ":
            glub_set = set()
            for num in base_numbers:
                glub_set.update(generate_6_glub(num))
            numbers = sorted(glub_set)
        else:
            numbers = base_numbers

    session["numbers"] = numbers

# ลบเลขตาม index

def delete_number(idx):
    numbers = session.get("numbers", [])
    if 0 <= idx < len(numbers):
        numbers.pop(idx)
        session["numbers"] = numbers

# toggle เบิ้ล/ตอง

def toggle_double():
    session["double_mode"] = not session.get("double_mode", False)
