"""
Disease Information Center Page
"""

import tkinter as tk
from tkinter import ttk
import sys, os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.helpers import COLORS, FONTS, styled_button, scrollable_frame

DISEASE_INFO_DB = {
    "Diabetes": {
        "icon": "🩺", "color": "#E67E22",
        "full_name": "Diabetes Mellitus",
        "overview": "Diabetes is a chronic metabolic disease characterized by elevated blood glucose (blood sugar) levels. It occurs when the body cannot produce enough insulin (Type 1) or cannot effectively use the insulin it produces (Type 2).",
        "symptoms": ["Frequent urination (polyuria)", "Excessive thirst (polydipsia)", "Unexplained weight loss", "Extreme hunger", "Blurred vision", "Slow-healing sores", "Fatigue and weakness", "Numbness or tingling in hands/feet"],
        "causes": ["Autoimmune destruction of insulin-producing cells (Type 1)", "Insulin resistance due to obesity or inactivity (Type 2)", "Genetic predisposition", "Gestational hormones (Gestational Diabetes)", "Unhealthy diet high in refined carbohydrates", "Physical inactivity"],
        "prevention": ["Maintain healthy body weight", "Exercise regularly (150+ min/week)", "Eat a balanced, low-glycemic diet", "Limit sugar and processed foods", "Regular blood sugar screenings", "Avoid smoking and excessive alcohol"],
        "treatment": ["Lifestyle changes: diet and exercise", "Blood glucose monitoring", "Oral medications (e.g., Metformin)", "Insulin therapy (Type 1 & advanced Type 2)", "Regular HbA1c tests", "Management of complications"],
        "stats": {"Prevalence": "422 million people worldwide", "Type 2 share": "~90-95% of all cases", "Deaths/year": "~1.5 million directly"},
    },
    "Hypertension": {
        "icon": "💓", "color": "#E74C3C",
        "full_name": "High Blood Pressure",
        "overview": "Hypertension (high blood pressure) is a condition in which the force of blood against artery walls is consistently too high (≥130/80 mmHg). It is often called the 'silent killer' because it usually has no symptoms.",
        "symptoms": ["Often no symptoms (asymptomatic)", "Headaches (especially in the morning)", "Dizziness or lightheadedness", "Nosebleeds", "Shortness of breath", "Blurred vision", "Chest pain (in severe cases)"],
        "causes": ["High sodium diet", "Physical inactivity", "Obesity/overweight", "Excessive alcohol intake", "Stress and anxiety", "Genetic/family history", "Kidney disease", "Thyroid disorders"],
        "prevention": ["Follow DASH diet (low sodium)", "Regular aerobic exercise", "Achieve and maintain healthy weight", "Limit alcohol to 1-2 drinks/day", "Quit smoking", "Manage stress through meditation/yoga", "Regular blood pressure monitoring"],
        "treatment": ["Lifestyle changes (first line)", "ACE inhibitors", "Calcium channel blockers", "Beta-blockers", "Diuretics", "ARBs (Angiotensin receptor blockers)"],
        "stats": {"Prevalence": "1.28 billion adults worldwide", "Awareness": "Only 46% know they have it", "Target BP": "< 120/80 mmHg"},
    },
    "COVID-19": {
        "icon": "🦠", "color": "#8E44AD",
        "full_name": "Coronavirus Disease 2019",
        "overview": "COVID-19 is an infectious disease caused by the SARS-CoV-2 coronavirus. It was declared a pandemic in March 2020 and primarily affects the respiratory system, though it can impact multiple organ systems.",
        "symptoms": ["Fever or chills", "Dry cough", "Fatigue", "Loss of taste or smell", "Sore throat", "Shortness of breath", "Muscle or body aches", "Headache", "Diarrhea", "Runny nose"],
        "causes": ["SARS-CoV-2 virus spread through respiratory droplets", "Close contact with infected individuals", "Touching contaminated surfaces then touching face", "Airborne transmission in enclosed spaces"],
        "prevention": ["Vaccination (strongly recommended)", "Wear masks in crowded indoor settings", "Maintain physical distance", "Wash hands for 20+ seconds", "Improve indoor ventilation", "Isolate if symptomatic"],
        "treatment": ["Most cases: rest, fluids, symptom management", "Antiviral medications (Paxlovid) for high-risk", "Oxygen therapy for moderate-severe cases", "Hospitalization for severe cases", "Steroids (dexamethasone) for severe inflammation"],
        "stats": {"Global cases": "700+ million", "Deaths": "7+ million globally", "Vaccines available": "20+ approved worldwide"},
    },
    "Tuberculosis": {
        "icon": "🫁", "color": "#27AE60",
        "full_name": "Tuberculosis (TB)",
        "overview": "Tuberculosis is a serious infectious disease caused by Mycobacterium tuberculosis bacteria. It primarily affects the lungs but can spread to other organs. TB is preventable and curable with proper treatment.",
        "symptoms": ["Persistent cough lasting 3+ weeks", "Blood in sputum", "Chest pain", "Fever (especially evening/night)", "Night sweats", "Unexplained weight loss", "Fatigue and weakness", "Loss of appetite"],
        "causes": ["Mycobacterium tuberculosis bacteria", "Airborne transmission from coughs/sneezes", "Weakened immune system (HIV, malnutrition)", "Crowded or poorly ventilated spaces", "Close prolonged contact with active TB patient"],
        "prevention": ["BCG vaccination (children)", "Early detection and treatment", "Improve ventilation in living/working spaces", "TB screening for high-risk groups", "Proper nutrition to maintain immunity", "HIV prevention (co-infection risk)"],
        "treatment": ["Standard 6-month antibiotic regimen (DOTS)", "First-line drugs: Isoniazid, Rifampicin, Ethambutol, Pyrazinamide", "Directly Observed Treatment (DOT)", "Drug-resistant TB needs 18-24 month treatment", "Complete full course — stopping early causes resistance"],
        "stats": {"New cases/year": "10 million worldwide", "Deaths/year": "~1.3 million", "Curable": "Yes, with full treatment"},
    },
    "Malaria": {
        "icon": "🦟", "color": "#2ECC71",
        "full_name": "Malaria",
        "overview": "Malaria is a life-threatening disease caused by Plasmodium parasites transmitted through the bites of infected female Anopheles mosquitoes. It is a major public health problem in tropical and subtropical regions.",
        "symptoms": ["High fever with chills", "Sweating", "Severe headache", "Nausea and vomiting", "Muscle and joint pain", "Fatigue", "Rapid breathing", "Anemia", "Enlarged spleen (chronic cases)"],
        "causes": ["Plasmodium falciparum (most dangerous)", "Plasmodium vivax", "Plasmodium malariae", "Plasmodium ovale", "Transmitted by infected Anopheles mosquito bite"],
        "prevention": ["Use insecticide-treated bed nets (ITNs)", "Indoor residual spraying (IRS)", "Antimalarial prophylaxis when traveling", "Protective clothing (long sleeves/pants)", "Mosquito repellents (DEET)", "Eliminate standing water breeding sites"],
        "treatment": ["Artemisinin-based Combination Therapies (ACTs)", "Chloroquine (for non-resistant strains)", "Primaquine (for P. vivax relapses)", "Severe malaria: IV artesunate", "Seek treatment within 24h of symptoms"],
        "stats": {"Cases/year": "247 million (2021)", "Deaths/year": "~619,000", "Most affected": "Sub-Saharan Africa (95%)"},
    },
    "Dengue": {
        "icon": "🦟", "color": "#F39C12",
        "full_name": "Dengue Fever",
        "overview": "Dengue fever is a mosquito-borne viral infection caused by the dengue virus (DENV). It is transmitted by Aedes mosquitoes, primarily Aedes aegypti. Dengue is prevalent in tropical and subtropical regions.",
        "symptoms": ["Sudden high fever (40°C/104°F)", "Severe headache", "Pain behind the eyes", "Muscle and joint pain ('breakbone fever')", "Nausea and vomiting", "Rash (appears 3-4 days after fever)", "Mild bleeding (nose/gums)", "Fatigue"],
        "causes": ["Dengue virus (4 serotypes: DENV 1-4)", "Bite of infected Aedes aegypti mosquito", "Peak transmission: dawn and dusk", "Standing water breeding grounds"],
        "prevention": ["Eliminate standing water in containers, tyres, pots", "Use mosquito repellents (DEET)", "Wear full-sleeve clothing", "Use bed nets and window screens", "Dengvaxia vaccine (for previously infected)"],
        "treatment": ["No specific antiviral treatment", "Supportive care: rest and fluids", "Pain relievers: paracetamol (NOT aspirin/ibuprofen)", "Monitor platelet count and hematocrit", "Hospitalization for severe dengue", "IV fluids if severe dehydration"],
        "stats": {"Cases/year": "400 million infections", "Severe cases": "~96 million symptomatic", "At risk population": "3.9 billion people"},
    },
    "Asthma": {
        "icon": "💨", "color": "#3498DB",
        "full_name": "Bronchial Asthma",
        "overview": "Asthma is a chronic inflammatory disease of the airways that causes recurring episodes of wheezing, breathlessness, chest tightness, and coughing. The airways narrow and swell, producing extra mucus.",
        "symptoms": ["Shortness of breath", "Wheezing (high-pitched whistling)", "Chest tightness or pain", "Coughing (especially at night)", "Difficulty breathing during exercise", "Worsening symptoms with cold air or infections"],
        "causes": ["Airway inflammation and hypersensitivity", "Allergens: dust mites, pollen, pet dander, mold", "Air pollution and smoke", "Respiratory infections (cold/flu)", "Exercise (exercise-induced asthma)", "Strong emotions/stress", "Genetic predisposition"],
        "prevention": ["Identify and avoid personal triggers", "Use prescribed preventive (controller) inhalers", "Keep home dust-free and well-ventilated", "Avoid cigarette smoke", "Manage allergies proactively", "Get influenza vaccine annually"],
        "treatment": ["Short-acting bronchodilators (reliever inhalers)", "Inhaled corticosteroids (controller inhalers)", "Long-acting beta-agonists (LABAs)", "Leukotriene modifiers", "Biologics (for severe asthma)", "Develop an Asthma Action Plan with your doctor"],
        "stats": {"Prevalence": "235-300 million worldwide", "Deaths/year": "~455,000", "Controllable": "Yes, with proper treatment"},
    },
    "Cancer": {
        "icon": "🎗️", "color": "#C0392B",
        "full_name": "Cancer (Overview)",
        "overview": "Cancer is a disease caused by uncontrolled division of abnormal cells. There are over 100 types. It can affect virtually any organ. Early detection significantly improves outcomes.",
        "symptoms": ["Unexplained weight loss", "Fatigue that doesn't improve", "Persistent pain", "Skin changes (new moles, sores)", "Change in bowel/bladder habits", "Unusual bleeding or discharge", "A lump or thickening under skin", "Difficulty swallowing"],
        "causes": ["Genetic mutations (inherited or acquired)", "Tobacco smoking", "Ultraviolet radiation (skin cancer)", "Certain viral infections (HPV, Hepatitis B/C)", "Carcinogen exposure", "Obesity and poor diet", "Alcohol consumption", "Age (risk increases with age)"],
        "prevention": ["Don't smoke; avoid secondhand smoke", "Maintain healthy weight", "Regular physical activity", "Healthy diet (fruits, vegetables, whole grains)", "Sun protection (SPF, shade, clothing)", "HPV and Hepatitis B vaccination", "Regular cancer screenings (mammogram, colonoscopy, etc.)"],
        "treatment": ["Surgery (remove tumor)", "Chemotherapy", "Radiation therapy", "Immunotherapy", "Targeted therapy", "Hormone therapy", "Bone marrow/stem cell transplant", "Palliative care"],
        "stats": {"New cases/year": "~20 million worldwide", "Deaths/year": "~10 million", "Survival improving": "Due to early detection & new treatments"},
    },
}


