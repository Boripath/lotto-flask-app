# _9_gspread_utils.py
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# ✅ เชื่อมต่อ Google Sheet
SHEET_NAME = "LottoBills"

# ✅ เชื่อ Scope สอนุํม Sheets + Drive
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# ✅ เชื่อไฟล์ credentials.json ที่ถูกวางไว้ใน root

def connect_sheet():
    creds = Credentials.from_service_account_file("credentials.json", scopes=SCOPES)
    client = gspread.authorize(creds)
    sheet = client.open(SHEET_NAME)
    return sheet

# ✅ บันทึกบิลไป Google Sheet (2 ชีท: โพย+รวม)

def save_to_google_sheet(bills):
    if not bills:
        return

    sheet = connect_sheet()
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # กรรมเป็น rows โพย
    rows = []
    for bill in bills:
        rows.append([
            ts,
            bill.get("draw_date", ""),
            bill.get("type", ""),
            bill.get("number", ""),
            bill.get("top", 0),
            bill.get("bottom", 0),
            bill.get("tod", 0)
        ])

    # เขียน "Bills" และ append
    ws1 = sheet.worksheet("Bills")
    ws1.append_rows(rows)

    # ✅ รวมยอดตามเลข
    summary = {}
    for bill in bills:
        key = bill.get("number", "")
        if key not in summary:
            summary[key] = {"top": 0, "bottom": 0, "tod": 0}
        summary[key]["top"] += bill.get("top", 0)
        summary[key]["bottom"] += bill.get("bottom", 0)
        summary[key]["tod"] += bill.get("tod", 0)

    sum_rows = []
    for number, data in summary.items():
        sum_rows.append([ts, number, data["top"], data["bottom"], data["tod"]])

    # เขียน "Summary" และ append
    ws2 = sheet.worksheet("Summary")
    ws2.append_rows(sum_rows)
