# Simple Company Management - Python Tutorial

A beginner-friendly project using OOP, SQL, CSV, and Pandas.

---

## 🎯 What We'll Build

A simple employee management system that can:
- Add and view employees
- Save data to a database
- Import/Export CSV files
- Analyze employee data

---

## 📦 Setup

```bash
pip install pandas
```

---

## Step 1: Create an Employee Class (OOP)

**File: `employee.py`**

```python
class Employee:
    """Represents a company employee"""
    
    def __init__(self, id, name, department, salary):
        self.id = id
        self.name = name
        self.department = department
        self.salary = salary
    
    def give_raise(self, percent):
        """Increase salary by percentage"""
        self.salary = self.salary * (1 + percent/100)
        return self.salary
    
    def __str__(self):
        return f"{self.name} - {self.department} - ${self.salary:,.0f}"

# Test it
if __name__ == "__main__":
    emp = Employee(1, "John Doe", "IT", 60000)
    print(emp)
    emp.give_raise(10)
    print(f"After raise: ${emp.salary:,.0f}")
```

**Output:**
```
John Doe - IT - $60,000
After raise: $66,000
```

---

## Step 2: Work with CSV Files

**File: `csv_demo.py`**

```python
import csv
from employee import Employee

# Write employees to CSV
def save_to_csv(employees, filename='employees.csv'):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['ID', 'Name', 'Department', 'Salary'])
        
        for emp in employees:
            writer.writerow([emp.id, emp.name, emp.department, emp.salary])
    print(f"Saved {len(employees)} employees to {filename}")

# Read employees from CSV
def load_from_csv(filename='employees.csv'):
    employees = []
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            emp = Employee(
                int(row['ID']),
                row['Name'],
                row['Department'],
                float(row['Salary'])
            )
            employees.append(emp)
    print(f"Loaded {len(employees)} employees")
    return employees

# Test it
if __name__ == "__main__":
    # Create sample employees
    employees = [
        Employee(1, "Alice", "IT", 70000),
        Employee(2, "Bob", "Sales", 55000),
        Employee(3, "Charlie", "IT", 80000)
    ]
    
    # Save to CSV
    save_to_csv(employees)
    
    # Load from CSV
    loaded = load_from_csv('employees.csv')
    for emp in loaded:
        print(emp)
```

---

## Step 3: Use SQL Database

**File: `database.py`**

```python
import sqlite3
from employee import Employee

class EmployeeDB:
    """Manages employee database"""
    
    def __init__(self, db_name='company.db'):
        self.conn = sqlite3.connect(db_name)
        self.create_table()
    
    def create_table(self):
        """Create employees table"""
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY,
                name TEXT,
                department TEXT,
                salary REAL
            )
        ''')
        self.conn.commit()
    
    def add_employee(self, emp):
        """Add employee to database"""
        self.conn.execute(
            'INSERT OR REPLACE INTO employees VALUES (?, ?, ?, ?)',
            (emp.id, emp.name, emp.department, emp.salary)
        )
        self.conn.commit()
        print(f"Added {emp.name} to database")
    
    def get_all(self):
        """Get all employees"""
        cursor = self.conn.execute('SELECT * FROM employees')
        employees = []
        for row in cursor:
            emp = Employee(row[0], row[1], row[2], row[3])
            employees.append(emp)
        return employees
    
    def get_by_department(self, department):
        """Get employees by department"""
        cursor = self.conn.execute(
            'SELECT * FROM employees WHERE department = ?',
            (department,)
        )
        return [Employee(r[0], r[1], r[2], r[3]) for r in cursor]
    
    def close(self):
        self.conn.close()

# Test it
if __name__ == "__main__":
    db = EmployeeDB()
    
    # Add employees
    db.add_employee(Employee(1, "Alice", "IT", 70000))
    db.add_employee(Employee(2, "Bob", "Sales", 55000))
    db.add_employee(Employee(3, "Charlie", "IT", 80000))
    
    # Get all employees
    print("\nAll Employees:")
    for emp in db.get_all():
        print(emp)
    
    # Get IT employees
    print("\nIT Department:")
    for emp in db.get_by_department("IT"):
        print(emp)
    
    db.close()
```

---

## Step 4: Analyze Data with Pandas

**File: `analytics.py`**

```python
import pandas as pd
import sqlite3

def analyze_employees(db_name='company.db'):
    """Analyze employee data using Pandas"""
    
    # Load data from database
    conn = sqlite3.connect(db_name)
    df = pd.read_sql_query('SELECT * FROM employees', conn)
    conn.close()
    
    print("=== Employee Data ===")
    print(df)
    
    print("\n=== Summary Statistics ===")
    print(df.describe())
    
    print("\n=== Average Salary by Department ===")
    dept_avg = df.groupby('department')['salary'].mean()
    print(dept_avg)
    
    print("\n=== Employee Count by Department ===")
    dept_count = df['department'].value_counts()
    print(dept_count)
    
    # Export analysis to CSV
    dept_summary = df.groupby('department').agg({
        'id': 'count',
        'salary': ['mean', 'min', 'max']
    })
    dept_summary.to_csv('department_summary.csv')
    print("\n✓ Saved analysis to department_summary.csv")
    
    return df

# Test it
if __name__ == "__main__":
    analyze_employees()
```

