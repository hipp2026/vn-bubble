from vnstock import Vnstock
from datetime import datetime
import json

symbols = ["VCB", "FPT", "HPG", "BID", "CTG"]

data = {}

for sym in symbols:
    stock = Vnstock().stock(symbol=sym, source="VCI")
    df = stock.quote.history(
        start="2024-01-01",
        end=datetime.today().strftime("%Y-%m-%d"),
        interval="1D"
    )

    last = df.iloc[-1]
    prev = df.iloc[-2]

    data[sym] = {
        "price": float(last["close"]),
        "volume": int(last["volume"]),
        "change_pct": round(
            (last["close"] - prev["close"]) / prev["close"] * 100, 2
        )
    }

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("✅ data.json updated")