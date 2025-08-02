import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# ชื่อตารางใน Google Sheet
SHEET_NAME = "LottoBills"
WORKSHEET_NAME = "โพย"

# เชื่อมต่อ Google Sheet ด้วย Scope ครบ (Sheets + Drive)
def connect_gsheet():
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"  # ✅ เพิ่ม scope Drive
    ]
    credentials = Credentials.from_service_account_file("credentials.json", scopes=scopes)
    client = gspread.authorize(credentials)
    sheet = client.open(SHEET_NAME)
    return sheet


# บันทึกโพยลง Google Sheet
def save_to_google_sheet(bills):
    sheet = connect_gsheet()

    try:
        worksheet = sheet.worksheet(WORKSHEET_NAME)
    except gspread.exceptions.WorksheetNotFound:
        worksheet = sheet.add_worksheet(title=WORKSHEET_NAME, rows="1000", cols="10")
        worksheet.append_row(["เวลา", "เลข", "ราคา"])

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    rows = [[now, bill["number"], bill["price"]] for bill in bills]
    worksheet.append_rows(rows)
