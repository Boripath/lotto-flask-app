from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime
import os

import session_state
from _0_select_draw import select_draw_date_and_countdown
from _1_header import render_header
from _2_pricerate import get_pricerate
from _3_bet_type import get_bet_type
from _4_input_number import process_number_input, get_number_input, delete_number, toggle_double
from _5_input_price import get_price_inputs, set_price_inputs, submit_bill
from _6_bill_table import get_bill_table_data, calculate_total, render_bill_html
from _7_note import get_memo_and_total, set_memo
from _8_summary_footer import clear_all_data
from _9_gspread_utils import save_all_bills_to_sheet, update_summary_from_all_bills

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "lotto_secret_key")

@app.route("/", methods=["GET", "POST"])
def index():
    session_state.init_session()

    if request.method == "POST":
        action = request.form.get("action")

        if action == "set_lottery_type":
            session["lottery_type"] = request.form.get("lottery_type", "หวยรัฐบาลไทย")

        elif action == "set_pricerate":
            session["pricerate"] = int(request.form.get("pricerate", 90))

        elif action == "set_bet_type":
            session["bet_type"] = request.form.get("bet_type", "2 ตัว")

        elif action == "add_number":
            process_number_input(request.form.get("numbers_input", ""))

        elif action == "delete_number":
            delete_number(int(request.form.get("delete_idx", -1)))

        elif action == "add_bill":
            if session.get("allow_bet", True):
                set_price_inputs(
                    float(request.form.get("price_top", 0)),
                    float(request.form.get("price_bottom", 0)),
                    float(request.form.get("price_tod", 0)))
                submit_bill()

        elif action == "delete_bill":
            session_state.delete_bill(int(request.form.get("bill_idx", -1)))

        elif action == "edit_bill":
            session_state.edit_bill(int(request.form.get("bill_idx", -1)))

        elif action == "save_all":
            if session.get("allow_bet", True):
                save_all_bills_to_sheet(session.get("bills", []))
                update_summary_from_all_bills()
                clear_all_data()

        elif action == "clear_input":
            session_state.clear_input_only()

        elif action == "set_memo":
            set_memo(request.form.get("memo", ""))

        elif action == "toggle_double":
            toggle_double()
            process_number_input("")

        return redirect(url_for("index"))

    # ดึงข้อมูลแสดงผล
    draw_info, countdown_str, countdown_seconds, allow_bet = select_draw_date_and_countdown()
    header_html = render_header(draw_info, countdown_str)
    pricerate = get_pricerate()
    bet_type = get_bet_type()
    numbers, double_mode = get_number_input()
    price_top, price_bottom, price_tod = get_price_inputs()
    bills = get_bill_table_data()
    memo, total_amount = get_memo_and_total()
    bill_html = render_bill_html()

    return render_template("index.html",
                           header_html=header_html,
                           draw_info=draw_info,
                           countdown=countdown_str,
                           countdown_seconds=countdown_seconds,
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
                           double_mode=double_mode,
                           allow_bet=allow_bet)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
