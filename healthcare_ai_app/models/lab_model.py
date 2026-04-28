"""
Lab Report Analyzer Model
Interprets common lab values and provides explanations.
"""

from typing import Dict, Tuple


# Reference ranges and interpretations
LAB_RANGES = {
    "blood_sugar": {
        "label": "Blood Sugar (Fasting)",
        "unit": "mg/dL",
        "ranges": [
            (0, 70, "Low", "⚠️", "#E74C3C",
             "Hypoglycemia detected. Eat something sweet immediately. If severe, seek emergency care."),
            (70, 100, "Normal", "✅", "#28B463",
             "Your fasting blood sugar is in the healthy range. Maintain a balanced diet."),
            (100, 126, "Pre-diabetic", "⚠️", "#E67E22",
             "Slightly elevated. Indicates pre-diabetes. Exercise regularly, reduce sugar intake."),
            (126, 300, "High (Diabetic Range)", "🔴", "#E74C3C",
             "Significantly elevated. Consistent values indicate Type 2 Diabetes. Consult a doctor."),
            (300, 9999, "Critical High", "🆘", "#8E44AD",
             "Dangerously high. Seek emergency medical care immediately."),
        ]
    },
    "cholesterol": {
        "label": "Total Cholesterol",
        "unit": "mg/dL",
        "ranges": [
            (0, 200, "Desirable", "✅", "#28B463",
             "Excellent cholesterol level! Maintain with a heart-healthy diet."),
            (200, 240, "Borderline High", "⚠️", "#E67E22",
             "Borderline high. Reduce saturated fats, increase fiber intake, exercise more."),
            (240, 9999, "High", "🔴", "#E74C3C",
             "High cholesterol increases cardiovascular risk. Consult a doctor about medication and diet."),
        ]
    },
    "systolic_bp": {
        "label": "Systolic Blood Pressure",
        "unit": "mmHg",
        "ranges": [
            (0, 90, "Low (Hypotension)", "⚠️", "#E74C3C",
             "Low blood pressure. Stay hydrated, add salt if advised, change positions slowly."),
            (90, 120, "Normal", "✅", "#28B463",
             "Excellent blood pressure! Keep up your healthy habits."),
            (120, 130, "Elevated", "⚠️", "#E67E22",
             "Slightly elevated. Reduce sodium, manage stress, increase physical activity."),
            (130, 140, "High Stage 1", "🔴", "#E74C3C",
             "High blood pressure Stage 1. Lifestyle changes recommended. Monitor regularly."),
            (140, 180, "High Stage 2", "🔴", "#E74C3C",
             "High blood pressure Stage 2. Medication likely needed. See your doctor."),
            (180, 9999, "Hypertensive Crisis", "🆘", "#8E44AD",
             "HYPERTENSIVE CRISIS! Seek emergency care immediately."),
        ]
    },
    "diastolic_bp": {
        "label": "Diastolic Blood Pressure",
        "unit": "mmHg",
        "ranges": [
            (0, 60, "Low", "⚠️", "#E74C3C",
             "Low diastolic pressure. Monitor closely and consult a doctor if symptomatic."),
            (60, 80, "Normal", "✅", "#28B463",
             "Normal diastolic pressure. Maintain healthy lifestyle."),
            (80, 90, "High Stage 1", "⚠️", "#E67E22",
             "Slightly elevated diastolic pressure. Lifestyle modifications recommended."),
            (90, 120, "High Stage 2", "🔴", "#E74C3C",
             "High diastolic pressure. Please consult a healthcare provider."),
            (120, 9999, "Crisis", "🆘", "#8E44AD",
             "Diastolic crisis! Seek emergency care immediately."),
        ]
    },
    "hemoglobin": {
        "label": "Hemoglobin",
        "unit": "g/dL",
        "ranges": [
            (0, 8, "Severe Anemia", "🆘", "#8E44AD",
             "Severely low hemoglobin. May need blood transfusion. Seek immediate care."),
            (8, 11, "Moderate Anemia", "🔴", "#E74C3C",
             "Low hemoglobin indicating anemia. Iron supplements and diet change needed."),
            (11, 13, "Mild Anemia", "⚠️", "#E67E22",
             "Mild anemia. Increase iron-rich foods (red meat, spinach, legumes) and Vitamin C."),
            (13, 17.5, "Normal", "✅", "#28B463",
             "Normal hemoglobin range. Maintain iron-rich diet."),
            (17.5, 9999, "High (Polycythemia)", "⚠️", "#E67E22",
             "Elevated hemoglobin. Can indicate dehydration or polycythemia. Consult a doctor."),
        ]
    },
}


def interpret_value(test_key: str, value: float) -> Dict:
    """Return interpretation for a lab value."""
    if test_key not in LAB_RANGES:
        return {"label": "Unknown", "status": "N/A", "icon": "❓", "color": "#7F8C8D", "advice": ""}

    test = LAB_RANGES[test_key]
    for low, high, status, icon, color, advice in test["ranges"]:
        if low <= value < high:
            return {
                "label": test["label"],
                "unit": test["unit"],
                "value": value,
                "status": status,
                "icon": icon,
                "color": color,
                "advice": advice
            }

    return {"label": test["label"], "status": "Out of range", "icon": "❓", "color": "#7F8C8D", "advice": ""}


class LabAnalyzer:
    """Analyzes lab report values."""

    def analyze(self, blood_sugar: float = None, cholesterol: float = None,
                systolic: float = None, diastolic: float = None,
                hemoglobin: float = None) -> Dict:
        """
        Analyze all provided lab values.

        Returns dict with results for each provided test.
        """
        results = {}
        if blood_sugar is not None:
            results["blood_sugar"] = interpret_value("blood_sugar", blood_sugar)
        if cholesterol is not None:
            results["cholesterol"] = interpret_value("cholesterol", cholesterol)
        if systolic is not None:
            results["systolic_bp"] = interpret_value("systolic_bp", systolic)
        if diastolic is not None:
            results["diastolic_bp"] = interpret_value("diastolic_bp", diastolic)
        if hemoglobin is not None:
            results["hemoglobin"] = interpret_value("hemoglobin", hemoglobin)
        return results
