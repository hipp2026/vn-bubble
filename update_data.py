from vnstock import Vnstock
import json
from datetime import datetime

symbols = ["VCB", "FPT", "HPG", "VNINDEX"]

data = {}

for sym in symbols:
    stock = Vnstock().stock(symbol=sym, source="VCI")
    df = stock.quote.history(
        start="2024-01-01",
        end=datetime.today().strftime("%Y-%m-%d"),
        interval="1D"
    )

    last = df.iloc[-1]

    data[sym] = {
        "price": float(last["close"]),
        "volume": int(last["volume"]),
        "change_pct": float(
            (last["close"] - df.iloc[-2]["close"])
            / df.iloc[-2]["close"] * 100
        )
    }

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("✅ Updated data.json")