"""
UI Components Module
Reusable UI components for the application
"""

import tkinter as tk
from tkinter import ttk
from ui.theme import COLORS, FONTS, PADDING

class CustomButton(tk.Button):
    """Custom button with consistent styling"""
    
    def __init__(self, parent, text="", bg=COLORS["primary"], fg=COLORS["white"], 
                 command=None, style="primary", **kwargs):
        """
        Initialize custom button
        Args:
            parent: Parent widget
            text: Button text
            bg: Background color
            fg: Text color
            command: Command to execute
            style: Button style (primary, success, danger, secondary)
            **kwargs: Additional keyword arguments
        """
        super().__init__(
            parent,
            text=text,
            bg=bg,
            fg=fg,
            command=command,
            font=FONTS["button"],
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=8,
            **kwargs
        )
        self.config(activebackground=bg, activeforeground=fg)

class CustomEntry(tk.Entry):
    """Custom entry field with consistent styling"""
    
    def __init__(self, parent, placeholder="", **kwargs):
        """
        Initialize custom entry
        Args:
            parent: Parent widget
            placeholder: Placeholder text
            **kwargs: Additional keyword arguments
        """
        super().__init__(
            parent,
            font=FONTS["input"],
            relief="flat",
            bg=COLORS["white"],
            fg=COLORS["black"],
            insertbackground=COLORS["primary"],
            **kwargs
        )
        
        self.placeholder = placeholder
        self.placeholder_color = COLORS["gray"]
        self.default_color = COLORS["black"]
        
        if placeholder:
            self.insert(0, placeholder)
            self.config(fg=self.placeholder_color)
            self.bind("<FocusIn>", self.on_focus_in)
            self.bind("<FocusOut>", self.on_focus_out)
    
    def on_focus_in(self, event):
        """Handle focus in event"""
        if self.get() == self.placeholder:
            self.delete(0, tk.END)
            self.config(fg=self.default_color)
    
    def on_focus_out(self, event):
        """Handle focus out event"""
        if not self.get():
            self.insert(0, self.placeholder)
            self.config(fg=self.placeholder_color)
    
    def get_value(self):
        """Get entry value (excluding placeholder)"""
        value = self.get()
        if value == self.placeholder:
            return ""
        return value

class CustomLabel(tk.Label):
    """Custom label with consistent styling"""
    
    def __init__(self, parent, text="", **kwargs):
        """
        Initialize custom label
        Args:
            parent: Parent widget
            text: Label text
            **kwargs: Additional keyword arguments
        """
        super().__init__(
            parent,
            text=text,
            font=FONTS["body_medium"],
            bg=COLORS["light_gray"],
            fg=COLORS["black"],
            **kwargs
        )

class CardFrame(tk.Frame):
    """Card frame with shadow effect"""
    
    def __init__(self, parent, title="", **kwargs):
        """
        Initialize card frame
        Args:
            parent: Parent widget
            title: Card title
            **kwargs: Additional keyword arguments
        """
        super().__init__(
            parent,
            bg=COLORS["card_bg"],
            relief="raised",
            bd=1,
            **kwargs
        )
        
        if title:
            title_label = tk.Label(
                self,
                text=title,
                font=FONTS["heading_2"],
                bg=COLORS["card_bg"],
                fg=COLORS["black"],
                padx=PADDING["md"],
                pady=PADDING["sm"]
            )
            title_label.pack(fill=tk.X, pady=(5, 10), padx=5)

class SectionFrame(tk.Frame):
    """Frame for grouping related components"""
    
    def __init__(self, parent, title="", **kwargs):
        """
        Initialize section frame
        Args:
            parent: Parent widget
            title: Section title
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent, bg=COLORS["light_gray"], **kwargs)
        
        if title:
            title_label = tk.Label(
                self,
                text=title,
                font=FONTS["heading_1"],
                bg=COLORS["light_gray"],
                fg=COLORS["black"],
                padx=PADDING["md"],
                pady=PADDING["sm"]
            )
            title_label.pack(fill=tk.X, pady=(0, 10))
        
        self.content_frame = tk.Frame(self, bg=COLORS["light_gray"])
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=PADDING["md"], 
                               pady=PADDING["md"])
    
    def get_content_frame(self):
        """Get the content frame for adding widgets"""
        return self.content_frame

class ScrollableFrame(tk.Frame):
    """Scrollable frame with canvas"""
    
    def __init__(self, parent, **kwargs):
        """
        Initialize scrollable frame
        Args:
            parent: Parent widget
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent, bg=COLORS["light_gray"], **kwargs)
        
        # Create canvas
        self.canvas = tk.Canvas(
            self,
            bg=COLORS["light_gray"],
            highlightthickness=0
        )
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=COLORS["light_gray"])
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # Bind mousewheel
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind_all("<Button-4>", self._on_mousewheel)
        self.canvas.bind_all("<Button-5>", self._on_mousewheel)
    
    def _on_mousewheel(self, event):
        """Handle mousewheel scrolling"""
        if event.num == 5 or event.delta < 0:
            self.canvas.yview_scroll(1, "units")
        elif event.num == 4 or event.delta > 0:
            self.canvas.yview_scroll(-1, "units")
    
    def get_frame(self):
        """Get the scrollable content frame"""
        return self.scrollable_frame

