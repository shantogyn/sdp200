"""
Image Analyzer Module
Analyzes medical images using simulated OCR
"""

import tkinter as tk
from tkinter import messagebox, filedialog
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ui.theme import COLORS, FONTS, PADDING
from ui.components import CustomButton, InfoBox

class ImageAnalyzerUI:
    """Image Analyzer Feature UI"""
    
    def __init__(self, parent, user_id):
        """Initialize image analyzer UI"""
        self.parent = parent
        self.user_id = user_id
        self.create_ui()
    
    def create_ui(self):
        """Create image analyzer UI"""
        # Title
        title = tk.Label(
            self.parent,
            text="🖼️ Medical Image Analyzer",
            font=FONTS["title_medium"],
            bg=COLORS["light_gray"],
            fg=COLORS["black"]
        )
        title.pack(anchor="w", pady=(0, PADDING["lg"]))
        
        # Main container
        content = tk.Frame(self.parent, bg=COLORS["light_gray"])
        content.pack(fill=tk.BOTH, expand=True)
        
        # Info box
        info_box = tk.Frame(content, bg=COLORS["info"], relief="raised", bd=1)
        info_box.pack(fill=tk.X, padx=0, pady=(0, PADDING["lg"]))
        
        info_text = tk.Label(
            info_box,
            text="⚠️ DISCLAIMER: This is a simulation. For actual medical diagnosis, consult qualified healthcare professionals.",
            font=FONTS["body_medium"],
            bg=COLORS["info"],
            fg=COLORS["white"],
            wraplength=600,
            justify="center",
            padx=PADDING["md"],
            pady=PADDING["md"]
        )
        info_text.pack()
        
        # Left panel - Upload
        left_panel = tk.Frame(content, bg=COLORS["white"], relief="raised", bd=1)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, PADDING["md"]), pady=0)
        
        upload_label = tk.Label(
            left_panel,
            text="Upload Medical Image",
            font=FONTS["heading_2"],
            bg=COLORS["white"],
            fg=COLORS["black"],
            padx=PADDING["md"],
            pady=PADDING["md"]
        )
        upload_label.pack(anchor="w", fill=tk.X)
        
        form_frame = tk.Frame(left_panel, bg=COLORS["white"])
        form_frame.pack(fill=tk.BOTH, expand=True, padx=PADDING["md"], pady=PADDING["md"])
        
        # File selection
        file_frame = tk.Frame(form_frame, bg=COLORS["light_gray"], relief="solid", bd=1, height=100)
        file_frame.pack(fill=tk.BOTH, expand=True, pady=(0, PADDING["lg"]))
        file_frame.pack_propagate(False)
        
        self.file_label = tk.Label(
            file_frame,
            text="📁 Click 'Choose File' to select an image",
            font=FONTS["body_medium"],
            bg=COLORS["light_gray"],
            fg=COLORS["gray"],
            wraplength=300
        )
        self.file_label.pack(expand=True)
        
        # File button
        file_btn = CustomButton(
            form_frame,
            text="📤 Choose File",
            command=self.choose_file,
            padx=20
        )
        file_btn.pack(pady=(0, PADDING["lg"]))
        
        # Image type
        tk.Label(form_frame, text="Image Type", font=FONTS["label"], bg=COLORS["white"]).pack(anchor="w")
        self.image_type = tk.StringVar(value="xray")
        type_menu = tk.OptionMenu(
            form_frame,
            self.image_type,
            "xray",
            "ct_scan",
            "ultrasound",
            "mri",
            "other"
        )
        type_menu.pack(fill=tk.X, pady=(0, PADDING["lg"]))
        
        # Analyze button
        analyze_btn = CustomButton(
            form_frame,
            text="🔍 Analyze Image",
            bg=COLORS["success"],
            command=self.analyze_image
        )
        analyze_btn.pack(fill=tk.X)
        
        # Right panel - Results
        right_panel = tk.Frame(content, bg=COLORS["white"], relief="raised", bd=1)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(PADDING["md"], 0), pady=0)
        
        result_label = tk.Label(
            right_panel,
            text="Analysis Results",
            font=FONTS["heading_2"],
            bg=COLORS["white"],
            fg=COLORS["black"],
            padx=PADDING["md"],
            pady=PADDING["md"]
        )
        result_label.pack(anchor="w", fill=tk.X)
        
        # Results text
        self.result_text = tk.Text(
            right_panel,
            font=FONTS["body_medium"],
            bg=COLORS["light_gray"],
            relief="solid",
            bd=1,
            state="disabled"
        )
        self.result_text.pack(fill=tk.BOTH, expand=True, padx=PADDING["md"], pady=PADDING["md"])
        
        # Show welcome message
        self.show_welcome()
    
    def show_welcome(self):
        """Show welcome message"""
        self.result_text.config(state="normal")
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert("1.0", "Select an image and click 'Analyze Image' to begin.\n\nSupported formats: JPG, PNG\nSupported image types: X-Ray, CT Scan, Ultrasound, MRI")
        self.result_text.config(state="disabled")
    
    def choose_file(self):
        """Choose image file"""
        filename = filedialog.askopenfilename(
            title="Select Medical Image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png"), ("All files", "*.*")]
        )
        
        if filename:
            self.selected_file = filename
            self.file_label.config(text=f"📄 {os.path.basename(filename)}")
        else:
            self.selected_file = None
    
    def analyze_image(self):
        """Simulate image analysis"""
        if not hasattr(self, 'selected_file'):
            messagebox.showerror("Error", "Please select an image first")
            return
        
        image_type = self.image_type.get()
        
        # Simulated analysis results
        results = {
            "xray": """X-RAY ANALYSIS REPORT
            
Image Quality: Good
Resolution: 512x512 pixels
Analyzed at: 2024-04-29 14:30:00

KEY FINDINGS:
✓ Heart size: Normal
✓ Lungs: Clear, no consolidation
✓ Diaphragm: Normal contour
✓ Mediastinum: No widening
✓ Ribs: Intact without fractures

OBSERVATIONS:
• Minimal peribronchial markings
• No pleural effusion detected
• Overall impression: Within normal limits

RECOMMENDATION:
No acute abnormality detected. Follow-up imaging not indicated unless clinically indicated.""",
            
            "ct_scan": """CT SCAN ANALYSIS REPORT

Image Quality: Excellent
Slice Thickness: 5mm
Analyzed at: 2024-04-29 14:30:00

KEY FINDINGS:
✓ Brain parenchyma: Symmetrical
✓ Ventricles: Normal size and configuration
✓ No mass effect or midline shift
✓ Cerebellum: Normal
✓ Brainstem: Intact

OBSERVATIONS:
• No acute intracranial pathology
• Cortical sulci: Prominent
• White matter: No abnormal attenuation
• Bone windows: No fractures

RECOMMENDATION:
No acute intracranial abnormality. Clinical correlation recommended.""",
            
            "ultrasound": """ULTRASOUND ANALYSIS REPORT

Image Quality: Good
Frequency: 3.5 MHz probe
Analyzed at: 2024-04-29 14:30:00

KEY FINDINGS:
✓ Organ dimensions: Within normal limits
✓ Echotexture: Homogeneous
✓ No focal lesions or masses
✓ Vascularity: Normal
✓ No free fluid

OBSERVATIONS:
• Smooth borders and margins
• Normal echogenicity
• No shadowing artifacts
• Clear visualization of anatomical structures

RECOMMENDATION:
No sonographic evidence of abnormality.""",
            
            "mri": """MRI ANALYSIS REPORT

Image Quality: Excellent
Field Strength: 1.5 Tesla
Analyzed at: 2024-04-29 14:30:00

KEY FINDINGS:
✓ T1 sequences: Normal signal intensity
✓ T2 sequences: No abnormal hyperintensities
✓ FLAIR: No focal lesions
✓ No restricted diffusion
✓ Normal enhancement pattern

OBSERVATIONS:
• Bilateral symmetry maintained
• Normal gray-white matter differentiation
• No mass effect
• Vessels: Normal flow voids

RECOMMENDATION:
No acute MRI findings. Clinical correlation advised.""",
            
            "other": """IMAGE ANALYSIS REPORT

Image Type: Other
Analyzed at: 2024-04-29 14:30:00

KEY FINDINGS:
✓ Image processing completed successfully
✓ No obvious abnormalities detected
✓ Image quality: Acceptable
✓ Analysis parameters: Standard

OBSERVATIONS:
• General analysis completed
• Image suitable for further evaluation
• No critical findings

RECOMMENDATION:
For detailed analysis, please consult with a radiologist or medical professional.""",
        }
        
        # Display results
        self.result_text.config(state="normal")
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert("1.0", results.get(image_type, "Analysis complete"))
        self.result_text.config(state="disabled")
        
        messagebox.showinfo("Success", "Image analysis complete. Review results on the right.")
