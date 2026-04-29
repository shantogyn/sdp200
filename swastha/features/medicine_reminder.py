"""
Medicine Reminder Module
Tracks and reminds users about their medicines
"""

import tkinter as tk
from tkinter import messagebox
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ui.theme import COLORS, FONTS, PADDING
from ui.components import CustomButton, CustomEntry, CardFrame
from db.db_connection import db

class MedicineReminderUI:
    """Medicine Reminder Feature UI"""
    
    def __init__(self, parent, user_id):
        """Initialize medicine reminder UI"""
        self.parent = parent
        self.user_id = user_id
        self.medicines_list = []
        self.create_ui()
        self.load_medicines()
    
    def create_ui(self):
        """Create medicine reminder UI"""
        # Title
        title = tk.Label(
            self.parent,
            text="💊 Medicine Reminder",
            font=FONTS["title_medium"],
            bg=COLORS["light_gray"],
            fg=COLORS["black"]
        )
        title.pack(anchor="w", pady=(0, PADDING["lg"]))
        
        # Main container
        content = tk.Frame(self.parent, bg=COLORS["light_gray"])
        content.pack(fill=tk.BOTH, expand=True)
        
        # Left panel - Add medicine
        left_panel = tk.Frame(content, bg=COLORS["white"], relief="raised", bd=1)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, PADDING["md"]), pady=0)
        
        add_label = tk.Label(
            left_panel,
            text="Add New Medicine",
            font=FONTS["heading_2"],
            bg=COLORS["white"],
            fg=COLORS["black"],
            padx=PADDING["md"],
            pady=PADDING["md"]
        )
        add_label.pack(anchor="w", fill=tk.X)
        
        form_frame = tk.Frame(left_panel, bg=COLORS["white"])
        form_frame.pack(fill=tk.BOTH, expand=True, padx=PADDING["md"], pady=PADDING["md"])
        
        # Medicine name
        tk.Label(form_frame, text="Medicine Name", font=FONTS["label"], bg=COLORS["white"]).pack(anchor="w")
        self.medicine_name = tk.Entry(form_frame, font=FONTS["body_medium"], relief="solid", bd=1)
        self.medicine_name.pack(fill=tk.X, pady=(0, PADDING["md"]))
        
        # Dosage
        tk.Label(form_frame, text="Dosage", font=FONTS["label"], bg=COLORS["white"]).pack(anchor="w")
        self.dosage = tk.Entry(form_frame, font=FONTS["body_medium"], relief="solid", bd=1)
        self.dosage.pack(fill=tk.X, pady=(0, PADDING["md"]))
        
        # Times
        tk.Label(form_frame, text="Times (comma-separated, e.g., 8:00, 14:00, 20:00)", font=FONTS["label"], bg=COLORS["white"]).pack(anchor="w")
        self.medicine_times = tk.Entry(form_frame, font=FONTS["body_medium"], relief="solid", bd=1)
        self.medicine_times.pack(fill=tk.X, pady=(0, PADDING["md"]))
        
        # Notes
        tk.Label(form_frame, text="Notes", font=FONTS["label"], bg=COLORS["white"]).pack(anchor="w")
        self.medicine_notes = tk.Entry(form_frame, font=FONTS["body_medium"], relief="solid", bd=1)
        self.medicine_notes.pack(fill=tk.X, pady=(0, PADDING["lg"]))
        
        # Add button
        add_btn = CustomButton(
            form_frame,
            text="Add Medicine",
            bg=COLORS["success"],
            command=self.add_medicine
        )
        add_btn.pack(fill=tk.X)
        
        # Right panel - Medicines list
        right_panel = tk.Frame(content, bg=COLORS["white"], relief="raised", bd=1)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(PADDING["md"], 0), pady=0)
        
        list_label = tk.Label(
            right_panel,
            text="Your Medicines",
            font=FONTS["heading_2"],
            bg=COLORS["white"],
            fg=COLORS["black"],
            padx=PADDING["md"],
            pady=PADDING["md"]
        )
        list_label.pack(anchor="w", fill=tk.X)
        
        # Medicines listbox
        list_frame = tk.Frame(right_panel, bg=COLORS["white"])
        list_frame.pack(fill=tk.BOTH, expand=True, padx=PADDING["md"], pady=PADDING["md"])
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.medicines_listbox = tk.Listbox(
            list_frame,
            font=FONTS["body_medium"],
            bg=COLORS["light_gray"],
            fg=COLORS["black"],
            yscrollcommand=scrollbar.set,
            height=12
        )
        self.medicines_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.medicines_listbox.bind("<<ListboxSelect>>", lambda _: self.show_selected_medicine_details())
        scrollbar.config(command=self.medicines_listbox.yview)
        
        # Delete button
        delete_btn = CustomButton(
            right_panel,
            text="Delete Selected",
            bg=COLORS["danger"],
            command=self.delete_medicine,
            padx=20
        )
        delete_btn.pack(padx=PADDING["md"], pady=(0, PADDING["sm"]), fill=tk.X)

        # View details button
        view_btn = CustomButton(
            right_panel,
            text="View Details",
            bg=COLORS["info"],
            command=self.view_medicine_details,
            padx=20
        )
        view_btn.pack(padx=PADDING["md"], pady=(0, PADDING["sm"]), fill=tk.X)

        # Details label
        self.details_text = tk.Label(
            right_panel,
            text="Select a medicine to see details.",
            font=FONTS["body_small"],
            bg=COLORS["white"],
            fg=COLORS["dark_gray"],
            justify="left",
            wraplength=260,
            anchor="nw"
        )
        self.details_text.pack(fill=tk.BOTH, expand=True, padx=PADDING["md"], pady=(0, PADDING["md"]))
    
    def add_medicine(self):
        """Add new medicine"""
        name = self.medicine_name.get().strip()
        dosage = self.dosage.get().strip()
        times = self.medicine_times.get().strip()
        notes = self.medicine_notes.get().strip()
        
        if not name:
            messagebox.showerror("Error", "Please enter medicine name")
            return
        
        if not times:
            messagebox.showerror("Error", "Please enter medicine times")
            return
        
        if not db.is_connected():
            db.connect()
        
        query = "INSERT INTO medicines (user_id, medicine_name, dosage, time_hours, notes) VALUES (%s, %s, %s, %s, %s)"
        
        if db.execute_update(query, (self.user_id, name, dosage, times, notes)):
            messagebox.showinfo("Success", "Medicine added successfully!")
            self.medicine_name.delete(0, tk.END)
            self.dosage.delete(0, tk.END)
            self.medicine_times.delete(0, tk.END)
            self.medicine_notes.delete(0, tk.END)
            self.load_medicines()
        else:
            messagebox.showerror("Error", "Failed to add medicine")
    
    def load_medicines(self):
        """Load medicines from database"""
        if not db.is_connected():
            db.connect()
        
        query = "SELECT id, medicine_name, dosage, time_hours, notes FROM medicines WHERE user_id = %s"
        results = db.execute_query(query, (self.user_id,))
        
        self.medicines_listbox.delete(0, tk.END)
        self.medicines_list = results if results else []
        self.details_text.config(text="Select a medicine to see details.")
        
        for medicine in self.medicines_list:
            display_text = f"{medicine['medicine_name']} - {medicine['dosage']} ({medicine['time_hours']})"
            self.medicines_listbox.insert(tk.END, display_text)
    
    def delete_medicine(self):
        """Delete selected medicine"""
        selection = self.medicines_listbox.curselection()
        
        if not selection:
            messagebox.showerror("Error", "Please select a medicine to delete")
            return
        
        medicine = self.medicines_list[selection[0]]
        
        if messagebox.askyesno("Confirm", f"Delete {medicine['medicine_name']}?"):
            if not db.is_connected():
                db.connect()
            
            query = "DELETE FROM medicines WHERE id = %s"
            if db.execute_update(query, (medicine['id'],)):
                messagebox.showinfo("Success", "Medicine deleted")
                self.load_medicines()

    def show_selected_medicine_details(self):
        """Show selected medicine details"""
        selection = self.medicines_listbox.curselection()
        if not selection:
            return
        medicine = self.medicines_list[selection[0]]
        notes = medicine.get('notes', '') or 'No notes provided.'
        details = (
            f"Medicine: {medicine['medicine_name']}\n"
            f"Dosage: {medicine['dosage']}\n"
            f"Times: {medicine['time_hours']}\n"
            f"Notes: {notes}"
        )
        self.details_text.config(text=details)

    def view_medicine_details(self):
        """View details for selected medicine"""
        selection = self.medicines_listbox.curselection()
        if not selection:
            messagebox.showerror("Error", "Please select a medicine to view details")
            return
        medicine = self.medicines_list[selection[0]]
        notes = medicine.get('notes', '') or 'No notes provided.'
        messagebox.showinfo(
            "Medicine Details",
            (
                f"Medicine: {medicine['medicine_name']}\n"
                f"Dosage: {medicine['dosage']}\n"
                f"Times: {medicine['time_hours']}\n"
                f"Notes: {notes}"
            )
        )
