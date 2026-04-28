# services/diet_service.py
# eita diet recommendation er backend logic
# user er age, weight, disease input niye personalized diet plan return kore

from config.db_config import get_connection, close_connection


def get_diet_by_disease(disease: str) -> str:
    """
    Disease name diye database theke diet recommendation fetch kore.
    Jodi database e na thake, general recommendation return kore.
    """
    conn = get_connection()
    if not conn:
        return _general_diet()  # connection fail hole general diet debo

    try:
        cursor = conn.cursor(dictionary=True)

        # disease name diye diet plan khuje ber korbo (case-insensitive)
        cursor.execute(
            "SELECT recommendation FROM diet_plans WHERE disease LIKE %s",
            (f"%{disease}%",)
        )
        result = cursor.fetchone()

        if result:
            return result["recommendation"]
        else:
            return _general_diet()  # match na hole general diet

    except Exception as e:
        print(f"[Diet Service ERROR] {e}")
        return _general_diet()

    finally:
        close_connection(conn)


def get_personalized_diet(age: int, weight: float, disease: str) -> str:
    """
    Age, weight, disease niye ekটা personalized diet plan generate kore.
    Rule-based approach use kora hocche ekhane.
    """
    # BMI calculate kora hocche — weight/height^2, ekhane simplified version
    # Ideal weight range assume kora hocche height theke

    lines = []

    # base diet — disease er upor base kora
    base_diet = get_diet_by_disease(disease)
    lines.append(f"📋 Disease-based Diet: {disease}")
    lines.append("-" * 40)
    lines.append(base_diet)
    lines.append("")

    # age-based additional advice
    lines.append("👤 Age-based Recommendations:")
    if age < 18:
        lines.append("• Calcium-rich foods (milk, dairy) — bone development er jonno")
        lines.append("• Iron-rich foods — anemia theke bachao")
        lines.append("• High protein diet — growth er jonno")
    elif age <= 40:
        lines.append("• Balanced diet with all nutrients")
        lines.append("• Regular hydration (8-10 glasses water daily)")
        lines.append("• Fiber-rich foods — digestion bhalo rakhte")
    elif age <= 60:
        lines.append("• Calcium + Vitamin D — bone health er jonno")
        lines.append("• Low saturated fat — heart health er jonno")
        lines.append("• Antioxidant foods — cell damage theke bachao")
    else:
        lines.append("• Soft, easy to digest foods")
        lines.append("• High Vitamin B12 — nerve health er jonno")
        lines.append("• Low sodium — blood pressure control er jonno")

    lines.append("")

    # weight-based advice
    lines.append("⚖️ Weight-based Recommendations:")
    if weight < 50:
        lines.append("• Calorie-dense healthy foods — weight gain er jonno")
        lines.append("• Nuts, avocado, whole grains, legumes")
        lines.append("• 5-6 small meals per day")
    elif weight <= 80:
        lines.append("• Maintain current healthy weight")
        lines.append("• Balanced macros: 40% carbs, 30% protein, 30% fat")
    elif weight <= 100:
        lines.append("• Moderate calorie reduction — weight control")
        lines.append("• Increase vegetables and fruits")
        lines.append("• Avoid fried and processed foods")
    else:
        lines.append("• Low carb, high protein diet")
        lines.append("• Avoid sugar, fast food, soft drinks")
        lines.append("• Consult a nutritionist for structured plan")

    lines.append("")
    lines.append("💧 General Daily Habits:")
    lines.append("• Drink at least 8 glasses of water daily")
    lines.append("• Eat slowly and mindfully")
    lines.append("• Avoid eating 2 hours before sleep")
    lines.append("• Include at least 30 min exercise daily")

    return "\n".join(lines)


def _general_diet() -> str:
    """
    Jodi specific disease-based diet na thake, eita default return hobe.
    """
    return (
        "Balanced diet follow korun:\n"
        "• Beshi shobji o fol khun\n"
        "• Processed food avoid korun\n"
        "• Pani beshi khun (8-10 glass daily)\n"
        "• Regular exercise korun\n"
        "• Salt o sugar kom khun"
    )


def get_all_diet_plans() -> list:
    """
    Database theke sob diet plans fetch kore — diet list screen er jonno.
    """
    conn = get_connection()
    if not conn:
        return []

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM diet_plans ORDER BY disease ASC")
        return cursor.fetchall()

    except Exception as e:
        print(f"[Diet Service ERROR] {e}")
        return []

    finally:
        close_connection(conn)