class FeatureCard(tk.Frame):
    """Card for displaying features"""
    
    def __init__(self, parent, title="", icon="", description="", command=None, **kwargs):
        """
        Initialize feature card
        Args:
            parent: Parent widget
            title: Card title
            icon: Icon/emoji
            description: Card description
            command: Command to execute on click
            **kwargs: Additional keyword arguments
        """
        super().__init__(
            parent,
            bg=COLORS["card_bg"],
            relief="raised",
            bd=1,
            **kwargs
        )
        
        # Icon
        if icon:
            icon_label = tk.Label(
                self,
                text=icon,
                font=("Arial", 32),
                bg=COLORS["card_bg"],
                fg=COLORS["primary"]
            )
            icon_label.pack(pady=(10, 5))
        
        # Title
        title_label = tk.Label(
            self,
            text=title,
            font=FONTS["heading_2"],
            bg=COLORS["card_bg"],
            fg=COLORS["black"],
            wraplength=150
        )
        title_label.pack(pady=(5, 10), padx=10)
        
        # Description
        if description:
            desc_label = tk.Label(
                self,
                text=description,
                font=FONTS["body_small"],
                bg=COLORS["card_bg"],
                fg=COLORS["gray"],
                wraplength=150,
                justify="center"
            )
            desc_label.pack(pady=(0, 10), padx=10)
        
        # Click command
        if command:
            for widget in self.winfo_children():
                widget.bind("<Button-1>", lambda e: command())
            self.bind("<Button-1>", lambda e: command())
            self.config(cursor="hand2")

class InfoBox(tk.Frame):
    """Information display box"""
    
    def __init__(self, parent, title="", message="", info_type="info", **kwargs):
        """
        Initialize info box
        Args:
            parent: Parent widget
            title: Box title
            message: Message text
            info_type: Type (info, success, warning, danger)
            **kwargs: Additional keyword arguments
        """
        colors = {
            "info": COLORS["info"],
            "success": COLORS["success"],
            "warning": COLORS["warning"],
            "danger": COLORS["danger"],
        }
        
        bg_color = colors.get(info_type, COLORS["info"])
        
        super().__init__(parent, bg=bg_color, **kwargs)
        
        if title:
            title_label = tk.Label(
                self,
                text=title,
                font=FONTS["heading_2"],
                bg=bg_color,
                fg=COLORS["white"],
                padx=PADDING["md"],
                pady=PADDING["sm"]
            )
            title_label.pack(anchor="w")
        
        if message:
            msg_label = tk.Label(
                self,
                text=message,
                font=FONTS["body_medium"],
                bg=bg_color,
                fg=COLORS["white"],
                wraplength=400,
                justify="left",
                padx=PADDING["md"],
                pady=PADDING["md"]
            )
            msg_label.pack(anchor="w")

class ProgressBar(tk.Frame):
    """Custom progress bar"""
    
    def __init__(self, parent, max_value=100, **kwargs):
        """
        Initialize progress bar
        Args:
            parent: Parent widget
            max_value: Maximum value
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent, bg=COLORS["light_gray"], height=20, **kwargs)
        
        self.max_value = max_value
        self.current_value = 0
        
        # Background bar
        self.bg_bar = tk.Frame(
            self,
            bg=COLORS["gray"],
            height=20,
            relief="flat"
        )
        self.bg_bar.pack(fill=tk.X, padx=1, pady=1)
        
        # Progress bar
        self.progress_bar = tk.Frame(
            self.bg_bar,
            bg=COLORS["primary"],
            height=20
        )
        self.progress_bar.pack(side="left", fill=tk.Y)
    
    def set_progress(self, value):
        """Set progress value"""
        self.current_value = min(value, self.max_value)
        percentage = (self.current_value / self.max_value) * 100
        self.progress_bar.config(width=int(percentage))
        self.update()
