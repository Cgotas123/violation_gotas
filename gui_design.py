"""
gui_design.py - GUI Design Components
Contains all design elements, colors, and reusable widgets
"""

import tkinter as tk
from tkinter import ttk

class DesignConfig:
    """Design configuration and color scheme"""
    
    # Color Palette
    BG_PRIMARY = "#1a1a2e"      # Dark navy blue
    BG_SECONDARY = "#16213e"    # Slightly lighter navy
    ACCENT = "#0f3460"          # Deep blue
    HIGHLIGHT = "#e94560"       # Red accent
    SUCCESS = "#2d4a2b"         # Dark green
    DANGER = "#8B0000"          # Dark red
    TEXT_COLOR = "#eaeaea"      # Light gray
    TEXT_SECONDARY = "#a0a0a0"  # Medium gray
    
    # Fonts
    FONT_TITLE = ("Arial", 24, "bold")
    FONT_HEADING = ("Arial", 16, "bold")
    FONT_SUBHEADING = ("Arial", 14, "bold")
    FONT_NORMAL = ("Arial", 10)
    FONT_BUTTON = ("Arial", 11, "bold")
    FONT_SMALL = ("Arial", 9)
    
    # Spacing
    PADDING_LARGE = 20
    PADDING_MEDIUM = 10
    PADDING_SMALL = 5


class StyledButton(tk.Button):
    """Custom styled button"""
    
    def __init__(self, parent, text, command=None, bg_color=DesignConfig.HIGHLIGHT, 
                 width=15, **kwargs):
        super().__init__(
            parent,
            text=text,
            command=command,
            bg=bg_color,
            fg="white",
            font=DesignConfig.FONT_BUTTON,
            width=width,
            cursor="hand2",
            relief=tk.FLAT,
            activebackground=self._darken_color(bg_color),
            activeforeground="white",
            **kwargs
        )
        
        # Hover effects
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.default_bg = bg_color
    
    def _on_enter(self, e):
        self['background'] = self._darken_color(self.default_bg)
    
    def _on_leave(self, e):
        self['background'] = self.default_bg
    
    @staticmethod
    def _darken_color(hex_color):
        """Darken a hex color by 20%"""
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        darkened = tuple(int(c * 0.8) for c in rgb)
        return '#{:02x}{:02x}{:02x}'.format(*darkened)


class StyledLabel(tk.Label):
    """Custom styled label"""
    
    def __init__(self, parent, text, font=DesignConfig.FONT_NORMAL, 
                 fg=DesignConfig.TEXT_COLOR, **kwargs):
        super().__init__(
            parent,
            text=text,
            font=font,
            fg=fg,
            bg=DesignConfig.BG_SECONDARY,
            **kwargs
        )


class StyledEntry(tk.Entry):
    """Custom styled entry field"""
    
    def __init__(self, parent, width=25, **kwargs):
        super().__init__(
            parent,
            width=width,
            font=DesignConfig.FONT_NORMAL,
            relief=tk.FLAT,
            bd=2,
            highlightthickness=1,
            highlightbackground=DesignConfig.ACCENT,
            highlightcolor=DesignConfig.HIGHLIGHT,
            **kwargs
        )


class StyledFrame(tk.Frame):
    """Custom styled frame with rounded appearance"""
    
    def __init__(self, parent, bg=DesignConfig.BG_SECONDARY, **kwargs):
        super().__init__(
            parent,
            bg=bg,
            relief=tk.RAISED,
            bd=2,
            **kwargs
        )


class TitleLabel(tk.Label):
    """Title label for sections"""
    
    def __init__(self, parent, text, icon="", **kwargs):
        display_text = f"{icon} {text}" if icon else text
        super().__init__(
            parent,
            text=display_text,
            font=DesignConfig.FONT_HEADING,
            bg=DesignConfig.BG_SECONDARY,
            fg=DesignConfig.TEXT_COLOR,
            **kwargs
        )


