import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
from flask import session

SHEET_NAME = "LottoBills"
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

def connect_sheet():
    creds = Credentials.from_service_account_file("credentials.json", scopes=SCOPES)
    client = gspread.authorize(creds)
    sheet = client.open(SHEET_NAME)
    return sheet

def save_to_google_sheet(bills):
    if not bills:
        return

    sheet = connect_sheet()
    ws_all = sheet.worksheet("All_Bills")
    ws_sum = sheet.worksheet("Summary_By_Number")

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    draw_date = session.get("draw_date", "")
    memo = session.get("memo", "")

    # ✅ ตั้งค่าขีดจำกัดยอด (thresholds)
    threshold_top = 100
    threshold_bottom = 100
    threshold_trong = 10
    threshold_tod = 10

    # ✅ เตรียมข้อมูลสำหรับ All_Bills
    rows_all = []
    for bill in bills:
        bet_type = bill.get("type", "")
        numbers = bill.get("numbers", [])
        top = float(bill.get("top", 0))
        bottom = float(bill.get("bottom", 0))
        tod = float(bill.get("tod", 0))

        for number in numbers:
            if bet_type == "2 ตัว":
                rows_all.append([timestamp, draw_date, bet_type, number, top, bottom, "", "", memo])
            else:  # 3 ตัว / 6 กลับ
                rows_all.append([timestamp, draw_date, bet_type, number, "", "", top, tod, memo])

    # ✅ เขียน All_Bills (append)
    ws_all.append_rows(rows_all)

    # ✅ สรุปยอดเลขทั้งหมด (รวมจาก rows_all)
    summary_dict = {}
    for row in rows_all:
        number = row[3]
        top = float(row[4]) if row[4] else 0
        bottom = float(row[5]) if row[5] else 0
        trong = float(row[6]) if row[6] else 0
        tod = float(row[7]) if row[7] else 0

        if number not in summary_dict:
            summary_dict[number] = {"top": 0, "bottom": 0, "trong": 0, "tod": 0}

        summary_dict[number]["top"] += top
        summary_dict[number]["bottom"] += bottom
        summary_dict[number]["trong"] += trong
        summary_dict[number]["tod"] += tod

    # ✅ เตรียม Summary: เรียงเลขจากน้อย → มาก
    rows_sum = [["เลข", "รวม บน", "รวม ล่าง", "รวม ตรง", "รวม โต๊ด"]]
    numbers_sorted = sorted(summary_dict.keys(), key=lambda x: int(x))

    for number in numbers_sorted:
        data = summary_dict[number]
        rows_sum.append([number, data["top"], data["bottom"], data["trong"], data["tod"]])

    # ✅ ล้างข้อมูลเก่า + เขียนใหม่ใน Summary_By_Number
    ws_sum.clear()
    ws_sum.update("A1", rows_sum)

    # ✅ เพิ่มสีแดงอ่อนถ้าเกิน threshold
    from gspread_formatting import CellFormat, Color, format_cell_range

    red_bg = Color(1, 0.8, 0.8)  # แดงอ่อน
    default_bg = Color(1, 1, 1)

    for i, row in enumerate(rows_sum[1:], start=2):  # เริ่มจากแถว 2
        num, top, bottom, trong, tod = row
        format_ranges = []

        if top > threshold_top:
            format_ranges.append(f"B{i}")
        if bottom > threshold_bottom:
            format_ranges.append(f"C{i}")
        if trong > threshold_trong:
            format_ranges.append(f"D{i}")
        if tod > threshold_tod:
            format_ranges.append(f"E{i}")
        if format_ranges:
            format_ranges.append(f"A{i}")  # เลข ต้องแดงด้วยถ้าเกิน

        for cell in format_ranges:
            format_cell_range(ws_sum, cell, CellFormat(backgroundColor=red_bg))
