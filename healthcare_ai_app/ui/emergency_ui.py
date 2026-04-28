"""
Emergency First Aid Guide Page
"""

import tkinter as tk
from tkinter import ttk
import sys, os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.helpers import COLORS, FONTS, scrollable_frame

FIRST_AID_DATA = {
    "CPR": {
        "icon": "❤️",
        "color": "#E74C3C",
        "subtitle": "Cardiopulmonary Resuscitation",
        "warning": "Call emergency services (911/999) FIRST before starting CPR!",
        "steps": [
            ("Check Safety", "Ensure the scene is safe for you and the victim. Do not put yourself in danger."),
            ("Check Responsiveness", "Tap the person's shoulder firmly and shout 'Are you OK?' loudly."),
            ("Call for Help", "Call emergency services immediately. Ask a bystander to get an AED if available."),
            ("Position", "Lay the person on their back on a firm, flat surface."),
            ("Chest Compressions", "Place the heel of your hand on the center of the chest (lower half of breastbone). Interlock fingers. Push hard and fast — at least 2 inches (5cm) deep at 100-120 compressions/min."),
            ("Rescue Breaths", "After 30 compressions: tilt head back, lift chin. Pinch nose, create a seal over mouth and give 2 breaths (1 second each). Chest should rise."),
            ("Continue", "Repeat 30:2 cycle (30 compressions, 2 breaths) until help arrives, an AED is available, or the person starts breathing."),
            ("AED", "If an AED arrives, turn it on and follow its voice instructions immediately."),
        ]
    },
    "Burns": {
        "icon": "🔥",
        "color": "#E67E22",
        "subtitle": "Thermal / Chemical Burns",
        "warning": "For severe burns covering large areas, call emergency services immediately!",
        "steps": [
            ("Stop the Burning", "Remove the person from the source of heat. For chemical burns, brush off dry chemicals first, then flush with water."),
            ("Cool the Burn", "Run cool (NOT cold) water over the burn for 10-20 minutes. Do not use ice, butter, or toothpaste."),
            ("Remove Accessories", "Remove jewelry, watches, or tight clothing NEAR the burn — not from burned skin."),
            ("Cover the Burn", "Loosely cover with a sterile non-fluffy bandage or clean plastic wrap. Do not burst blisters."),
            ("Pain Relief", "Take over-the-counter pain relief (ibuprofen or paracetamol) if needed."),
            ("Do NOT", "Do NOT use ice, ice water, creams, butter, or any home remedies on the burn."),
            ("Seek Medical Help", "Go to the hospital if: burn is larger than 3 inches, on face/hands/genitals/feet, or is deep/white/leathery."),
        ]
    },
    "Choking": {
        "icon": "🫁",
        "color": "#9B59B6",
        "subtitle": "Airway Obstruction",
        "warning": "If the person cannot speak, cough, or breathe — ACT IMMEDIATELY!",
        "steps": [
            ("Assess Severity", "If the person can cough forcefully, encourage them to keep coughing. Do NOT interfere with an effective cough."),
            ("5 Back Blows", "Stand to the side and slightly behind. Support the chest with one hand. Give 5 firm blows between the shoulder blades with the heel of your hand."),
            ("Check Mouth", "After each back blow, check if the object has come out. Remove it if visible."),
            ("5 Abdominal Thrusts (Heimlich)", "Stand behind the person. Make a fist above the navel, below the breastbone. Grasp your fist with your other hand. Give 5 inward and upward thrusts."),
            ("Alternate", "Alternate 5 back blows with 5 abdominal thrusts until the object is cleared or help arrives."),
            ("If Unconscious", "If the person loses consciousness, lower them to the floor and begin CPR. Each time you open the airway to give breaths, look for the object."),
            ("Infants (< 1 year)", "Use 5 back blows + 5 CHEST thrusts (not abdominal). Never use abdominal thrusts on infants."),
        ]
    },
    "Bleeding": {
        "icon": "🩸",
        "color": "#C0392B",
        "subtitle": "Wound & Hemorrhage Control",
        "warning": "Call emergency services if bleeding is severe or does not stop within 10-15 minutes!",
        "steps": [
            ("Personal Safety", "Protect yourself — wear gloves if available to prevent infection."),
            ("Apply Pressure", "Press firmly on the wound with a clean cloth, sterile bandage, or clothing. Use the flat of your hand for large wounds."),
            ("Maintain Pressure", "Keep steady pressure for at least 10-15 minutes. Do NOT lift to check — this disturbs clotting."),
            ("Elevate", "If the wound is on a limb (and no fracture suspected), raise it above the level of the heart."),
            ("Secure Dressing", "Once bleeding slows, secure the dressing with a bandage. If blood soaks through, add another layer on top."),
            ("Tourniquet (Last Resort)", "Only if bleeding is life-threatening and cannot be controlled: apply a tourniquet 2-3 inches above the wound. Note the time applied."),
            ("Shock Management", "Lay the person down, elevate legs if possible, keep warm, do NOT give anything to eat/drink."),
            ("Seek Care", "All but the most minor wounds should be evaluated by a healthcare professional."),
        ]
    },
    "Fracture": {
        "icon": "🦴",
        "color": "#2980B9",
        "subtitle": "Broken Bones",
        "warning": "Do NOT try to realign the bone. Keep the injured area still.",
        "steps": [
            ("Stop Bleeding", "If there is an open wound, apply gentle pressure to stop bleeding with a clean cloth."),
            ("Immobilize", "Immobilize the injured area. Do NOT try to straighten it. Support it in the position you find it."),
            ("Splint", "If help is not coming quickly, make an improvised splint using a board, rolled newspaper, or stiff object. Pad it well."),
            ("Ice", "Apply ice (wrapped in cloth) to the area to reduce swelling and pain. Do NOT apply directly to skin."),
            ("Elevate", "If possible, gently elevate the injured limb."),
            ("Do NOT Move", "For spine/neck injuries: do NOT move the person unless they are in immediate danger."),
            ("Seek Medical Care", "All suspected fractures need X-ray confirmation. Seek medical help promptly."),
        ]
    },
    "Seizure": {
        "icon": "⚡",
        "color": "#F39C12",
        "subtitle": "Convulsions / Epileptic Episode",
        "warning": "Call emergency services if: seizure lasts >5 min, person is pregnant, injured, or does not regain consciousness.",
        "steps": [
            ("Stay Calm", "Do NOT panic. Most seizures end on their own in 1-3 minutes."),
            ("Time It", "Note when the seizure started. Call 911 if it lasts more than 5 minutes."),
            ("Clear Space", "Move sharp or hard objects away from the person to prevent injury."),
            ("Ease to Ground", "If standing, gently guide them to the floor. Cushion their head."),
            ("Positioning", "Turn the person gently onto their side (recovery position) to prevent choking."),
            ("Do NOT", "Do NOT restrain them. Do NOT put anything in their mouth. Do NOT give water or food."),
            ("After Seizure", "Stay with them. They may be confused. Speak calmly. Check for injury."),
            ("Recovery", "Help them rest. Most people need to sleep after a seizure."),
        ]
    },
}


