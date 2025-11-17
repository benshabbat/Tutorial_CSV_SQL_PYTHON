# Python OOP + SQL + Pandas + CSV - Complete Guide

A step-by-step beginner tutorial showing how everything connects.

---

## 🎯 What You'll Learn

1. Work with CSV files
2. Connect to SQL database
3. Use Pandas with SQL
4. Build it all with OOP

---

## Step 1: Basic CSV Operations

### Read CSV

```python
import csv

# Read CSV file
with open('employees.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        print(f"{row['name']} - ${row['salary']}")
```

### Write CSV

```python
import csv

data = [
    {'name': 'Alice', 'department': 'IT', 'salary': 70000},
    {'name': 'Bob', 'department': 'Sales', 'salary': 60000}
]

with open('employees.csv', 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=['name', 'department', 'salary'])
    writer.writeheader()
    writer.writerows(data)
```

---

## Step 2: Basic SQL Operations

```python
import sqlite3

# Connect to database
conn = sqlite3.connect('company.db')
cursor = conn.cursor()

# Create table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY,
        name TEXT,
        department TEXT,
        salary REAL
    )
''')

# Insert data
cursor.execute('''
    INSERT INTO employees (id, name, department, salary)
    VALUES (1, 'Alice', 'IT', 70000)
''')
conn.commit()

# Read data
cursor.execute('SELECT * FROM employees')
for row in cursor.fetchall():
    print(row)

conn.close()
```

---

## Step 3: Connect Pandas with CSV

```python
import pandas as pd

# Read CSV with Pandas
df = pd.read_csv('employees.csv')
print(df)

# Analyze data
print("\nAverage Salary:", df['salary'].mean())
print("\nBy Department:")
print(df.groupby('department')['salary'].mean())

# Write to CSV
df.to_csv('output.csv', index=False)
```

---

## Step 4: Connect Pandas with SQL

### Load SQL data into Pandas

```python
import pandas as pd
import sqlite3

# Connect to database
conn = sqlite3.connect('company.db')

# Read SQL table into DataFrame
df = pd.read_sql_query('SELECT * FROM employees', conn)
print(df)

# Analyze
print("\nStatistics:")
print(df.describe())

conn.close()
```

### Write Pandas to SQL

```python
import pandas as pd
import sqlite3

# Create DataFrame
df = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie'],
    'department': ['IT', 'Sales', 'IT'],
    'salary': [70000, 60000, 80000]
})

# Connect to database
conn = sqlite3.connect('company.db')

# Write DataFrame to SQL table
df.to_sql('employees', conn, if_exists='replace', index=False)

conn.close()
print("✓ Data saved to SQL!")
```

---

## Step 5: CSV → SQL → Pandas (Complete Flow)

```python
import pandas as pd
import sqlite3

# 1. Read CSV with Pandas
print("Step 1: Reading CSV...")
df = pd.read_csv('employees.csv')
print(df)

# 2. Save to SQL database
print("\nStep 2: Saving to SQL...")
conn = sqlite3.connect('company.db')
df.to_sql('employees', conn, if_exists='replace', index=False)

# 3. Query from SQL back to Pandas
print("\nStep 3: Querying from SQL...")
query = '''
    SELECT department, AVG(salary) as avg_salary
    FROM employees
    GROUP BY department
'''
result = pd.read_sql_query(query, conn)
print(result)

# 4. Export analysis to new CSV
result.to_csv('analysis.csv', index=False)

conn.close()
print("\n✓ Complete!")
```

---

## Step 6: Without OOP (Procedural Style)

```python
import pandas as pd
import sqlite3

def create_database():
    """Create database and table"""
    conn = sqlite3.connect('company.db')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            department TEXT,
            salary REAL
        )
    ''')
    conn.commit()
    return conn

def add_employee(conn, name, department, salary):
    """Add employee to database"""
    conn.execute(
        'INSERT INTO employees (name, department, salary) VALUES (?, ?, ?)',
        (name, department, salary)
    )
    conn.commit()
    print(f"✓ Added {name}")

def get_all_employees(conn):
    """Get all employees as DataFrame"""
    df = pd.read_sql_query('SELECT * FROM employees', conn)
    return df

def analyze_salaries(conn):
    """Analyze salary data"""
    df = pd.read_sql_query('SELECT * FROM employees', conn)
    print("\n=== Salary Analysis ===")
    print(f"Average: ${df['salary'].mean():,.0f}")
    print(f"Max: ${df['salary'].max():,.0f}")
    print(f"\nBy Department:")
    print(df.groupby('department')['salary'].mean())

def export_to_csv(conn, filename='employees.csv'):
    """Export database to CSV"""
    df = pd.read_sql_query('SELECT * FROM employees', conn)
    df.to_csv(filename, index=False)
    print(f"✓ Exported to {filename}")

# Usage
conn = create_database()
add_employee(conn, "Alice", "IT", 70000)
add_employee(conn, "Bob", "Sales", 60000)
add_employee(conn, "Charlie", "IT", 80000)

print("\nAll Employees:")
print(get_all_employees(conn))

analyze_salaries(conn)
export_to_csv(conn)

conn.close()
```

