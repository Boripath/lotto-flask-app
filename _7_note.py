def get_memo_and_total():
    memo = session.get("memo", "")
    bills = session.get("bills", [])
    total_amount = 0

    for bill in bills:
        numbers = bill.get("numbers", [])
        count = len(numbers)
        bet_type = bill.get("type", "2 ตัว")
        top = float(bill.get("top", 0))
        bottom = float(bill.get("bottom", 0))
        tod = float(bill.get("tod", 0))

        if bet_type == "2 ตัว":
            total_amount += count * (top + bottom)
        else:
            total_amount += count * (top + tod)

    return memo, total_amount