class EmergencyPage:
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
        self._selected = None
        self._build()

    def _build(self):
        hdr = tk.Frame(self.parent, bg=COLORS["red"], height=60)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
        tk.Label(hdr, text="🚑 Emergency First Aid Guide",
                 font=FONTS["title"], bg=COLORS["red"], fg="white"
                 ).place(relx=0.02, rely=0.5, anchor="w")
        tk.Label(hdr, text="⚠️ Always call emergency services first!",
                 font=FONTS["small"], bg=COLORS["red"], fg="#FADBD8"
                 ).place(relx=0.98, rely=0.5, anchor="e")

        main = tk.Frame(self.parent, bg=COLORS["bg"])
        main.pack(fill="both", expand=True)

        # Left: buttons
        left = tk.Frame(main, bg=COLORS["bg"], width=220)
        left.pack(side="left", fill="y", padx=12, pady=12)
        left.pack_propagate(False)
        self._build_buttons(left)

        # Right: guide content
        right = tk.Frame(main, bg=COLORS["bg"])
        right.pack(side="right", fill="both", expand=True, padx=12, pady=12)
        self.guide_frame = right
        self._show_placeholder()

    def _build_buttons(self, parent):
        tk.Label(parent, text="Select Emergency:",
                 font=FONTS["subhead"], bg=COLORS["bg"], fg=COLORS["text"]
                 ).pack(anchor="w", pady=(0, 8))

        for key, data in FIRST_AID_DATA.items():
            color = data["color"]
            btn = tk.Button(
                parent,
                text=f"{data['icon']}  {key}",
                font=("Segoe UI", 11, "bold"),
                bg=color, fg="white",
                relief="flat", cursor="hand2",
                anchor="w", padx=12, pady=10,
                command=lambda k=key: self._show_guide(k)
            )
            btn.pack(fill="x", pady=3)

            def on_enter(e, b=btn, c=color):
                b.config(bg=self._darken(c))
            def on_leave(e, b=btn, c=color):
                b.config(bg=c)
            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)

        # Emergency numbers
        nums = tk.Frame(parent, bg="#FDEDEC")
        nums.pack(fill="x", pady=(16, 0))
        ni = tk.Frame(nums, bg="#FDEDEC")
        ni.pack(padx=10, pady=10, fill="x")

        tk.Label(ni, text="📞 Emergency Numbers",
                 font=FONTS["subhead"], bg="#FDEDEC", fg=COLORS["red"]).pack(anchor="w")
        numbers = [
            ("Bangladesh", "999"),
            ("India", "112"),
            ("US / Canada", "911"),
            ("UK", "999"),
            ("EU", "112"),
        ]
        for country, num in numbers:
            row = tk.Frame(ni, bg="#FDEDEC")
            row.pack(fill="x", pady=1)
            tk.Label(row, text=country, font=FONTS["small"], bg="#FDEDEC",
                     fg=COLORS["text_lt"], width=14, anchor="w").pack(side="left")
            tk.Label(row, text=num, font=("Segoe UI", 10, "bold"), bg="#FDEDEC",
                     fg=COLORS["red"]).pack(side="left")

    def _show_placeholder(self):
        tk.Label(
            self.guide_frame,
            text="👆 Select an emergency type\nfrom the left panel",
            font=FONTS["heading"], bg=COLORS["bg"], fg=COLORS["text_lt"],
            justify="center"
        ).place(relx=0.5, rely=0.4, anchor="center")

    def _show_guide(self, key):
        for w in self.guide_frame.winfo_children():
            w.destroy()

        data = FIRST_AID_DATA[key]
        color = data["color"]

        # Title card
        title_card = tk.Frame(self.guide_frame, bg=color)
        title_card.pack(fill="x", pady=(0, 10))
        ti = tk.Frame(title_card, bg=color)
        ti.pack(padx=16, pady=12, fill="x")

        tk.Label(ti, text=f"{data['icon']}  {key}",
                 font=("Segoe UI", 18, "bold"), bg=color, fg="white").pack(anchor="w")
        tk.Label(ti, text=data["subtitle"],
                 font=FONTS["body"], bg=color, fg="white").pack(anchor="w")

        # Warning box
        warn = tk.Frame(self.guide_frame, bg="#FFF3CD")
        warn.pack(fill="x", pady=(0, 8))
        wi = tk.Frame(warn, bg="#FFF3CD")
        wi.pack(padx=14, pady=8, fill="x")
        tk.Label(wi, text=f"⚠️ {data['warning']}",
                 font=("Segoe UI", 10, "bold"), bg="#FFF3CD", fg="#856404",
                 wraplength=620, justify="left").pack(anchor="w")

        # Steps
        outer, scroll = scrollable_frame(self.guide_frame)
        outer.pack(fill="both", expand=True)

        for i, (title, desc) in enumerate(data["steps"]):
            step_card = tk.Frame(scroll, bg="white")
            step_card.pack(fill="x", pady=3)
            si = tk.Frame(step_card, bg="white")
            si.pack(padx=14, pady=10, fill="x")

            # Step number badge
            badge_row = tk.Frame(si, bg="white")
            badge_row.pack(fill="x")
            badge = tk.Label(badge_row, text=f" {i+1} ", font=("Segoe UI", 10, "bold"),
                             bg=color, fg="white", padx=6, pady=2)
            badge.pack(side="left")
            tk.Label(badge_row, text=f"  {title}",
                     font=FONTS["subhead"], bg="white", fg=COLORS["text"]).pack(side="left")

            tk.Label(si, text=desc, font=FONTS["body"],
                     bg="white", fg=COLORS["text"],
                     wraplength=580, justify="left").pack(anchor="w", pady=(4, 0))

    @staticmethod
    def _darken(color):
        r = int(color[1:3], 16)
        g = int(color[3:5], 16)
        b = int(color[5:7], 16)
        f = 0.8
        return "#{:02x}{:02x}{:02x}".format(int(r*f), int(g*f), int(b*f))
