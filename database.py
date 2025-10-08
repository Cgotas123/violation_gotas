"""
database.py - Database Layer for Vehicle Violation System
Handles all database operations (CRUD) - MySQL/MariaDB via XAMPP
"""

import mysql.connector
from mysql.connector import Error
from datetime import datetime
from typing import List, Tuple, Optional

class ViolationDatabase:
    def __init__(self, host='localhost', user='root', password='', database='vehicle_violations_db'):
        """Initialize database connection to XAMPP MySQL"""
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.conn = None
        self.cursor = None
        self.connect()
        self.create_database()
        self.create_tables()
    
    def connect(self):
        """Establish database connection to MySQL"""
        try:
            # First connect without database to create it if needed
            self.conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password
            )
            self.cursor = self.conn.cursor()
            print(f"✓ Connected to MySQL server")
        except Error as e:
            print(f"✗ Database connection error: {e}")
            raise
    
    def create_database(self):
        """Create database if it doesn't exist"""
        try:
            self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")
            self.cursor.execute(f"USE {self.database}")
            self.conn.commit()
            print(f"✓ Database '{self.database}' created/selected successfully")
        except Error as e:
            print(f"✗ Error creating database: {e}")
            raise
    
    def create_tables(self):
        """Create violations table if it doesn't exist"""
        try:
            create_table_query = '''
                CREATE TABLE IF NOT EXISTS violations (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    plate_number VARCHAR(20) NOT NULL,
                    vehicle_type VARCHAR(50) NOT NULL,
                    violation_type VARCHAR(100) NOT NULL,
                    location VARCHAR(255) NOT NULL,
                    fine_amount DECIMAL(10, 2) NOT NULL,
                    date_time DATETIME NOT NULL,
                    officer_name VARCHAR(100) NOT NULL,
                    status VARCHAR(20) DEFAULT 'Pending',
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    INDEX idx_plate (plate_number),
                    INDEX idx_status (status),
                    INDEX idx_date (date_time)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            '''
            self.cursor.execute(create_table_query)
            self.conn.commit()
            print("✓ Tables created/verified successfully")
        except Error as e:
            print(f"✗ Error creating tables: {e}")
            raise
    
    # CREATE - Insert new violation
    def create_violation(self, plate_number: str, vehicle_type: str, 
                        violation_type: str, location: str, fine_amount: float,
                        officer_name: str, status: str = 'Pending', 
                        notes: str = '') -> int:
        """Insert a new violation record"""
        try:
            date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            query = '''
                INSERT INTO violations 
                (plate_number, vehicle_type, violation_type, location, 
                 fine_amount, date_time, officer_name, status, notes)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            '''
            
            values = (
                plate_number.upper(), vehicle_type, violation_type, 
                location, fine_amount, date_time, officer_name, status, notes
            )
            
            self.cursor.execute(query, values)
            self.conn.commit()
            
            violation_id = self.cursor.lastrowid
            print(f"✓ Violation created with ID: {violation_id}")
            return violation_id
            
        except Error as e:
            print(f"✗ Error creating violation: {e}")
            self.conn.rollback()
            raise
    
    # READ - Get all violations
    def get_all_violations(self) -> List[Tuple]:
        """Retrieve all violation records"""
        try:
            query = '''
                SELECT id, plate_number, vehicle_type, violation_type, 
                       fine_amount, date_time, status
                FROM violations
                ORDER BY date_time DESC
            '''
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Error as e:
            print(f"✗ Error fetching violations: {e}")
            return []
    
    # READ - Get violation by ID
    def get_violation_by_id(self, violation_id: int) -> Optional[Tuple]:
        """Retrieve a specific violation by ID"""
        try:
            query = 'SELECT * FROM violations WHERE id = %s'
            self.cursor.execute(query, (violation_id,))
            return self.cursor.fetchone()
        except Error as e:
            print(f"✗ Error fetching violation: {e}")
            return None
    
    # READ - Search violations
    def search_violations(self, search_term: str) -> List[Tuple]:
        """Search violations by plate number, violation type, or location"""
        try:
            query = '''
                SELECT id, plate_number, vehicle_type, violation_type, 
                       fine_amount, date_time, status
                FROM violations
                WHERE plate_number LIKE %s 
                   OR violation_type LIKE %s 
                   OR location LIKE %s
                   OR officer_name LIKE %s
                ORDER BY date_time DESC
            '''
            search_pattern = f'%{search_term}%'
            self.cursor.execute(query, (search_pattern, search_pattern, 
                                       search_pattern, search_pattern))
            return self.cursor.fetchall()
        except Error as e:
            print(f"✗ Error searching violations: {e}")
            return []
    
    # READ - Filter by status
    def get_violations_by_status(self, status: str) -> List[Tuple]:
        """Get violations filtered by status"""
        try:
            query = '''
                SELECT id, plate_number, vehicle_type, violation_type, 
                       fine_amount, date_time, status
                FROM violations
                WHERE status = %s
                ORDER BY date_time DESC
            '''
            self.cursor.execute(query, (status,))
            return self.cursor.fetchall()
        except Error as e:
            print(f"✗ Error filtering violations: {e}")
            return []
    
    # UPDATE - Update violation
    def update_violation(self, violation_id: int, plate_number: str, 
                        vehicle_type: str, violation_type: str, location: str,
                        fine_amount: float, officer_name: str, status: str,
                        notes: str) -> bool:
        """Update an existing violation record"""
        try:
            query = '''
                UPDATE violations 
                SET plate_number = %s, vehicle_type = %s, violation_type = %s,
                    location = %s, fine_amount = %s, officer_name = %s,
                    status = %s, notes = %s
                WHERE id = %s
            '''
            
            values = (
                plate_number.upper(), vehicle_type, violation_type, location,
                fine_amount, officer_name, status, notes, violation_id
            )
            
            self.cursor.execute(query, values)
            self.conn.commit()
            
            if self.cursor.rowcount > 0:
                print(f"✓ Violation {violation_id} updated successfully")
                return True
            else:
                print(f"✗ No violation found with ID: {violation_id}")
                return False
                
        except Error as e:
            print(f"✗ Error updating violation: {e}")
            self.conn.rollback()
            return False
    
    # UPDATE - Update status only
    def update_status(self, violation_id: int, status: str) -> bool:
        """Update only the status of a violation"""
        try:
            query = '''
                UPDATE violations 
                SET status = %s
                WHERE id = %s
            '''
            
            self.cursor.execute(query, (status, violation_id))
            self.conn.commit()
            
            if self.cursor.rowcount > 0:
                print(f"✓ Status updated for violation {violation_id}")
                return True
            else:
                print(f"✗ No violation found with ID: {violation_id}")
                return False
                
        except Error as e:
            print(f"✗ Error updating status: {e}")
            self.conn.rollback()
            return False
    
    # DELETE - Delete violation
    def delete_violation(self, violation_id: int) -> bool:
        """Delete a violation record"""
        try:
            query = 'DELETE FROM violations WHERE id = %s'
            self.cursor.execute(query, (violation_id,))
            self.conn.commit()
            
            if self.cursor.rowcount > 0:
                print(f"✓ Violation {violation_id} deleted successfully")
                return True
            else:
                print(f"✗ No violation found with ID: {violation_id}")
                return False
                
        except Error as e:
            print(f"✗ Error deleting violation: {e}")
            self.conn.rollback()
            return False
    
    # STATISTICS
    def get_statistics(self) -> dict:
        """Get violation statistics"""
        try:
            stats = {}
            
            # Total violations
            self.cursor.execute('SELECT COUNT(*) FROM violations')
            stats['total'] = self.cursor.fetchone()[0]
            
            # By status
            self.cursor.execute('SELECT COUNT(*) FROM violations WHERE status = "Pending"')
            stats['pending'] = self.cursor.fetchone()[0]
            
            self.cursor.execute('SELECT COUNT(*) FROM violations WHERE status = "Paid"')
            stats['paid'] = self.cursor.fetchone()[0]
            
            self.cursor.execute('SELECT COUNT(*) FROM violations WHERE status = "Cancelled"')
            stats['cancelled'] = self.cursor.fetchone()[0]
            
            # Total revenue
            self.cursor.execute('SELECT SUM(fine_amount) FROM violations WHERE status = "Paid"')
            result = self.cursor.fetchone()[0]
            stats['revenue'] = float(result) if result else 0.0
            
            # Top violation types
            self.cursor.execute('''
                SELECT violation_type, COUNT(*) as count 
                FROM violations 
                GROUP BY violation_type 
                ORDER BY count DESC 
                LIMIT 5
            ''')
            stats['top_violations'] = self.cursor.fetchall()
            
            # Top violators
            self.cursor.execute('''
                SELECT plate_number, COUNT(*) as count 
                FROM violations 
                GROUP BY plate_number 
                ORDER BY count DESC 
                LIMIT 5
            ''')
            stats['top_violators'] = self.cursor.fetchall()
            
            return stats
            
        except Error as e:
            print(f"✗ Error getting statistics: {e}")
            return {}
    
    def close(self):
        """Close database connection"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
            print("✓ Database connection closed")
    
    def __del__(self):
        """Destructor to ensure connection is closed"""
        self.close()


# Test the database functions
if __name__ == "__main__":
    print("=" * 60)
    print("Testing Vehicle Violation Database (MySQL/XAMPP)")
    print("=" * 60)
    
    try:
        # Initialize database
        db = ViolationDatabase()
        
        # Test CREATE
        print("\n[TEST] Creating sample violations...")
        id1 = db.create_violation("ABC123", "Car", "Speeding", "Main St", 150.00, "Officer Smith")
        id2 = db.create_violation("XYZ789", "Motorcycle", "Illegal Parking", "5th Ave", 75.00, "Officer Jones", "Pending", "Near park entrance")
        
        # Test READ
        print("\n[TEST] Reading all violations...")
        violations = db.get_all_violations()
        for v in violations:
            print(f"  ID: {v[0]}, Plate: {v[1]}, Type: {v[3]}, Fine: ${v[4]}")
        
        # Test UPDATE
        print("\n[TEST] Updating status...")
        db.update_status(id1, "Paid")
        
        # Test SEARCH
        print("\n[TEST] Searching for 'ABC'...")
        results = db.search_violations("ABC")
        print(f"  Found {len(results)} result(s)")
        
        # Test STATISTICS
        print("\n[TEST] Getting statistics...")
        stats = db.get_statistics()
        print(f"  Total: {stats['total']}, Pending: {stats['pending']}, Paid: {stats['paid']}")
        print(f"  Revenue: ${stats['revenue']:.2f}")
        
        print("\n✓ All tests completed!")
        
    except Exception as e:
        print(f"\n✗ Test failed: {e}")