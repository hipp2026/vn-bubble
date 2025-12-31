from xnoapi import client
from xnoapi.vn.data import stocks
import json
from datetime import datetime

# ===== INIT =====
client()  # nếu có API KEY thì truyền vào

VN30 = [
    "VCB","BID","CTG","TCB","VPB",
    "FPT","VNM","HPG","MWG","GAS",
    "VIC","VHM","VRE","SSI","STB",
    "MSN","SAB","PLX","POW","BVH",
    "ACB","SHB","TPB","MBB","HDB",
    "PNJ","GVR","BCM","VJC","VIB"
]

result = []

for s in VN30:
    try:
        info = stocks.get_stock_info(s)

        price = info["close"]
        vol = info["volume"]
        change = info["pct_change"]

        money = price * vol * change / 100 / 1e9  # tỷ VND

        result.append({
            "s": s,
            "price": price,
            "vol": vol,
            "p": change,
            "money": round(money, 2)
        })
    except:
        pass

data = {
    "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
    "group": "VN30",
    "stocks": result
}

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("UPDATED data.json")