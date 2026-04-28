# services/lab_service.py
# eita lab report analyze korar backend logic
# OCR theke extracted text niye values parse kore normal/abnormal check kore

import re  # regular expression — text theke numbers extract korar jonno
from config.db_config import get_connection, close_connection


# ============================
# NORMAL RANGES FOR LAB VALUES
# ============================

# ekhane common lab test er normal range define kora ache
# (min, max, unit) format
LAB_NORMAL_RANGES = {
    # Blood Sugar
    "glucose":         (70,   100,   "mg/dL",  "Blood Glucose (Fasting)"),
    "blood sugar":     (70,   100,   "mg/dL",  "Blood Sugar"),
    "hba1c":           (4.0,  5.6,   "%",       "HbA1c"),

    # Cholesterol
    "cholesterol":     (0,    200,   "mg/dL",  "Total Cholesterol"),
    "ldl":             (0,    100,   "mg/dL",  "LDL Cholesterol"),
    "hdl":             (60,   999,   "mg/dL",  "HDL Cholesterol"),
    "triglycerides":   (0,    150,   "mg/dL",  "Triglycerides"),

    # Blood Pressure
    "systolic":        (90,   120,   "mmHg",   "Systolic BP"),
    "diastolic":       (60,   80,    "mmHg",   "Diastolic BP"),

    # Blood Count
    "hemoglobin":      (12.0, 17.5,  "g/dL",   "Hemoglobin"),
    "hgb":             (12.0, 17.5,  "g/dL",   "Hemoglobin"),
    "wbc":             (4.5,  11.0,  "x10^9/L","White Blood Cells"),
    "rbc":             (4.5,  5.9,   "x10^12/L","Red Blood Cells"),
    "platelets":       (150,  400,   "x10^9/L","Platelets"),
    "platelet":        (150,  400,   "x10^9/L","Platelets"),

    # Kidney Function
    "creatinine":      (0.6,  1.2,   "mg/dL",  "Creatinine"),
    "urea":            (7,    25,    "mg/dL",  "Blood Urea"),
    "uric acid":       (2.4,  7.0,   "mg/dL",  "Uric Acid"),

    # Liver Function
    "bilirubin":       (0.2,  1.2,   "mg/dL",  "Total Bilirubin"),
    "sgpt":            (7,    56,    "U/L",    "SGPT (ALT)"),
    "sgot":            (10,   40,    "U/L",    "SGOT (AST)"),
    "alt":             (7,    56,    "U/L",    "ALT"),
    "ast":             (10,   40,    "U/L",    "AST"),

    # Thyroid
    "tsh":             (0.4,  4.0,   "mIU/L",  "TSH"),
    "t3":              (80,   200,   "ng/dL",  "T3"),
    "t4":              (5.0,  12.0,  "μg/dL",  "T4"),
}


def analyze_report_text(text: str) -> list:
    """
    Lab report er extracted text analyze kore.
    Protiটা recognized value ke normal/abnormal check kore result list return kore.
    Returns list of dicts: {name, value, unit, status, normal_range, display_name}
    """
    if not text.strip():
        return []

    results = []
    text_lower = text.lower()

    # protiটা known lab test keyword check kora hocche
    for keyword, (min_val, max_val, unit, display_name) in LAB_NORMAL_RANGES.items():
        # keyword text e ache kina check koro
        if keyword in text_lower:
            # keyword er kache kache number extract korar cheshta
            # Pattern: keyword er pore kono number (decimal o support kore)
            pattern = rf"{re.escape(keyword)}[\s:=\-]*(\d+\.?\d*)"
            match = re.search(pattern, text_lower)

            if match:
                try:
                    value = float(match.group(1))

                    # normal range er sathe compare kora hocche
                    if min_val <= value <= max_val:
                        status = "NORMAL"
                    elif value < min_val:
                        status = "LOW"
                    else:
                        status = "HIGH"

                    results.append({
                        "name":         keyword,
                        "display_name": display_name,
                        "value":        value,
                        "unit":         unit,
                        "status":       status,
                        "normal_range": f"{min_val} - {max_val} {unit}",
                        "min":          min_val,
                        "max":          max_val,
                    })
                except ValueError:
                    pass  # number parse na hole skip koro

    return results


def save_report(user_id: int, report_text: str) -> dict:
    """
    OCR extracted report text database e save kore.
    User future e report history dekhte parbe.
    """
    conn = get_connection()
    if not conn:
        return {"success": False, "message": "Database connection fail!"}

    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO reports (user_id, report_text) VALUES (%s, %s)",
            (user_id, report_text)
        )
        conn.commit()
        return {"success": True, "message": "Report save hoyeche!"}

    except Exception as e:
        return {"success": False, "message": f"Report save error: {e}"}

    finally:
        close_connection(conn)


def get_status_color(status: str) -> str:
    """
    Lab value er status hisebe color return kore — UI highlight er jonno.
    """
    # status anujaye color return kora hocche theme.py COLORS er sathe match kore
    return {
        "NORMAL": "#2ECC71",   # green — normal range
        "LOW":    "#3498DB",   # blue — normal er niche
        "HIGH":   "#E74C3C",   # red — normal er upore
    }.get(status, "#A0AEC0")   # default grey