---

## Step 7: With OOP (Object-Oriented Style)

```python
import pandas as pd
import sqlite3

class Employee:
    """Represents an employee"""
    
    def __init__(self, name, department, salary):
        self.name = name
        self.department = department
        self.salary = salary
    
    def __str__(self):
        return f"{self.name} - {self.department} - ${self.salary:,}"

class EmployeeDatabase:
    """Manages employees with SQL + Pandas"""
    
    def __init__(self, db_name='company.db'):
        self.db_name = db_name
        self.conn = sqlite3.connect(db_name)
        self.create_table()
    
    def create_table(self):
        """Create employees table"""
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                department TEXT,
                salary REAL
            )
        ''')
        self.conn.commit()
    
    def add_employee(self, employee):
        """Add employee to database"""
        self.conn.execute(
            'INSERT INTO employees (name, department, salary) VALUES (?, ?, ?)',
            (employee.name, employee.department, employee.salary)
        )
        self.conn.commit()
        print(f"✓ Added {employee.name}")
    
    def get_dataframe(self):
        """Get all employees as Pandas DataFrame"""
        return pd.read_sql_query('SELECT * FROM employees', self.conn)
    
    def analyze(self):
        """Analyze employee data using Pandas"""
        df = self.get_dataframe()
        
        print("\n=== Employee Analysis ===")
        print(f"Total Employees: {len(df)}")
        print(f"Average Salary: ${df['salary'].mean():,.0f}")
        print(f"\nSalary by Department:")
        print(df.groupby('department')['salary'].agg(['count', 'mean', 'max']))
    
    def export_to_csv(self, filename='employees.csv'):
        """Export to CSV using Pandas"""
        df = self.get_dataframe()
        df.to_csv(filename, index=False)
        print(f"✓ Exported to {filename}")
    
    def import_from_csv(self, filename='employees.csv'):
        """Import from CSV using Pandas"""
        df = pd.read_csv(filename)
        df.to_sql('employees', self.conn, if_exists='append', index=False)
        print(f"✓ Imported {len(df)} employees from {filename}")
    
    def close(self):
        """Close database connection"""
        self.conn.close()

# Usage
db = EmployeeDatabase()

# Add employees
db.add_employee(Employee("Alice", "IT", 70000))
db.add_employee(Employee("Bob", "Sales", 60000))
db.add_employee(Employee("Charlie", "IT", 80000))

# Get as DataFrame
print("\nAll Employees:")
print(db.get_dataframe())

# Analyze
db.analyze()

# Export to CSV
db.export_to_csv()

db.close()
```

---

## Step 8: Complete Application with OOP

