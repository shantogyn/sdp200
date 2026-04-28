"""
First Aid Module
Provides emergency first aid instructions
"""

import tkinter as tk
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ui.theme import COLORS, FONTS, PADDING
from ui.components import CustomButton

class FirstAidUI:
    """First Aid Feature UI"""
    
    def __init__(self, parent, user_id):
        """Initialize first aid UI"""
        self.parent = parent
        self.user_id = user_id
        self.first_aid_guide = self.load_first_aid_guide()
        self.create_ui()
    
    def create_ui(self):
        """Create first aid UI"""
        # Title
        title = tk.Label(
            self.parent,
            text="🚑 First Aid Guide",
            font=FONTS["title_medium"],
            bg=COLORS["light_gray"],
            fg=COLORS["black"]
        )
        title.pack(anchor="w", pady=(0, PADDING["lg"]))
        
        # Emergency info
        emergency_frame = tk.Frame(self.parent, bg=COLORS["danger"], relief="raised", bd=1)
        emergency_frame.pack(fill=tk.X, padx=0, pady=(0, PADDING["lg"]))
        
        emergency_text = tk.Label(
            emergency_frame,
            text="🚨 FOR LIFE-THREATENING EMERGENCIES, CALL EMERGENCY SERVICES (911 / 112) IMMEDIATELY",
            font=FONTS["heading_2"],
            bg=COLORS["danger"],
            fg=COLORS["white"],
            wraplength=600,
            justify="center",
            padx=PADDING["md"],
            pady=PADDING["md"]
        )
        emergency_text.pack()
        
        # Main container
        content = tk.Frame(self.parent, bg=COLORS["light_gray"])
        content.pack(fill=tk.BOTH, expand=True)
        
        # Left panel - Categories
        left_panel = tk.Frame(content, bg=COLORS["white"], relief="raised", bd=1)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, PADDING["md"]), pady=0)
        
        categories_label = tk.Label(
            left_panel,
            text="Emergencies",
            font=FONTS["heading_2"],
            bg=COLORS["white"],
            fg=COLORS["black"],
            padx=PADDING["md"],
            pady=PADDING["md"]
        )
        categories_label.pack(anchor="w", fill=tk.X)
        
        categories_frame = tk.Frame(left_panel, bg=COLORS["white"])
        categories_frame.pack(fill=tk.BOTH, expand=True, padx=PADDING["md"], pady=PADDING["md"])
        
        # Category buttons
        for category in self.first_aid_guide.keys():
            btn = tk.Button(
                categories_frame,
                text=f"• {category}",
                font=FONTS["body_medium"],
                bg=COLORS["light_gray"],
                fg=COLORS["black"],
                relief="flat",
                anchor="w",
                padx=PADDING["md"],
                pady=PADDING["sm"],
                cursor="hand2",
                command=lambda c=category: self.display_guide(c)
            )
            btn.pack(fill=tk.X, pady=PADDING["sm"])
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=COLORS["primary"], fg=COLORS["white"]))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=COLORS["light_gray"], fg=COLORS["black"]))
        
        # Right panel - Instructions
        right_panel = tk.Frame(content, bg=COLORS["white"], relief="raised", bd=1)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(PADDING["md"], 0), pady=0)
        
        guide_label = tk.Label(
            right_panel,
            text="Instructions",
            font=FONTS["heading_2"],
            bg=COLORS["white"],
            fg=COLORS["black"],
            padx=PADDING["md"],
            pady=PADDING["md"]
        )
        guide_label.pack(anchor="w", fill=tk.X)
        
        # Instructions text
        scrollbar_frame = tk.Frame(right_panel)
        scrollbar_frame.pack(fill=tk.BOTH, expand=True, padx=PADDING["md"], pady=PADDING["md"])
        
        scrollbar = tk.Scrollbar(scrollbar_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.guide_text = tk.Text(
            scrollbar_frame,
            font=FONTS["body_medium"],
            bg=COLORS["light_gray"],
            relief="solid",
            bd=1,
            yscrollcommand=scrollbar.set,
            state="disabled"
        )
        self.guide_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.guide_text.yview)
        
        # Show first category
        if self.first_aid_guide:
            first_category = list(self.first_aid_guide.keys())[0]
            self.display_guide(first_category)
    
    def load_first_aid_guide(self):
        """Load first aid guide data"""
        return {
            "CPR": """CARDIOPULMONARY RESUSCITATION (CPR)

🔴 CHECK RESPONSIVENESS
1. Tap and shout at the person
2. Call emergency services immediately
3. Get an AED if available

🔴 POSITION THE PERSON
1. Place on firm, flat surface
2. Tilt head back slightly
3. Clear airway of obstructions

🔴 CHEST COMPRESSIONS
1. Place heel of hand on center of chest
2. Place other hand on top
3. Push hard and fast (100-120 compressions/min)
4. Allow chest to recoil between compressions

🔴 RESCUE BREATHS
1. Open airway by tilting head back
2. Pinch nose and seal mouth
3. Give 2 rescue breaths
4. Return to chest compressions

🔴 CONTINUE UNTIL
• Emergency responders arrive
• Signs of life appear
• You are too exhausted
• AED advises stopping""",
            
            "Choking": """CHOKING - HEIMLICH MANEUVER

🔴 IF PERSON CAN'T TALK/COUGH/BREATHE
1. Stand behind the person
2. Make a fist above navel, below ribcage
3. Grasp fist with other hand
4. Press inward and upward with sudden thrust
5. Repeat 5-10 times

🔴 IF PERSON BECOMES UNCONSCIOUS
1. Lay person on back
2. Open mouth and clear airway
3. Begin CPR
4. Check mouth after each compression

🔴 INFANT CHOKING (< 1 year)
1. Support infant's jaw
2. Give 5 back blows between shoulders
3. Place 2 fingers on breastbone
4. Give 5 chest thrusts
5. Check mouth and repeat if needed

🔴 CALL EMERGENCY IF
• Choking persists after 1 minute
• Person becomes unconscious
• Unable to clear airway""",
            
            "Severe Bleeding": """SEVERE BLEEDING CONTROL

🔴 INITIAL RESPONSE
1. Safety first - wear gloves if available
2. Call emergency services
3. Do not remove embedded objects

🔴 APPLY DIRECT PRESSURE
1. Use clean cloth or gauze
2. Press firmly on wound
3. Maintain pressure (don't peek)
4. Apply for 10-15 minutes minimum

🔴 IF BLEEDING CONTINUES
1. Add more cloth (don't remove first)
2. Maintain continuous pressure
3. Elevate bleeding area above heart if possible
4. Apply tourniquet if limb amputation risk

🔴 APPLY TOURNIQUET (Life/Limb Threat)
1. Place 2-3 inches above wound
2. Make tight - should stop bleeding
3. Note the time applied
4. Do not remove in emergency care

🔴 DRESS THE WOUND
1. Use sterile bandages
2. Wrap snugly but not too tight
3. Check circulation below bandage
4. Prepare for transport""",
            
            "Burns": """BURN TREATMENT

🔴 IMMEDIATE CARE
1. Stop the burning - remove from heat source
2. Remove burning clothing (except stuck items)
3. Cool the burn with water (not ice)
4. Cool for 10-20 minutes minimum

🔴 ASSESSING BURN SEVERITY
• 1st degree: Red, painful (sun exposure)
• 2nd degree: Blistered, severe pain
• 3rd degree: White/black, painless

🔴 FOR MINOR BURNS
1. Cool with lukewarm water
2. Apply antibiotic ointment
3. Use non-stick dressing
4. Take pain relief if needed

🔴 FOR SEVERE BURNS
1. Call emergency services
2. DO NOT remove stuck clothing
3. DO NOT apply ice directly
4. DO NOT pop blisters
5. Cover loosely with clean cloth
6. Elevate burned area

🔴 SEEK IMMEDIATE HELP IF
• Burn larger than 3 inches
• Third degree burn
• On face, joints, genitals
• From chemicals or electricity""",
            
            "Fractures": """BONE FRACTURE MANAGEMENT

🔴 INITIAL ASSESSMENT
1. Safety first - move to safe location
2. Check for circulation/sensation below fracture
3. Call emergency if severe

🔴 RICE PROTOCOL
R - REST: Stop activity immediately
I - ICE: Apply ice pack (20 mins on/off)
C - COMPRESSION: Wrap with elastic bandage
E - ELEVATION: Raise above heart level

🔴 IMMOBILIZATION
1. Support the injured area
2. Use sling, splint, or bandage
3. Prevent any movement
4. Check for numbness/tingling

🔴 GENERAL CARE
1. Elevate injured limb
2. Apply ice for first 24-48 hours
3. Take pain reliever as needed
4. Avoid putting weight on injury

🔴 WHEN TO SEEK MEDICAL AID
• Any severe deformity
• Inability to move
• Severe swelling/pain
• Numbness or tingling
• Bleeding from wound""",
            
            "Poisoning": """POISONING & OVERDOSE

🔴 CALL POISON CONTROL IMMEDIATELY
Call: 1-800-222-1222 (US)
Or: Emergency Services (911)

🔴 PROVIDE INFORMATION
1. What substance was ingested
2. When it was taken
3. How much was taken
4. Person's age and weight
5. Current symptoms

🔴 DO NOT
❌ Induce vomiting
❌ Give activated charcoal
❌ Leave person alone
❌ Try to drive to hospital alone

🔴 CARE WHILE WAITING
1. Keep person calm
2. Loosely position on side
3. Monitor breathing
4. Keep substance container for reference
5. Stay on line with poison control

🔴 COMMON POISONS
• Medications (aspirin, painkillers)
• Household chemicals (bleach, pesticides)
• Carbon monoxide
• Alcohol overdose
• Food poisoning""",
        }
    
    def display_guide(self, category):
        """Display guide for category"""
        self.guide_text.config(state="normal")
        self.guide_text.delete("1.0", tk.END)
        self.guide_text.insert("1.0", self.first_aid_guide.get(category, ""))
        self.guide_text.config(state="disabled")
