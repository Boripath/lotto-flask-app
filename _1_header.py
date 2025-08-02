from flask import session

# ✅ แสดงหัวเว็บ ชื่อหวย + งวด + เวลานับถี่ ปิดโพย

def render_header(draw_date_str, countdown_str):
    flag_url = "https://upload.wikimedia.org/wikipedia/commons/a/a9/Flag_of_Thailand.svg"
    lottery_name = "หวยรัฐบาลไทย"

    # เสริ่ม HTML Header
    header_html = f"""
    <div style='background:#fff; padding:10px 20px; border-radius:8px; border:1px solid #ccc; margin-bottom:10px;'>
        <table style='width:100%; vertical-align:middle;'>
            <tr>
                <td style='font-size:20px;'>
                    <img src='{flag_url}' width='30' style='vertical-align: middle;'>
                    <b>{lottery_name}</b>
                    งวด <b>{draw_date_str or "-"}</b>
                </td>
                <td style='text-align:right; font-size:16px;'>
                    <span style='color:red;'>{countdown_str}</span>
                </td>
            </tr>
        </table>
    </div>
    """
    return header_html
