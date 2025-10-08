"""
style.py - Premium Aesthetic Styling for Tkinter GUI
Modern gradient design with beautiful animations - FONTS FIXED
"""

import tkinter as tk
from tkinter import ttk

class ModernStyle:
    def __init__(self):
        self.colors = {
            # Modern gradient color palette
            'primary': '#2c3e50',
            'primary_light': '#34495e',
            'secondary': '#3498db',
            'secondary_light': '#5dade2',
            'success': '#27ae60',
            'success_light': '#58d68d',
            'warning': '#f39c12',
            'warning_light': '#f8c471',
            'danger': '#e74c3c',
            'danger_light': '#ec7063',
            'accent': '#9b59b6',
            'accent_light': '#bb8fce',
            'dark': '#2c3e50',
            'light': '#ecf0f1',
            'white': '#ffffff',
            'gray': '#bdc3c7',
            'background': '#f8f9fa',
            'card_bg': '#ffffff'
        }

def apply_style(root):
    """Apply premium aesthetic styling to Tkinter app - FONTS REMOVED"""
    style = ttk.Style(root)
    modern = ModernStyle()
    
    # Configure root window with gradient background
    root.configure(bg=modern.colors['background'])
    # REMOVED: root.option_add('*Font', 'Segoe UI 10') - This was causing the error
    
    # Use clam theme for better customization
    style.theme_use("clam")
    
    # 🎨 CONFIGURE ALL STYLES - NO FONTS
    
    # Base configuration
    style.configure(".",
                   background=modern.colors['background'],
                   foreground=modern.colors['dark'],
                   borderwidth=0,
                   focuscolor=modern.colors['secondary'] + '30')
    
    # 🏷 Premium Label Styling - NO FONTS
    style.configure("TLabel",
                   background=modern.colors['background'],
                   foreground=modern.colors['primary'],
                   padding=8)
    
    style.configure("Title.TLabel",
                   foreground=modern.colors['primary'],
                   background=modern.colors['background'])
    
    style.configure("Subtitle.TLabel",
                   foreground=modern.colors['primary_light'],
                   background=modern.colors['background'])
    
    # 🔘 Premium Button Styling - NO FONTS
    style.configure("Primary.TButton",
                   background=modern.colors['secondary'],
                   foreground=modern.colors['white'],
                   borderwidth=0,
                   focuscolor="",
                   padding=(20, 12),
                   relief="flat")
    
    style.configure("Success.TButton",
                   background=modern.colors['success'],
                   foreground=modern.colors['white'],
                   borderwidth=0,
                   padding=(20, 12),
                   relief="flat")
    
    style.configure("Danger.TButton",
                   background=modern.colors['danger'],
                   foreground=modern.colors['white'],
                   borderwidth=0,
                   padding=(20, 12),
                   relief="flat")
    
    style.configure("Accent.TButton",
                   background=modern.colors['accent'],
                   foreground=modern.colors['white'],
                   borderwidth=0,
                   padding=(20, 12),
                   relief="flat")
    
    # Button hover effects
    style.map("Primary.TButton",
             background=[("active", modern.colors['secondary_light']),
                        ("pressed", modern.colors['primary'])])
    
    style.map("Success.TButton",
             background=[("active", modern.colors['success_light']),
                        ("pressed", modern.colors['success'])])
    
    style.map("Danger.TButton",
             background=[("active", modern.colors['danger_light']),
                        ("pressed", modern.colors['danger'])])
    
    style.map("Accent.TButton",
             background=[("active", modern.colors['accent_light']),
                        ("pressed", modern.colors['accent'])])
    
    # 🧾 Premium Entry Styling - NO FONTS
    style.configure("TEntry",
                   fieldbackground=modern.colors['white'],
                   foreground=modern.colors['dark'],
                   borderwidth=2,
                   relief="flat",
                   padding=10,
                   insertcolor=modern.colors['secondary'])
    
    style.map("TEntry",
             fieldbackground=[("focus", modern.colors['white']),
                            ("!focus", modern.colors['white'])],
             bordercolor=[("focus", modern.colors['secondary']),
                         ("!focus", modern.colors['gray'])])
    
    # 📋 Premium Combobox Styling - NO FONTS
    style.configure("TCombobox",
                   fieldbackground=modern.colors['white'],
                   background=modern.colors['white'],
                   foreground=modern.colors['dark'],
                   borderwidth=2,
                   relief="flat",
                   padding=10,
                   arrowsize=14)
    
    style.map("TCombobox",
             fieldbackground=[("focus", modern.colors['white']),
                            ("!focus", modern.colors['white'])],
             background=[("readonly", modern.colors['white'])],
             bordercolor=[("focus", modern.colors['secondary']),
                         ("!focus", modern.colors['gray'])])
    
    # 🧩 Premium Frame Styling
    style.configure("TFrame",
                   background=modern.colors['background'],
                   relief="flat",
                   borderwidth=0)
    
    style.configure("Card.TFrame",
                   background=modern.colors['card_bg'],
                   relief="flat",
                   borderwidth=1)
    
    # 📊 Premium Treeview Styling - NO FONTS
    style.configure("Treeview",
                   background=modern.colors['white'],
                   foreground=modern.colors['dark'],
                   rowheight=32,
                   fieldbackground=modern.colors['white'],
                   borderwidth=0)
    
    style.configure("Treeview.Heading",
                   background=modern.colors['primary'],
                   foreground=modern.colors['white'],
                   relief="flat",
                   borderwidth=0,
                   padding=12)
    
    style.map("Treeview",
             background=[("selected", modern.colors['secondary'] + '40')],
             foreground=[("selected", modern.colors['dark'])])
    
    style.map("Treeview.Heading",
             background=[("active", modern.colors['primary_light'])])
    
    # 📏 Scrollbar Styling
    style.configure("TScrollbar",
                   background=modern.colors['gray'],
                   darkcolor=modern.colors['gray'],
                   lightcolor=modern.colors['gray'],
                   troughcolor=modern.colors['light'],
                   bordercolor=modern.colors['light'],
                   arrowcolor=modern.colors['dark'],
                   relief="flat")
    
    # 🌟 Window title with emoji
    root.title("Vehicle Violation Management System")
    
    return modern

