import json
from datetime import datetime
import pandas as pd

from vnstock import stock_historical_data
from vnstock.connector.xno import xno_market_data


# ================== CONFIG ==================
VN30 = [
    "FPT", "VCB", "HPG", "SSI", "TCB", "VHM",
    "MWG", "BID", "CTG", "VPB"
]

VN100 = VN30 + [
    "GAS", "VNM", "POW", "MSN", "BVH",
    "PLX", "REE", "SAB"
]

TODAY = datetime.now().strftime("%Y-%m-%d")


# ================== CORE FUNCTIONS ==================
def get_stock_data(symbol):
    """
    Lấy giá + volume gần nhất (HOSE)
    """
    try:
        df = stock_historical_data(
            symbol=symbol,
            start_date="2025-01-01",
            end_date=TODAY,
            resolution="1D",
            type="stock",
            source="VCI"
        )

        if df.empty or len(df) < 2:
            return None

        last = df.iloc[-1]
        prev = df.iloc[-2]

        price = float(last["close"])
        volume = float(last["volume"])
        change_pct = (price - prev["close"]) / prev["close"] * 100
        value = price * volume / 1e9  # GTGD (tỷ)

        return {
            "symbol": symbol,
            "price": round(price, 2),
            "change_pct": round(change_pct, 2),
            "volume": int(volume),
            "value": round(value, 2),
            "flow": "IN" if change_pct > 0 else "OUT"
        }

    except Exception as e:
        print(f"❌ {symbol} error:", e)
        return None


def build_index(symbols):
    stocks = []
    total_value = 0
    flow_score = 0

    for s in symbols:
        data = get_stock_data(s)
        if not data:
            continue

        stocks.append(data)
        total_value += data["value"]
        flow_score += data["change_pct"]

    return {
        "total_value": round(total_value, 2),
        "money_flow": "IN" if flow_score > 0 else "OUT",
        "stocks": sorted(stocks, key=lambda x: x["value"], reverse=True)
    }


# ================== BUILD DATA ==================
def main():
    print("⏳ Building data.json ...")

    data = {
        "updated": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "indexes": {
            "VN30": build_index(VN30),
            "VN100": build_index(VN100)
        }
    }

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("✅ data.json updated successfully")


if __name__ == "__main__":
    main()