# ui/first_aid.py
# eita emergency first aid guide screen er UI
# CPR, burn care, choking er step-by-step instructions show kore

import tkinter as tk
from theme import COLORS, FONTS
from ui.components import make_scrollable_frame


# First aid topics er data — icon, title, steps list
FIRST_AID_TOPICS = {
    "cpr": {
        "icon":  "❤️",
        "title": "CPR (Cardiopulmonary Resuscitation)",
        "subtitle": "Heart attack ba cardiac arrest er somoy",
        "urgency": "EMERGENCY",
        "steps": [
            ("1", "Safety check", "Scene safe kina check korun. Personal safety prothom."),
            ("2", "Consciousness check", "Victim er kandhe haath rekhe shake kore dakun: 'Aap theek achen?'"),
            ("3", "Emergency call", "Immediately 999 / 112 call korun ba kake call korar jonno bolun."),
            ("4", "Airway open", "Victim ke chit kore shuiye mathar niche ektu uthu kore chin tilt-head lift maneuver korun."),
            ("5", "Breathing check", "10 seconds check korun: buk uthanama nema, nishwas er shobdo, mukhe batasher anubhuti."),
            ("6", "Chest compressions", "Buke dui hat rekhe (sternum er nichhe) 30 bar gura cha press korun — 100-120/minute speed e, 5-6 cm gove."),
            ("7", "Rescue breaths", "2টি rescue breath dun — naak band rekhe mukhe batas dun, buk uthanama dekhun."),
            ("8", "Continue cycle", "30 compression + 2 breath cycle chalie jan — ambulance ashar age ba victim sopormuk na haoa porionto."),
        ]
    },
    "burn": {
        "icon":  "🔥",
        "title": "Burn Care (Poda/Jalun)",
        "subtitle": "Hot liquid, fire, chemical burn er jonno",
        "urgency": "URGENT",
        "steps": [
            ("1", "Source remove", "Burn er source theke shore aso — fire, hot liquid, chemical."),
            ("2", "Cool the burn", "20 minutes thanda (room temperature) choltey paani diye dhute thakun. Ice use korben NA."),
            ("3", "Remove clothing", "Burn area theke kapor ba gehena khule felon — jodi te legey na thake."),
            ("4", "Cover loosely", "Porikar non-stick bandage ba porikar kapor diye dhekey din — tightly na."),
            ("5", "Pain management", "Paracetamol dite paren mild pain er jonno. Aspirin deben na."),
            ("6", "Infection signs", "Lali, ful, pus ba jowr holey doctor dekhun immediately."),
            ("7", "Seek help", "Mukher, hatir, genitallyer poda ba bair poda (3rd degree) hole ambulance dakun."),
        ]
    },
    "choking": {
        "icon":  "🫁",
        "title": "Choking (Gola Atke Jana)",
        "subtitle": "Khabar ba kono kichu gola atke gele",
        "urgency": "EMERGENCY",
        "steps": [
            ("1", "Coughing first", "Victim ke forcefully cough korte bolun — mild choking e eita kaaj kore."),
            ("2", "Back blows", "Victim er pichone dakiye eser bent forwade kore shoulder blade er modhe 5টি sharp blows dun."),
            ("3", "Heimlich maneuver", "Victim er pichon theke dui hat diye gele kole rakhuun, ekti mutthi nabi er upore rakhun, onyo hat diye dhore 5টi inward-upward thrusts dun."),
            ("4", "Alternate", "5 back blows + 5 abdominal thrusts — cycle chalie jan jotokhon obstructionata na bare."),
            ("5", "Unconscious victim", "Victim unconscious hole shoiye CPR run shuru korun. Chest compressions object ber korte sahoj hote paare."),
            ("6", "Infant choking", "1 bochor er niche shishu hole: Face-down position e 5 back slaps + face-up e 5 chest thrusts."),
            ("7", "Emergency call", "Yadi object ber na hoy, 999/112 immediately call korun."),
        ]
    },
    "bleeding": {
        "icon":  "🩹",
        "title": "Severe Bleeding (Beshi Roktopat)",
        "subtitle": "Kata cha, gahir jokhom er somoy",
        "urgency": "URGENT",
        "steps": [
            ("1", "Protect yourself", "Gloves ba plastic bag use kore nijer haath rakuun — blood borne disease theke."),
            ("2", "Direct pressure", "Porikar kapor ba bandage diye wound er upore soja chap dun — pressure maintain rakuun."),
            ("3", "Elevate", "Possible hole injured limb heart er upore tule rakhun."),
            ("4", "Do not remove", "Bandage blood soaked holey tao na tuleye upor theke ar ekটা layer dun."),
            ("5", "Tourniquet", "Limb bleeding thamanor jonno tourniquet use korte paren — last resort hisebe."),
            ("6", "Shock prevention", "Victim ke sobuj kore khablen na, shakta rakhuun, chador diye dhekey din."),
            ("7", "Emergency call", "Beshi roktopat hole ambulance immediately dakhun — delay korben na."),
        ]
    },
    "fracture": {
        "icon":  "🦴",
        "title": "Fracture (Haddi Vanga)",
        "subtitle": "Suspected bone fracture er somoy",
        "urgency": "URGENT",
        "steps": [
            ("1", "Don't move", "Injured area move koraben na — movement damage barate paare."),
            ("2", "Immobilize", "Splint diye fixed kore din — straight stick ba cardboard use korte paren."),
            ("3", "Padding", "Splint ar skin er modhe soft padding dun — comfort er jonno."),
            ("4", "Check circulation", "Splint er por fingers/toes er color, sensation, movement check korun."),
            ("5", "Ice pack", "Swelling komato cloth diye wrapped ice pack area te lagun — skin e direct na."),
            ("6", "Elevate", "Possible hole fracture area elevate korun — swelling komte help korbe."),
            ("7", "Hospital", "X-ray ar proper treatment er jonno hospital niye jan."),
        ]
    }
}


