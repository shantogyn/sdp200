"""
Medical Chatbot Model
Rule-based chatbot with medical knowledge base.
"""

import random
import re
from typing import Tuple


RESPONSES = {
    # Greetings
    "greet": {
        "patterns": ["hello", "hi", "hey", "good morning", "good afternoon", "good evening", "howdy"],
        "replies": [
            "Hello! 👋 I'm MediBot, your AI health assistant. How can I help you today?",
            "Hi there! 😊 I'm here to answer your health questions. What's on your mind?",
            "Hey! Welcome to the Healthcare Assistant. Ask me anything about your health! 🏥",
        ]
    },
    # How are you
    "how_are_you": {
        "patterns": ["how are you", "how r u", "what's up", "how do you do"],
        "replies": [
            "I'm functioning perfectly and ready to help you with your health queries! 💪",
            "I'm great, thanks for asking! More importantly, how are YOU feeling? 😊",
        ]
    },
    # Fever
    "fever": {
        "patterns": ["fever", "high temperature", "temperature", "feeling hot", "body heat"],
        "replies": [
            "🌡️ **Fever Guidance:**\n\n• Normal temperature: 98.6°F (37°C)\n• Low-grade fever: 100.4-102°F\n• High fever: >103°F\n\n**When to see a doctor:**\n• Fever >103°F in adults\n• Lasts more than 3 days\n• Accompanied by stiff neck or rash\n\n**Home care:** Rest, stay hydrated, use acetaminophen or ibuprofen as directed.",
        ]
    },
    # Headache
    "headache": {
        "patterns": ["headache", "head pain", "head ache", "migraine", "head hurts"],
        "replies": [
            "🤕 **Headache Help:**\n\n**Common causes:**\n• Tension, dehydration, eye strain\n• Lack of sleep, stress\n• Sinusitis, migraine\n\n**Self-care tips:**\n• Drink water — dehydration is the #1 cause\n• Rest in a quiet, dark room\n• Apply a cold or warm compress\n• Over-the-counter pain relievers\n\n⚠️ See a doctor if: sudden severe headache, or with vision changes/fever.",
        ]
    },
    # Cold / flu
    "cold_flu": {
        "patterns": ["cold", "flu", "influenza", "runny nose", "sneezing", "cough", "sore throat"],
        "replies": [
            "🤧 **Cold & Flu Tips:**\n\n• Get plenty of rest\n• Stay well hydrated (water, herbal teas, broths)\n• Honey and ginger are natural soothers\n• Saline nasal rinse for congestion\n• Steam inhalation for relief\n\n💊 OTC options: decongestants, antihistamines, pain relievers\n\n⚠️ See a doctor if symptoms worsen after 10 days or breathing difficulty develops.",
        ]
    },
    # Stomach
    "stomach": {
        "patterns": ["stomach", "stomach ache", "abdominal pain", "belly ache", "nausea", "vomiting", "diarrhea", "indigestion", "bloating"],
        "replies": [
            "🫃 **Stomach Discomfort Guide:**\n\n**For nausea/vomiting:**\n• Ginger tea or ginger ale\n• BRAT diet (Bananas, Rice, Applesauce, Toast)\n• Small sips of clear fluids\n\n**For diarrhea:**\n• Stay hydrated with oral rehydration solution\n• Avoid dairy, fatty, spicy foods\n• Probiotics can help\n\n⚠️ Seek care if: blood in stool, severe pain, or symptoms >48 hours.",
        ]
    },
    # Diabetes
    "diabetes": {
        "patterns": ["diabetes", "blood sugar", "sugar level", "insulin", "diabetic"],
        "replies": [
            "🩺 **Diabetes Information:**\n\n**Type 1:** Autoimmune; body doesn't produce insulin\n**Type 2:** Body doesn't use insulin effectively\n\n**Warning signs:**\n• Frequent urination, excessive thirst\n• Unexplained weight loss\n• Blurred vision, slow healing wounds\n\n**Management:**\n• Monitor blood glucose regularly\n• Balanced diet (low GI foods)\n• Regular physical activity\n• Take prescribed medications\n\n✅ Regular check-ups with your doctor are essential!",
        ]
    },
    # Blood pressure
    "blood_pressure": {
        "patterns": ["blood pressure", "hypertension", "bp", "high bp", "low bp", "hypotension"],
        "replies": [
            "💓 **Blood Pressure Guide:**\n\n**Normal:** 120/80 mmHg\n**Elevated:** 120-129/<80\n**High (Stage 1):** 130-139/80-89\n**High (Stage 2):** ≥140/≥90\n**Crisis:** >180/>120 — seek emergency care!\n\n**Lifestyle tips to manage BP:**\n• Reduce sodium intake\n• Exercise 30 min/day\n• Limit alcohol and caffeine\n• Manage stress (meditation, yoga)\n• Maintain healthy weight",
        ]
    },
    # Sleep
    "sleep": {
        "patterns": ["sleep", "insomnia", "can't sleep", "sleepless", "tired", "fatigue", "exhausted"],
        "replies": [
            "😴 **Sleep Health Tips:**\n\n**Good sleep hygiene:**\n• Maintain consistent sleep/wake times\n• Avoid screens 1 hour before bed\n• Keep bedroom cool and dark\n• Avoid caffeine after 2 PM\n• Try relaxation techniques\n\n**Adults need 7-9 hours per night**\n\n💡 Natural aids: melatonin, chamomile tea, lavender aromatherapy\n\nIf insomnia persists >3 weeks, consult a doctor.",
        ]
    },
    # Exercise
    "exercise": {
        "patterns": ["exercise", "workout", "fitness", "physical activity", "gym"],
        "replies": [
            "🏃 **Exercise Recommendations (WHO):**\n\n• **Adults:** 150-300 min moderate activity/week\n• **OR** 75-150 min vigorous activity/week\n• **Plus** muscle strengthening 2×/week\n\n**Benefits:**\n✅ Reduces risk of heart disease, diabetes\n✅ Improves mental health\n✅ Strengthens bones and muscles\n✅ Better sleep quality\n\n💡 Start slow and gradually increase intensity!",
        ]
    },
    # Nutrition
    "nutrition": {
        "patterns": ["diet", "nutrition", "eat", "food", "healthy eating", "vitamins", "minerals"],
        "replies": [
            "🥗 **Nutrition Basics:**\n\n**Balanced plate:**\n• ½ plate: vegetables and fruits\n• ¼ plate: whole grains\n• ¼ plate: lean protein\n• Small amount: healthy fats\n\n**Key nutrients:**\n• Protein: meat, legumes, eggs, dairy\n• Fiber: whole grains, veggies, fruits\n• Omega-3: fatty fish, walnuts, flaxseed\n• Calcium: dairy, leafy greens\n\n💧 Drink 8-10 glasses of water daily!",
        ]
    },
    # Mental health
    "mental_health": {
        "patterns": ["stress", "anxiety", "depression", "mental health", "sad", "worried", "nervous", "panic"],
        "replies": [
            "🧠 **Mental Health Support:**\n\nIt's okay to not be okay. Here are some strategies:\n\n**For stress & anxiety:**\n• Deep breathing (4-7-8 technique)\n• Progressive muscle relaxation\n• Mindfulness meditation\n• Physical exercise\n\n**For low mood:**\n• Connect with loved ones\n• Get outside in sunlight\n• Engage in activities you enjoy\n• Limit social media\n\n💬 If you're struggling, please reach out to a mental health professional. You don't have to go through it alone! 💙",
        ]
    },
    # Emergency
    "emergency": {
        "patterns": ["emergency", "chest pain", "heart attack", "stroke", "can't breathe", "unconscious", "collapse"],
        "replies": [
            "🚨 **EMERGENCY ALERT!**\n\nIf this is a medical emergency, please:\n\n📞 **Call 911 / Emergency Services IMMEDIATELY**\n\n**Signs of Heart Attack:**\n• Chest pain or pressure\n• Pain in arm, jaw, or back\n• Shortness of breath, sweating\n\n**Signs of Stroke (FAST):**\n• **F**ace drooping\n• **A**rm weakness\n• **S**peech difficulty\n• **T**ime to call 911!\n\n⏱️ Every second counts — call for help now!",
        ]
    },
    # Default
    "default": {
        "replies": [
            "I'm not sure about that. Could you ask a health-related question? For example:\n• 'What are symptoms of diabetes?'\n• 'How to manage high blood pressure?'\n• 'Tips for better sleep?'",
            "That's outside my knowledge base right now. Try asking about symptoms, diseases, diet, or lifestyle tips! 🏥",
            "I specialize in health topics. Ask me about symptoms, nutrition, medications, or wellness tips! 😊",
        ]
    }
}


class MedicalChatbot:
    """Rule-based medical chatbot with pattern matching."""

    def __init__(self):
        self._compile_patterns()

    def _compile_patterns(self):
        """Pre-compile pattern → category mapping."""
        self.pattern_map = {}
        for category, data in RESPONSES.items():
            if category == "default":
                continue
            for pattern in data.get("patterns", []):
                self.pattern_map[pattern] = category

    def get_response(self, user_message: str) -> str:
        """Return a bot response for the given user message."""
        text = user_message.lower().strip()

        # Match patterns
        for pattern, category in self.pattern_map.items():
            if pattern in text:
                return random.choice(RESPONSES[category]["replies"])

        # Fallback
        return random.choice(RESPONSES["default"]["replies"])
