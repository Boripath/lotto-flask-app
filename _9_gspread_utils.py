import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
from flask import session

# ✅ ชื่อไฟล์ Google Sheet และ Scope
SHEET_NAME = "LottoBills"

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# ✅ เชื่อมต่อ Google Sheet
def connect_sheet():
    creds = Credentials.from_service_account_file("credentials.json", scopes=SCOPES)
    client = gspread.authorize(creds)
    sheet = client.open(SHEET_NAME)
    return sheet

# ✅ บันทึกบิลทั้งหมดลง 2 ชีท: All_Bills และ Summary_By_Number
def save_to_google_sheet(bills):
    if not bills:
        return

    sheet = connect_sheet()
    ws_all = sheet.worksheet("All_Bills")
    ws_sum = sheet.worksheet("Summary_By_Number")

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    draw_date = session.get("draw_date", "")
    memo = session.get("memo", "")

    # ✅ เตรียมข้อมูลสำหรับ All_Bills (แยกเลขเป็นแถว)
    rows_all = []
    for bill in bills:
        bet_type = bill.get("type", "")
        numbers = bill.get("numbers", [])
        top = float(bill.get("top", 0))
        bottom = float(bill.get("bottom", 0))
        tod = float(bill.get("tod", 0))

        for number in numbers:
            if bet_type == "2 ตัว":
                rows_all.append([timestamp, draw_date, bet_type, number, top, bottom, "", memo])
            else:  # 3 ตัว / 6 กลับ
                rows_all.append([timestamp, draw_date, bet_type, number, top, "", tod, memo])

    # ✅ เขียน All_Bills
    ws_all.append_rows(rows_all)

    # ✅ สรุปยอดรวมแต่ละเลข (รวมจากทุกราคา)
    summary_dict = {}
    for row in rows_all:
        number = row[3]
        top = float(row[4]) if row[4] else 0
        bottom = float(row[5]) if row[5] else 0
        tod = float(row[6]) if row[6] else 0

        if number not in summary_dict:
            summary_dict[number] = {"top": 0, "bottom": 0, "tod": 0}

        summary_dict[number]["top"] += top
        summary_dict[number]["bottom"] += bottom
        summary_dict[number]["tod"] += tod

    # ✅ เตรียมข้อมูล Summary_By_Number
    rows_sum = []
    for number, data in summary_dict.items():
        rows_sum.append([timestamp, number, data["top"], data["bottom"], data["tod"]])

    # ✅ เขียน Summary_By_Number
    ws_sum.append_rows(rows_sum)
