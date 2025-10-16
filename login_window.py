"""
login_window.py - Login and Registration UI for Vehicle Violation System
"""
import tkinter as tk
from tkinter import ttk, messagebox
from auth import AuthManager
from database import ViolationDatabase

class LoginWindow:
    def __init__(self, root, on_login_success):
        self.root = root
        self.on_login_success = on_login_success
        self.db = ViolationDatabase()
        self.auth = AuthManager(self.db)
        
        self.root.title("Vehicle Violation System - Login")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        
        self.create_widgets()
    
    def create_widgets(self):
        """Create login/registration interface"""
        # Style
        style = ttk.Style()
        style.configure("TFrame", background="#f8f9fa")
        style.configure("TLabel", background="#f8f9fa", font=("Arial", 10))
        style.configure("TButton", font=("Arial", 10))
        style.configure("Accent.TButton", font=("Arial", 10, "bold"), background="#007bff", foreground="white")
        style.configure("TNotebook", background="#f8f9fa")
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill="both", expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="🚗 Vehicle Violation System", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill="both", expand=True, pady=10)
        
        # Login Frame
        login_frame = ttk.Frame(self.notebook, padding=20)
        self.notebook.add(login_frame, text="Login")
        
        ttk.Label(login_frame, text="Username:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.login_username = ttk.Entry(login_frame, width=25)
        self.login_username.grid(row=0, column=1, padx=10, pady=10)
        
        ttk.Label(login_frame, text="Password:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.login_password = ttk.Entry(login_frame, show="*", width=25)
        self.login_password.grid(row=1, column=1, padx=10, pady=10)
        
        login_btn = ttk.Button(login_frame, text="Login", command=self.handle_login, style="Accent.TButton", padding=5)
        login_btn.grid(row=2, column=1, pady=20, sticky="e")
        
        # Registration Frame
        register_frame = ttk.Frame(self.notebook, padding=20)
        self.notebook.add(register_frame, text="Register")
        
        ttk.Label(register_frame, text="Username:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.reg_username = ttk.Entry(register_frame, width=25)
        self.reg_username.grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Label(register_frame, text="Email:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.reg_email = ttk.Entry(register_frame, width=25)
        self.reg_email.grid(row=1, column=1, padx=10, pady=5)
        
        ttk.Label(register_frame, text="Password:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.reg_password = ttk.Entry(register_frame, show="*", width=25)
        self.reg_password.grid(row=2, column=1, padx=10, pady=5)
        
        ttk.Label(register_frame, text="Confirm Password:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.reg_confirm = ttk.Entry(register_frame, show="*", width=25)
        self.reg_confirm.grid(row=3, column=1, padx=10, pady=5)
        
        register_btn = ttk.Button(register_frame, text="Register", command=self.handle_register, padding=5)
        register_btn.grid(row=4, column=1, pady=10, sticky="e")
        
        # Configure grid weights
        for frame in [login_frame, register_frame]:
            frame.columnconfigure(1, weight=1)
    
    def handle_login(self):
        """Handle login attempt"""
        username = self.login_username.get().strip()
        password = self.login_password.get().strip()
        
        if not username or not password:
            messagebox.showwarning("Validation", "Please enter both username and password")
            return
        
        user = self.auth.login_user(username, password)
        if user:
            messagebox.showinfo("Success", f"Welcome {user['username']}!")
            self.on_login_success(user)
        else:
            messagebox.showerror("Error", "Invalid username or password")
    
    def handle_register(self):
        """Handle registration attempt"""
        username = self.reg_username.get().strip()
        email = self.reg_email.get().strip()
        password = self.reg_password.get().strip()
        confirm = self.reg_confirm.get().strip()
        
        if not all([username, email, password, confirm]):
            messagebox.showwarning("Validation", "Please fill in all fields")
            return
            
        if password != confirm:
            messagebox.showwarning("Validation", "Passwords do not match")
            return
            
        if len(password) < 8:
            messagebox.showwarning("Validation", "Password must be at least 8 characters")
            return
            
        try:
            user_id = self.auth.register_user(username, email, password)
            messagebox.showinfo("Success", f"Account created! ID: {user_id}")
            self.notebook.select(0)  # Switch to login tab
        except Exception as e:
            messagebox.showerror("Error", f"Registration failed: {str(e)}")
    
    def run(self):
        """Run the login window"""
        self.root.mainloop()
