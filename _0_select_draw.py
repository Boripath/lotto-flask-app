from flask import session
from datetime import datetime, timedelta

# ปิดรับโพยเวลาต่าง ๆ ต่อชนิดหวย
CUTOFF_TIMES = {
    "หวยรัฐบาลไทย": "15:00:00",
    "หวยลาวพัฒนา (จ,พ,ศ)": "20:00:00",
    "หวยฮานอย พิเศษ": "17:00:00",
    "หวยฮานอย": "18:00:00",
    "หวยฮานอย VIP": "19:00:00"
}

# ชื่อวันภาษาไทย
THAI_DAYS = ["จันทร์", "อังคาร", "พุธ", "พฤหัสบดี", "ศุกร์", "เสาร์", "อาทิตย์"]

def get_next_draw_date(lotto_type):
    now = datetime.now()
    if lotto_type == "หวยรัฐบาลไทย":
        day = now.day
        month = now.month
        year = now.year
        if day < 16:
            target_day = 16
        else:
            target_day = 1
            month += 1
            if month > 12:
                month = 1
                year += 1
        draw_date = datetime(year, month, target_day)
    elif lotto_type == "หวยลาวพัฒนา (จ,พ,ศ)":
        weekday = now.weekday()
        days_map = [0, 2, 4]  # จันทร์ พุธ ศุกร์
        days_ahead = min((d - weekday) % 7 for d in days_map)
        draw_date = now + timedelta(days=days_ahead)
    else:  # ฮานอยทุกชนิด
        draw_date = now
    return draw_date

def select_draw_date_and_countdown():
    lotto_type = session.get("lottery_type", "หวยรัฐบาลไทย")
    cutoff_time = CUTOFF_TIMES.get(lotto_type, "15:00:00")
    draw_date = get_next_draw_date(lotto_type)
    day_th = THAI_DAYS[draw_date.weekday()]
    draw_date_th = draw_date.strftime(f"{day_th} %d/%m/%Y")
    draw_info = f"{lotto_type} งวด {draw_date_th}"

    # เวลาปิดโพย
    cutoff_dt = datetime.strptime(draw_date.strftime("%Y-%m-%d") + " " + cutoff_time, "%Y-%m-%d %H:%M:%S")
    now = datetime.now()
    remaining = cutoff_dt - now
    if remaining.total_seconds() > 0:
        days = remaining.days
        hours, rem = divmod(remaining.seconds, 3600)
        minutes, seconds = divmod(rem, 60)
        countdown_str = f"เหลือเวลา: {days} วัน {hours:02}:{minutes:02}:{seconds:02}"
    else:
        countdown_str = "ปิดรับโพยแล้ว"
    countdown_seconds = max(int(remaining.total_seconds()), 0)
    allow_bet = countdown_seconds > 0
    session["draw_date"] = draw_date.strftime("%d/%m/%Y")
    session["allow_bet"] = allow_bet
    return draw_info, countdown_str, countdown_seconds, allow_bet
