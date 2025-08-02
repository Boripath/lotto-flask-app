# utils.py

def split_numbers(raw_input, step):
    """
    ตัดตัวเลขจากข้อความ เช่น "123456" → ["12", "34", "56"] ถ้า step=2
    """
    clean = ''.join(filter(str.isdigit, raw_input))
    return [clean[i:i+step] for i in range(0, len(clean), step) if len(clean[i:i+step]) == step]


def generate_double_numbers(digits=2):
    """
    สร้างเลขเบิ้ล: digits=2 → 00-99 แบบเบิ้ล เช่น 11, 22 ...
    digits=3 → 2ตัวเหมือน + 1 ต่าง เช่น 112, 121, 211
    """
    if digits == 2:
        return [f"{i}{i}" for i in range(10)]
    elif digits == 3:
        results = []
        for i in range(10):
            for j in range(10):
                if i != j:
                    results.append(f"{i}{i}{j}")
                    results.append(f"{i}{j}{i}")
                    results.append(f"{j}{i}{i}")
        return sorted(set(results))
    return []


def generate_triple_numbers():
    """
    สร้างเลขตอง: 000, 111, ... 999
    """
    return [f"{i}{i}{i}" for i in range(10)]


def generate_6_glub(number):
    """
    รับเลข 3 หลัก เช่น 123 → คืน permutation 6 แบบ
    """
    if len(number) != 3 or not number.isdigit():
        return []
    perms = set()
    digits = list(number)
    from itertools import permutations
    for p in permutations(digits):
        perms.add(''.join(p))
    return list(perms)
    
def format_currency(amount):
    """
    แปลงจำนวนเงินเป็นรูปแบบ 1,234 บาท
    """
    return f"{int(amount):,} บาท"
