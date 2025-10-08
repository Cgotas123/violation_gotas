"""
config.py - Configuration File
Contains all configuration settings for the application
"""

# Database Configuration
DATABASE_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  # Default XAMPP password is empty
    'database': 'vehicle_violations_db',
    'port': 3306  # Default MySQL port
}

# Application Settings
APP_CONFIG = {
    'title': 'Vehicle Violation Management System',
    'version': '1.0.0',
    'window_width': 1400,
    'window_height': 800,
    'min_width': 1200,
    'min_height': 600
}

# Form Validation Rules
VALIDATION_RULES = {
    'plate_number': {
        'max_length': 20,
        'required': True
    },
    'location': {
        'max_length': 255,
        'required': True
    },
    'fine_amount': {
        'min_value': 0,
        'max_value': 999999.99,
        'required': True
    },
    'officer_name': {
        'max_length': 100,
        'required': True
    },
    'notes': {
        'max_length': 1000,
        'required': False
    }
}

# Dropdown Options
VEHICLE_TYPES = [
    "Car",
    "Motorcycle",
    "Truck",
    "Bus",
    "Van",
    "SUV",
    "Pickup Truck",
    "Bicycle"
]

VIOLATION_TYPES = [
    "Speeding",
    "Illegal Parking",
    "Running Red Light",
    "No License",
    "No Registration",
    "DUI (Driving Under Influence)",
    "Reckless Driving",
    "No Insurance",
    "Expired License",
    "Improper Lane Change",
    "No Seatbelt",
    "Using Phone While Driving",
    "Illegal U-Turn",
    "Overloading",
    "Tinted Windows",
    "Modified Exhaust",
    "No Helmet (Motorcycle)",
    "Other"
]

STATUS_TYPES = [
    "Pending",
    "Paid",
    "Cancelled",
    "Under Review"
]

# Fine Amounts (Default suggestions)
DEFAULT_FINES = {
    "Speeding": 150.00,
    "Illegal Parking": 50.00,
    "Running Red Light": 200.00,
    "No License": 300.00,
    "No Registration": 250.00,
    "DUI (Driving Under Influence)": 1000.00,
    "Reckless Driving": 500.00,
    "No Insurance": 400.00,
    "Expired License": 100.00,
    "Improper Lane Change": 75.00,
    "No Seatbelt": 100.00,
    "Using Phone While Driving": 150.00,
    "Illegal U-Turn": 75.00,
    "Overloading": 200.00,
    "Tinted Windows": 100.00,
    "Modified Exhaust": 150.00,
    "No Helmet (Motorcycle)": 100.00,
    "Other": 100.00
}

# Export Settings
EXPORT_CONFIG = {
    'csv_delimiter': ',',
    'date_format': '%Y-%m-%d %H:%M:%S',
    'default_filename': 'violations_export'
}

# Backup Settings
BACKUP_CONFIG = {
    'backup_folder': 'backups',
    'auto_backup': True,
    'backup_interval_days': 7,
    'max_backups': 10
}

# Logging Configuration
LOGGING_CONFIG = {
    'log_file': 'app.log',
    'log_level': 'INFO',
    'max_log_size': 5242880,  # 5MB
    'backup_count': 3
}

# UI Messages
MESSAGES = {
    'success': {
        'create': 'Violation record created successfully!',
        'update': 'Violation record updated successfully!',
        'delete': 'Violation record deleted successfully!',
        'export': 'Data exported successfully!'
    },
    'error': {
        'database': 'Database connection error. Please check XAMPP MySQL service.',
        'validation': 'Please fill in all required fields correctly.',
        'not_selected': 'Please select a violation record first.',
        'delete_confirm': 'Are you sure you want to delete this record?'
    },
    'warning': {
        'empty_fields': 'Some required fields are empty.',
        'invalid_amount': 'Please enter a valid fine amount.',
        'no_results': 'No violations found matching your search.'
    }
}

# About Information
ABOUT_INFO = {
    'app_name': 'Vehicle Violation Management System',
    'version': '1.0.0',
    'developer': 'Your Name',
    'description': 'A comprehensive system for managing traffic violation records with full CRUD operations.',
    'database': 'MySQL via XAMPP',
    'framework': 'Tkinter Python GUI',
    'license': 'MIT License'
}


def get_database_config():
    """Get database configuration"""
    return DATABASE_CONFIG


def get_app_config():
    """Get application configuration"""
    return APP_CONFIG


def get_default_fine(violation_type):
    """Get default fine amount for violation type"""
    return DEFAULT_FINES.get(violation_type, 100.00)


def validate_fine_amount(amount):
    """Validate fine amount"""
    try:
        fine = float(amount)
        rules = VALIDATION_RULES['fine_amount']
        return rules['min_value'] <= fine <= rules['max_value']
    except ValueError:
        return False


# Test configuration
if __name__ == "__main__":
    print("=" * 60)
    print("Vehicle Violation System - Configuration")
    print("=" * 60)
    
    print("\n[Database Configuration]")
    for key, value in DATABASE_CONFIG.items():
        print(f"  {key}: {value}")
    
    print("\n[Application Settings]")
    for key, value in APP_CONFIG.items():
        print(f"  {key}: {value}")
    
    print("\n[Vehicle Types]")
    for vtype in VEHICLE_TYPES:
        print(f"  • {vtype}")
    
    print("\n[Violation Types with Default Fines]")
    for vtype, fine in DEFAULT_FINES.items():
        print(f"  • {vtype}: ${fine:.2f}")
    
    print("\n✓ Configuration loaded successfully!")