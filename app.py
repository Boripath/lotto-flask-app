from flask import Flask, render_template, request, redirect, url_for
from save import save_to_google_sheet  # เปลี่ยนจาก save_to_csv
import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"  # ต้องมี เพื่อใช้ session


bills = []
MAX_PER_NUMBER = 500  # ✅ เพดานรับซื้อแต่ละเลข (บาท)

# ✅ รวมยอดซื้อแต่ละเลข
def get_summary(bills):
    summary = {}
    for bill in bills:
        num = bill["number"]
        price = float(bill["price"])
        if num not in summary:
            summary[num] = 0
        summary[num] += price
    return summary

# ✅ ตรวจว่าเลขไหนเกินเพดาน
def get_over_limit(summary, limit):
    over_limit = {}
    for num, total in summary.items():
        if total > limit:
            over_limit[num] = total
    return over_limit

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        selected_date = request.form.get("draw_date")
        if selected_date:
            session["draw_date"] = selected_date
        return redirect(url_for('index'))

    draw_date = session.get("draw_date", datetime.today().strftime("%Y-%m-%d"))
    return render_template("index.html", draw_date=draw_date)


    summary = get_summary(bills)
    over_limit = get_over_limit(summary, MAX_PER_NUMBER)
    return render_template("index.html", bills=bills, summary=summary, over_limit=over_limit, limit=MAX_PER_NUMBER)

@app.route("/clear")
def clear():
    global bills
    bills = []
    return redirect(url_for('index'))

@app.route("/save")
def save():
    global bills
    save_to_google_sheet(bills)  # เปลี่ยนจาก save_to_csv
    bills = []
    return redirect(url_for('index'))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