class FirstAidScreen:
    """
    Emergency first aid guide screen.
    Topic select korle step-by-step instructions dekha jabe.
    """

    def __init__(self, parent, user):
        self.parent = parent
        self.user = user
        self.current_topic = None
        self.frame = tk.Frame(parent, bg=COLORS["bg_main"])
        self._build_ui()

    def _build_ui(self):
        # page header
        header = tk.Frame(self.frame, bg=COLORS["danger"], padx=25, pady=18)
        header.pack(fill="x")

        tk.Label(
            header,
            text="🚑  Emergency First Aid Guide",
            font=FONTS["heading"],
            bg=COLORS["danger"],
            fg=COLORS["text_light"],
        ).pack(side="left")

        tk.Label(
            header,
            text="Emergency te ki korben janun",
            font=FONTS["body"],
            bg=COLORS["danger"],
            fg="#FFD0D0",
        ).pack(side="left", padx=15)

        # emergency hotline
        tk.Label(
            header,
            text="📞 Emergency: 999 / 112",
            font=FONTS["body_bold"],
            bg=COLORS["danger"],
            fg=COLORS["text_light"],
        ).pack(side="right")

        # main layout
        main = tk.Frame(self.frame, bg=COLORS["bg_main"], padx=20, pady=15)
        main.pack(fill="both", expand=True)

        # ---- LEFT: topic list ----
        left = tk.Frame(
            main, bg=COLORS["bg_card"], padx=0, pady=0,
            highlightthickness=1, highlightbackground=COLORS["border"],
            width=220
        )
        left.pack(side="left", fill="y", padx=(0, 15))
        left.pack_propagate(False)

        tk.Label(
            left,
            text="  📋  Topics",
            font=FONTS["subheading"],
            bg=COLORS["bg_card"],
            fg=COLORS["text_primary"],
            anchor="w",
            pady=12,
        ).pack(fill="x")

        tk.Frame(left, bg=COLORS["border"], height=1).pack(fill="x")

        # topic buttons
        for key, data in FIRST_AID_TOPICS.items():
            btn = tk.Button(
                left,
                text=f"  {data['icon']}  {data['title'][:22]}...",
                command=lambda k=key: self._show_topic(k),
                font=FONTS["sidebar"],
                bg=COLORS["bg_card"],
                fg=COLORS["text_primary"],
                relief="flat",
                anchor="w",
                padx=12,
                pady=10,
                cursor="hand2",
                activebackground=COLORS["bg_main"],
                bd=0,
            )
            btn.pack(fill="x")
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=COLORS["bg_main"]))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=COLORS["bg_card"]))

            tk.Frame(left, bg=COLORS["border"], height=1).pack(fill="x", padx=10)

        # ---- RIGHT: steps ----
        right = tk.Frame(main, bg=COLORS["bg_main"])
        right.pack(side="left", fill="both", expand=True)

        self.steps_scroll, self.steps_frame = make_scrollable_frame(right)
        self.steps_scroll.pack(fill="both", expand=True)

        # initial state
        tk.Label(
            self.steps_frame,
            text="👈  Bame ekটা topic select korun",
            font=FONTS["body"],
            bg=COLORS["bg_main"],
            fg=COLORS["text_muted"],
        ).pack(expand=True, pady=60)

    def _show_topic(self, topic_key):
        """Topic select korle steps show kore."""
        self.current_topic = topic_key
        data = FIRST_AID_TOPICS[topic_key]

        # clear previous steps
        for w in self.steps_frame.winfo_children():
            w.destroy()

        # urgency banner
        urgency_color = COLORS["danger"] if data["urgency"] == "EMERGENCY" else COLORS["warning"]

        banner = tk.Frame(self.steps_frame, bg=urgency_color, padx=18, pady=12)
        banner.pack(fill="x", pady=(0, 15))

        tk.Label(
            banner,
            text=f"{data['icon']}  {data['title']}",
            font=FONTS["subheading"],
            bg=urgency_color,
            fg=COLORS["text_light"],
        ).pack(anchor="w")

        tk.Label(
            banner,
            text=data["subtitle"],
            font=FONTS["body"],
            bg=urgency_color,
            fg="#FFE0E0" if data["urgency"] == "EMERGENCY" else "#FFF3C4",
        ).pack(anchor="w", pady=(4, 0))

        # steps
        for step_num, step_title, step_desc in data["steps"]:
            self._render_step(step_num, step_title, step_desc)

        # footer note
        tk.Frame(self.steps_frame, bg=COLORS["border"], height=1).pack(fill="x", pady=15)
        tk.Label(
            self.steps_frame,
            text="⚠  Ei guide shudhumatra basic tottho der jonno. Emergency te trained professional er help neben.",
            font=FONTS["small"],
            bg=COLORS["bg_main"],
            fg=COLORS["warning"],
            wraplength=560,
            justify="left",
        ).pack(anchor="w")

    def _render_step(self, step_num, title, description):
        """Ekटা step card render kore."""
        row = tk.Frame(self.steps_frame, bg=COLORS["bg_main"], pady=4)
        row.pack(fill="x")

        # step number circle
        num_label = tk.Label(
            row,
            text=step_num,
            font=("Segoe UI", 12, "bold"),
            bg=COLORS["primary"],
            fg=COLORS["text_light"],
            width=3,
            height=1,
            padx=8,
            pady=4,
        )
        num_label.pack(side="left", anchor="n", pady=4)

        # step content
        content = tk.Frame(row, bg=COLORS["bg_card"], padx=15, pady=10,
                           highlightthickness=1, highlightbackground=COLORS["border"])
        content.pack(side="left", fill="x", expand=True, padx=(6, 0))

        tk.Label(
            content,
            text=title,
            font=FONTS["body_bold"],
            bg=COLORS["bg_card"],
            fg=COLORS["text_primary"],
            anchor="w",
        ).pack(fill="x")

        tk.Label(
            content,
            text=description,
            font=FONTS["body"],
            bg=COLORS["bg_card"],
            fg=COLORS["text_secondary"],
            anchor="w",
            wraplength=520,
            justify="left",
        ).pack(fill="x", pady=(4, 0))

    def show(self):
        self.frame.pack(fill="both", expand=True)

    def hide(self):
        self.frame.pack_forget()