```python
import pandas as pd
import sqlite3
import os

class Employee:
    """Represents an employee"""
    
    def __init__(self, id=None, name="", department="", salary=0):
        self.id = id
        self.name = name
        self.department = department
        self.salary = salary
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'name': self.name,
            'department': self.department,
            'salary': self.salary
        }
    
    def __str__(self):
        return f"ID {self.id}: {self.name} - {self.department} - ${self.salary:,.0f}"

class CompanyDatabase:
    """Complete company database manager using SQL + Pandas + CSV"""
    
    def __init__(self, db_name='company.db'):
        self.db_name = db_name
        self.conn = sqlite3.connect(db_name)
        self.setup()
    
    def setup(self):
        """Create necessary tables"""
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                department TEXT,
                salary REAL
            )
        ''')
        self.conn.commit()
    
    # === Basic CRUD Operations ===
    
    def add_employee(self, employee):
        """Add employee to database"""
        cursor = self.conn.execute(
            'INSERT INTO employees (name, department, salary) VALUES (?, ?, ?)',
            (employee.name, employee.department, employee.salary)
        )
        self.conn.commit()
        print(f"✓ Added {employee.name} (ID: {cursor.lastrowid})")
        return cursor.lastrowid
    
    def get_all_employees(self):
        """Get all employees as list of Employee objects"""
        cursor = self.conn.execute('SELECT * FROM employees')
        employees = []
        for row in cursor:
            emp = Employee(row[0], row[1], row[2], row[3])
            employees.append(emp)
        return employees
    
    def update_salary(self, emp_id, new_salary):
        """Update employee salary"""
        self.conn.execute(
            'UPDATE employees SET salary = ? WHERE id = ?',
            (new_salary, emp_id)
        )
        self.conn.commit()
        print(f"✓ Updated salary for employee {emp_id}")
    
    def delete_employee(self, emp_id):
        """Delete employee"""
        self.conn.execute('DELETE FROM employees WHERE id = ?', (emp_id,))
        self.conn.commit()
        print(f"✓ Deleted employee {emp_id}")
    
    # === Pandas Operations ===
    
    def get_dataframe(self):
        """Get all data as Pandas DataFrame"""
        return pd.read_sql_query('SELECT * FROM employees', self.conn)
    
    def analyze_data(self):
        """Analyze data using Pandas"""
        df = self.get_dataframe()
        
        if df.empty:
            print("No data to analyze")
            return
        
        print("\n" + "="*50)
        print("         EMPLOYEE DATA ANALYSIS")
        print("="*50)
        
        print(f"\nTotal Employees: {len(df)}")
        print(f"Total Departments: {df['department'].nunique()}")
        
        print(f"\nSalary Statistics:")
        print(f"  Average: ${df['salary'].mean():,.2f}")
        print(f"  Median:  ${df['salary'].median():,.2f}")
        print(f"  Min:     ${df['salary'].min():,.2f}")
        print(f"  Max:     ${df['salary'].max():,.2f}")
        
        print(f"\nBy Department:")
        dept_stats = df.groupby('department').agg({
            'id': 'count',
            'salary': ['mean', 'sum']
        })
        print(dept_stats)
    
    def filter_by_department(self, department):
        """Get employees from specific department using Pandas"""
        df = self.get_dataframe()
        filtered = df[df['department'] == department]
        return filtered
    
    def top_earners(self, n=5):
        """Get top N earners using Pandas"""
        df = self.get_dataframe()
        return df.nlargest(n, 'salary')[['name', 'department', 'salary']]
    
    # === CSV Operations ===
    
    def export_to_csv(self, filename='employees.csv'):
        """Export database to CSV using Pandas"""
        df = self.get_dataframe()
        df.to_csv(filename, index=False)
        print(f"✓ Exported {len(df)} employees to {filename}")
    
    def import_from_csv(self, filename='employees.csv'):
        """Import CSV to database using Pandas"""
        if not os.path.exists(filename):
            print(f"File {filename} not found!")
            return
        
        df = pd.read_csv(filename)
        df.to_sql('employees', self.conn, if_exists='append', index=False)
        print(f"✓ Imported {len(df)} employees from {filename}")
    
    def export_report(self, filename='report.csv'):
        """Export analyzed data to CSV"""
        df = self.get_dataframe()
        
        # Add calculated columns
        df['annual_salary'] = df['salary'] * 12
        df['salary_grade'] = pd.cut(df['salary'], 
                                     bins=[0, 60000, 80000, 100000],
                                     labels=['Junior', 'Mid', 'Senior'])
        
        df.to_csv(filename, index=False)
        print(f"✓ Report exported to {filename}")
    
    # === Display Methods ===
    
    def display_all(self):
        """Display all employees"""
        employees = self.get_all_employees()
        
        if not employees:
            print("No employees found")
            return
        
        print(f"\n{'ID':<5} {'Name':<15} {'Department':<12} {'Salary':<12}")
        print("-" * 50)
        for emp in employees:
            print(f"{emp.id:<5} {emp.name:<15} {emp.department:<12} ${emp.salary:<11,.0f}")
        print(f"\nTotal: {len(employees)} employees")
    
    def close(self):
        """Close database connection"""
        self.conn.close()

class CompanyApp:
    """Interactive application"""
    
    def __init__(self):
        self.db = CompanyDatabase()
    
    def menu(self):
        """Display menu"""
        print("\n" + "="*50)
        print("        COMPANY MANAGEMENT SYSTEM")
        print("="*50)
        print("1.  Add Employee")
        print("2.  View All Employees")
        print("3.  Update Salary")
        print("4.  Delete Employee")
        print("5.  Analyze Data (Pandas)")
        print("6.  View Top Earners")
        print("7.  Filter by Department")
        print("8.  Export to CSV")
        print("9.  Import from CSV")
        print("10. Export Report")
        print("0.  Exit")
        print("="*50)
    
    def run(self):
        """Run application"""
        while True:
            self.menu()
            choice = input("\nChoice: ").strip()
            
            if choice == '1':
                self.add_employee()
            elif choice == '2':
                self.db.display_all()
            elif choice == '3':
                self.update_salary()
            elif choice == '4':
                self.delete_employee()
            elif choice == '5':
                self.db.analyze_data()
            elif choice == '6':
                self.view_top_earners()
            elif choice == '7':
                self.filter_department()
            elif choice == '8':
                self.db.export_to_csv()
            elif choice == '9':
                self.import_csv()
            elif choice == '10':
                self.db.export_report()
            elif choice == '0':
                print("\nGoodbye!")
                self.db.close()
                break
            else:
                print("Invalid choice!")
    
    def add_employee(self):
        """Add new employee"""
        print("\n--- Add Employee ---")
        try:
            name = input("Name: ")
            dept = input("Department: ")
            salary = float(input("Salary: "))
            
            emp = Employee(name=name, department=dept, salary=salary)
            self.db.add_employee(emp)
        except ValueError:
            print("Invalid input!")
    
    def update_salary(self):
        """Update employee salary"""
        try:
            emp_id = int(input("\nEmployee ID: "))
            new_salary = float(input("New Salary: "))
            self.db.update_salary(emp_id, new_salary)
        except ValueError:
            print("Invalid input!")
    
    def delete_employee(self):
        """Delete employee"""
        try:
            emp_id = int(input("\nEmployee ID to delete: "))
            confirm = input("Are you sure? (yes/no): ")
            if confirm.lower() == 'yes':
                self.db.delete_employee(emp_id)
        except ValueError:
            print("Invalid ID!")
    
    def view_top_earners(self):
        """View top earners"""
        try:
            n = int(input("\nHow many top earners? (default 5): ") or 5)
            print(f"\nTop {n} Earners:")
            print(self.db.top_earners(n))
        except ValueError:
            print("Invalid number!")
    
    def filter_department(self):
        """Filter by department"""
        dept = input("\nDepartment: ")
        result = self.db.filter_by_department(dept)
        if not result.empty:
            print(f"\n{dept} Department:")
            print(result)
        else:
            print(f"No employees in {dept}")
    
    def import_csv(self):
        """Import from CSV"""
        filename = input("\nCSV filename (default: employees.csv): ").strip()
        if not filename:
            filename = 'employees.csv'
        self.db.import_from_csv(filename)

# Run the application
if __name__ == "__main__":
    app = CompanyApp()
    app.run()
```

