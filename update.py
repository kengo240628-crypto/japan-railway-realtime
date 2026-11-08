
import json
import urllib.request
from datetime import datetime, timezone

API_URL = "https://train.teraren.com/lines.json"
OUTPUT_FILE = "data.json"

def main():
    print("全国の路線データを取得中...")

    request = urllib.request.Request(
        API_URL,
        headers={"User-Agent": "JapanRailwayRealtime/1.0"}
    )

    with urllib.request.urlopen(request, timeout=30) as response:
        raw_data = json.loads(response.read().decode("utf-8"))

    if not isinstance(raw_data, list) or not raw_data:
        raise ValueError("路線データが正しくありません")

    routes = []

    for item in raw_data:
        name = item.get("line_name") or item.get("name")
        if not name:
            continue

        company = (
            item.get("company_name")
            or item.get("operator_name")
            or item.get("company")
            or item.get("operator")
            or ""
        )

        routes.append({
            "id": str(item.get("line_cd", "")),
            "name": name,
            "company": company,
            "region": "",
            "status": "unknown",
            "reason": "",
            "location": "",
            "time": ""
        })

    if not routes:
        raise ValueError("有効な路線がありません")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(routes, file, ensure_ascii=False, indent=2)

    print(f"{len(routes)}路線を保存しました")
    print("運行状況はまだ未取得です")

if __name__ == "__main__":
    main()