class InfoPage:
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
        self._build()

    def _build(self):
        hdr = tk.Frame(self.parent, bg="#795548", height=60)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
        tk.Label(hdr, text="📚 Disease Information Center",
                 font=FONTS["title"], bg="#795548", fg="white"
                 ).place(relx=0.02, rely=0.5, anchor="w")

        main = tk.Frame(self.parent, bg=COLORS["bg"])
        main.pack(fill="both", expand=True)

        # Left: disease list
        left = tk.Frame(main, bg=COLORS["bg"], width=230)
        left.pack(side="left", fill="y")
        left.pack_propagate(False)
        self._build_list(left)

        # Right: disease details
        right = tk.Frame(main, bg=COLORS["bg"])
        right.pack(side="right", fill="both", expand=True)
        self.detail_frame = right
        self._show_placeholder()

    def _build_list(self, parent):
        # Search
        search_frame = tk.Frame(parent, bg=COLORS["sidebar"])
        search_frame.pack(fill="x")
        si = tk.Frame(search_frame, bg=COLORS["sidebar"])
        si.pack(padx=10, pady=10, fill="x")

        tk.Label(si, text="🔍 Search Disease",
                 font=FONTS["small"], bg=COLORS["sidebar"], fg="white").pack(anchor="w")
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self._filter_list)
        tk.Entry(si, textvariable=self.search_var, font=FONTS["body"],
                 relief="flat", bg="#2C3E50", fg="white",
                 insertbackground="white").pack(fill="x", ipady=5, pady=4)

        # Disease buttons container
        self.list_container = tk.Frame(parent, bg=COLORS["sidebar"])
        self.list_container.pack(fill="both", expand=True)
        self._render_list(list(DISEASE_INFO_DB.keys()))

    def _render_list(self, diseases):
        for w in self.list_container.winfo_children():
            w.destroy()

        for name in diseases:
            data = DISEASE_INFO_DB[name]
            btn = tk.Button(
                self.list_container,
                text=f"{data['icon']}  {name}",
                font=("Segoe UI", 10),
                bg=COLORS["sidebar"],
                fg="#BDC3C7",
                relief="flat",
                cursor="hand2",
                anchor="w",
                padx=14, pady=8,
                command=lambda n=name: self._show_disease(n)
            )
            btn.pack(fill="x")

            def on_enter(e, b=btn):
                b.config(bg=COLORS["sidebar_lt"], fg="white")
            def on_leave(e, b=btn):
                b.config(bg=COLORS["sidebar"], fg="#BDC3C7")
            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)

    def _filter_list(self, *args):
        q = self.search_var.get().lower()
        filtered = [n for n in DISEASE_INFO_DB if q in n.lower()] if q else list(DISEASE_INFO_DB.keys())
        self._render_list(filtered)

    def _show_placeholder(self):
        tk.Label(
            self.detail_frame,
            text="📖 Select a disease from the left\nto view detailed information",
            font=FONTS["heading"], bg=COLORS["bg"], fg=COLORS["text_lt"],
            justify="center"
        ).place(relx=0.5, rely=0.4, anchor="center")

    def _show_disease(self, name):
        for w in self.detail_frame.winfo_children():
            w.destroy()

        data = DISEASE_INFO_DB[name]
        color = data["color"]

        # Header
        hdr = tk.Frame(self.detail_frame, bg=color)
        hdr.pack(fill="x")
        hi = tk.Frame(hdr, bg=color)
        hi.pack(padx=16, pady=14, fill="x")
        tk.Label(hi, text=f"{data['icon']}  {name}",
                 font=("Segoe UI", 18, "bold"), bg=color, fg="white").pack(anchor="w")
        tk.Label(hi, text=data["full_name"],
                 font=FONTS["body"], bg=color, fg="white").pack(anchor="w")

        # Stats badges
        if data.get("stats"):
            stats_row = tk.Frame(hi, bg=color)
            stats_row.pack(anchor="w", pady=(6, 0))
            for key, val in data["stats"].items():
                badge = tk.Frame(stats_row, bg="white")
                badge.pack(side="left", padx=(0, 6))
                bi = tk.Frame(badge, bg="white")
                bi.pack(padx=8, pady=4)
                tk.Label(bi, text=key, font=("Segoe UI", 7), bg="white", fg=COLORS["text_lt"]).pack()
                tk.Label(bi, text=val, font=("Segoe UI", 8, "bold"), bg="white", fg=color).pack()

        # Scrollable content
        outer, scroll = scrollable_frame(self.detail_frame)
        outer.pack(fill="both", expand=True)

        # Overview
        self._section(scroll, "📋 Overview", data["overview"], color, is_text=True)

        # Structured sections
        sections = [
            ("🤒 Common Symptoms", "symptoms"),
            ("🔬 Causes & Risk Factors", "causes"),
            ("🛡️ Prevention", "prevention"),
            ("💊 Treatment", "treatment"),
        ]
        for label, key in sections:
            if data.get(key):
                self._section(scroll, label, data[key], color, is_text=False)

    def _section(self, parent, title, content, color, is_text=False):
        card = tk.Frame(parent, bg="white")
        card.pack(fill="x", padx=12, pady=4)
        inner = tk.Frame(card, bg="white")
        inner.pack(padx=14, pady=12, fill="x")

        title_row = tk.Frame(inner, bg="white")
        title_row.pack(fill="x")
        tk.Frame(title_row, bg=color, width=4, height=20).pack(side="left", padx=(0, 8))
        tk.Label(title_row, text=title, font=FONTS["subhead"],
                 bg="white", fg=color).pack(side="left")

        if is_text:
            tk.Label(inner, text=content, font=FONTS["body"],
                     bg="white", fg=COLORS["text"],
                     wraplength=600, justify="left").pack(anchor="w", pady=(6, 0))
        else:
            for item in content:
                row = tk.Frame(inner, bg="white")
                row.pack(fill="x", pady=1)
                tk.Label(row, text="•", font=FONTS["body"],
                         bg="white", fg=color, width=2).pack(side="left", anchor="n")
                tk.Label(row, text=item, font=FONTS["body"],
                         bg="white", fg=COLORS["text"],
                         wraplength=590, justify="left").pack(side="left", anchor="w")
