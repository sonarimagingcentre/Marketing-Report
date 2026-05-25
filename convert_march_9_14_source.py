import json
import re
from pathlib import Path

import pandas as pd

SRC = Path("MARCH DATA 9TH - 14TH.xlsx")
OUT_JSON = Path("web_report_feb/data/march_9_14_source.json")
OUT_JS = Path("web_report_feb/data/march_9_14_source.js")
OUT_FLAT_JSON = Path("web_report_feb/march_9_14_source.json")
OUT_FLAT_JS = Path("web_report_feb/march_9_14_source.js")
OUT_GH_JSON = Path("github file/march_9_14_source.json")
OUT_GH_JS = Path("github file/march_9_14_source.js")


def norm_mod(value: object) -> str:
    s = str(value).strip().upper()
    if not s or s == "NAN":
        return "OTHER"
    if "MRI" in s:
        return "MRI"
    if re.search(r"\bCT\b|CAT", s):
        return "CT"
    if "X-RAY" in s or "XRAY" in s or "X-R" in s:
        return "XRAY"
    if s in {"US", "U/S"} or "ULTRA" in s:
        return "ULTRASOUND"
    return s


def clean_text(value: object) -> str:
    if pd.isna(value):
        return ""
    return str(value).strip()


def get_scan_count(modality: str, item_service: str) -> int:
    desc = item_service.upper()

    if modality == "XRAY":
        if "BOTH" in desc or "BILATERAL" in desc:
            return 2

    if modality == "ULTRASOUND":
        if "ABDOMINO-PELVIC" in desc or "ABDOMINAL PELVIC" in desc:
            return 2
        if "DOPPLER VENOUS" in desc and "BILATERAL" in desc:
            return 2

    if modality == "CT":
        if "CHEST" in desc and "ABDOMEN" in desc:
            return 2

    if modality == "MRI":
        if "MOBIVIEW" in desc and "WHOLE SPINE" in desc:
            return 1
        if "NECK" in desc and "POSTNASAL" in desc:
            return 2
        if "THORACO-LUMBAR SPINE" in desc or "THORACO LUMBAR SPINE" in desc:
            return 2
        if "WHOLE SPINE" in desc:
            return 3
        if "ABDOMEN" in desc and "PELV" in desc:
            return 2
        if "BRAIN" in desc and "TEMPORAL" in desc:
            return 2
        if "BOTH" in desc or "BILATERAL" in desc:
            return 2

    return 1


def main() -> None:
    df = pd.read_excel(SRC, sheet_name=0)
    df.columns = [str(c).strip() for c in df.columns]

    rows = []
    for _, r in df.iterrows():
        posting_date = pd.to_datetime(r.get("Posting Date"), errors="coerce")
        date_str = "" if pd.isna(posting_date) else posting_date.strftime("%Y-%m-%d")

        revenue = r.get("Row Total")
        try:
            revenue_val = float(revenue) if pd.notna(revenue) else 0.0
        except Exception:
            revenue_val = 0.0

        item_service = clean_text(r.get("Item/Service Description"))
        modality = norm_mod(r.get("Modalities"))
        marketer = clean_text(r.get("Marketer"))
        count = get_scan_count(modality, item_service)

        row_data = {
            "doctor": clean_text(r.get("Referring Doctor")),
            "marketer": marketer,
            "patient": clean_text(r.get("Patient Name")),
            "itemServiceDescription": item_service,
            "revenue": revenue_val,
            "modality": modality,
            "date": date_str,
            "scanCount": count,
        }

        # Keep one source row and store scanCount metadata.
        rows.append(row_data)

    payload = {"rows": rows}
    json_text = json.dumps(payload, ensure_ascii=True)
    js_text = "window.doctorRevenueData = " + json_text + ";\n"

    # Write to web_report_feb/data/ (create dir if missing)
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json_text, encoding="utf-8")
    OUT_JS.write_text(js_text, encoding="utf-8")

    # Write flat copies in web_report_feb/ root
    OUT_FLAT_JSON.write_text(json_text, encoding="utf-8")
    OUT_FLAT_JS.write_text(js_text, encoding="utf-8")

    # Write directly to github file/ folder (create dir if missing)
    OUT_GH_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_GH_JSON.write_text(json_text, encoding="utf-8")
    OUT_GH_JS.write_text(js_text, encoding="utf-8")

    grace_rows = sum(1 for row in rows if row["marketer"].strip().upper() == "GRACE")
    print(
        {
            "rows": len(rows),
            "grace": grace_rows,
            "json": str(OUT_JSON),
            "js": str(OUT_JS),
        }
    )


if __name__ == "__main__":
    main()
