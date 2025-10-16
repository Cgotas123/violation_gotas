# Vehicle Violation Management System

This system manages vehicle violations using a Python GUI and MySQL database.

## Revisions

Based on the panel's recommendations, we have implemented the following revisions for the login/registration system:

1. **User Authentication**
   - Added secure login and registration functionality
   - Implemented password hashing for security
   - Created user sessions for dashboard access

2. **Database Integration**
   - Added users table to store account information
   - Linked violations to logged-in officers

3. **UI Improvements**
   - Modernized login window design
   - Added logout button to main dashboard
   - Improved form validation and error messages

## File Structure

Key files for the login/registration system:

- `app.py`: Main application entry point
- `auth.py`: Authentication logic
- `login_window.py`: Login/registration UI
- `database.py`: Database operations (extended for user management)
- `requirements.txt`: Dependencies

## Setup Instructions

1. Install requirements: `pip install -r requirements.txt`
2. Start XAMPP and run MySQL
3. Run the application: `python app.py`

## GitHub Repository

https://github.com/Cgotas123/violation_gotas.git
