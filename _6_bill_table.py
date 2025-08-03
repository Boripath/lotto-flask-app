# _6_bill_table.py
from flask import session
from utils import format_currency

def get_bill_table_data():
    bills = session.get("bills", [])
    table_rows = []

    grouped = {}
    for bill in bills:
        key = (bill.get("type", ""), bill.get("top", 0), bill.get("bottom", 0), bill.get("tod", 0))
        if key not in grouped:
            grouped[key] = []
        grouped[key].append(bill.get("number", ""))

    for idx, ((bet_type, top, bottom, tod), numbers) in enumerate(grouped.items()):
        table_rows.append({
            "idx": idx,
            "type": bet_type,
            "top": top,
            "bottom": bottom,
            "tod": tod,
            "numbers": " ".join(numbers)
        })

    return table_rows

def calculate_total():
    bills = session.get("bills", [])
    total = 0
    for bill in bills:
        total += float(bill.get("top", 0))
        total += float(bill.get("bottom", 0))
        total += float(bill.get("tod", 0))
    return total

def render_bill_html():
    rows = get_bill_table_data()
    html_parts = []

    for row in rows:
        bet_type = row["type"]
        numbers = row["numbers"]
        top = int(row["top"])
        bottom = int(row["bottom"])
        tod = int(row["tod"])

        if bet_type == "2 ตัว":
            label = "บน x ล่าง"
            price_text = f"{top} x {bottom}"
        else:
            label = "ตรง x โต๊ด"
            price_text = f"{top} x {tod}"

        html = f"""
        <table style='width:100%; border-collapse:collapse; margin-bottom:10px;'>
            <tr style='border:1px solid #ccc;'>
                <td style='width:20%; text-align:center; vertical-align:middle; border:1px solid #ccc; padding:10px;'>
                    <div style='color:#3498db; font-weight:bold;'>{bet_type}</div>
                </td>
                <td rowspan='3' style='width:60%; text-align:left; vertical-align:middle; border:1px solid #ccc; padding:10px;'>
                    {numbers}
                </td>
                <td rowspan='3' style='width:10%; text-align:center; vertical-align:middle; border:1px solid #ccc;'>
                    <form method='POST'>
                        <input type='hidden' name='bill_idx' value='{row['idx']}'>
                        <button type='submit' name='action' value='edit_bill' style='border:none; background-color:#fff; cursor:pointer;'>✏️</button>
                    </form>
                </td>
                <td rowspan='3' style='width:10%; text-align:center; vertical-align:middle; border:1px solid #ccc;'>
                    <form method='POST'>
                        <input type='hidden' name='bill_idx' value='{row['idx']}'>
                        <button type='submit' name='action' value='delete_bill' style='border:none; background-color:#fff; cursor:pointer;'>🗑️</button>
                    </form>
                </td>
            </tr>
            <tr style='border:1px solid #ccc;'>
                <td style='text-align:center; border:1px solid #ccc; padding:5px;'>
                    <div style='color:#e74c3c;'>{label}</div>
                </td>
            </tr>
            <tr style='border:1px solid #ccc;'>
                <td style='text-align:center; border:1px solid #ccc; padding:5px;'>
                    <div style='color:#3498db;'>{price_text}</div>
                </td>
            </tr>
        </table>
        """
        html_parts.append(html)

    return "".join(html_parts)
