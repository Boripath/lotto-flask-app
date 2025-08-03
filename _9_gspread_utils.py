import gspread
from google.oauth2.service_account import Credentials
from gspread_formatting import CellFormat, Color, format_cell_range
from datetime import datetime
from flask import session

# ✅ Google Sheet config
SHEET_NAME = "LottoBills"
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# ✅ Threshold ค่าที่ตั้งไว้
THRESHOLD_TOP = 100
THRESHOLD_BOTTOM = 100
THRESHOLD_TRONG = 10
THRESHOLD_TOD = 10

# ✅ เชื่อมต่อ Google Sheet
def connect_sheet():
    creds = Credentials.from_service_account_file("credentials.json", scopes=SCOPES)
    client = gspread.authorize(creds)
    return client.open(SHEET_NAME)

# ✅ ฟังก์ชันที่ 1: บันทึก All_Bills
def save_all_bills_to_sheet(bills):
    if not bills:
        return

    sheet = connect_sheet()
    ws_all = sheet.worksheet("All_Bills")

    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    draw_date = session.get("draw_date", "")
    memo = session.get("memo", "")

    rows = []
    for bill in bills:
        bet_type = bill.get("type", "")
        numbers = bill.get("numbers", [])
        top = bill.get("top", 0)
        bottom = bill.get("bottom", 0)
        tod = bill.get("tod", 0)

        for number in numbers:
            if bet_type == "2 ตัว":
                rows.append([ts, draw_date, bet_type, number, top, bottom, "", "", memo])
            else:  # 3 ตัว / 6 กลับ
                rows.append([ts, draw_date, bet_type, number, "", "", top, tod, memo])

    ws_all.append_rows(rows)

# ✅ ฟังก์ชันที่ 2: สรุปยอดและแสดง 2 คอลัมน์ (เลข 2 ตัว + 3 ตัว)
def update_summary_from_all_bills():
    sheet = connect_sheet()
    ws_all = sheet.worksheet("All_Bills")
    ws_sum = sheet.worksheet("Summary_By_Number")

    all_data = ws_all.get_all_values()
    if len(all_data) <= 1:
        return

    header = all_data[0]
    data_rows = all_data[1:]

    idx_number = header.index("Number")
    idx_top = header.index("Top")
    idx_bottom = header.index("Bottom")
    idx_trong = header.index("Trong")
    idx_tod = header.index("Tod")

    # ✅ แยกเลข 2 ตัว / 3 ตัว
    summary_2digit = {}
    summary_3digit = {}

    for row in data_rows:
        number = row[idx_number]
        top = float(row[idx_top]) if row[idx_top] else 0
        bottom = float(row[idx_bottom]) if row[idx_bottom] else 0
        trong = float(row[idx_trong]) if row[idx_trong] else 0
        tod = float(row[idx_tod]) if row[idx_tod] else 0

        if len(number) == 2:
            if number not in summary_2digit:
                summary_2digit[number] = {"top": 0, "bottom": 0}
            summary_2digit[number]["top"] += top
            summary_2digit[number]["bottom"] += bottom
        elif len(number) == 3:
            if number not in summary_3digit:
                summary_3digit[number] = {"trong": 0, "tod": 0}
            summary_3digit[number]["trong"] += trong
            summary_3digit[number]["tod"] += tod

    # ✅ เตรียมข้อมูลแสดงแบบ 2 ฝั่งในแถวเดียวกัน
    max_len = max(len(summary_2digit), len(summary_3digit))
    sorted_2 = sorted(summary_2digit.keys(), key=lambda x: int(x))
    sorted_3 = sorted(summary_3digit.keys(), key=lambda x: int(x))

    rows_sum = [["เลข 2 ตัว", "รวม บน", "รวม ล่าง", "", "เลข 3 ตัว", "รวม ตรง", "รวม โต๊ด"]]

    for i in range(max_len):
        row = []
        # ฝั่งเลข 2 ตัว
        if i < len(sorted_2):
            num2 = sorted_2[i]
            row += [num2, summary_2digit[num2]["top"], summary_2digit[num2]["bottom"]]
        else:
            row += ["", "", ""]

        row.append("")  # ช่องเว้นว่าง

        # ฝั่งเลข 3 ตัว
        if i < len(sorted_3):
            num3 = sorted_3[i]
            row += [num3, summary_3digit[num3]["trong"], summary_3digit[num3]["tod"]]
        else:
            row += ["", "", ""]

        rows_sum.append(row)

    # ✅ เขียนข้อมูลใหม่ทั้งหมดลง Summary_By_Number
    ws_sum.clear()
    ws_sum.update("A1", rows_sum)

    # ✅ ล้างสีพื้นหลังด้วยสีขาว
    white_bg = CellFormat(backgroundColor=Color(1, 1, 1))
    format_cell_range(ws_sum, "A2:G1000", white_bg)

    # ✅ ใส่สีแดงอ่อนถ้ายอดเกิน threshold
    red_bg = Color(1, 0.8, 0.8)

    for i, row in enumerate(rows_sum[1:], start=2):  # เริ่มแถว 2
        red_cells = []
        num2, top, bottom = row[0], row[1], row[2]
        num3, trong, tod = row[4], row[5], row[6]

        if num2:
            if float(top) > THRESHOLD_TOP:
                red_cells.append(f"B{i}")
            if float(bottom) > THRESHOLD_BOTTOM:
                red_cells.append(f"C{i}")
            if red_cells:
                red_cells.append(f"A{i}")  # ช่องเลข 2 ตัว

        if num3:
            if float(trong) > THRESHOLD_TRONG:
                red_cells.append(f"F{i}")
            if float(tod) > THRESHOLD_TOD:
                red_cells.append(f"G{i}")
            if "F{i}" in red_cells or "G{i}" in red_cells:
                red_cells.append(f"E{i}")  # ช่องเลข 3 ตัว

        for cell in red_cells:
            format_cell_range(ws_sum, cell, CellFormat(backgroundColor=red_bg))
