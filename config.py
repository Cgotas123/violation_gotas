"""
config.py - Configuration File for Vehicle Violation System
"""

# Database Configuration for XAMPP MySQL
# CONNECTS TO YOUR EXISTING DATABASE
DATABASE_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  # Change if you set a MySQL password
    'database': 'vehicle_violations_db',  # YOUR EXISTING DATABASE NAME
    'port': 3306
}

# Application Settings
APP_CONFIG = {
    'title': '🚗 Vehicle Violation Management System',
    'version': '2.0.0',
    'window_width': 1400,
    'window_height': 800,
    'min_width': 1200,
    'min_height': 600
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
    "Bicycle",
    "Tricycle"
]

VIOLATION_TYPES = [
    "Speeding",
    "Illegal Parking",
    "Running Red Light",
    "No License",
    "No Registration",
    "Expired License",
    "Reckless Driving",
    "No Insurance",
    "Improper Lane Change",
    "No Seatbelt",
    "Using Phone While Driving",
    "Illegal U-Turn",
    "Overloading",
    "Tinted Windows",
    "Modified Exhaust",
    "No Helmet (Motorcycle)",
    "Driving Under Influence (DUI)",
    "Illegal Overtaking",
    "Obstruction",
    "Other"
]

STATUS_TYPES = [
    "Pending",
    "Paid",
    "Cancelled",
    "Under Review"
]

# Default Fine Amounts (in Philippine Peso)
DEFAULT_FINES = {
    "Speeding": 1200.00,
    "Illegal Parking": 500.00,
    "Running Red Light": 1000.00,
    "No License": 3000.00,
    "No Registration": 10000.00,
    "Expired License": 3000.00,
    "Reckless Driving": 2000.00,
    "No Insurance": 5000.00,
    "Improper Lane Change": 1000.00,
    "No Seatbelt": 1000.00,
    "Using Phone While Driving": 1200.00,
    "Illegal U-Turn": 500.00,
    "Overloading": 1000.00,
    "Tinted Windows": 1500.00,
    "Modified Exhaust": 1500.00,
    "No Helmet (Motorcycle)": 1500.00,
    "Driving Under Influence (DUI)": 20000.00,
    "Illegal Overtaking": 1200.00,
    "Obstruction": 1000.00,
    "Other": 500.00
}

# Messages
MESSAGES = {
    'success': {
        'create': 'Violation record created successfully!',
        'update': 'Violation record updated successfully!',
        'delete': 'Violation record deleted successfully!'
    },
    'error': {
        'database': 'Database connection error. Please ensure XAMPP MySQL is running.',
        'validation': 'Please fill in all required fields correctly.',
        'not_selected': 'Please select a violation record first.'
    },
    'warning': {
        'empty_fields': 'Please fill in all required fields.',
        'invalid_amount': 'Please enter a valid fine amount.',
        'delete_confirm': 'Are you sure you want to delete this record?'
    }
}

def get_default_fine(violation_type):
    """Get default fine amount for violation type"""
    return DEFAULT_FINES.get(violation_type, 500.00)