def add_hover_effects(widget, hover_bg="#2980b9", normal_bg="#3498db"):
    """Enhanced hover animation to buttons"""
    def on_enter(event):
        try:
            widget.configure(background=hover_bg)
            # Add subtle scale effect
            widget.configure(relief="raised")
        except Exception:
            pass
    
    def on_leave(event):
        try:
            widget.configure(background=normal_bg)
            widget.configure(relief="flat")
        except Exception:
            pass
    
    widget.bind("<Enter>", on_enter)
    widget.bind("<Leave>", on_leave)

def create_modern_button(parent, text, style_type="Primary.TButton", command=None):
    """Create a modern button with premium styling"""
    return ttk.Button(parent, text=text, style=style_type, command=command)

def create_card_frame(parent, **kwargs):
    """Create a modern card-style frame"""
    return ttk.Frame(parent, style="Card.TFrame", **kwargs)

# For backward compatibility
def apply_premium_style(root):
    """Alias for apply_style"""
    return apply_style(root)

# 🎯 Quick styling utilities - NO FONTS
def style_as_title(label):
    """Style a label as title"""
    label.configure(foreground="#2c3e50", background="#f8f9fa")

def style_as_subtitle(label):
    """Style a label as subtitle"""
    label.configure(foreground="#34495e", background="#f8f9fa")

def style_as_success(label):
    """Style a label with success color"""
    label.configure(foreground="#27ae60")

def style_as_danger(label):
    """Style a label with danger color"""
    label.configure(foreground="#e74c3c")

def style_as_warning(label):
    """Style a label with warning color"""
    label.configure(foreground="#f39c12")