from flask import Flask, render_template, request, redirect, url_for
from save import save_to_csv  # หรือ save_to_google_sheet (ถ้ามี)
import os

app = Flask(__name__)

bills = []

@app.route("/", methods=["GET", "POST"])
def index():
    global bills
    if request.method == "POST":
        number = request.form.get("number")
        price = request.form.get("price")
        if number and price:
            bills.append({"number": number, "price": float(price)})
        return redirect(url_for('index'))
    return render_template("index.html", bills=bills)

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