---

## Step 5: Complete Application

**File: `main.py`**

```python
from employee import Employee
from database import EmployeeDB
from analytics import analyze_employees
import pandas as pd

class CompanyApp:
    """Simple company management application"""
    
    def __init__(self):
        self.db = EmployeeDB()
    
    def menu(self):
        """Display menu"""
        print("\n" + "="*40)
        print("  COMPANY MANAGEMENT SYSTEM")
        print("="*40)
        print("1. Add Employee")
        print("2. View All Employees")
        print("3. View by Department")
        print("4. Analyze Data")
        print("5. Export to CSV")
        print("0. Exit")
        print("="*40)
    
    def add_employee(self):
        """Add new employee"""
        print("\n--- Add Employee ---")
        id = int(input("ID: "))
        name = input("Name: ")
        dept = input("Department: ")
        salary = float(input("Salary: "))
        
        emp = Employee(id, name, dept, salary)
        self.db.add_employee(emp)
    
    def view_all(self):
        """View all employees"""
        print("\n--- All Employees ---")
        employees = self.db.get_all()
        for emp in employees:
            print(emp)
        print(f"\nTotal: {len(employees)} employees")
    
    def view_by_dept(self):
        """View employees by department"""
        dept = input("\nEnter department: ")
        print(f"\n--- {dept} Department ---")
        employees = self.db.get_by_department(dept)
        for emp in employees:
            print(emp)
    
    def analyze(self):
        """Run data analysis"""
        print("\n--- Data Analysis ---")
        analyze_employees()
    
    def export_csv(self):
        """Export to CSV"""
        import sqlite3
        conn = sqlite3.connect('company.db')
        df = pd.read_sql_query('SELECT * FROM employees', conn)
        df.to_csv('employees_export.csv', index=False)
        conn.close()
        print("\n✓ Exported to employees_export.csv")
    
    def run(self):
        """Run the application"""
        while True:
            self.menu()
            choice = input("\nChoice: ")
            
            if choice == '1':
                self.add_employee()
            elif choice == '2':
                self.view_all()
            elif choice == '3':
                self.view_by_dept()
            elif choice == '4':
                self.analyze()
            elif choice == '5':
                self.export_csv()
            elif choice == '0':
                print("\nGoodbye!")
                self.db.close()
                break
            else:
                print("Invalid choice!")

# Run the app
if __name__ == "__main__":
    app = CompanyApp()
    app.run()
```

---

## Quick Start Guide

### 1. Create the files

Create these 5 files:
- `employee.py` (Step 1)
- `csv_demo.py` (Step 2)
- `database.py` (Step 3)
- `analytics.py` (Step 4)
- `main.py` (Step 5)

### 2. Add sample data

Run this once to add test data:

```python
# add_sample_data.py
from employee import Employee
from database import EmployeeDB

db = EmployeeDB()

employees = [
    Employee(1, "Alice Johnson", "IT", 70000),
    Employee(2, "Bob Smith", "Sales", 55000),
    Employee(3, "Charlie Brown", "IT", 80000),
    Employee(4, "Diana Prince", "Sales", 60000),
    Employee(5, "Eve Wilson", "HR", 50000),
]

for emp in employees:
    db.add_employee(emp)

db.close()
print("✓ Sample data added!")
```

```bash
python add_sample_data.py
```

### 3. Run the app

```bash
python main.py
```

---

## What You Learned

### OOP (Object-Oriented Programming)
- ✓ Created a `class` (Employee)
- ✓ Used `__init__` constructor
- ✓ Added methods (functions in a class)
- ✓ Used `self` to access object data

### SQL Database
- ✓ Created a database table
- ✓ INSERT data into database
- ✓ SELECT data with queries
- ✓ Filter data with WHERE clause

### CSV Files
- ✓ Write data to CSV with `csv.writer`
- ✓ Read data from CSV with `csv.DictReader`
- ✓ Handle file operations

### Pandas
- ✓ Load data into DataFrame
- ✓ Calculate statistics with `describe()`
- ✓ Group data with `groupby()`
- ✓ Export analysis to CSV

---

## Practice Exercises

**Easy:**
1. Add a method to calculate annual salary (salary × 12)
2. Add a new employee through the menu
3. Export data to a different CSV filename

**Medium:**
1. Add a feature to delete an employee
2. Add a search by name function
3. Calculate total company salary cost

**Challenge:**
1. Add a `Manager` class that inherits from `Employee`
2. Add a bonus field and calculate total compensation
3. Create a chart showing salaries by department

---

## Common Issues

**Problem:** `ModuleNotFoundError`
```bash
# Solution: Install pandas
pip install pandas
```

**Problem:** `FileNotFoundError` for CSV
```python
# Solution: Check if file exists first
import os
if os.path.exists('employees.csv'):
    # load file
```

**Problem:** Database locked
```python
# Solution: Always close database
db.close()
```

---

## Next Steps

1. ✨ Add more fields (email, phone, hire_date)
2. 📊 Create visualizations with matplotlib
3. 🌐 Build a web interface with Flask
4. 🔐 Add user authentication
5. ☁️ Deploy to the cloud

---

**That's it! You now have a working company management system! 🎉**