class FormField:
    """Reusable form field with label and input"""
    
    def __init__(self, parent, label_text, row, column=0, field_type="entry", 
                 values=None, width=25):
        self.label = StyledLabel(parent, label_text + ":")
        self.label.grid(row=row, column=column, sticky=tk.W, 
                       pady=DesignConfig.PADDING_SMALL)
        
        if field_type == "entry":
            self.widget = StyledEntry(parent, width=width)
        elif field_type == "combobox":
            self.widget = ttk.Combobox(parent, width=width-2, 
                                      font=DesignConfig.FONT_NORMAL,
                                      state="readonly")
            if values:
                self.widget['values'] = values
                self.widget.current(0)
        elif field_type == "text":
            self.widget = tk.Text(parent, width=width, height=4, 
                                 font=DesignConfig.FONT_SMALL,
                                 relief=tk.FLAT, bd=2)
        
        self.widget.grid(row=row, column=column+1, 
                        pady=DesignConfig.PADDING_SMALL, 
                        padx=DesignConfig.PADDING_SMALL)
    
    def get(self):
        """Get value from widget"""
        if isinstance(self.widget, tk.Text):
            return self.widget.get("1.0", tk.END).strip()
        return self.widget.get()
    
    def set(self, value):
        """Set value to widget"""
        if isinstance(self.widget, tk.Text):
            self.widget.delete("1.0", tk.END)
            self.widget.insert("1.0", value)
        elif isinstance(self.widget, ttk.Combobox):
            self.widget.set(value)
        else:
            self.widget.delete(0, tk.END)
            self.widget.insert(0, value)
    
    def clear(self):
        """Clear widget value"""
        if isinstance(self.widget, tk.Text):
            self.widget.delete("1.0", tk.END)
        else:
            self.widget.delete(0, tk.END)


class SearchBar:
    """Search bar component"""
    
    def __init__(self, parent, search_callback):
        self.frame = StyledFrame(parent)
        
        StyledLabel(self.frame, "🔍 Search:", 
                   font=DesignConfig.FONT_NORMAL).pack(side=tk.LEFT, 
                                                       padx=DesignConfig.PADDING_SMALL)
        
        self.entry = StyledEntry(self.frame, width=30)
        self.entry.pack(side=tk.LEFT, padx=DesignConfig.PADDING_SMALL)
        self.entry.bind('<KeyRelease>', lambda e: search_callback())
        
        self.search_btn = StyledButton(
            self.frame,
            text="Search",
            command=search_callback,
            bg_color=DesignConfig.ACCENT,
            width=10
        )
        self.search_btn.pack(side=tk.LEFT, padx=DesignConfig.PADDING_SMALL)
    
    def get(self):
        return self.entry.get().strip()
    
    def clear(self):
        self.entry.delete(0, tk.END)


class StyledTreeview:
    """Styled treeview with scrollbars"""
    
    def __init__(self, parent, columns, headings, column_widths):
        self.frame = StyledFrame(parent)
        
        # Create scrollbars
        vsb = ttk.Scrollbar(self.frame, orient="vertical")
        hsb = ttk.Scrollbar(self.frame, orient="horizontal")
        
        # Create treeview
        self.tree = ttk.Treeview(
            self.frame,
            columns=columns,
            show="headings",
            yscrollcommand=vsb.set,
            xscrollcommand=hsb.set,
            height=15
        )
        
        vsb.config(command=self.tree.yview)
        hsb.config(command=self.tree.xview)
        
        # Configure columns
        for col, heading, width in zip(columns, headings, column_widths):
            self.tree.heading(col, text=heading)
            self.tree.column(col, width=width, anchor=tk.CENTER)
        
        # Configure styles
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
                       background=DesignConfig.BG_SECONDARY,
                       foreground=DesignConfig.TEXT_COLOR,
                       fieldbackground=DesignConfig.BG_SECONDARY,
                       borderwidth=0)
        style.configure("Treeview.Heading",
                       background=DesignConfig.ACCENT,
                       foreground=DesignConfig.TEXT_COLOR,
                       borderwidth=1)
        style.map('Treeview',
                 background=[('selected', DesignConfig.HIGHLIGHT)])
        
        # Pack elements
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        hsb.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.pack(fill=tk.BOTH, expand=True)
    
    def insert(self, values):
        """Insert row into treeview"""
        return self.tree.insert('', tk.END, values=values)
    
    def clear(self):
        """Clear all items"""
        for item in self.tree.get_children():
            self.tree.delete(item)
    
    def get_selected(self):
        """Get selected item"""
        selected = self.tree.selection()
        if selected:
            return self.tree.item(selected[0])
        return None
    
    def bind(self, event, callback):
        """Bind event to treeview"""
        self.tree.bind(event, callback)


