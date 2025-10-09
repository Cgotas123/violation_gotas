"""
app.py - Vehicle Violation Management System
Modern GUI with XAMPP MySQL Database
"""

import tkinter as tk
from tkinter import ttk, messagebox
import traceback

def main():
    try:
        print("=" * 60)
        print("🚗 Vehicle Violation Management System")
        print("=" * 60)
        print("\nStep 1: Initializing application...")
        
        # Create root window
        root = tk.Tk()
        root.title("🚗 Vehicle Violation Management System")
        root.geometry("1400x800")
        root.minsize(1200, 600)
        print("✓ Window created")
        
        # Apply modern styling
        print("\nStep 2: Loading styles...")
        try:
            from style import apply_style
            modern = apply_style(root)
            print("✓ Styles applied")
        except Exception as e:
            print(f"⚠ Style loading issue: {e}")
            modern = None
        
        # Load configuration
        print("\nStep 3: Loading configuration...")
        try:
            from config import (APP_CONFIG, VEHICLE_TYPES, VIOLATION_TYPES, 
                               STATUS_TYPES, get_default_fine)
            print("✓ Configuration loaded")
        except Exception as e:
            print(f"✗ Config error: {e}")
            messagebox.showerror("Config Error", str(e))
            return
        
        # Connect to database
        print("\nStep 4: Connecting to database...")
        try:
            from database import ViolationDatabase
            print("  - Importing database module...")
            db = ViolationDatabase()
            print("✓ Database connected")
        except Exception as e:
            print(f"\n✗ Database error: {e}")
            print(f"Error type: {type(e).__name__}")
            traceback.print_exc()
            
            error_msg = (
                "Cannot connect to MySQL database!\n\n"
                "Please make sure:\n"
                "1. XAMPP Control Panel is running\n"
                "2. MySQL service is started (green)\n"
                "3. MySQL is running on port 3306\n"
                "4. Database 'vehicle_violations_db' exists\n\n"
                f"Error: {str(e)}"
            )
            messagebox.showerror("Database Connection Error", error_msg)
            input("\nPress Enter to exit...")
            return
        
        print("\nStep 5: Building interface...")
        
        # Main Application Class
        class ViolationApp:
            def __init__(self, root):
                self.root = root
                self.db = db
                self.selected_id = None
                
                # Main container with background color
                if modern:
                    main_bg = modern.colors['background']
                else:
                    main_bg = '#f8f9fa'
                
                self.root.configure(bg=main_bg)
                
                # Title Frame
                title_frame = tk.Frame(self.root, bg=main_bg, height=80)
                title_frame.pack(fill="x", padx=20, pady=(10, 5))
                title_frame.pack_propagate(False)
                
                title_label = tk.Label(
                    title_frame,
                    text="🚗 Vehicle Violation Management System",
                    font=("Arial", 20, "bold"),
                    fg="#2c3e50",
                    bg=main_bg
                )
                title_label.pack(expand=True)
                
                subtitle = tk.Label(
                    title_frame,
                    text="XAMPP MySQL Database System",
                    font=("Arial", 10),
                    fg="#7f8c8d",
                    bg=main_bg
                )
                subtitle.pack()
                
                # Main content area
                content_frame = tk.Frame(self.root, bg=main_bg)
                content_frame.pack(fill="both", expand=True, padx=20, pady=10)
                
                # Form Section
                self.create_form_section(content_frame)
                
                # Table Section
                self.create_table_section(content_frame)
                
                # Status Bar
                self.status_bar = tk.Label(
                    self.root,
                    text="Ready | Database: vehicle_violations_db",
                    bg="#2c3e50",
                    fg="white",
                    font=("Arial", 9),
                    anchor="w",
                    relief="flat"
                )
                self.status_bar.pack(side="bottom", fill="x")
                
                # Load data
                self.load_data()
                print("✓ Interface built successfully")
            
            def create_form_section(self, parent):
                """Create form input section"""
                form_frame = ttk.LabelFrame(
                    parent,
                    text="  Violation Details  ",
                    padding=15
                )
                form_frame.pack(fill="x", pady=(0, 10))
                
                # Create input fields
                self.inputs = {}
                
                # Row 0
                tk.Label(form_frame, text="Plate Number:", font=("Arial", 10, "bold")).grid(
                    row=0, column=0, padx=10, pady=8, sticky="w")
                self.inputs["plate"] = ttk.Entry(form_frame, width=25)
                self.inputs["plate"].grid(row=0, column=1, padx=10, pady=8, sticky="ew")
                
                tk.Label(form_frame, text="Vehicle Type:", font=("Arial", 10, "bold")).grid(
                    row=0, column=2, padx=10, pady=8, sticky="w")
                self.inputs["vehicle"] = ttk.Combobox(
                    form_frame, values=VEHICLE_TYPES, state="readonly", width=23)
                self.inputs["vehicle"].grid(row=0, column=3, padx=10, pady=8, sticky="ew")
                
                # Row 1
                tk.Label(form_frame, text="Violation Type:", font=("Arial", 10, "bold")).grid(
                    row=1, column=0, padx=10, pady=8, sticky="w")
                self.inputs["violation"] = ttk.Combobox(
                    form_frame, values=VIOLATION_TYPES, state="readonly", width=23)
                self.inputs["violation"].grid(row=1, column=1, padx=10, pady=8, sticky="ew")
                self.inputs["violation"].bind("<<ComboboxSelected>>", self.on_violation_select)
                
                tk.Label(form_frame, text="Location:", font=("Arial", 10, "bold")).grid(
                    row=1, column=2, padx=10, pady=8, sticky="w")
                self.inputs["location"] = ttk.Entry(form_frame, width=25)
                self.inputs["location"].grid(row=1, column=3, padx=10, pady=8, sticky="ew")
                
                # Row 2
                tk.Label(form_frame, text="Fine Amount (₱):", font=("Arial", 10, "bold")).grid(
                    row=2, column=0, padx=10, pady=8, sticky="w")
                self.inputs["fine"] = ttk.Entry(form_frame, width=25)
                self.inputs["fine"].grid(row=2, column=1, padx=10, pady=8, sticky="ew")
                
                tk.Label(form_frame, text="Status:", font=("Arial", 10, "bold")).grid(
                    row=2, column=2, padx=10, pady=8, sticky="w")
                self.inputs["status"] = ttk.Combobox(
                    form_frame, values=STATUS_TYPES, state="readonly", width=23)
                self.inputs["status"].grid(row=2, column=3, padx=10, pady=8, sticky="ew")
                self.inputs["status"].set("Pending")
                
                # Buttons
                btn_frame = tk.Frame(form_frame, bg="white")
                btn_frame.grid(row=3, column=0, columnspan=4, pady=15)
                
                ttk.Button(
                    btn_frame, text="➕ Add Violation", 
                    style="Success.TButton", command=self.add_violation
                ).pack(side="left", padx=5)
                
                ttk.Button(
                    btn_frame, text="✏️ Update", 
                    style="Primary.TButton", command=self.update_violation
                ).pack(side="left", padx=5)
                
                ttk.Button(
                    btn_frame, text="🗑️ Delete", 
                    style="Danger.TButton", command=self.delete_violation
                ).pack(side="left", padx=5)
                
                ttk.Button(
                    btn_frame, text="🔄 Refresh", 
                    style="Accent.TButton", command=self.load_data
                ).pack(side="left", padx=5)
                
                ttk.Button(
                    btn_frame, text="🧹 Clear Form", 
                    command=self.clear_form
                ).pack(side="left", padx=5)
                
                # Configure grid weights
                for i in range(4):
                    form_frame.columnconfigure(i, weight=1)
            
            def create_table_section(self, parent):
                """Create table display section"""
                table_frame = ttk.LabelFrame(
                    parent,
                    text="  Violation Records  ",
                    padding=10
                )
                table_frame.pack(fill="both", expand=True)
                
                # Search bar
                search_frame = tk.Frame(table_frame, bg="white")
                search_frame.pack(fill="x", pady=(0, 10))
                
                tk.Label(search_frame, text="🔍 Search:", 
                        font=("Arial", 10, "bold"), bg="white").pack(side="left", padx=(0, 10))
                
                self.search_var = tk.StringVar()
                self.search_var.trace("w", lambda *args: self.on_search())
                search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=40)
                search_entry.pack(side="left")
                
                # Table
                table_container = tk.Frame(table_frame)
                table_container.pack(fill="both", expand=True)
                
                # Scrollbars
                y_scroll = ttk.Scrollbar(table_container)
                y_scroll.pack(side="right", fill="y")
                
                x_scroll = ttk.Scrollbar(table_container, orient="horizontal")
                x_scroll.pack(side="bottom", fill="x")
                
                # Treeview
                columns = ("ID", "Plate", "Vehicle", "Violation", "Location", "Fine", "Date", "Status")
                
                self.tree = ttk.Treeview(
                    table_container,
                    columns=columns,
                    show="headings",
                    height=15,
                    yscrollcommand=y_scroll.set,
                    xscrollcommand=x_scroll.set
                )
                
                # Configure scrollbars
                y_scroll.config(command=self.tree.yview)
                x_scroll.config(command=self.tree.xview)
                
                # Column settings
                col_config = {
                    "ID": (60, "center"),
                    "Plate": (120, "center"),
                    "Vehicle": (120, "center"),
                    "Violation": (180, "center"),
                    "Location": (150, "center"),
                    "Fine": (120, "center"),
                    "Date": (180, "center"),
                    "Status": (120, "center")
                }
                
                for col, (width, anchor) in col_config.items():
                    self.tree.heading(col, text=col)
                    self.tree.column(col, width=width, anchor=anchor)
                
                self.tree.pack(fill="both", expand=True)
                self.tree.bind("<<TreeviewSelect>>", self.on_row_select)
            
            def on_violation_select(self, event=None):
                """Auto-fill fine amount when violation type is selected"""
                violation_type = self.inputs["violation"].get()
                if violation_type:
                    default_fine = get_default_fine(violation_type)
                    self.inputs["fine"].delete(0, tk.END)
                    self.inputs["fine"].insert(0, str(default_fine))
            
            def on_search(self):
                """Search violations"""
                search_term = self.search_var.get().strip()
                if not search_term:
                    self.load_data()
                    return
                
                try:
                    self.tree.delete(*self.tree.get_children())
                    results = self.db.search_violations(search_term)
                    
                    for row in results:
                        formatted_row = (
                            row[0], row[1], row[2], row[3], row[4],
                            f"₱{float(row[5]):,.2f}",
                            row[6].strftime("%Y-%m-%d %H:%M") if hasattr(row[6], 'strftime') else str(row[6]),
                            row[7]
                        )
                        self.tree.insert("", "end", values=formatted_row)
                    
                    self.status_bar.config(text=f"Found {len(results)} record(s)")
                except Exception as e:
                    messagebox.showerror("Search Error", str(e))
            
            def on_row_select(self, event):
                """Handle row selection"""
                try:
                    selected = self.tree.selection()
                    
                    if not selected or len(selected) == 0:
                        print("No row selected")
                        return
                    
                    # Get the first selected item
                    item = selected[0]
                    values = self.tree.item(item, "values")
                    
                    if not values or len(values) == 0:
                        print("No values in selected row")
                        return
                    
                    # Store selected ID - FORCE IT TO BE SET
                    self.selected_id = int(values[0])
                    print(f"Selected ID: {self.selected_id}")  # Debug print
                    
                    # Clear form first
                    for field, widget in self.inputs.items():
                        if isinstance(widget, ttk.Entry):
                            widget.delete(0, tk.END)
                        elif isinstance(widget, ttk.Combobox):
                            widget.set('')
                    
                    # Fill form with selected data
                    self.inputs["plate"].insert(0, str(values[1]))
                    self.inputs["vehicle"].set(str(values[2]))
                    self.inputs["violation"].set(str(values[3]))
                    self.inputs["location"].insert(0, str(values[4]))
                    
                    # Clean fine amount
                    fine_str = str(values[5]).replace('₱', '').replace(',', '').strip()
                    self.inputs["fine"].insert(0, fine_str)
                    
                    self.inputs["status"].set(str(values[7]))
                    
                    self.status_bar.config(text=f"✓ SELECTED: Record ID {self.selected_id} | Ready to Update/Delete")
                    print(f"Status bar updated for ID: {self.selected_id}")
                    
                except Exception as e:
                    print(f"Error in on_row_select: {e}")
                    import traceback
                    traceback.print_exc()
            
            def load_data(self):
                """Load all violations from database"""
                try:
                    self.tree.delete(*self.tree.get_children())
                    data = self.db.get_all_violations()
                    
                    for row in data:
                        formatted_row = (
                            row[0], row[1], row[2], row[3], row[4],
                            f"₱{float(row[5]):,.2f}",
                            row[6].strftime("%Y-%m-%d %H:%M") if hasattr(row[6], 'strftime') else str(row[6]),
                            row[7]
                        )
                        self.tree.insert("", "end", values=formatted_row)
                    
                    self.status_bar.config(text=f"Loaded {len(data)} record(s)")
                except Exception as e:
                    messagebox.showerror("Load Error", str(e))
            
            def add_violation(self):
                """Add new violation"""
                try:
                    plate = self.inputs["plate"].get().strip()
                    vehicle = self.inputs["vehicle"].get().strip()
                    violation = self.inputs["violation"].get().strip()
                    location = self.inputs["location"].get().strip()
                    fine = self.inputs["fine"].get().strip()
                    status = self.inputs["status"].get().strip()
                    
                    if not all([plate, vehicle, violation, location, fine]):
                        messagebox.showwarning("Validation", "Please fill in all required fields!")
                        return
                    
                    try:
                        fine_amount = float(fine)
                        if fine_amount <= 0:
                            messagebox.showwarning("Validation", "Fine amount must be positive!")
                            return
                    except ValueError:
                        messagebox.showwarning("Validation", "Please enter a valid fine amount!")
                        return
                    
                    officer_name = "Officer"  # You can add officer name field if needed
                    violation_id = self.db.create_violation(
                        plate, vehicle, violation, location, 
                        fine_amount, officer_name, status
                    )
                    
                    messagebox.showinfo("Success", f"Violation added! ID: {violation_id}")
                    self.load_data()
                    self.clear_form()
                    
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to add violation:\n{str(e)}")
            
            def update_violation(self):
                """Update selected violation"""
                # Check if a record is selected from the table
                if not hasattr(self, 'selected_id') or self.selected_id is None:
                    # Check if there's a selected row in the table
                    selected_items = self.tree.selection()
                    if selected_items:
                        # Get the ID from the selected row
                        values = self.tree.item(selected_items[0], "values")
                        if values:
                            self.selected_id = str(values[0])
                    else:
                        messagebox.showwarning("No Selection", 
                            "Please click on a row in the table to select a violation record to update!\n\n"
                            "Steps:\n"
                            "1. Click on any row in the table below\n"
                            "2. The data will fill the form\n"
                            "3. Modify the fields\n"
                            "4. Click Update button")
                        return
                
                try:
                    plate = self.inputs["plate"].get().strip()
                    vehicle = self.inputs["vehicle"].get().strip()
                    violation = self.inputs["violation"].get().strip()
                    location = self.inputs["location"].get().strip()
                    fine = self.inputs["fine"].get().strip()
                    status = self.inputs["status"].get().strip()
                    
                    if not all([plate, vehicle, violation, location, fine]):
                        messagebox.showwarning("Validation", "Please fill in all required fields!")
                        return
                    
                    try:
                        fine_amount = float(fine)
                        if fine_amount <= 0:
                            messagebox.showwarning("Validation", "Fine amount must be positive!")
                            return
                    except ValueError:
                        messagebox.showwarning("Validation", "Please enter a valid fine amount!")
                        return
                    
                    # Confirm update
                    confirm = messagebox.askyesno(
                        "Confirm Update",
                        f"Update Record ID {self.selected_id}?\n\n"
                        f"Plate: {plate}\n"
                        f"Violation: {violation}\n"
                        f"Fine: ₱{fine_amount:,.2f}"
                    )
                    
                    if not confirm:
                        return
                    
                    officer_name = "Officer"
                    notes = ""
                    
                    updated = self.db.update_violation(
                        int(self.selected_id), plate, vehicle, violation,
                        location, fine_amount, officer_name, status, notes
                    )
                    
                    if updated:
                        messagebox.showinfo("Success", "✓ Violation updated successfully!")
                        self.load_data()
                        self.clear_form()
                        self.selected_id = None
                    else:
                        messagebox.showwarning("Warning", "Update failed! Record may not exist.")
                        
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to update:\n{str(e)}")
            
            def delete_violation(self):
                """Delete selected violation"""
                # Check if a record is selected from the table
                if not hasattr(self, 'selected_id') or self.selected_id is None:
                    # Check if there's a selected row in the table
                    selected_items = self.tree.selection()
                    if selected_items:
                        # Get the ID from the selected row
                        values = self.tree.item(selected_items[0], "values")
                        if values:
                            self.selected_id = str(values[0])
                    else:
                        messagebox.showwarning("No Selection", 
                            "Please click on a row in the table to select a violation record to delete!\n\n"
                            "Steps:\n"
                            "1. Click on any row in the table below\n"
                            "2. Click the Delete button\n"
                            "3. Confirm deletion")
                        return
                
                # Get plate number for confirmation message
                plate = self.inputs["plate"].get().strip() if self.inputs["plate"].get() else "Unknown"
                
                confirm = messagebox.askyesno(
                    "Confirm Delete",
                    f"⚠️ DELETE Record ID {self.selected_id}?\n\n"
                    f"Plate Number: {plate}\n\n"
                    f"This action cannot be undone!"
                )
                
                if not confirm:
                    return
                
                try:
                    deleted = self.db.delete_violation(int(self.selected_id))
                    
                    if deleted:
                        messagebox.showinfo("Success", "✓ Violation deleted successfully!")
                        self.load_data()
                        self.clear_form()
                        self.selected_id = None
                    else:
                        messagebox.showwarning("Warning", "Delete failed! Record may not exist.")
                        
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to delete:\n{str(e)}")
            
            def clear_form(self):
                """Clear all form fields"""
                for field, widget in self.inputs.items():
                    if isinstance(widget, ttk.Entry):
                        widget.delete(0, tk.END)
                    elif isinstance(widget, ttk.Combobox):
                        if field == "status":
                            widget.set("Pending")
                        else:
                            widget.set('')
                
                # Clear selected ID
                self.selected_id = None
                self.status_bar.config(text="Form cleared | Ready")
        
        # Create and run application
        app = ViolationApp(root)
        
        print("\n" + "=" * 60)
        print("✓ Application started successfully!")
        print("=" * 60)
        
        root.mainloop()
        
    except Exception as e:
        print(f"\n✗ FATAL ERROR: {e}")
        traceback.print_exc()
        messagebox.showerror("Fatal Error", f"Application failed to start:\n{str(e)}")

if __name__ == "__main__":
    main()