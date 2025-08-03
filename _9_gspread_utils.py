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

# ✅ ฟังก์ชันที่ 2: คำนวณสรุปจาก All_Bills → เขียน Summary_By_Number
def update_summary_from_all_bills():
    sheet = connect_sheet()
    ws_all = sheet.worksheet("All_Bills")
    ws_sum = sheet.worksheet("Summary_By_Number")

    # ✅ ดึงข้อมูล All_Bills
    all_data = ws_all.get_all_values()
    if len(all_data) <= 1:
        return

    header = all_data[0]
    data_rows = all_data[1:]

    # ✅ Index
    idx_number = header.index("Number")
    idx_top = header.index("Top")
    idx_bottom = header.index("Bottom")
    idx_trong = header.index("Trong")
    idx_tod = header.index("Tod")

    # ✅ รวมยอดแต่ละเลข
    summary = {}
    for row in data_rows:
        number = row[idx_number]
        top = float(row[idx_top]) if row[idx_top] else 0
        bottom = float(row[idx_bottom]) if row[idx_bottom] else 0
        trong = float(row[idx_trong]) if row[idx_trong] else 0
        tod = float(row[idx_tod]) if row[idx_tod] else 0

        if number not in summary:
            summary[number] = {"top": 0, "bottom": 0, "trong": 0, "tod": 0}

        summary[number]["top"] += top
        summary[number]["bottom"] += bottom
        summary[number]["trong"] += trong
        summary[number]["tod"] += tod

    # ✅ เตรียมข้อมูลแบบเรียงเลขน้อย→มาก
    sorted_numbers = sorted(summary.keys(), key=lambda x: int(x))
    rows_sum = [["เลข", "รวม บน", "รวม ล่าง", "รวม ตรง", "รวม โต๊ด"]]

    for number in sorted_numbers:
        data = summary[number]
        rows_sum.append([
            number,
            data["top"],
            data["bottom"],
            data["trong"],
            data["tod"]
        ])

    # ✅ เขียนใหม่ทั้งหมดใน Summary_By_Number
    ws_sum.clear()
    ws_sum.update("A1", rows_sum)

    # ✅ ล้างสีเก่า → สีพื้นขาว
    white_bg = CellFormat(backgroundColor=Color(1, 1, 1))
    format_cell_range(ws_sum, "A2:E1000", white_bg)

    # ✅ เติมสีแดงอ่อนถ้าเกิน threshold
    red_bg = Color(1, 0.8, 0.8)

    for i, row in enumerate(rows_sum[1:], start=2):
        number, top, bottom, trong, tod = row
        red_cells = []

        if float(top) > THRESHOLD_TOP:
            red_cells.append(f"B{i}")
        if float(bottom) > THRESHOLD_BOTTOM:
            red_cells.append(f"C{i}")
        if float(trong) > THRESHOLD_TRONG:
            red_cells.append(f"D{i}")
        if float(tod) > THRESHOLD_TOD:
            red_cells.append(f"E{i}")

        if red_cells:
            red_cells.append(f"A{i}")  # ไฮไลต์ช่องเลข
            for cell in red_cells:
                format_cell_range(ws_sum, cell, CellFormat(backgroundColor=red_bg))
