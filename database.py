"""
database.py - MySQL Database Handler for XAMPP
Vehicle Violation Management System
"""

import mysql.connector
from mysql.connector import Error
from datetime import datetime
from typing import List, Tuple, Optional

class ViolationDatabase:
    def __init__(self):
        """Initialize MySQL database connection"""
        self.connection = None
        self.cursor = None
        self.connect()
        self.create_database()
        self.create_tables()
    
    def connect(self):
        """Connect to MySQL server (XAMPP)"""
        try:
            print("  - Attempting MySQL connection...")
            print(f"    Host: localhost")
            print(f"    User: root")
            print(f"    Port: 3306")
            
            self.connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',  # Default XAMPP password is empty
                port=3306,
                connect_timeout=10
            )
            self.cursor = self.connection.cursor()
            print("✓ Connected to MySQL server")
        except Error as e:
            error_code = e.errno if hasattr(e, 'errno') else 'Unknown'
            print(f"\n✗ MySQL connection error!")
            print(f"   Error Code: {error_code}")
            print(f"   Error Message: {e}")
            
            if error_code == 2003:
                raise Exception("Cannot connect to MySQL server. Is XAMPP MySQL running?")
            elif error_code == 1045:
                raise Exception("Access denied. Check MySQL username/password.")
            elif error_code == 2002:
                raise Exception("MySQL server is not responding. Check if port 3306 is available.")
            else:
                raise Exception(f"MySQL Error ({error_code}): {e}")
    
    def create_database(self):
        """Use existing database"""
        try:
            self.cursor.execute("USE vehicle_violations_db")
            self.connection.commit()
            print("✓ Connected to existing database: vehicle_violations_db")
        except Error as e:
            print(f"✗ Database error: {e}")
            raise Exception(f"Cannot connect to database 'vehicle_violations_db'. Make sure it exists!")
    
    def create_tables(self):
        """Check if violations table exists"""
        try:
            # Just verify table exists, don't create
            self.cursor.execute("SHOW TABLES LIKE 'violations'")
            result = self.cursor.fetchone()
            
            if result:
                print("✓ Connected to existing 'violations' table")
            else:
                print("⚠ Warning: 'violations' table not found!")
                # Create table if it doesn't exist
                create_table_query = """
                    CREATE TABLE violations (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        plate_number VARCHAR(20) NOT NULL,
                        vehicle_type VARCHAR(50) NOT NULL,
                        violation_type VARCHAR(100) NOT NULL,
                        location VARCHAR(255) NOT NULL,
                        fine_amount DECIMAL(10, 2) NOT NULL,
                        date_time DATETIME NOT NULL,
                        officer_name VARCHAR(100) NOT NULL,
                        status VARCHAR(50) DEFAULT 'Pending',
                        notes TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """
                self.cursor.execute(create_table_query)
                self.connection.commit()
                print("✓ Table 'violations' created")
        except Error as e:
            print(f"✗ Table check error: {e}")
            raise
    
    def create_violation(self, plate_number: str, vehicle_type: str, 
                        violation_type: str, location: str, fine_amount: float,
                        officer_name: str, status: str = 'Pending', 
                        notes: str = '') -> int:
        """Insert a new violation record"""
        try:
            date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            query = """
                INSERT INTO violations 
                (plate_number, vehicle_type, violation_type, location, 
                 fine_amount, date_time, officer_name, status, notes)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            values = (
                plate_number.upper(), vehicle_type, violation_type, 
                location, fine_amount, date_time, officer_name, status, notes
            )
            
            self.cursor.execute(query, values)
            self.connection.commit()
            
            violation_id = self.cursor.lastrowid
            print(f"✓ Violation created with ID: {violation_id}")
            return violation_id
            
        except Error as e:
            print(f"✗ Error creating violation: {e}")
            raise
    
    def get_all_violations(self) -> List[Tuple]:
        """Retrieve all violation records"""
        try:
            query = """
                SELECT id, plate_number, vehicle_type, violation_type, 
                       location, fine_amount, date_time, status
                FROM violations
                ORDER BY date_time DESC
            """
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Error as e:
            print(f"✗ Error fetching violations: {e}")
            return []
    
    def search_violations(self, search_term: str) -> List[Tuple]:
        """Search violations by plate number, violation type, or location"""
        try:
            query = """
                SELECT id, plate_number, vehicle_type, violation_type, 
                       location, fine_amount, date_time, status
                FROM violations
                WHERE plate_number LIKE %s 
                   OR violation_type LIKE %s 
                   OR location LIKE %s
                ORDER BY date_time DESC
            """
            search_pattern = f'%{search_term}%'
            self.cursor.execute(query, (search_pattern, search_pattern, search_pattern))
            return self.cursor.fetchall()
        except Error as e:
            print(f"✗ Error searching violations: {e}")
            return []
    
    def update_violation(self, violation_id: int, plate_number: str, 
                        vehicle_type: str, violation_type: str, location: str,
                        fine_amount: float, officer_name: str, status: str,
                        notes: str) -> bool:
        """Update an existing violation record"""
        try:
            query = """
                UPDATE violations 
                SET plate_number = %s, vehicle_type = %s, violation_type = %s,
                    location = %s, fine_amount = %s, officer_name = %s,
                    status = %s, notes = %s
                WHERE id = %s
            """
            
            values = (
                plate_number.upper(), vehicle_type, violation_type, location,
                fine_amount, officer_name, status, notes, violation_id
            )
            
            self.cursor.execute(query, values)
            self.connection.commit()
            
            if self.cursor.rowcount > 0:
                print(f"✓ Violation {violation_id} updated successfully")
                return True
            else:
                print(f"✗ No violation found with ID: {violation_id}")
                return False
                
        except Error as e:
            print(f"✗ Error updating violation: {e}")
            return False
    
    def delete_violation(self, violation_id: int) -> bool:
        """Delete a violation record"""
        try:
            query = 'DELETE FROM violations WHERE id = %s'
            self.cursor.execute(query, (violation_id,))
            self.connection.commit()
            
            if self.cursor.rowcount > 0:
                print(f"✓ Violation {violation_id} deleted successfully")
                return True
            else:
                print(f"✗ No violation found with ID: {violation_id}")
                return False
                
        except Error as e:
            print(f"✗ Error deleting violation: {e}")
            return False
    
    def close(self):
        """Close database connection"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print("✓ Database connection closed")

# Test the database
if __name__ == "__main__":
    print("=" * 60)
    print("Testing Vehicle Violation Database (MySQL/XAMPP)")
    print("=" * 60)
    
    try:
        db = ViolationDatabase()
        
        print("\n[TEST] Creating sample violations...")
        id1 = db.create_violation("ABC123", "Car", "Speeding", "Main St", 2000.00, "Officer Smith")
        id2 = db.create_violation("XYZ789", "Motorcycle", "Illegal Parking", "5th Ave", 500.00, "Officer Jones")
        
        print("\n[TEST] Reading all violations...")
        violations = db.get_all_violations()
        for v in violations:
            print(f"  ID: {v[0]}, Plate: {v[1]}, Type: {v[3]}, Fine: ₱{v[5]}")
        
        print("\n✓ All tests passed!")
        db.close()
        
    except Exception as e:
        print(f"\n✗ Test failed: {e}")