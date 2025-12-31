import json
from vnstock import Vnstock

# ================== CONFIG ==================
GROUPS = {
    "VN30": [
        "VCB","TCB","BID","CTG","VPB",
        "FPT","MWG","HPG","SSI","VHM"
    ],
    "VN100": [
        "VCB","TCB","FPT","HPG","SSI",
        "MWG","VNM","VHM","GAS","POW"
    ]
}

# ================== INIT ==================
vn = Vnstock().stock(source="xno")

result = {}

# ================== BUILD DATA ==================
for group, symbols in GROUPS.items():
    stocks = []
    total_value = 0
    flow_score = 0

    for s in symbols:
        try:
            q = vn.quote(symbol=s)

            value = float(q.get("value", 0))
            change = float(q.get("pct_change", 0))

            flow = "IN" if change > 0 else "OUT" if change < 0 else "NEUTRAL"

            stocks.append({
                "symbol": s,
                "value": round(value, 2),
                "change": round(change, 2),
                "flow": flow
            })

            total_value += value
            flow_score += change * value

        except Exception as e:
            print(f"Skip {s}: {e}")

    result[group] = {
        "index": round(flow_score / total_value, 2) if total_value else 0,
        "total": round(total_value, 0),
        "money": "IN" if flow_score > 0 else "OUT",
        "sectors": [],   # có thể mở rộng sau
        "stocks": sorted(
            stocks,
            key=lambda x: x["value"],
            reverse=True
        )
    }

# ================== SAVE ==================
with open("../web/data.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print("✅ data.json generated")