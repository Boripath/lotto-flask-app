from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime
import os

# Import โมดูลย่อยที่คุณจะสร้างทีละไฟล์
import session_state
from _0_select_draw import select_draw_date
from _1_header import render_header
from _2_pricerate import get_pricerate
from _3_bet_type import get_bet_type
from _4_input_number import process_numbers_input
from _5_input_price import process_price_input
from _6_bill_table import get_bill_table_data
from _7_note import get_memo_and_total
from _8_summary_footer import handle_actions
from _9_gspread_utils import save_to_google_sheet

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "lotto_secret_key")  # 🔐 ใช้ Session

# ✅ Route หลัก
@app.route("/", methods=["GET", "POST"])
def index():
    # ✅ เริ่มต้นค่า session_state (บิล, ข้อมูล input ฯลฯ)
    session_state.init_session()

    # ✅ อ่านค่าจาก POST (ถ้ามี) แล้วอัปเดต session
    if request.method == "POST":
        action = request.form.get("action")

        if action == "select_draw":
            selected_date = request.form.get("draw_date")
            session["draw_date"] = selected_date

        elif action == "set_pricerate":
            session["pricerate"] = int(request.form.get("pricerate", 90))

        elif action == "set_bet_type":
            session["bet_type"] = request.form.get("bet_type", "2 ตัว")

        elif action == "add_number":
            numbers_input = request.form.get("numbers_input", "")
            session_state.process_numbers(numbers_input)

        elif action == "delete_number":
            delete_idx = int(request.form.get("delete_idx", -1))
            session_state.delete_number(delete_idx)

        elif action == "add_bill":
            price_top = float(request.form.get("price_top", 0))
            price_bottom = float(request.form.get("price_bottom", 0))
            price_tod = float(request.form.get("price_tod", 0))
            session_state.add_bill(price_top, price_bottom, price_tod)

        elif action == "delete_bill":
            bill_idx = int(request.form.get("bill_idx", -1))
            session_state.delete_bill(bill_idx)

        elif action == "save_all":
            save_to_google_sheet(session_state.get_bills())
            session_state.clear_all()
            return redirect(url_for("index"))

        elif action == "clear_input":
            session_state.clear_input_only()

        return redirect(url_for("index"))

    # ✅ เตรียมข้อมูลส่งให้ index.html
    draw_date = select_draw_date()
    pricerate = get_pricerate()
    bet_type = get_bet_type()
    numbers = session_state.get_numbers()
    bills = get_bill_table_data()
    memo, total_amount = get_memo_and_total()

    return render_template("index.html",
                           draw_date=draw_date,
                           pricerate=pricerate,
                           bet_type=bet_type,
                           numbers=numbers,
                           bills=bills,
                           memo=memo,
                           total_amount=total_amount)


# ✅ Run Flask app
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
