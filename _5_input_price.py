# _5_input_price.py
from flask import session
from session_state import add_bill

# ✅ จัดการราคาบน/ล่าง/โต๊ด และเพิ่มบิล

# ✅ คืนค่าราคาใน session

def get_price_inputs():
    return (
        float(session.get("price_top", 0)),
        float(session.get("price_bottom", 0)),
        float(session.get("price_tod", 0))
    )

# ✅ เซตค่าราคา

def set_price_inputs(top, bottom, tod):
    session["price_top"] = top
    session["price_bottom"] = bottom
    session["price_tod"] = tod

# ✅ เพิ่มบิลจากราคาปัจจุบ และเลขที่กรอก

def submit_bill():
    top = session.get("price_top", 0)
    bottom = session.get("price_bottom", 0)
    tod = session.get("price_tod", 0)
    add_bill(top, bottom, tod)
