import sqlite3

class EmployeeDB:
    def __init__(self, db_name='employees.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()
    
    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                department TEXT,
                salary REAL
            )
        ''')
        self.conn.commit()
    
    def add_employee(self, name, department, salary):
        self.cursor.execute('''
            INSERT INTO employees (name, department, salary)
            VALUES (?, ?, ?)
        ''', (name, department, salary))
        self.conn.commit()
        print(f"✓ Added {name}")
    
    def get_all(self):
        self.cursor.execute('SELECT * FROM employees')
        return self.cursor.fetchall()
    
    def search_by_name(self, name):
        self.cursor.execute('''
            SELECT * FROM employees 
            WHERE name LIKE ?
        ''', (f'%{name}%',))
        return self.cursor.fetchall()
    
    def update_salary(self, employee_id, new_salary):
        self.cursor.execute('''
            UPDATE employees 
            SET salary = ? 
            WHERE id = ?
        ''', (new_salary, employee_id))
        self.conn.commit()
        print(f"✓ Updated salary for ID {employee_id}")
    
    def delete_employee(self, employee_id):
        self.cursor.execute('DELETE FROM employees WHERE id = ?', (employee_id,))
        self.conn.commit()
        print(f"✓ Deleted employee ID {employee_id}")
    
    def get_stats(self):
        self.cursor.execute('''
            SELECT 
                COUNT(*) as total,
                AVG(salary) as avg_salary,
                MIN(salary) as min_salary,
                MAX(salary) as max_salary
            FROM employees
        ''')
        return self.cursor.fetchone()
    
    def close(self):
        self.conn.close()

# Usage Example
if __name__ == "__main__":
    db = EmployeeDB()
    
    # Add employees
    db.add_employee("Alice", "IT", 75000)
    db.add_employee("Bob", "Sales", 60000)
    db.add_employee("Charlie", "IT", 80000)
    
    # View all
    print("\nAll Employees:")
    for emp in db.get_all():
        print(emp)
    
    # Search
    print("\nSearch for 'Alice':")
    for emp in db.search_by_name("Alice"):
        print(emp)
    
    # Update
    db.update_salary(1, 85000)
    
    # Statistics
    total, avg, min_sal, max_sal = db.get_stats()
    print(f"\nStats: {total} employees, Avg: ${avg:,.0f}")
    
    db.close()