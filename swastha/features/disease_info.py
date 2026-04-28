"""
Disease Info Module
Provides comprehensive disease information
"""

import tkinter as tk
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ui.theme import COLORS, FONTS, PADDING

class DiseaseInfoUI:
    """Disease Info Feature UI"""
    
    def __init__(self, parent, user_id):
        """Initialize disease info UI"""
        self.parent = parent
        self.user_id = user_id
        self.disease_database = self.load_diseases()
        self.create_ui()
    
    def create_ui(self):
        """Create disease info UI"""
        # Title
        title = tk.Label(
            self.parent,
            text="📚 Disease Information",
            font=FONTS["title_medium"],
            bg=COLORS["light_gray"],
            fg=COLORS["black"]
        )
        title.pack(anchor="w", pady=(0, PADDING["lg"]))
        
        # Main container
        content = tk.Frame(self.parent, bg=COLORS["light_gray"])
        content.pack(fill=tk.BOTH, expand=True)
        
        # Left panel - Disease list
        left_panel = tk.Frame(content, bg=COLORS["white"], relief="raised", bd=1)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, PADDING["md"]), pady=0, sticky="ns")
        
        list_label = tk.Label(
            left_panel,
            text="Select Disease",
            font=FONTS["heading_2"],
            bg=COLORS["white"],
            fg=COLORS["black"],
            padx=PADDING["md"],
            pady=PADDING["md"]
        )
        list_label.pack(anchor="w", fill=tk.X)
        
        # Search box
        search_frame = tk.Frame(left_panel, bg=COLORS["white"])
        search_frame.pack(fill=tk.X, padx=PADDING["md"], pady=PADDING["sm"])
        
        search_label = tk.Label(search_frame, text="Search", font=FONTS["label"], bg=COLORS["white"])
        search_label.pack(anchor="w")
        
        self.search_var = tk.StringVar()
        self.search_var.trace("w", lambda *args: self.update_disease_list())
        search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=FONTS["body_medium"],
            relief="solid",
            bd=1
        )
        search_entry.pack(fill=tk.X, pady=(5, 0))
        
        # Disease listbox
        list_frame = tk.Frame(left_panel, bg=COLORS["white"])
        list_frame.pack(fill=tk.BOTH, expand=True, padx=PADDING["md"], pady=PADDING["md"])
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.disease_listbox = tk.Listbox(
            list_frame,
            font=FONTS["body_small"],
            bg=COLORS["light_gray"],
            yscrollcommand=scrollbar.set,
            width=25
        )
        self.disease_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.disease_listbox.bind("<<ListboxSelect>>", self.on_disease_select)
        scrollbar.config(command=self.disease_listbox.yview)
        
        self.update_disease_list()
        
        # Right panel - Disease details
        right_panel = tk.Frame(content, bg=COLORS["white"], relief="raised", bd=1)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(PADDING["md"], 0), pady=0)
        
        info_label = tk.Label(
            right_panel,
            text="Disease Details",
            font=FONTS["heading_2"],
            bg=COLORS["white"],
            fg=COLORS["black"],
            padx=PADDING["md"],
            pady=PADDING["md"]
        )
        info_label.pack(anchor="w", fill=tk.X)
        
        # Information display
        scrollbar_frame = tk.Frame(right_panel)
        scrollbar_frame.pack(fill=tk.BOTH, expand=True, padx=PADDING["md"], pady=PADDING["md"])
        
        scrollbar2 = tk.Scrollbar(scrollbar_frame)
        scrollbar2.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.info_text = tk.Text(
            scrollbar_frame,
            font=FONTS["body_medium"],
            bg=COLORS["light_gray"],
            relief="solid",
            bd=1,
            yscrollcommand=scrollbar2.set,
            state="disabled"
        )
        self.info_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar2.config(command=self.info_text.yview)
        
        # Show welcome
        self.show_welcome()
    
    def load_diseases(self):
        """Load disease database"""
        return {
            "Common Cold": """COMMON COLD

DEFINITION:
The common cold is a viral infection that primarily affects the upper respiratory tract.

SYMPTOMS:
• Sneezing
• Nasal congestion
• Runny nose
• Sore throat
• Cough
• Mild fever
• Fatigue
• Headache

CAUSES:
• Rhinovirus (most common)
• Coronavirus
• Parainfluenza virus
• Droplet transmission for 3-5 days

TREATMENT:
✓ Rest and adequate sleep
✓ Stay hydrated (water, warm liquids)
✓ Use saline nasal drops
✓ Honey for cough relief
✓ Pain relievers for discomfort
✓ Decongestants if needed

PREVENTION:
• Wash hands frequently
• Avoid touching face
• Maintain hygiene
• Get adequate sleep
• Use masks when sick

DURATION: Usually 7-10 days

WHEN TO SEE DOCTOR:
• Symptoms persist beyond 10 days
• High fever develops
• Difficulty breathing
• Symptoms worsen dramatically""",
            
            "Diabetes": """DIABETES MELLITUS

DEFINITION:
Chronic metabolic disorder affecting blood sugar regulation.

TYPES:
• Type 1: Pancreas doesn't produce insulin
• Type 2: Body resists insulin (most common)
• Gestational: During pregnancy

SYMPTOMS:
• Excessive thirst
• Frequent urination
• Fatigue
• Blurred vision
• Slow healing wounds
• Tingling in feet/hands
• Weight loss (Type 1)

RISK FACTORS:
• Family history
• Obesity
• Sedentary lifestyle
• Poor diet
• Age (over 45)

MANAGEMENT:
✓ Regular blood glucose monitoring
✓ Balanced diet (whole grains, vegetables)
✓ Regular exercise (150 mins/week)
✓ Weight management
✓ Medications as prescribed
✓ Stress management
✓ Regular check-ups

COMPLICATIONS:
• Heart disease
• Kidney damage
• Vision problems
• Nerve damage (neuropathy)
• Poor wound healing

PREVENTION:
• Maintain healthy weight
• Regular physical activity
• Balanced nutrition
• Manage stress
• Regular screening""",
            
            "Hypertension": """HYPERTENSION (HIGH BLOOD PRESSURE)

DEFINITION:
Persistent elevation of blood pressure above normal levels.

BLOOD PRESSURE CATEGORIES:
• Normal: < 120/80 mmHg
• Elevated: 120-129/<80 mmHg
• Stage 1: 130-139/80-89 mmHg
• Stage 2: ≥ 140/90 mmHg

SYMPTOMS (Often Asymptomatic):
• Headaches
• Shortness of breath
• Dizziness
• Chest pain
• Nosebleeds

RISK FACTORS:
• Age (over 60)
• Family history
• Smoking
• Excessive alcohol
• Poor diet (high sodium)
• Obesity
• Lack of exercise
• Stress

MANAGEMENT:
✓ Reduce sodium intake
✓ Regular exercise (30 mins/day)
✓ Maintain healthy weight
✓ Limit alcohol
✓ DASH diet (fruits, vegetables, whole grains)
✓ Stress management
✓ Medications as needed
✓ Regular monitoring

COMPLICATIONS:
• Heart disease
• Stroke
• Kidney disease
• Vision problems

PREVENTION:
• Balanced diet
• Regular exercise
• Stress reduction
• Avoid smoking
• Limit alcohol""",
            
            "Asthma": """ASTHMA

DEFINITION:
Chronic respiratory condition causing inflammation and narrowing of airways.

SYMPTOMS:
• Shortness of breath
• Wheezing
• Chest tightness
• Frequent cough (especially at night)
• Difficulty sleeping due to breathing issues

TRIGGERS:
• Allergens (pollen, pets, dust)
• Exercise
• Cold air
• Stress
• Pollution
• Infections
• Strong emotions

SEVERITY LEVELS:
• Intermittent: Symptoms < 2 days/week
• Persistent (mild to severe): Regular symptoms

MANAGEMENT:
✓ Identify and avoid triggers
✓ Use rescue inhaler (reliever) as needed
✓ Use maintenance inhaler (controller) daily
✓ Monitor peak flow regularly
✓ Create action plan with doctor
✓ Regular check-ups

EMERGENCY SIGNS:
🚨 Seek immediate help if:
• Severe shortness of breath
• No improvement with inhaler
• Difficulty speaking
• Bluish lips/face
• Severe panic

PREVENTION:
• Use air purifier
• Maintain clean environment
• Stay physically active
• Manage allergies
• Avoid respiratory infections""",
            
            "Allergies": """ALLERGIES

DEFINITION:
Abnormal immune response to usually harmless substances.

COMMON ALLERGENS:
• Pollen
• Dust mites
• Pet dander
• Mold spores
• Food (nuts, shellfish, eggs)
• Medications
• Insect venom

SYMPTOMS:
• Sneezing
• Itchy/watery eyes
• Runny/stuffy nose
• Skin rash
• Itching
• Swelling (in severe cases)

TYPES:
• Seasonal allergies
• Perennial allergies
• Food allergies
• Drug allergies
• Contact allergies

MANAGEMENT:
✓ Avoid known allergens
✓ Keep home clean
✓ Use air filters
✓ Take antihistamines
✓ Use nasal sprays
✓ Immunotherapy (long-term)
✓ Keep EpiPen for severe allergies

EMERGENCY:
🚨 Anaphylaxis requires immediate medical care:
• Severe swelling
• Difficulty breathing
• Loss of consciousness

PREVENTION:
• Read food labels
• Know your allergens
• Carry medication
• Inform others of allergies
• Wear medical alert bracelet""",
        }
    
    def update_disease_list(self):
        """Update disease list based on search"""
        search_term = self.search_var.get().lower()
        
        self.disease_listbox.delete(0, tk.END)
        
        for disease in self.disease_database.keys():
            if search_term in disease.lower():
                self.disease_listbox.insert(tk.END, disease)
    
    def on_disease_select(self, event):
        """Display selected disease information"""
        selection = self.disease_listbox.curselection()
        
        if selection:
            disease_name = self.disease_listbox.get(selection[0])
            self.display_disease_info(disease_name)
    
    def display_disease_info(self, disease_name):
        """Display disease information"""
        self.info_text.config(state="normal")
        self.info_text.delete("1.0", tk.END)
        
        if disease_name in self.disease_database:
            self.info_text.insert("1.0", self.disease_database[disease_name])
        else:
            self.info_text.insert("1.0", "Disease information not found.")
        
        self.info_text.config(state="disabled")
    
    def show_welcome(self):
        """Show welcome message"""
        self.info_text.config(state="normal")
        self.info_text.delete("1.0", tk.END)
        self.info_text.insert("1.0", "Select a disease from the list to view detailed information.\n\nYou can search for diseases using the search box on the left.\n\nDisclaimer: This information is for educational purposes. Always consult healthcare professionals for medical advice.")
        self.info_text.config(state="disabled")
