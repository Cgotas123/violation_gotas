"""
app.py - Vehicle Violation Management System (Tkinter GUI)
Connected to MySQL via XAMPP using database.py
LABELS AND TITLES FIXED
"""

import tkinter as tk
from tkinter import ttk, messagebox
from database import ViolationDatabase
from config import APP_CONFIG, VEHICLE_TYPES, VIOLATION_TYPES, STATUS_TYPES, MESSAGES
from style import apply_style, add_hover_effects


class ViolationApp:
    def __init__(self, root):
        self.root = root
        apply_style(root)
        self.root.geometry(f"{APP_CONFIG['window_width']}x{APP_CONFIG['window_height']}")
        self.root.minsize(APP_CONFIG['min_width'], APP_CONFIG['min_height'])

        # Database connection
        self.db = ViolationDatabase()

        # Title bar
        title_label = tk.Label(
            self.root,
            text="🚓 Vehicle Violation Management System",
            fg="#2c3e50",
            bg="#f8f9fa"
        )
        title_label.pack(pady=20)

        # Main container
        main_container = ttk.Frame(self.root)
        main_container.pack(fill="both", expand=True, padx=20, pady=10)

        # Form Frame
        form_frame = ttk.Frame(main_container)
        form_frame.pack(fill="x", pady=(0, 20))

        # Form fields
        self.create_form(form_frame)

        # Table Frame
        table_frame = ttk.Frame(main_container)
        table_frame.pack(fill="both", expand=True)

        self.create_table(table_frame)
        self.load_data()

    def create_form(self, frame):
        """Create the top form for adding/editing violations"""
        # CORRECTED LABELS
        labels = [
            ("Plate Number:", "plate"),
            ("Vehicle Type:", "vehicle"),
            ("Violation Type:", "violation"),
            ("Location:", "location"),
            ("Fine Amount:", "fine"),
            ("Status:", "status")
        ]

        self.inputs = {}

        for i, (label_text, field) in enumerate(labels):
            ttk.Label(frame, text=label_text).grid(
                row=i, column=0, padx=15, pady=8, sticky="w")

            if field == "vehicle":
                cb = ttk.Combobox(frame, values=VEHICLE_TYPES, state="readonly", width=30)
                cb.grid(row=i, column=1, padx=15, pady=8, sticky="ew")
                self.inputs[field] = cb

            elif field == "violation":
                cb = ttk.Combobox(frame, values=VIOLATION_TYPES, state="readonly", width=30)
                cb.grid(row=i, column=1, padx=15, pady=8, sticky="ew")
                self.inputs[field] = cb

            elif field == "status":
                cb = ttk.Combobox(frame, values=STATUS_TYPES, state="readonly", width=30)
                cb.current(0)
                cb.grid(row=i, column=1, padx=15, pady=8, sticky="ew")
                self.inputs[field] = cb

            else:
                entry = ttk.Entry(frame, width=33)
                entry.grid(row=i, column=1, padx=15, pady=8, sticky="ew")
                self.inputs[field] = entry

        # Buttons Frame
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=len(labels), columnspan=2, pady=20)

        # Buttons with hover effect
        btn_add = tk.Button(btn_frame, text="Add Violation", 
                           bg="#3498db", fg="white",
                           relief="flat", padx=20, pady=8, cursor="hand2",
                           command=self.add_violation)
        
        btn_update = tk.Button(btn_frame, text="Update", 
                              bg="#27ae60", fg="white",
                              relief="flat", padx=20, pady=8, cursor="hand2",
                              command=self.update_violation)
        
        btn_delete = tk.Button(btn_frame, text="Delete", 
                              bg="#e74c3c", fg="white",
                              relief="flat", padx=20, pady=8, cursor="hand2",
                              command=self.delete_violation)
        
        btn_refresh = tk.Button(btn_frame, text="Refresh", 
                               bg="#9b59b6", fg="white",
                               relief="flat", padx=20, pady=8, cursor="hand2",
                               command=self.load_data)

        btn_add.grid(row=0, column=0, padx=8)
        btn_update.grid(row=0, column=1, padx=8)
        btn_delete.grid(row=0, column=2, padx=8)
        btn_refresh.grid(row=0, column=3, padx=8)

        # Apply hover effects
        add_hover_effects(btn_add, "#2980b9", "#3498db")
        add_hover_effects(btn_update, "#229954", "#27ae60")
        add_hover_effects(btn_delete, "#c0392b", "#e74c3c")
        add_hover_effects(btn_refresh, "#8e44ad", "#9b59b6")

        # Configure grid weights for responsive layout
        frame.columnconfigure(1, weight=1)

    def create_table(self, frame):
        """Create table for displaying violations"""
        # CORRECTED COLUMN NAMES
        columns = ("ID", "Plate", "Vehicle Type", "Violation Type", "Location", "Fine", "Date", "Status")

        # Create treeview with scrollbar
        table_container = ttk.Frame(frame)
        table_container.pack(fill="both", expand=True)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(table_container)
        scrollbar.pack(side="right", fill="y")

        self.tree = ttk.Treeview(table_container, columns=columns, show="headings", 
                                yscrollcommand=scrollbar.set, height=12)
        
        # Configure columns with proper widths
        column_widths = {
            "ID": 50, "Plate": 100, "Vehicle Type": 120, "Violation Type": 150,
            "Location": 150, "Fine": 80, "Date": 120, "Status": 100
        }
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=column_widths.get(col, 100), anchor="center")

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.tree.yview)
        
        self.tree.bind("<<TreeviewSelect>>", self.on_row_select)

    def on_row_select(self, event):
        """When selecting a record in table"""
        selected = self.tree.focus()
        if not selected:
            return
        values = self.tree.item(selected, "values")
        if not values:
            return

        # Fill form with selected record - CORRECTED MAPPING
        self.selected_id = values[0]
        
        # Clear all fields first
        for field, widget in self.inputs.items():
            if isinstance(widget, ttk.Entry):
                widget.delete(0, tk.END)
            elif isinstance(widget, ttk.Combobox):
                widget.set('')
        
        # Set values from selected row
        self.inputs["plate"].insert(0, values[1])  # Plate
        self.inputs["vehicle"].set(values[2])      # Vehicle Type
        self.inputs["violation"].set(values[3])    # Violation Type
        self.inputs["location"].insert(0, values[4])  # Location
        self.inputs["fine"].insert(0, values[5])   # Fine
        self.inputs["status"].set(values[7])       # Status

    def add_violation(self):
        """Add a new violation"""
        try:
            plate = self.inputs["plate"].get()
            vehicle = self.inputs["vehicle"].get()
            violation = self.inputs["violation"].get()
            location = self.inputs["location"].get()
            fine = self.inputs["fine"].get()
            status = self.inputs["status"].get()

            # Validate required fields
            if not all([plate, vehicle, violation, location, fine]):
                messagebox.showwarning("Warning", MESSAGES['warning']['empty_fields'])
                return

            # Validate fine amount
            try:
                fine_amount = float(fine)
                if fine_amount <= 0:
                    messagebox.showwarning("Warning", "Fine amount must be positive")
                    return
            except ValueError:
                messagebox.showwarning("Warning", "Please enter a valid fine amount")
                return

            self.db.create_violation(plate, vehicle, violation, location, fine_amount, status)
            messagebox.showinfo("Success", MESSAGES['success']['create'])
            self.load_data()
            self.clear_form()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add violation: {e}")

    def update_violation(self):
        """Update selected violation"""
        if not hasattr(self, "selected_id"):
            messagebox.showwarning("Warning", MESSAGES['error']['not_selected'])
            return

        try:
            plate = self.inputs["plate"].get()
            vehicle = self.inputs["vehicle"].get()
            violation = self.inputs["violation"].get()
            location = self.inputs["location"].get()
            fine = self.inputs["fine"].get()
            status = self.inputs["status"].get()

            # Validate fields
            if not all([plate, vehicle, violation, location, fine]):
                messagebox.showwarning("Warning", MESSAGES['warning']['empty_fields'])
                return

            # Validate fine amount
            try:
                fine_amount = float(fine)
                if fine_amount <= 0:
                    messagebox.showwarning("Warning", "Fine amount must be positive")
                    return
            except ValueError:
                messagebox.showwarning("Warning", "Please enter a valid fine amount")
                return

            updated = self.db.update_violation(self.selected_id, plate, vehicle, violation, location, fine_amount, status)
            if updated:
                messagebox.showinfo("Success", MESSAGES['success']['update'])
                self.load_data()
                self.clear_form()
            else:
                messagebox.showwarning("Warning", "No record found to update.")
        except Exception as e:
            messagebox.showerror("Error", f"Update failed: {e}")

    def delete_violation(self):
        """Delete selected violation"""
        if not hasattr(self, "selected_id"):
            messagebox.showwarning("Warning", MESSAGES['error']['not_selected'])
            return

        confirm = messagebox.askyesno("Confirm", MESSAGES['error']['delete_confirm'])
        if not confirm:
            return

        try:
            deleted = self.db.delete_violation(self.selected_id)
            if deleted:
                messagebox.showinfo("Success", MESSAGES['success']['delete'])
                self.load_data()
                self.clear_form()
            else:
                messagebox.showwarning("Warning", "No record deleted.")
        except Exception as e:
            messagebox.showerror("Error", f"Delete failed: {e}")

    def clear_form(self):
        """Clear all form fields"""
        for field, widget in self.inputs.items():
            if isinstance(widget, ttk.Entry):
                widget.delete(0, tk.END)
            elif isinstance(widget, ttk.Combobox):
                widget.set('')
        # Reset status to default
        self.inputs["status"].current(0)
        
        # Remove selected ID
        if hasattr(self, 'selected_id'):
            delattr(self, 'selected_id')

    def load_data(self):
        """Load data from database"""
        # Clear existing data
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        # Load new data
        data = self.db.get_all_violations()
        for row in data:
            self.tree.insert("", "end", values=row)


# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = ViolationApp(root)
    root.mainloop()