---

## Create Sample Data

```python
import pandas as pd

# Create sample CSV file
data = {
    'name': ['Alice Johnson', 'Bob Smith', 'Charlie Brown', 'Diana Prince', 'Eve Wilson'],
    'department': ['IT', 'Sales', 'IT', 'HR', 'Sales'],
    'salary': [70000, 60000, 80000, 55000, 65000]
}

df = pd.DataFrame(data)
df.to_csv('employees.csv', index=False)
print("✓ Sample data created: employees.csv")
```

---

## Key Concepts Summary

### How They Connect:

```
CSV File ←→ Pandas DataFrame ←→ SQL Database
    ↓              ↓                   ↓
  Read/Write    Analysis          Storage
```

### Flow Example:

1. **CSV → Pandas:** `df = pd.read_csv('file.csv')`
2. **Pandas → SQL:** `df.to_sql('table', conn)`
3. **SQL → Pandas:** `df = pd.read_sql_query('SELECT...', conn)`
4. **Pandas → CSV:** `df.to_csv('output.csv')`

### Why Use Each:

- **CSV:** Simple storage, universal format
- **SQL:** Structured queries, relationships, large data
- **Pandas:** Data analysis, manipulation, statistics
- **OOP:** Organized code, reusable, maintainable

---

## Quick Reference

### Pandas + SQL

```python
import pandas as pd
import sqlite3

conn = sqlite3.connect('db.db')

# SQL → Pandas
df = pd.read_sql_query('SELECT * FROM table', conn)

# Pandas → SQL
df.to_sql('table', conn, if_exists='replace', index=False)

conn.close()
```

### Pandas + CSV

```python
import pandas as pd

# CSV → Pandas
df = pd.read_csv('file.csv')

# Pandas → CSV
df.to_csv('output.csv', index=False)
```

### OOP Pattern

```python
class DatabaseManager:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
    
    def get_dataframe(self):
        return pd.read_sql_query('SELECT * FROM table', self.conn)
    
    def export_csv(self, filename):
        df = self.get_dataframe()
        df.to_csv(filename, index=False)
```

---

## Practice Exercises

### Easy
1. Create CSV with 5 products
2. Load into Pandas
3. Save to SQL database

### Medium
1. Query SQL data with Pandas
2. Filter products by price > 100
3. Export filtered results to new CSV

### Challenge
1. Build a complete system with OOP
2. Support CSV import/export
3. Use Pandas for analysis
4. Store data in SQL

---

**You now know how to connect Python, OOP, SQL, Pandas, and CSV! 🎉**
