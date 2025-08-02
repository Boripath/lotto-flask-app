from flask import Flask, render_template, request, redirect, url_for
from save import save_to_csv
import os

app = Flask(__name__)

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
    global bills
    if request.method == "POST":
        number = request.form.get("number")
        price = request.form.get("price")
        if number and price:
            bills.append({"number": number, "price": float(price)})
        return redirect(url_for('index'))

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
    save_to_csv(bills)
    bills = []
    return redirect(url_for('index'))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
