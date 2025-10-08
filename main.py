"""
main.py - Main Application
Vehicle Violation Management System with Full CRUD Operations
"""

import tkinter as tk
from tkinter import ttk
import sys

# Import database and GUI modules
from database import ViolationDatabase
from gui_design import (
    DesignConfig, StyledButton, StyledFrame, TitleLabel,
    FormField, SearchBar, StyledTreeview, StatusBar, DialogBox
)


class ViolationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Vehicle Violation Management System")
        self.root.geometry("1400x800")
        self.root.configure(bg=DesignConfig.BG_PRIMARY)
        
        # Initialize database
        try:
            self.db = ViolationDatabase()
            print("✓ Database initialized successfully")
        except Exception as e:
            DialogBox.show_error(f"Database connection failed:\n{e}\n\nMake sure XAMPP MySQL is running!")
            sys.exit(1)
        
        # Track selected violation ID
        self.selected_id = None
        
        # Create UI
        self.create_widgets()
        self.load_violations()
        
        # Status bar message
        self.status_bar.set_status("System ready - Connected to database", "success")
    
    def create_widgets(self):
        """Create all UI widgets"""
        # Title bar
        title_frame = tk.Frame(self.root, bg=DesignConfig.BG_PRIMARY)
        title_frame.pack(fill=tk.X, pady=20)
        
        title = TitleLabel(title_frame, "Vehicle Violation Management System", icon="🚗")
        title.pack()
        
        subtitle = tk.Label(
            title_frame,
            text="Comprehensive CRUD Operations - MySQL Database",
            font=DesignConfig.FONT_SMALL,
            bg=DesignConfig.BG_PRIMARY,
            fg=DesignConfig.TEXT_SECONDARY
        )
        subtitle.pack()
        
        # Main container
        main_container = tk.Frame(self.root, bg=DesignConfig.BG_PRIMARY)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Left panel - Form
        self.create_left_panel(main_container)
        
        # Right panel - Data view
        self.create_right_panel(main_container)
        
        # Status bar
        self.status_bar = StatusBar(self.root)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def create_left_panel(self, parent):
        """Create left panel with form"""
        left_panel = StyledFrame(parent)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 10), pady=5)
        
        # Form title
        form_title = TitleLabel(left_panel, "Violation Form", icon="📝")
        form_title.pack(pady=15)
        
        # Form frame
        form_frame = tk.Frame(left_panel, bg=DesignConfig.BG_SECONDARY)
        form_frame.pack(padx=20, pady=10, fill=tk.BOTH)
        
        # Create form fields
        self.plate_field = FormField(form_frame, "Plate Number", 0)
        
        self.vehicle_field = FormField(
            form_frame, "Vehicle Type", 1,
            field_type="combobox",
            values=("Car", "Motorcycle", "Truck", "Bus", "Van", "SUV")
        )
        
        self.violation_field = FormField(
            form_frame, "Violation Type", 2,
            field_type="combobox",
            values=(
                "Speeding", "Illegal Parking", "Running Red Light",
                "No License", "No Registration", "DUI", "Reckless Driving",
                "No Insurance", "Expired License", "Improper Lane Change",
                "No Seatbelt", "Using Phone While Driving", "Other"
            )
        )
        
        self.location_field = FormField(form_frame, "Location", 3)
        
        self.fine_field = FormField(form_frame, "Fine Amount (₱)", 4)
        
        self.officer_field = FormField(form_frame, "Officer Name", 5)
        
        self.status_field = FormField(
            form_frame, "Status", 6,
            field_type="combobox",
            values=("Pending", "Paid", "Cancelled")
        )
        
        self.notes_field = FormField(form_frame, "Notes", 7, field_type="text")
        
        # CRUD Buttons
        btn_frame = tk.Frame(form_frame, bg=DesignConfig.BG_SECONDARY)
        btn_frame.grid(row=8, column=0, columnspan=2, pady=20)
        
        # CREATE Button
        self.create_btn = StyledButton(
            btn_frame,
            text="➕ CREATE",
            command=self.create_violation,
            bg_color=DesignConfig.HIGHLIGHT,
            width=12
        )
        self.create_btn.pack(side=tk.LEFT, padx=3)
        
        # UPDATE Button
        self.update_btn = StyledButton(
            btn_frame,
            text="✏️ UPDATE",
            command=self.update_violation,
            bg_color=DesignConfig.ACCENT,
            width=12
        )
        self.update_btn.pack(side=tk.LEFT, padx=3)
        
        # DELETE Button
        self.delete_btn = StyledButton(
            btn_frame,
            text="🗑️ DELETE",
            command=self.delete_violation,
            bg_color=DesignConfig.DANGER,
            width=12
        )
        self.delete_btn.pack(side=tk.LEFT, padx=3)
        
        # Clear Button
        btn_frame2 = tk.Frame(form_frame, bg=DesignConfig.BG_SECONDARY)
        btn_frame2.grid(row=9, column=0, columnspan=2, pady=5)
        
        self.clear_btn = StyledButton(
            btn_frame2,
            text="🔄 CLEAR FORM",
            command=self.clear_form,
            bg_color=DesignConfig.SUCCESS,
            width=25
        )
        self.clear_btn.pack()
    
    def create_right_panel(self, parent):
        """Create right panel with data view"""
        right_panel = StyledFrame(parent)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, pady=5)
        
        # Title
        list_title = TitleLabel(right_panel, "Violation Records", icon="📋")
        list_title.pack(pady=15)
        
        # Search bar
        self.search_bar = SearchBar(right_panel, self.search_violations)
        self.search_bar.frame.pack(padx=20, pady=10, fill=tk.X)
        
        # Filter buttons
        filter_frame = tk.Frame(right_panel, bg=DesignConfig.BG_SECONDARY)
        filter_frame.pack(padx=20, pady=5)
        
        tk.Label(
            filter_frame,
            text="Filter by Status:",
            bg=DesignConfig.BG_SECONDARY,
            fg=DesignConfig.TEXT_COLOR,
            font=DesignConfig.FONT_NORMAL
        ).pack(side=tk.LEFT, padx=5)
        
        StyledButton(
            filter_frame, "All", 
            command=lambda: self.filter_by_status(None),
            bg_color=DesignConfig.ACCENT, width=8
        ).pack(side=tk.LEFT, padx=2)
        
        StyledButton(
            filter_frame, "Pending",
            command=lambda: self.filter_by_status("Pending"),
            bg_color="#FFA500", width=8
        ).pack(side=tk.LEFT, padx=2)
        
        StyledButton(
            filter_frame, "Paid",
            command=lambda: self.filter_by_status("Paid"),
            bg_color=DesignConfig.SUCCESS, width=8
        ).pack(side=tk.LEFT, padx=2)
        
        StyledButton(
            filter_frame, "Cancelled",
            command=lambda: self.filter_by_status("Cancelled"),
            bg_color=DesignConfig.DANGER, width=8
        ).pack(side=tk.LEFT, padx=2)
        
        # Treeview
        columns = ("ID", "Plate", "Vehicle", "Violation", "Fine", "Date", "Status")
        headings = ("ID", "Plate Number", "Vehicle Type", "Violation", "Fine ($)", "Date/Time", "Status")
        widths = (50, 120, 100, 150, 80, 150, 100)
        
        self.tree_view = StyledTreeview(right_panel, columns, headings, widths)
        self.tree_view.frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
        
        # Bind events
        self.tree_view.bind('<ButtonRelease-1>', self.on_tree_select)
        self.tree_view.bind('<Double-1>', self.view_details)
        
        # Action buttons
        action_frame = tk.Frame(right_panel, bg=DesignConfig.BG_SECONDARY)
        action_frame.pack(pady=15)
        
        StyledButton(
            action_frame, "📊 Statistics",
            command=self.show_statistics,
            bg_color=DesignConfig.SUCCESS, width=12
        ).pack(side=tk.LEFT, padx=5)
        
        StyledButton(
            action_frame, "🔄 Refresh",
            command=self.load_violations,
            bg_color=DesignConfig.ACCENT, width=12
        ).pack(side=tk.LEFT, padx=5)
        
        StyledButton(
            action_frame, "ℹ️ View Details",
            command=lambda e=None: self.view_details(e),
            bg_color="#4A90E2", width=12
        ).pack(side=tk.LEFT, padx=5)
    
    # ==================== CRUD OPERATIONS ====================
    
    def create_violation(self):
        """CREATE - Add new violation to database"""
        try:
            # Get form values
            plate = self.plate_field.get().strip()
            vehicle = self.vehicle_field.get()
            violation = self.violation_field.get()
            location = self.location_field.get().strip()
            fine = self.fine_field.get().strip()
            officer = self.officer_field.get().strip()
            status = self.status_field.get()
            notes = self.notes_field.get()
            
            # Validate inputs
            if not all([plate, vehicle, violation, location, fine, officer]):
                DialogBox.show_warning("Please fill in all required fields!")
                return
            
            try:
                fine_amount = float(fine)
                if fine_amount < 0:
                    raise ValueError
            except ValueError:
                DialogBox.show_error("Fine amount must be a valid positive number!")
                return
            
            # Insert into database
            violation_id = self.db.create_violation(
                plate, vehicle, violation, location,
                fine_amount, officer, status, notes
            )
            
            DialogBox.show_success(f"Violation created successfully!\nID: {violation_id}")
            self.clear_form()
            self.load_violations()
            self.status_bar.set_status(f"Created violation ID: {violation_id}", "success")
            
        except Exception as e:
            DialogBox.show_error(f"Error creating violation:\n{e}")
            self.status_bar.set_status("Error creating violation", "error")
    
    def load_violations(self):
        """READ - Load all violations from database"""
        try:
            self.tree_view.clear()
            violations = self.db.get_all_violations()
            
            for violation in violations:
                self.tree_view.insert(violation)
            
            count = len(violations)
            self.status_bar.set_status(f"Loaded {count} violation(s)", "info")
            
        except Exception as e:
            DialogBox.show_error(f"Error loading violations:\n{e}")
            self.status_bar.set_status("Error loading data", "error")
    
    def update_violation(self):
        """UPDATE - Update selected violation"""
        if not self.selected_id:
            DialogBox.show_warning("Please select a violation to update!")
            return
        
        try:
            # Get form values
            plate = self.plate_field.get().strip()
            vehicle = self.vehicle_field.get()
            violation = self.violation_field.get()
            location = self.location_field.get().strip()
            fine = self.fine_field.get().strip()
            officer = self.officer_field.get().strip()
            status = self.status_field.get()
            notes = self.notes_field.get()
            
            # Validate
            if not all([plate, vehicle, violation, location, fine, officer]):
                DialogBox.show_warning("Please fill in all required fields!")
                return
            
            try:
                fine_amount = float(fine)
                if fine_amount < 0:
                    raise ValueError
            except ValueError:
                DialogBox.show_error("Fine amount must be a valid positive number!")
                return
            
            # Update in database
            success = self.db.update_violation(
                self.selected_id, plate, vehicle, violation,
                location, fine_amount, officer, status, notes
            )
            
            if success:
                DialogBox.show_success(f"Violation ID {self.selected_id} updated successfully!")
                self.clear_form()
                self.load_violations()
                self.status_bar.set_status(f"Updated violation ID: {self.selected_id}", "success")
            else:
                DialogBox.show_error("Failed to update violation!")
                
        except Exception as e:
            DialogBox.show_error(f"Error updating violation:\n{e}")
            self.status_bar.set_status("Error updating violation", "error")
    
    def delete_violation(self):
        """DELETE - Delete selected violation"""
        if not self.selected_id:
            DialogBox.show_warning("Please select a violation to delete!")
            return
        
        if not DialogBox.ask_confirmation(
            f"Are you sure you want to delete violation ID {self.selected_id}?\n\nThis action cannot be undone!"
        ):
            return
        
        try:
            success = self.db.delete_violation(self.selected_id)
            
            if success:
                DialogBox.show_success(f"Violation ID {self.selected_id} deleted successfully!")
                self.clear_form()
                self.load_violations()
                self.status_bar.set_status(f"Deleted violation ID: {self.selected_id}", "success")
                self.selected_id = None
            else:
                DialogBox.show_error("Failed to delete violation!")
                
        except Exception as e:
            DialogBox.show_error(f"Error deleting violation:\n{e}")
            self.status_bar.set_status("Error deleting violation", "error")
    
    # ==================== HELPER FUNCTIONS ====================
    
    def on_tree_select(self, event):
        """Handle treeview selection"""
        selected = self.tree_view.get_selected()
        if selected:
            values = selected['values']
            self.selected_id = values[0]
            
            # Load full data
            violation = self.db.get_violation_by_id(self.selected_id)
            if violation:
                self.populate_form(violation)
                self.status_bar.set_status(f"Selected violation ID: {self.selected_id}", "info")
    
    def populate_form(self, violation):
        """Populate form with violation data"""
        self.plate_field.set(violation[1])
        self.vehicle_field.set(violation[2])
        self.violation_field.set(violation[3])
        self.location_field.set(violation[4])
        self.fine_field.set(str(violation[5]))
        self.officer_field.set(violation[7])
        self.status_field.set(violation[8])
        self.notes_field.set(violation[9] if violation[9] else "")
    
    def clear_form(self):
        """Clear all form fields"""
        self.plate_field.clear()
        self.vehicle_field.widget.current(0)
        self.violation_field.widget.current(0)
        self.location_field.clear()
        self.fine_field.clear()
        self.officer_field.clear()
        self.status_field.widget.current(0)
        self.notes_field.clear()
        self.selected_id = None
        self.status_bar.set_status("Form cleared", "info")
    
    def search_violations(self):
        """Search violations"""
        search_term = self.search_bar.get()
        
        if search_term:
            try:
                self.tree_view.clear()
                results = self.db.search_violations(search_term)
                
                for result in results:
                    self.tree_view.insert(result)
                
                count = len(results)
                self.status_bar.set_status(f"Found {count} result(s) for '{search_term}'", "info")
                
            except Exception as e:
                DialogBox.show_error(f"Error searching:\n{e}")
        else:
            self.load_violations()
    
    def filter_by_status(self, status):
        """Filter violations by status"""
        try:
            self.tree_view.clear()
            
            if status:
                violations = self.db.get_violations_by_status(status)
                self.status_bar.set_status(f"Filtered by: {status}", "info")
            else:
                violations = self.db.get_all_violations()
                self.status_bar.set_status("Showing all violations", "info")
            
            for violation in violations:
                self.tree_view.insert(violation)
                
        except Exception as e:
            DialogBox.show_error(f"Error filtering:\n{e}")
    
    def view_details(self, event):
        """View full details of selected violation"""
        if not self.selected_id:
            DialogBox.show_warning("Please select a violation to view!")
            return
        
        try:
            violation = self.db.get_violation_by_id(self.selected_id)
            
            if violation:
                details = f"""
╔═══════════════════════════════════════════════╗
         VIOLATION DETAILS - ID: {violation[0]}
╚═══════════════════════════════════════════════╝

📋 Basic Information:
   • Plate Number: {violation[1]}
   • Vehicle Type: {violation[2]}
   • Violation Type: {violation[3]}

📍 Location & Details:
   • Location: {violation[4]}
   • Fine Amount: ${violation[5]:.2f}
   • Date/Time: {violation[6]}

👮 Officer Information:
   • Officer Name: {violation[7]}
   • Status: {violation[8]}

📝 Additional Notes:
   {violation[9] if violation[9] else 'No notes'}

🕒 Record Timestamps:
   • Created: {violation[10]}
   • Last Updated: {violation[11]}
                """
                DialogBox.show_info("Violation Details", details)
            
        except Exception as e:
            DialogBox.show_error(f"Error viewing details:\n{e}")
    
    def show_statistics(self):
        """Show violation statistics"""
        try:
            stats = self.db.get_statistics()
            
            top_violations = "\n".join([
                f"   • {v[0]}: {v[1]} cases" 
                for v in stats.get('top_violations', [])
            ]) or "   No data"
            
            top_violators = "\n".join([
                f"   • {v[0]}: {v[1]} violations" 
                for v in stats.get('top_violators', [])
            ]) or "   No data"
            
            stats_text = f"""
╔═══════════════════════════════════════════════╗
              SYSTEM STATISTICS
╚═══════════════════════════════════════════════╝

📊 Overall Summary:
   • Total Violations: {stats.get('total', 0)}
   • Pending: {stats.get('pending', 0)}
   • Paid: {stats.get('paid', 0)}
   • Cancelled: {stats.get('cancelled', 0)}

💰 Financial Summary:
   • Total Revenue (Paid): ${stats.get('revenue', 0):.2f}

🔝 Top Violation Types:
{top_violations}

🚗 Top Violators (by plate):
{top_violators}
            """
            
            DialogBox.show_info("Statistics Dashboard", stats_text)
            
        except Exception as e:
            DialogBox.show_error(f"Error getting statistics:\n{e}")
    
    def on_closing(self):
        """Handle window closing"""
        if DialogBox.ask_confirmation("Are you sure you want to exit?"):
            self.db.close()
            self.root.destroy()


# ==================== MAIN ENTRY POINT ====================

def main():
    """Main entry point"""
    root = tk.Tk()
    app = ViolationApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()