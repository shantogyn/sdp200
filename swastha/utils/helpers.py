"""
Helper Functions Module
Utility functions for common operations
"""

import hashlib
import os
from typing import Dict, Any
from datetime import datetime

class PasswordHelper:
    """Class for password hashing and verification"""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hash password using SHA256
        Args:
            password: Plain text password
        Returns:
            Hashed password
        """
        salt = os.urandom(32)
        pwd_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
        return salt.hex() + pwd_hash.hex()
    
    @staticmethod
    def verify_password(stored_password: str, provided_password: str) -> bool:
        """
        Verify password against hash
        Args:
            stored_password: Hashed password from database
            provided_password: Plain text password to verify
        Returns:
            True if password matches, False otherwise
        """
        try:
            salt = bytes.fromhex(stored_password[:64])
            stored_hash = stored_password[64:]
            pwd_hash = hashlib.pbkdf2_hmac('sha256', provided_password.encode('utf-8'), salt, 100000)
            return pwd_hash.hex() == stored_hash
        except:
            return False

class DateHelper:
    """Class for date and time operations"""
    
    @staticmethod
    def get_current_time() -> str:
        """Get current time in HH:MM format"""
        return datetime.now().strftime("%H:%M")
    
    @staticmethod
    def get_current_date() -> str:
        """Get current date in YYYY-MM-DD format"""
        return datetime.now().strftime("%Y-%m-%d")
    
    @staticmethod
    def get_current_datetime() -> str:
        """Get current datetime in readable format"""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

class TextHelper:
    """Class for text operations"""
    
    @staticmethod
    def truncate_text(text: str, length: int) -> str:
        """
        Truncate text to specified length
        Args:
            text: Text to truncate
            length: Maximum length
        Returns:
            Truncated text with ellipsis
        """
        if len(text) > length:
            return text[:length-3] + "..."
        return text
    
    @staticmethod
    def capitalize_words(text: str) -> str:
        """Capitalize first letter of each word"""
        return ' '.join(word.capitalize() for word in text.split())
    
    @staticmethod
    def format_phone(phone: str) -> str:
        """Format phone number"""
        # Remove non-digits
        digits = ''.join(filter(str.isdigit, phone))
        if len(digits) == 10:
            return f"{digits[:3]}-{digits[3:6]}-{digits[6:]}"
        return phone

class BMICalculator:
    """Class for BMI calculations"""
    
    @staticmethod
    def calculate_bmi(weight: float, height: float) -> float:
        """
        Calculate BMI (Body Mass Index)
        Args:
            weight: Weight in kg
            height: Height in cm
        Returns:
            BMI value
        """
        height_m = height / 100
        bmi = weight / (height_m ** 2)
        return round(bmi, 2)
    
    @staticmethod
    def get_bmi_category(bmi: float) -> str:
        """
        Get BMI category
        Args:
            bmi: BMI value
        Returns:
            Category string
        """
        if bmi < 18.5:
            return "Underweight"
        elif bmi < 25:
            return "Normal weight"
        elif bmi < 30:
            return "Overweight"
        else:
            return "Obese"

class SymptomAnalyzer:
    """Class for symptom analysis"""
    
    # Disease symptom mapping
    DISEASE_SYMPTOMS = {
        "Common Cold": ["cough", "sneezing", "runny nose", "sore throat", "headache"],
        "Flu": ["fever", "cough", "body ache", "fatigue", "sore throat"],
        "Migraine": ["headache", "nausea", "sensitivity to light", "vision changes"],
        "Asthma": ["cough", "wheezing", "shortness of breath", "chest tightness"],
        "Diabetes": ["thirst", "frequent urination", "fatigue", "blurred vision"],
        "Hypertension": ["headache", "dizziness", "chest pain", "fatigue"],
        "Allergies": ["sneezing", "itchy eyes", "runny nose", "skin rash"],
        "Bronchitis": ["cough", "chest discomfort", "fatigue", "shortness of breath"],
        "Gastritis": ["stomach pain", "nausea", "loss of appetite", "acidity"],
        "Anxiety": ["stress", "panic", "restlessness", "rapid heartbeat"]
    }
    
    @staticmethod
    def predict_disease(symptoms: list) -> Dict[str, Any]:
        """
        Predict disease based on symptoms
        Args:
            symptoms: List of symptom strings
        Returns:
            Dictionary with top matches and confidence
        """
        symptoms_lower = [s.lower().strip() for s in symptoms]
        matches = {}
        
        for disease, disease_symptoms in SymptomAnalyzer.DISEASE_SYMPTOMS.items():
            match_count = sum(1 for symptom in disease_symptoms if any(sym in symptom for sym in symptoms_lower))
            if match_count > 0:
                confidence = (match_count / len(disease_symptoms)) * 100
                matches[disease] = round(confidence, 2)
        
        if not matches:
            return {"disease": "Unknown", "confidence": 0, "advice": "Please consult a doctor"}
        
        top_disease = max(matches, key=matches.get)
        confidence = matches[top_disease]
        
        return {
            "disease": top_disease,
            "confidence": confidence,
            "advice": f"You may have {top_disease}. Please consult a healthcare professional for accurate diagnosis."
        }
