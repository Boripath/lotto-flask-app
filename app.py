from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime
import os

# Import โมดูลใช้งานในระบบโพยหวย
import session_state
from _0_select_draw import select_draw_date
from _1_header import render_header
from _2_pricerate import get_pricerate
from _3_bet_type import get_bet_type
from _4_input_number import process_number_input, get_number_input, delete_number, toggle_double
from _5_input_price import get_price_inputs, set_price_inputs, submit_bill
from _6_bill_table import get_bill_table_data, calculate_total, render_bill_html
from _7_note import get_memo_and_total, set_memo
from _8_summary_footer import clear_all_data
from _9_gspread_utils import save_to_google_sheet

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "lotto_secret_key")

@app.route("/", methods=["GET", "POST"])
def index():
    session_state.init_session()

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
            process_number_input(numbers_input)

        elif action == "delete_number":
            delete_idx = int(request.form.get("delete_idx", -1))
            delete_number(delete_idx)

        elif action == "add_bill":
            price_top = float(request.form.get("price_top", 0))
            price_bottom = float(request.form.get("price_bottom", 0))
            price_tod = float(request.form.get("price_tod", 0))
            set_price_inputs(price_top, price_bottom, price_tod)
            submit_bill()

        elif action == "delete_bill":
            bill_idx = int(request.form.get("bill_idx", -1))
            session_state.delete_bill(bill_idx)
        
        elif action == "edit_bill":
            bill_idx = int(request.form.get("bill_idx", -1))
            session_state.edit_bill(bill_idx)
   
        elif action == "save_all":
            save_to_google_sheet(session_state.get_bills())
            clear_all_data()
            return redirect(url_for("index"))

        elif action == "clear_input":
            session_state.clear_input_only()

        elif action == "set_memo":
            memo_text = request.form.get("memo", "")
            set_memo(memo_text)

        elif action == "toggle_double":
            toggle_double()

        return redirect(url_for("index"))

    # ดึงข้อมูลทั้งหมดมาแสดง
    draw_date, countdown = select_draw_date()
    header_html = render_header(draw_date, countdown)
    pricerate = get_pricerate()
    bet_type = get_bet_type()
    numbers, double_mode = get_number_input()
    price_top, price_bottom, price_tod = get_price_inputs()
    bills = get_bill_table_data()
    memo, total_amount = get_memo_and_total()
    bill_html = render_bill_html()

    return render_template("index.html",
                           header_html=header_html,
                           draw_date=draw_date,
                           pricerate=pricerate,
                           bet_type=bet_type,
                           numbers=numbers,
                           price_top=price_top,
                           price_bottom=price_bottom,
                           price_tod=price_tod,
                           bills=bills,
                           memo=memo,
                           total_amount=total_amount,
                           bill_html=bill_html,
                           double_mode=double_mode)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
