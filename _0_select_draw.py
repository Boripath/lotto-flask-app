from flask import session
from datetime import datetime

# ✅ เลือกงวดหวยจากปฏิทิน และคำนวนเวลาปิดรับโพย

# ค่า default เวลาปิดรับ (เวลาปิดโพย)
CUTOFF_TIME = "15:00:00"  # ปิด 15:00

# ✅ ฟังก์ช่วยงวันที่ user เลือก

def select_draw_date():
    draw_date_str = session.get("draw_date")
    countdown_str = ""

    if draw_date_str:
        # แปลงจาก string เป็น datetime และคำนวน
        full_str = draw_date_str + " " + CUTOFF_TIME
        try:
            draw_dt = datetime.strptime(full_str, "%Y-%m-%d %H:%M:%S")
            now = datetime.now()
            remaining = draw_dt - now
            if remaining.total_seconds() > 0:
                days = remaining.days
                hours, rem = divmod(remaining.seconds, 3600)
                minutes, seconds = divmod(rem, 60)
                countdown_str = f"เหลือเวลา: {days} วัน {hours:02}:{minutes:02}:{seconds:02}"
            else:
                countdown_str = "ปิดรับโพยแล้ว"
        except Exception as e:
            countdown_str = ""

    return draw_date_str or "", countdown_str