class StatusBar(tk.Label):
    """Status bar at bottom of window"""
    
    def __init__(self, parent):
        super().__init__(
            parent,
            text="Ready",
            bg=DesignConfig.BG_PRIMARY,
            fg=DesignConfig.TEXT_SECONDARY,
            font=DesignConfig.FONT_SMALL,
            anchor=tk.W,
            relief=tk.SUNKEN,
            bd=1
        )
    
    def set_status(self, message, status_type="info"):
        """Set status message with type (info, success, error)"""
        colors = {
            "info": DesignConfig.TEXT_SECONDARY,
            "success": "#4CAF50",
            "error": DesignConfig.HIGHLIGHT
        }
        self.config(text=message, fg=colors.get(status_type, DesignConfig.TEXT_SECONDARY))


class DialogBox:
    """Custom dialog boxes"""
    
    @staticmethod
    def show_info(title, message):
        """Show info dialog"""
        from tkinter import messagebox
        messagebox.showinfo(title, message)
    
    @staticmethod
    def show_success(message):
        """Show success dialog"""
        from tkinter import messagebox
        messagebox.showinfo("✓ Success", message)
    
    @staticmethod
    def show_error(message):
        """Show error dialog"""
        from tkinter import messagebox
        messagebox.showerror("✗ Error", message)
    
    @staticmethod
    def show_warning(message):
        """Show warning dialog"""
        from tkinter import messagebox
        messagebox.showwarning("⚠ Warning", message)
    
    @staticmethod
    def ask_confirmation(message):
        """Ask for confirmation"""
        from tkinter import messagebox
        return messagebox.askyesno("Confirm", message)


# Test the design components
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Design Components Test")
    root.geometry("800x600")
    root.configure(bg=DesignConfig.BG_PRIMARY)
    
    # Test title
    title = TitleLabel(root, "Vehicle Violation System", icon="🚗")
    title.pack(pady=20)
    
    # Test frame with form fields
    frame = StyledFrame(root)
    frame.pack(padx=20, pady=10, fill=tk.BOTH)
    
    plate_field = FormField(frame, "Plate Number", 0)
    vehicle_field = FormField(frame, "Vehicle Type", 1, field_type="combobox",
                             values=["Car", "Motorcycle", "Truck"])
    
    # Test buttons
    btn_frame = tk.Frame(frame, bg=DesignConfig.BG_SECONDARY)
    btn_frame.grid(row=2, column=0, columnspan=2, pady=20)
    
    StyledButton(btn_frame, "Save", bg_color=DesignConfig.HIGHLIGHT).pack(side=tk.LEFT, padx=5)
    StyledButton(btn_frame, "Cancel", bg_color=DesignConfig.ACCENT).pack(side=tk.LEFT, padx=5)
    
    # Test status bar
    status = StatusBar(root)
    status.pack(side=tk.BOTTOM, fill=tk.X)
    status.set_status("System ready", "success")
    
    root.mainloop()