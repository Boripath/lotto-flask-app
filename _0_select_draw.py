from flask import session
from datetime import datetime, timedelta

# เวลาปิดโพยของแต่ละชนิดหวย
CUTOFF_TIMES = {
    "หวยรัฐบาลไทย": "15:00:00",
    "หวยลาวพัฒนา": "20:00:00",
    "หวยฮานอย พิเศษ": "17:00:00",
    "หวยฮานอย": "18:00:00",
    "หวยฮานอย VIP": "19:00:00"
}

# ชนิดหวยที่รองรับ
LOTTERY_TYPES = [
    "หวยรัฐบาลไทย",
    "หวยลาวพัฒนา",
    "หวยฮานอย พิเศษ",
    "หวยฮานอย",
    "หวยฮานอย VIP"
]

# แปลงชื่อวัน
DAY_NAMES = ["จันทร์", "อังคาร", "พุธ", "พฤหัสบดี", "ศุกร์", "เสาร์", "อาทิตย์"]

# ✅ ฟังก์ชันหลักเลือกชนิดหวยและคำนวณงวด
def select_draw_date():
    lottery_type = session.get("lottery_type", "หวยรัฐบาลไทย")
    now = datetime.now()

    # หา draw date ตามชนิดหวย
    draw_date = calculate_draw_date(lottery_type, now)
    cutoff_time_str = CUTOFF_TIMES.get(lottery_type, "15:00:00")
    draw_date_str = draw_date.strftime("%Y-%m-%d")
    full_draw_str = draw_date_str + " " + cutoff_time_str

    # แสดงงวด: งวด วันdd/mm/yyyy (พ.ศ.)
    weekday = DAY_NAMES[draw_date.weekday()]
    thai_year = draw_date.year + 543
    formatted_draw = draw_date.strftime(f"งวด วัน{weekday} %d/%m/{thai_year}")

    # คำนวณเวลานับถอยหลัง
    countdown_str = ""
    try:
        draw_dt = datetime.strptime(full_draw_str, "%Y-%m-%d %H:%M:%S")
        remaining = draw_dt - now
        if remaining.total_seconds() > 0:
            days = remaining.days
            hours, rem = divmod(remaining.seconds, 3600)
            minutes, seconds = divmod(rem, 60)
            countdown_str = f"เหลือเวลา: {days} วัน {hours:02}:{minutes:02}:{seconds:02}"
        else:
            countdown_str = "ปิดรับโพยแล้ว"
    except Exception:
        countdown_str = ""

    # บันทึก draw_date ใน session
    session["draw_date"] = draw_date_str
    return formatted_draw, countdown_str, lottery_type

# ✅ คำนวณ draw date ตามชนิดหวย
def calculate_draw_date(lottery_type, now):
    if lottery_type == "หวยรัฐบาลไทย":
        day = now.day
        month = now.month
        year = now.year
        if day <= 1:
            return datetime(year, month, 1)
        elif day <= 16:
            return datetime(year, month, 16)
        else:
            # เดือนถัดไป
            if month == 12:
                return datetime(year + 1, 1, 1)
            return datetime(year, month + 1, 1)

    elif lottery_type == "หวยลาวพัฒนา":
        # ออกวัน จ,พ,ศ → หา day_next
        weekday = now.weekday()  # 0=จันทร์, 1=อังคาร,...6=อาทิตย์
        target_days = [0, 2, 4]
        days_ahead = min((d - weekday) % 7 for d in target_days)
        return now + timedelta(days=days_ahead)

    else:
        # ฮานอยทุกแบบ → ออกทุกวัน
        return now
