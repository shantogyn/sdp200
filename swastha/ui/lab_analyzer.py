# ui/lab_analyzer.py
# eita lab report analyzer screen er UI
# user image upload korbe, OCR diye text extract hobe, values analyze hobe

import tkinter as tk
from tkinter import filedialog
from theme import COLORS, FONTS
from ui.components import make_button, make_scrollable_frame, make_badge
from utils.ocr import extract_text_from_image
from services.lab_service import analyze_report_text, save_report, get_status_color


class LabAnalyzerScreen:
    """
    Lab report analyzer screen.
    Image upload → OCR → value parsing → normal/abnormal display.
    """

    def __init__(self, parent, user):
        self.parent = parent
        self.user = user
        self.extracted_text = ""
        self.frame = tk.Frame(parent, bg=COLORS["bg_main"])
        self._build_ui()

    def _build_ui(self):
        # page header
        header = tk.Frame(self.frame, bg=COLORS["primary"], padx=25, pady=18)
        header.pack(fill="x")

        tk.Label(
            header,
            text="🧪  Lab Report Analyzer",
            font=FONTS["heading"],
            bg=COLORS["primary"],
            fg=COLORS["text_light"],
        ).pack(side="left")

        # main area
        main = tk.Frame(self.frame, bg=COLORS["bg_main"], padx=30, pady=20)
        main.pack(fill="both", expand=True)

        # ---- LEFT: Upload + OCR text ----
        left = tk.Frame(main, bg=COLORS["bg_card"], padx=20, pady=20,
                        highlightthickness=1, highlightbackground=COLORS["border"])
        left.pack(side="left", fill="y", padx=(0, 15), ipadx=5)

        tk.Label(
            left,
            text="📁  Report Upload / Input",
            font=FONTS["subheading"],
            bg=COLORS["bg_card"],
            fg=COLORS["text_primary"],
        ).pack(anchor="w", pady=(0, 12))

        # Upload button
        make_button(
            left,
            text="  📂  Image Upload Korun  ",
            command=self._upload_image,
        ).pack(fill="x", ipady=4)

        self.file_label = tk.Label(
            left,
            text="Kono file select kora hoy ni",
            font=FONTS["small"],
            bg=COLORS["bg_card"],
            fg=COLORS["text_muted"],
            wraplength=230,
        )
        self.file_label.pack(pady=(5, 12))

        # divider with OR text
        div_row = tk.Frame(left, bg=COLORS["bg_card"])
        div_row.pack(fill="x", pady=5)
        tk.Frame(div_row, bg=COLORS["border"], height=1).pack(side="left", fill="x", expand=True)
        tk.Label(div_row, text="  OR  ", font=FONTS["small"], bg=COLORS["bg_card"],
                 fg=COLORS["text_muted"]).pack(side="left")
        tk.Frame(div_row, bg=COLORS["border"], height=1).pack(side="left", fill="x", expand=True)

        # Manual text input
        tk.Label(
            left,
            text="Manually report text paste korun:",
            font=FONTS["body_bold"],
            bg=COLORS["bg_card"],
            fg=COLORS["text_secondary"],
        ).pack(anchor="w", pady=(8, 4))

        self.text_input = tk.Text(
            left,
            font=FONTS["monospace"],
            bg=COLORS["bg_main"],
            fg=COLORS["text_primary"],
            relief="flat",
            highlightthickness=1,
            highlightbackground=COLORS["border"],
            highlightcolor=COLORS["primary"],
            width=30,
            height=10,
            wrap="word",
            insertbackground=COLORS["text_primary"],
        )
        self.text_input.pack(fill="x", pady=(0, 12))

        # Analyze button
        make_button(
            left,
            text="  🔍  Analyze Report  ",
            command=self._analyze,
        ).pack(fill="x", ipady=4)

        # Save button
        tk.Button(
            left,
            text="💾  Save Report",
            command=self._save,
            font=FONTS["small"],
            bg=COLORS["bg_main"],
            fg=COLORS["primary"],
            relief="flat",
            cursor="hand2",
            pady=6,
        ).pack(fill="x", pady=(8, 0))

        # ---- RIGHT: Analysis results ----
        right = tk.Frame(main, bg=COLORS["bg_main"])
        right.pack(side="left", fill="both", expand=True)

        tk.Label(
            right,
            text="📊  Analysis Results",
            font=FONTS["subheading"],
            bg=COLORS["bg_main"],
            fg=COLORS["text_primary"],
        ).pack(anchor="w", pady=(0, 10))

        self.result_scroll, self.result_frame = make_scrollable_frame(right)
        self.result_scroll.pack(fill="both", expand=True)

        self._show_placeholder()

    def _upload_image(self):
        """File dialog khule image select kore OCR run kore."""
        file_path = filedialog.askopenfilename(
            title="Lab Report Image Select Korun",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.bmp *.tiff *.webp"),
                ("All files", "*.*"),
            ]
        )

        if not file_path:
            return  # user cancel korlechi

        # selected file er naam show koro
        import os
        self.file_label.config(
            text=f"✓  {os.path.basename(file_path)}",
            fg=COLORS["success"]
        )

        # OCR text extract kora hocche
        self.file_label.config(text="⏳ OCR processing...", fg=COLORS["warning"])
        self.frame.update()  # UI update force kora hocche

        extracted = extract_text_from_image(file_path)
        self.extracted_text = extracted

        # text box e show koro
        self.text_input.delete("1.0", tk.END)
        self.text_input.insert("1.0", extracted)

        self.file_label.config(
            text=f"✓  {os.path.basename(file_path)} — OCR done!",
            fg=COLORS["success"]
        )

    def _analyze(self):
        """Text analyze kore results show kore."""
        text = self.text_input.get("1.0", tk.END).strip()
        self.extracted_text = text

        if not text:
            self._clear_results()
            tk.Label(
                self.result_frame,
                text="⚠  Analyze korar jonno text input dite hobe!",
                font=FONTS["body"],
                bg=COLORS["bg_main"],
                fg=COLORS["warning"],
            ).pack(anchor="w", pady=20)
            return

        # lab service call kora hocche
        results = analyze_report_text(text)
        self._clear_results()

        if not results:
            tk.Label(
                self.result_frame,
                text="❓  Kono recognizable lab values pawa jacche na.\n"
                     "Report e glucose, cholesterol, hemoglobin etc. ache kina check korun.",
                font=FONTS["body"],
                bg=COLORS["bg_main"],
                fg=COLORS["text_secondary"],
                wraplength=480,
                justify="left",
            ).pack(anchor="w", pady=20)
            return

        # summary counts
        normal_count  = sum(1 for r in results if r["status"] == "NORMAL")
        high_count    = sum(1 for r in results if r["status"] == "HIGH")
        low_count     = sum(1 for r in results if r["status"] == "LOW")

        # summary bar
        summary = tk.Frame(
            self.result_frame,
            bg=COLORS["accent_dark"],
            padx=18,
            pady=12,
        )
        summary.pack(fill="x", pady=(0, 15))

        for label, count, color in [
            (f"✅  {normal_count} Normal",    normal_count, COLORS["success"]),
            (f"🔺  {high_count} High",        high_count,   COLORS["danger"]),
            (f"🔻  {low_count} Low",          low_count,    COLORS["info"]),
        ]:
            tk.Label(
                summary,
                text=label,
                font=FONTS["body_bold"],
                bg=COLORS["accent_dark"],
                fg=color,
            ).pack(side="left", padx=15)

        # individual result cards
        for result in results:
            self._render_result_row(result)

    def _render_result_row(self, result):
        """Ekটা lab value result row render kore."""
        status = result["status"]
        status_color = get_status_color(status)

        row = tk.Frame(
            self.result_frame,
            bg=COLORS["bg_card"],
            padx=18,
            pady=10,
            highlightthickness=1,
            highlightbackground=status_color,
        )
        row.pack(fill="x", pady=3)

        # left — test name
        tk.Label(
            row,
            text=result["display_name"],
            font=FONTS["body_bold"],
            bg=COLORS["bg_card"],
            fg=COLORS["text_primary"],
            width=22,
            anchor="w",
        ).pack(side="left")

        # value
        tk.Label(
            row,
            text=f"{result['value']} {result['unit']}",
            font=FONTS["body_bold"],
            bg=COLORS["bg_card"],
            fg=status_color,
            width=16,
            anchor="w",
        ).pack(side="left")

        # normal range
        tk.Label(
            row,
            text=f"Normal: {result['normal_range']}",
            font=FONTS["small"],
            bg=COLORS["bg_card"],
            fg=COLORS["text_muted"],
        ).pack(side="left", padx=10)

        # badge — right side
        badge = make_badge(row, status, status)
        badge.pack(side="right")

    def _save(self):
        """Extracted text database e save kore."""
        text = self.text_input.get("1.0", tk.END).strip()
        if not text:
            from tkinter import messagebox
            messagebox.showwarning("Empty", "Save korar jonno kono text nai!")
            return

        result = save_report(self.user["id"], text)
        from tkinter import messagebox
        if result["success"]:
            messagebox.showinfo("Saved", "✓  Report successfully save hoyeche!")
        else:
            messagebox.showerror("Error", result["message"])

    def _show_placeholder(self):
        tk.Label(
            self.result_frame,
            text="👈  Image upload ba text paste kore 'Analyze' korun",
            font=FONTS["body"],
            bg=COLORS["bg_main"],
            fg=COLORS["text_muted"],
        ).pack(expand=True, pady=60)

    def _clear_results(self):
        for w in self.result_frame.winfo_children():
            w.destroy()

    def show(self):
        self.frame.pack(fill="both", expand=True)

    def hide(self):
        self.frame.pack_forget()