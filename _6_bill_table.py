from flask import session

def get_bill_table_data():
    return session.get("bills", [])

def calculate_total():
    bills = session.get("bills", [])
    total = 0
    for bill in bills:
        total += float(bill.get("top", 0))
        total += float(bill.get("bottom", 0))
        total += float(bill.get("tod", 0))
    return total

def render_bill_html():
    bills = session.get("bills", [])
    html_parts = []

    for idx, bill in enumerate(bills):
        bet_type = bill.get("type", "")
        
        # ✅ แก้ KeyError: ตรวจว่าบิลนี้มีเลขแบบใหม่หรือเก่า
        if "numbers" in bill:
            numbers = " ".join(bill["numbers"])
        else:
            numbers = bill.get("number", "")

        top = int(bill.get("top", 0))
        bottom = int(bill.get("bottom", 0))
        tod = int(bill.get("tod", 0))

        if bet_type == "2 ตัว":
            label = "บน x ล่าง"
            price_text = f"{top} x {bottom}"
        else:
            label = "ตรง x โต๊ด"
            price_text = f"{top} x {tod}"

        html = f"""
        <table style='width:100%; border-collapse:collapse; margin-bottom:10px;'>
            <tr style='border:1px solid #ccc;'>
                <td style='width:20%; text-align:center; border:1px solid #ccc; padding:10px;'>
                    <div style='color:#3498db; font-weight:bold;'>{bet_type}</div>
                </td>
                <td rowspan='3' style='width:60%; text-align:left; border:1px solid #ccc; padding:10px;'>{numbers}</td>
                <td rowspan='3' style='width:10%; text-align:center; border:1px solid #ccc;'>
                    <form method='POST'>
                        <input type='hidden' name='bill_idx' value='{idx}'>
                        <button type='submit' name='action' value='edit_bill' style='border:none; background-color:#fff; cursor:pointer;'>✏️</button>
                    </form>
                </td>
                <td rowspan='3' style='width:10%; text-align:center; border:1px solid #ccc;'>
                    <form method='POST'>
                        <input type='hidden' name='bill_idx' value='{idx}'>
                        <button type='submit' name='action' value='delete_bill' style='border:none; background-color:#fff; cursor:pointer;'>🗑️</button>
                    </form>
                </td>
            </tr>
            <tr><td style='text-align:center; border:1px solid #ccc;'>{label}</td></tr>
            <tr><td style='text-align:center; border:1px solid #ccc;'>{price_text}</td></tr>
        </table>
        """
        html_parts.append(html)

    return "".join(html_parts)
