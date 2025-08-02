import csv
from datetime import datetime

def save_to_csv(bills):
    filename = f"saved_bills_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    with open(filename, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["เลข", "ราคา"])
        for bill in bills:
            writer.writerow([bill["number"], bill["price"]])
