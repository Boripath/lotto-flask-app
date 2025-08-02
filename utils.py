# ✅ ฟังก์ชันช่วยสำหรับระบบโพยหวย

def split_numbers(text, step=2):
    """
    ตัดเลขจากข้อความทุก step หลัก เช่น 2 ตัว, 3 ตัว
    """
    cleaned = ''.join(c for c in text if c.isdigit())
    numbers = []
    for i in range(0, len(cleaned), step):
        part = cleaned[i:i+step]
        if len(part) == step:
            numbers.append(part)
    return numbers


def generate_double_numbers(digits=2):
    """
    สร้างเลขเบิ้ล/ตอง เช่น 11, 22 หรือ 111, 222
    """
    return [str(i)*digits for i in range(10)]


def generate_6_glub(number):
    """
    รับเลข 3 หลัก แล้วคืนค่าเลขที่สลับได้ทั้งหมด (6 กลับ)
    """
    if len(number) != 3:
        return [number]
    return sorted(set(
        ["".join(p) for p in __import__('itertools').permutations(number)]
    ))


def format_currency(amount):
    """
    แปลงจำนวนเงินเป็นรูปแบบ 1,000 บาท
    """
    return f"{amount:,.0f} บาท"
