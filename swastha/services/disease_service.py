# services/disease_service.py
# eita disease prediction ar disease information er backend logic
# symptom input niye possible diseases return korbe

from config.db_config import get_connection, close_connection


# ============================
# RULE-BASED SYMPTOM → DISEASE MAP
# ============================

# eita ekta manual symptom-to-disease mapping
# jodi ML model use na kori, ekhane rule-based prediction hobe
# key = disease name, value = list of associated symptoms (lowercase)

SYMPTOM_DISEASE_MAP = {
    "Diabetes": [
        "frequent urination", "excessive thirst", "blurred vision",
        "fatigue", "weight loss", "slow healing wounds", "hunger"
    ],
    "Hypertension": [
        "headache", "dizziness", "chest pain", "shortness of breath",
        "nosebleed", "blurred vision", "palpitations"
    ],
    "Dengue": [
        "high fever", "severe headache", "joint pain", "muscle pain",
        "rash", "vomiting", "nausea", "eye pain", "fatigue"
    ],
    "Common Cold": [
        "runny nose", "sore throat", "cough", "sneezing",
        "mild fever", "congestion", "headache"
    ],
    "Typhoid": [
        "high fever", "stomach pain", "headache", "weakness",
        "diarrhea", "constipation", "loss of appetite", "rash"
    ],
    "Malaria": [
        "high fever", "chills", "sweating", "headache",
        "muscle pain", "nausea", "vomiting", "fatigue"
    ],
    "Asthma": [
        "wheezing", "shortness of breath", "chest tightness",
        "cough", "difficulty breathing", "night cough"
    ],
    "Anemia": [
        "fatigue", "weakness", "pale skin", "shortness of breath",
        "dizziness", "cold hands", "headache", "chest pain"
    ],
    "Gastritis": [
        "stomach pain", "nausea", "vomiting", "bloating",
        "loss of appetite", "indigestion", "burning sensation"
    ],
    "Arthritis": [
        "joint pain", "swelling", "stiffness", "reduced mobility",
        "redness", "warmth in joints", "fatigue"
    ],
}


def predict_disease(symptoms_input: str) -> list:
    """
    User er symptom input niye possible diseases predict kore.
    Rule-based scoring system use kora hocche.
    Joto beshi symptom match, toto beshi score.
    Returns: list of dicts sorted by match score (highest first)
    """
    if not symptoms_input.strip():
        return []

    # user er input lowercase kore, comma/newline e split kora hocche
    user_symptoms = [
        s.strip().lower()
        for s in symptoms_input.replace("\n", ",").split(",")
        if s.strip()
    ]

    results = []

    # protiটা disease er sathe user symptoms compare kora hocche
    for disease, disease_symptoms in SYMPTOM_DISEASE_MAP.items():
        matched = []

        for us in user_symptoms:
            for ds in disease_symptoms:
                # partial match check — "fever" likhlei "high fever" match korbe
                if us in ds or ds in us:
                    if ds not in matched:
                        matched.append(ds)
                    break

        if matched:
            # match score calculate kora hocche percentage e
            score = len(matched) / len(disease_symptoms) * 100

            results.append({
                "disease": disease,
                "matched_symptoms": matched,
                "score": round(score, 1),
                "total_symptoms": len(disease_symptoms)
            })

    # score er highest theke sort kore return kora hocche
    results.sort(key=lambda x: x["score"], reverse=True)

    # top 5 result return korbo
    return results[:5]


def get_all_diseases() -> list:
    """
    Database theke sob diseases fetch kore list e return kore.
    Disease Info screen e use hobe.
    """
    conn = get_connection()
    if not conn:
        return []

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM diseases ORDER BY name ASC")
        return cursor.fetchall()

    except Exception as e:
        print(f"[Disease Service ERROR] {e}")
        return []

    finally:
        close_connection(conn)


def get_disease_by_name(name: str) -> dict | None:
    """
    Ekটা specific disease er full info database theke niye ase.
    Disease name diye search kore.
    """
    conn = get_connection()
    if not conn:
        return None

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM diseases WHERE name LIKE %s",
            (f"%{name}%",)
        )
        return cursor.fetchone()  # prothom match return korbo

    except Exception as e:
        print(f"[Disease Service ERROR] {e}")
        return None

    finally:
        close_connection(conn)


def get_health_alerts() -> list:
    """
    Database theke sob active health alerts fetch kore.
    Dashboard e show kora hobe.
    Severity High theke sort kora hocche.
    """
    conn = get_connection()
    if not conn:
        return []

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT * FROM alerts
            ORDER BY
                FIELD(severity, 'High', 'Medium', 'Low'),
                created_at DESC
            LIMIT 10
        """)
        return cursor.fetchall()

    except Exception as e:
        print(f"[Alert Service ERROR] {e}")
        return []

    finally:
        close_connection(conn)