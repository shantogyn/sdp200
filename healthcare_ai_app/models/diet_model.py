"""
Diet Recommendation Model
Generates personalized diet plans based on age, weight, and health condition.
"""

from typing import Dict, List, Tuple


DIET_PLANS = {
    "diabetes": {
        "label": "Diabetic-Friendly Diet",
        "notes": "Focus on low glycemic index foods. Avoid refined sugars.",
        "morning": [
            "Oatmeal with chia seeds and berries",
            "2 boiled eggs + whole wheat toast",
            "Greek yogurt with walnuts and cinnamon",
        ],
        "lunch": [
            "Grilled chicken breast + steamed vegetables + brown rice",
            "Lentil soup + salad with olive oil dressing",
            "Baked fish + quinoa + broccoli",
        ],
        "dinner": [
            "Stir-fried tofu with vegetables + small portion brown rice",
            "Grilled salmon + mixed greens + sweet potato",
            "Vegetable curry with lentils (no potatoes)",
        ],
        "snacks": [
            "Handful of almonds or walnuts",
            "Celery sticks with hummus",
            "Apple slices with peanut butter (1 tbsp)",
        ]
    },
    "hypertension": {
        "label": "DASH Diet (Heart-Healthy)",
        "notes": "Reduce sodium to <2300mg/day. Increase potassium and magnesium.",
        "morning": [
            "Banana + low-fat yogurt + whole grain cereal",
            "Oatmeal with flaxseeds + berries",
            "Whole wheat toast with avocado + poached egg",
        ],
        "lunch": [
            "Grilled skinless chicken + steamed spinach + brown rice",
            "Tuna salad (low sodium) + whole grain bread",
            "Kidney bean soup + mixed vegetable salad",
        ],
        "dinner": [
            "Baked salmon + roasted vegetables + quinoa",
            "Tofu vegetable stir-fry (no added salt) + brown rice",
            "Lean beef (small portion) + sweet potato + greens",
        ],
        "snacks": [
            "Unsalted sunflower seeds",
            "Fresh fruit (banana, orange, kiwi)",
            "Low-fat milk or fortified plant milk",
        ]
    },
    "obesity": {
        "label": "Weight Loss Diet",
        "notes": "Create a caloric deficit. High protein, high fiber, low simple carbs.",
        "morning": [
            "Vegetable omelette (2 eggs) with spinach and tomatoes",
            "Overnight oats with protein powder and berries",
            "Smoothie: spinach, banana, protein powder, almond milk",
        ],
        "lunch": [
            "Large salad: chicken breast, mixed greens, chickpeas, lemon dressing",
            "Lentil soup + whole grain bread (small portion)",
            "Grilled fish tacos with cabbage slaw (corn tortilla)",
        ],
        "dinner": [
            "Baked chicken breast + roasted vegetables (no starch)",
            "Zucchini noodles with tomato sauce and lean turkey",
            "Vegetable soup + small salad",
        ],
        "snacks": [
            "Apple + 10 almonds",
            "Carrot sticks with hummus (2 tbsp)",
            "Low-fat Greek yogurt (plain)",
        ]
    },
    "anemia": {
        "label": "Iron-Rich Diet",
        "notes": "Combine iron sources with vitamin C for better absorption. Limit tea/coffee near meals.",
        "morning": [
            "Fortified cereal + orange juice",
            "Spinach omelette + whole grain toast",
            "Lentil porridge with iron-rich seeds",
        ],
        "lunch": [
            "Red meat (lean) + leafy green salad + lemon dressing",
            "Beans and lentil curry + brown rice",
            "Tuna salad with spinach + tomato",
        ],
        "dinner": [
            "Chicken liver (small portion) + sweet potato + broccoli",
            "Lentil soup + whole wheat bread",
            "Tofu + stir-fried dark leafy greens + sesame seeds",
        ],
        "snacks": [
            "Pumpkin seeds",
            "Dried apricots",
            "Dark chocolate (70%+) in moderation",
        ]
    },
    "general": {
        "label": "Balanced Healthy Diet",
        "notes": "Eat a variety of whole foods. Stay hydrated. Limit processed foods.",
        "morning": [
            "Oatmeal with fruits and nuts",
            "Whole grain toast + eggs + fresh juice",
            "Smoothie bowl with granola and mixed fruits",
        ],
        "lunch": [
            "Grilled protein + whole grain + vegetables",
            "Mixed salad with legumes + olive oil dressing",
            "Whole grain wrap with lean protein and salad",
        ],
        "dinner": [
            "Baked fish or chicken + roasted vegetables",
            "Vegetarian curry with lentils + brown rice",
            "Stir-fried tofu with mixed vegetables",
        ],
        "snacks": [
            "Mixed nuts and dried fruits",
            "Fresh seasonal fruits",
            "Yogurt with honey",
        ]
    }
}


def calculate_bmi(weight_kg: float, height_cm: float) -> Tuple:
    """Calculate BMI and return (bmi, category)."""
    if height_cm <= 0 or weight_kg <= 0:
        return 0, "Unknown"
    height_m = height_cm / 100
    bmi = weight_kg / (height_m ** 2)
    if bmi < 18.5:
        category = "Underweight"
    elif bmi < 25:
        category = "Normal"
    elif bmi < 30:
        category = "Overweight"
    else:
        category = "Obese"
    return round(bmi, 1), category


def calculate_calories(age: int, weight_kg: float, gender: str = "male", activity: str = "moderate") -> int:
    """Estimate daily caloric needs using Mifflin-St Jeor (assumes average height)."""
    height_cm = 170  # default average
    if gender.lower() == "female":
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age - 161
    else:
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5

    multipliers = {
        "sedentary": 1.2,
        "light": 1.375,
        "moderate": 1.55,
        "active": 1.725,
        "very active": 1.9
    }
    return int(bmr * multipliers.get(activity, 1.55))


class DietRecommender:
    """Generates diet plans based on user profile and health conditions."""

    def get_plan(self, age: int, weight: float, disease: str) -> Dict:
        """
        Returns a diet plan dictionary.

        Args:
            age: User age in years
            weight: User weight in kg
            disease: Health condition string

        Returns:
            Dict with plan details
        """
        disease_lower = disease.lower()

        # Map input to plan key
        if any(k in disease_lower for k in ["diabetes", "sugar", "diabetic"]):
            plan_key = "diabetes"
        elif any(k in disease_lower for k in ["hypertension", "blood pressure", "bp", "heart"]):
            plan_key = "hypertension"
        elif any(k in disease_lower for k in ["obesity", "overweight", "weight loss", "fat"]):
            plan_key = "obesity"
        elif any(k in disease_lower for k in ["anemia", "iron", "hemoglobin"]):
            plan_key = "anemia"
        else:
            plan_key = "general"

        plan = DIET_PLANS[plan_key].copy()
        calories = calculate_calories(age, weight)
        plan["calories"] = calories
        plan["plan_key"] = plan_key
        return plan
