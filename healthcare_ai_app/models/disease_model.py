"""
Disease Prediction Model
Uses rule-based logic with probability scores.
Can be swapped for a trained sklearn model.
"""

from typing import List, Dict, Tuple


# ── Symptom → Disease knowledge base ──────────────────────────────────────────
DISEASE_KB = {
    "Common Cold": {
        "symptoms": ["runny nose", "sneezing", "sore throat", "cough", "mild fever", "congestion", "headache"],
        "description": "A viral infection of the upper respiratory tract.",
        "prevention": "Wash hands frequently, avoid close contact with sick individuals.",
        "treatment": "Rest, fluids, over-the-counter decongestants."
    },
    "Influenza (Flu)": {
        "symptoms": ["high fever", "body ache", "fatigue", "cough", "sore throat", "headache", "chills", "muscle pain"],
        "description": "A contagious respiratory illness caused by influenza viruses.",
        "prevention": "Annual flu vaccine, good hygiene practices.",
        "treatment": "Antiviral medications, rest, hydration."
    },
    "COVID-19": {
        "symptoms": ["fever", "dry cough", "fatigue", "loss of taste", "loss of smell", "shortness of breath", "body ache", "sore throat"],
        "description": "A respiratory illness caused by the SARS-CoV-2 virus.",
        "prevention": "Vaccination, masking, social distancing, hand hygiene.",
        "treatment": "Rest, fluids; antivirals for severe cases."
    },
    "Diabetes (Type 2)": {
        "symptoms": ["frequent urination", "excessive thirst", "fatigue", "blurred vision", "slow healing", "weight loss", "numbness in feet"],
        "description": "A chronic condition affecting how the body processes blood sugar.",
        "prevention": "Healthy diet, regular exercise, maintain healthy weight.",
        "treatment": "Lifestyle changes, oral medications, insulin therapy."
    },
    "Hypertension": {
        "symptoms": ["headache", "dizziness", "blurred vision", "chest pain", "shortness of breath", "nosebleed", "fatigue"],
        "description": "High blood pressure that can lead to serious cardiovascular complications.",
        "prevention": "Low-sodium diet, exercise, reduce stress, limit alcohol.",
        "treatment": "Antihypertensive medications, lifestyle modifications."
    },
    "Malaria": {
        "symptoms": ["high fever", "chills", "sweating", "headache", "nausea", "vomiting", "muscle pain", "fatigue"],
        "description": "A mosquito-borne infectious disease caused by Plasmodium parasites.",
        "prevention": "Mosquito nets, repellents, antimalarial prophylaxis.",
        "treatment": "Antimalarial medications (chloroquine, artemisinin)."
    },
    "Dengue Fever": {
        "symptoms": ["high fever", "severe headache", "joint pain", "muscle pain", "rash", "nausea", "bleeding gums", "eye pain"],
        "description": "A mosquito-borne viral infection prevalent in tropical regions.",
        "prevention": "Mosquito control, protective clothing, repellents.",
        "treatment": "Supportive care, hydration, pain relievers (avoid aspirin)."
    },
    "Typhoid": {
        "symptoms": ["prolonged fever", "headache", "abdominal pain", "constipation", "diarrhea", "weakness", "loss of appetite", "rose spots"],
        "description": "A bacterial infection caused by Salmonella typhi.",
        "prevention": "Typhoid vaccine, safe water, good food hygiene.",
        "treatment": "Antibiotics (ciprofloxacin, azithromycin)."
    },
    "Asthma": {
        "symptoms": ["shortness of breath", "wheezing", "chest tightness", "cough", "breathing difficulty", "nighttime cough"],
        "description": "A chronic condition causing inflammation and narrowing of airways.",
        "prevention": "Avoid triggers, use prescribed preventive inhalers.",
        "treatment": "Bronchodilators, corticosteroids, allergy management."
    },
    "Gastroenteritis": {
        "symptoms": ["nausea", "vomiting", "diarrhea", "stomach cramps", "fever", "dehydration", "loss of appetite"],
        "description": "Inflammation of the stomach and intestines, usually from infection.",
        "prevention": "Hand hygiene, safe food practices, clean water.",
        "treatment": "Oral rehydration, rest, bland diet."
    },
    "Migraine": {
        "symptoms": ["severe headache", "nausea", "vomiting", "sensitivity to light", "sensitivity to sound", "blurred vision", "dizziness"],
        "description": "A neurological condition characterized by intense, debilitating headaches.",
        "prevention": "Identify and avoid triggers, stress management.",
        "treatment": "Triptans, pain relievers, preventive medications."
    },
    "Pneumonia": {
        "symptoms": ["cough", "chest pain", "fever", "shortness of breath", "chills", "fatigue", "confusion", "nausea"],
        "description": "Infection that inflames the air sacs in one or both lungs.",
        "prevention": "Pneumococcal vaccine, good hygiene, healthy immune system.",
        "treatment": "Antibiotics, antivirals, rest, oxygen therapy."
    },
    "Anemia": {
        "symptoms": ["fatigue", "weakness", "pale skin", "shortness of breath", "dizziness", "cold hands", "headache", "irregular heartbeat"],
        "description": "A condition where there aren't enough healthy red blood cells.",
        "prevention": "Iron-rich diet, folic acid, vitamin B12 supplementation.",
        "treatment": "Iron supplements, dietary changes, treating underlying cause."
    },
    "Appendicitis": {
        "symptoms": ["severe abdominal pain", "nausea", "vomiting", "fever", "loss of appetite", "abdominal bloating"],
        "description": "Inflammation of the appendix requiring immediate medical attention.",
        "prevention": "No known prevention; high-fiber diet may reduce risk.",
        "treatment": "Surgical removal of appendix (appendectomy)."
    },
    "UTI (Urinary Tract Infection)": {
        "symptoms": ["burning urination", "frequent urination", "cloudy urine", "pelvic pain", "strong urine odor", "blood in urine"],
        "description": "Infection in any part of the urinary system.",
        "prevention": "Stay hydrated, proper hygiene, urinate after intercourse.",
        "treatment": "Antibiotics, increased fluid intake."
    },
}

ALL_SYMPTOMS = sorted(set(
    symptom
    for disease_data in DISEASE_KB.values()
    for symptom in disease_data["symptoms"]
))


class DiseasePredictor:
    """Predicts likely diseases from a list of symptoms."""

    def predict(self, user_symptoms: List[str]) -> List[Tuple[str, float, Dict]]:
        """
        Returns top matching diseases sorted by probability.

        Args:
            user_symptoms: List of symptom strings (lowercase)

        Returns:
            List of (disease_name, probability_pct, disease_data) tuples
        """
        if not user_symptoms:
            return []

        user_set = set(s.lower().strip() for s in user_symptoms)
        scores = []

        for disease, data in DISEASE_KB.items():
            disease_symptoms = set(data["symptoms"])
            matched = user_set & disease_symptoms
            if not matched:
                continue

            # Jaccard-like scoring: matched / union
            union = user_set | disease_symptoms
            score = len(matched) / len(union)

            # Boost if many symptoms matched
            coverage = len(matched) / len(disease_symptoms)
            final_score = (score * 0.5) + (coverage * 0.5)

            scores.append((disease, round(final_score * 100, 1), data))

        # Sort descending by score, return top 5
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:5]

    def get_all_symptoms(self) -> List[str]:
        return ALL_SYMPTOMS
