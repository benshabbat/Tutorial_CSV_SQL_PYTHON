# Company Management System - OOP Python, SQL, CSV & Pandas Tutorial

## 🎯 Project Overview

In this tutorial, we'll build a **Company Management System** that handles employees, departments, and salaries. This beginner-friendly project will teach you:

- **Object-Oriented Programming (OOP)** in Python
- **SQL** database operations
- **CSV** file handling
- **Pandas** for data analysis

---

## 📋 Table of Contents

1. [Project Setup](#project-setup)
2. [Understanding OOP Concepts](#understanding-oop-concepts)
3. [Building the Employee Class](#building-the-employee-class)
4. [Building the Department Class](#building-the-department-class)
5. [Database Manager Class](#database-manager-class)
6. [CSV Import/Export](#csv-importexport)
7. [Data Analysis with Pandas](#data-analysis-with-pandas)
8. [Complete Application](#complete-application)
9. [Next Steps](#next-steps)

---

## Project Setup

### Create Project Structure

```
company_project/
├── main.py
├── models/
│   ├── __init__.py
│   ├── employee.py
│   └── department.py
├── database/
│   ├── __init__.py
│   └── db_manager.py
├── data/
│   ├── employees.csv
│   └── departments.csv
└── utils/
    ├── __init__.py
    └── csv_handler.py
```

### Install Required Libraries

```bash
pip install pandas
```

---

## Understanding OOP Concepts

### What is Object-Oriented Programming?

OOP is a programming paradigm based on the concept of "objects" that contain data (attributes) and code (methods).

#### Key Concepts:

**1. Class** - A blueprint for creating objects
```python
class Car:
    pass  # Template for a car
```

**2. Object** - An instance of a class
```python
my_car = Car()  # Create a specific car
```

**3. Attributes** - Data stored in an object
```python
class Car:
    def __init__(self, brand, model):
        self.brand = brand  # Attribute
        self.model = model  # Attribute
```

**4. Methods** - Functions that belong to a class
```python
class Car:
    def start_engine(self):
        print("Engine started!")  # Method
```

**5. Inheritance** - Creating new classes from existing ones
```python
class ElectricCar(Car):  # Inherits from Car
    pass
```

**6. Encapsulation** - Hiding internal details
```python
class BankAccount:
    def __init__(self):
        self.__balance = 0  # Private attribute
```

---

## Building the Employee Class

### File: `models/employee.py`

```python
class Employee:
    """
    Represents an employee in the company
    """
    
    # Class variable (shared by all instances)
    company_name = "TechCorp"
    employee_count = 0
    
    def __init__(self, emp_id, name, age, department, salary):
        """
        Initialize a new employee
        
        Args:
            emp_id (int): Employee ID
            name (str): Employee name
            age (int): Employee age
            department (str): Department name
            salary (float): Employee salary
        """
        # Instance variables (unique to each employee)
        self.emp_id = emp_id
        self.name = name
        self.age = age
        self.department = department
        self.salary = salary
        
        # Increment employee count
        Employee.employee_count += 1
    
    def get_info(self):
        """Return employee information as a string"""
        return f"ID: {self.emp_id}, Name: {self.name}, Department: {self.department}"
    
    def give_raise(self, percentage):
        """
        Increase employee salary by a percentage
        
        Args:
            percentage (float): Percentage increase (e.g., 10 for 10%)
        """
        increase = self.salary * (percentage / 100)
        self.salary += increase
        return f"{self.name} received a {percentage}% raise. New salary: ${self.salary:.2f}"
    
    def get_annual_salary(self):
        """Calculate annual salary"""
        return self.salary * 12
    
    def is_senior(self):
        """Check if employee is senior (salary > 70000)"""
        return self.salary > 70000
    
    def to_dict(self):
        """Convert employee to dictionary (useful for CSV/database)"""
        return {
            'emp_id': self.emp_id,
            'name': self.name,
            'age': self.age,
            'department': self.department,
            'salary': self.salary
        }
    
    def __str__(self):
        """String representation of employee"""
        return f"Employee({self.name}, {self.department}, ${self.salary})"
    
    def __repr__(self):
        """Official representation of employee"""
        return f"Employee(emp_id={self.emp_id}, name='{self.name}', age={self.age}, department='{self.department}', salary={self.salary})"
    
    @classmethod
    def from_dict(cls, data):
        """
        Create an Employee object from a dictionary
        
        Args:
            data (dict): Dictionary with employee data
            
        Returns:
            Employee: New employee instance
        """
        return cls(
            data['emp_id'],
            data['name'],
            data['age'],
            data['department'],
            data['salary']
        )
    
    @staticmethod
    def validate_salary(salary):
        """
        Validate if salary is acceptable
        
        Args:
            salary (float): Salary to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        return salary > 0 and salary < 1000000


# Example Usage
if __name__ == "__main__":
    # Create employee objects
    emp1 = Employee(1, "Alice Johnson", 28, "IT", 75000)
    emp2 = Employee(2, "Bob Smith", 35, "Sales", 65000)
    emp3 = Employee(3, "Charlie Brown", 42, "IT", 85000)
    
    # Use methods
    print(emp1.get_info())
    print(emp1.give_raise(10))
    print(f"Annual salary: ${emp1.get_annual_salary()}")
    print(f"Is senior: {emp1.is_senior()}")
    
    # Print employee
    print(emp1)
    
    # Check employee count
    print(f"\nTotal employees: {Employee.employee_count}")
    
    # Convert to dictionary
    print(f"\nEmployee as dict: {emp2.to_dict()}")
```

---

## Building the Department Class

### File: `models/department.py`

```python
from models.employee import Employee

class Department:
    """
    Represents a department in the company
    """
    
    def __init__(self, dept_id, name, manager=None):
        """
        Initialize a department
        
        Args:
            dept_id (int): Department ID
            name (str): Department name
            manager (str): Manager name (optional)
        """
        self.dept_id = dept_id
        self.name = name
        self.manager = manager
        self.employees = []  # List to store employee objects
    
    def add_employee(self, employee):
        """
        Add an employee to the department
        
        Args:
            employee (Employee): Employee object to add
        """
        if isinstance(employee, Employee):
            self.employees.append(employee)
            print(f"Added {employee.name} to {self.name} department")
        else:
            raise TypeError("Must provide an Employee object")
    
    def remove_employee(self, emp_id):
        """
        Remove an employee from the department
        
        Args:
            emp_id (int): Employee ID to remove
        """
        for i, emp in enumerate(self.employees):
            if emp.emp_id == emp_id:
                removed = self.employees.pop(i)
                print(f"Removed {removed.name} from {self.name} department")
                return
        print(f"Employee with ID {emp_id} not found")
    
    def get_employee_count(self):
        """Get number of employees in department"""
        return len(self.employees)
    
    def get_total_salary_cost(self):
        """Calculate total monthly salary cost for department"""
        return sum(emp.salary for emp in self.employees)
    
    def get_average_salary(self):
        """Calculate average salary in department"""
        if not self.employees:
            return 0
        return self.get_total_salary_cost() / len(self.employees)
    
    def get_highest_paid_employee(self):
        """Find the highest paid employee in department"""
        if not self.employees:
            return None
        return max(self.employees, key=lambda emp: emp.salary)
    
    def list_employees(self):
        """Print all employees in department"""
        print(f"\n--- {self.name} Department ---")
        print(f"Manager: {self.manager}")
        print(f"Employees: {len(self.employees)}\n")
        
        for emp in self.employees:
            print(f"  {emp.get_info()}")
    
    def to_dict(self):
        """Convert department to dictionary"""
        return {
            'dept_id': self.dept_id,
            'name': self.name,
            'manager': self.manager,
            'employee_count': len(self.employees)
        }
    
    def __str__(self):
        return f"Department({self.name}, {len(self.employees)} employees)"
    
    def __repr__(self):
        return f"Department(dept_id={self.dept_id}, name='{self.name}', manager='{self.manager}')"


# Example Usage
if __name__ == "__main__":
    # Create department
    it_dept = Department(1, "IT", "John Doe")
    
    # Create employees
    emp1 = Employee(1, "Alice Johnson", 28, "IT", 75000)
    emp2 = Employee(2, "Bob Smith", 35, "IT", 65000)
    emp3 = Employee(3, "Charlie Brown", 42, "IT", 85000)
    
    # Add employees to department
    it_dept.add_employee(emp1)
    it_dept.add_employee(emp2)
    it_dept.add_employee(emp3)
    
    # Department operations
    it_dept.list_employees()
    print(f"\nTotal salary cost: ${it_dept.get_total_salary_cost():,.2f}")
    print(f"Average salary: ${it_dept.get_average_salary():,.2f}")
    
    highest = it_dept.get_highest_paid_employee()
    print(f"Highest paid: {highest.name} - ${highest.salary:,.2f}")
```

---

## Database Manager Class

### File: `database/db_manager.py`

```python
import sqlite3
import pandas as pd
from models.employee import Employee
from models.department import Department

class DatabaseManager:
    """
    Manages database operations for the company system
    """
    
    def __init__(self, db_name='company.db'):
        """
        Initialize database connection
        
        Args:
            db_name (str): Database file name
        """
        self.db_name = db_name
        self.conn = None
        self.cursor = None
    
    def connect(self):
        """Establish database connection"""
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            print(f"Connected to database: {self.db_name}")
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")
    
    def disconnect(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            print("Database connection closed")
    
    def create_tables(self):
        """Create necessary tables if they don't exist"""
        # Create departments table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS departments (
                dept_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL UNIQUE,
                manager TEXT
            )
        ''')
        
        # Create employees table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS employees (
                emp_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                age INTEGER,
                department TEXT,
                salary REAL,
                FOREIGN KEY (department) REFERENCES departments(name)
            )
        ''')
        
        self.conn.commit()
        print("Tables created successfully")
    
    def insert_employee(self, employee):
        """
        Insert an employee into the database
        
        Args:
            employee (Employee): Employee object to insert
        """
        try:
            self.cursor.execute('''
                INSERT INTO employees (emp_id, name, age, department, salary)
                VALUES (?, ?, ?, ?, ?)
            ''', (employee.emp_id, employee.name, employee.age, 
                  employee.department, employee.salary))
            self.conn.commit()
            print(f"Employee {employee.name} added to database")
        except sqlite3.IntegrityError:
            print(f"Employee with ID {employee.emp_id} already exists")
    
    def insert_department(self, department):
        """
        Insert a department into the database
        
        Args:
            department (Department): Department object to insert
        """
        try:
            self.cursor.execute('''
                INSERT INTO departments (dept_id, name, manager)
                VALUES (?, ?, ?)
            ''', (department.dept_id, department.name, department.manager))
            self.conn.commit()
            print(f"Department {department.name} added to database")
        except sqlite3.IntegrityError:
            print(f"Department {department.name} already exists")
    
    def get_all_employees(self):
        """
        Retrieve all employees from database
        
        Returns:
            list: List of Employee objects
        """
        self.cursor.execute('SELECT * FROM employees')
        rows = self.cursor.fetchall()
        
        employees = []
        for row in rows:
            emp = Employee(row[0], row[1], row[2], row[3], row[4])
            employees.append(emp)
        
        return employees
    
    def get_employee_by_id(self, emp_id):
        """
        Get employee by ID
        
        Args:
            emp_id (int): Employee ID
            
        Returns:
            Employee: Employee object or None
        """
        self.cursor.execute('SELECT * FROM employees WHERE emp_id = ?', (emp_id,))
        row = self.cursor.fetchone()
        
        if row:
            return Employee(row[0], row[1], row[2], row[3], row[4])
        return None
    
    def update_employee_salary(self, emp_id, new_salary):
        """
        Update employee salary
        
        Args:
            emp_id (int): Employee ID
            new_salary (float): New salary amount
        """
        self.cursor.execute('''
            UPDATE employees
            SET salary = ?
            WHERE emp_id = ?
        ''', (new_salary, emp_id))
        self.conn.commit()
        print(f"Updated salary for employee ID {emp_id}")
    
    def delete_employee(self, emp_id):
        """
        Delete employee from database
        
        Args:
            emp_id (int): Employee ID
        """
        self.cursor.execute('DELETE FROM employees WHERE emp_id = ?', (emp_id,))
        self.conn.commit()
        print(f"Deleted employee ID {emp_id}")
    
    def get_employees_by_department(self, department_name):
        """
        Get all employees in a specific department
        
        Args:
            department_name (str): Department name
            
        Returns:
            list: List of Employee objects
        """
        self.cursor.execute('''
            SELECT * FROM employees 
            WHERE department = ?
        ''', (department_name,))
        
        rows = self.cursor.fetchall()
        return [Employee(row[0], row[1], row[2], row[3], row[4]) for row in rows]
    
    def get_department_statistics(self):
        """
        Get statistics for all departments
        
        Returns:
            pandas.DataFrame: Statistics dataframe
        """
        query = '''
            SELECT 
                department,
                COUNT(*) as employee_count,
                AVG(salary) as avg_salary,
                MIN(salary) as min_salary,
                MAX(salary) as max_salary,
                SUM(salary) as total_salary
            FROM employees
            GROUP BY department
        '''
        
        df = pd.read_sql_query(query, self.conn)
        return df
    
    def search_employees(self, name=None, min_salary=None, max_salary=None):
        """
        Search employees with filters
        
        Args:
            name (str): Search by name (partial match)
            min_salary (float): Minimum salary
            max_salary (float): Maximum salary
            
        Returns:
            list: List of matching employees
        """
        query = 'SELECT * FROM employees WHERE 1=1'
        params = []
        
        if name:
            query += ' AND name LIKE ?'
            params.append(f'%{name}%')
        
        if min_salary:
            query += ' AND salary >= ?'
            params.append(min_salary)
        
        if max_salary:
            query += ' AND salary <= ?'
            params.append(max_salary)
        
        self.cursor.execute(query, params)
        rows = self.cursor.fetchall()
        
        return [Employee(row[0], row[1], row[2], row[3], row[4]) for row in rows]


# Example Usage
if __name__ == "__main__":
    # Initialize database
    db = DatabaseManager('company.db')
    db.connect()
    db.create_tables()
    
    # Create and insert departments
    it_dept = Department(1, "IT", "John Manager")
    sales_dept = Department(2, "Sales", "Jane Director")
    
    db.insert_department(it_dept)
    db.insert_department(sales_dept)
    
    # Create and insert employees
    employees = [
        Employee(1, "Alice Johnson", 28, "IT", 75000),
        Employee(2, "Bob Smith", 35, "Sales", 65000),
        Employee(3, "Charlie Brown", 42, "IT", 85000),
        Employee(4, "Diana Prince", 30, "Sales", 70000)
    ]
    
    for emp in employees:
        db.insert_employee(emp)
    
    # Retrieve and display employees
    print("\n--- All Employees ---")
    all_employees = db.get_all_employees()
    for emp in all_employees:
        print(emp)
    
    # Get department statistics
    print("\n--- Department Statistics ---")
    stats = db.get_department_statistics()
    print(stats)
    
    db.disconnect()
```

---

## CSV Import/Export

### File: `utils/csv_handler.py`

```python
import csv
import pandas as pd
from models.employee import Employee
from models.department import Department

class CSVHandler:
    """
    Handles CSV import and export operations
    """
    
    @staticmethod
    def export_employees_to_csv(employees, filename='employees.csv'):
        """
        Export employees to CSV file
        
        Args:
            employees (list): List of Employee objects
            filename (str): Output filename
        """
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, 
                                   fieldnames=['emp_id', 'name', 'age', 'department', 'salary'])
            writer.writeheader()
            
            for emp in employees:
                writer.writerow(emp.to_dict())
        
        print(f"Exported {len(employees)} employees to {filename}")
    
    @staticmethod
    def import_employees_from_csv(filename='employees.csv'):
        """
        Import employees from CSV file
        
        Args:
            filename (str): Input filename
            
        Returns:
            list: List of Employee objects
        """
        employees = []
        
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                for row in reader:
                    emp = Employee(
                        int(row['emp_id']),
                        row['name'],
                        int(row['age']),
                        row['department'],
                        float(row['salary'])
                    )
                    employees.append(emp)
            
            print(f"Imported {len(employees)} employees from {filename}")
            return employees
            
        except FileNotFoundError:
            print(f"File {filename} not found")
            return []
    
    @staticmethod
    def export_employees_pandas(employees, filename='employees_pandas.csv'):
        """
        Export employees using pandas
        
        Args:
            employees (list): List of Employee objects
            filename (str): Output filename
        """
        data = [emp.to_dict() for emp in employees]
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)
        print(f"Exported {len(employees)} employees to {filename} using pandas")
    
    @staticmethod
    def import_employees_pandas(filename='employees.csv'):
        """
        Import employees using pandas
        
        Args:
            filename (str): Input filename
            
        Returns:
            list: List of Employee objects
        """
        try:
            df = pd.read_csv(filename)
            employees = []
            
            for _, row in df.iterrows():
                emp = Employee(
                    int(row['emp_id']),
                    row['name'],
                    int(row['age']),
                    row['department'],
                    float(row['salary'])
                )
                employees.append(emp)
            
            print(f"Imported {len(employees)} employees from {filename} using pandas")
            return employees
            
        except FileNotFoundError:
            print(f"File {filename} not found")
            return []
    
    @staticmethod
    def export_departments_to_csv(departments, filename='departments.csv'):
        """
        Export departments to CSV
        
        Args:
            departments (list): List of Department objects
            filename (str): Output filename
        """
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, 
                                   fieldnames=['dept_id', 'name', 'manager', 'employee_count'])
            writer.writeheader()
            
            for dept in departments:
                writer.writerow(dept.to_dict())
        
        print(f"Exported {len(departments)} departments to {filename}")


# Example Usage
if __name__ == "__main__":
    # Create sample employees
    employees = [
        Employee(1, "Alice Johnson", 28, "IT", 75000),
        Employee(2, "Bob Smith", 35, "Sales", 65000),
        Employee(3, "Charlie Brown", 42, "IT", 85000),
    ]
    
    # Export to CSV
    CSVHandler.export_employees_to_csv(employees, 'data/employees.csv')
    CSVHandler.export_employees_pandas(employees, 'data/employees_pandas.csv')
    
    # Import from CSV
    imported_employees = CSVHandler.import_employees_from_csv('data/employees.csv')
    print("\nImported Employees:")
    for emp in imported_employees:
        print(emp)
```

---

## Data Analysis with Pandas

### File: `analytics.py`

```python
import pandas as pd
import sqlite3
from database.db_manager import DatabaseManager

class CompanyAnalytics:
    """
    Perform data analysis on company data
    """
    
    def __init__(self, db_manager):
        """
        Initialize analytics with database manager
        
        Args:
            db_manager (DatabaseManager): Database manager instance
        """
        self.db = db_manager
    
    def get_employee_dataframe(self):
        """
        Get all employees as pandas DataFrame
        
        Returns:
            pandas.DataFrame: Employee data
        """
        query = 'SELECT * FROM employees'
        df = pd.read_sql_query(query, self.db.conn)
        return df
    
    def analyze_salaries(self):
        """Analyze salary distribution"""
        df = self.get_employee_dataframe()
        
        print("\n=== Salary Analysis ===")
        print(f"Total Employees: {len(df)}")
        print(f"Average Salary: ${df['salary'].mean():,.2f}")
        print(f"Median Salary: ${df['salary'].median():,.2f}")
        print(f"Minimum Salary: ${df['salary'].min():,.2f}")
        print(f"Maximum Salary: ${df['salary'].max():,.2f}")
        print(f"Standard Deviation: ${df['salary'].std():,.2f}")
        
        return df['salary'].describe()
    
    def department_comparison(self):
        """Compare departments"""
        df = self.get_employee_dataframe()
        
        dept_stats = df.groupby('department').agg({
            'emp_id': 'count',
            'salary': ['mean', 'min', 'max', 'sum'],
            'age': 'mean'
        }).round(2)
        
        dept_stats.columns = ['Employee_Count', 'Avg_Salary', 'Min_Salary', 
                              'Max_Salary', 'Total_Salary', 'Avg_Age']
        
        print("\n=== Department Comparison ===")
        print(dept_stats)
        
        return dept_stats
    
    def age_distribution(self):
        """Analyze age distribution"""
        df = self.get_employee_dataframe()
        
        # Create age groups
        bins = [0, 25, 35, 45, 100]
        labels = ['Under 25', '25-35', '36-45', 'Over 45']
        df['age_group'] = pd.cut(df['age'], bins=bins, labels=labels)
        
        age_dist = df['age_group'].value_counts().sort_index()
        
        print("\n=== Age Distribution ===")
        print(age_dist)
        
        return age_dist
    
    def top_earners(self, n=5):
        """
        Get top N earners
        
        Args:
            n (int): Number of top earners to return
        """
        df = self.get_employee_dataframe()
        top = df.nlargest(n, 'salary')[['name', 'department', 'salary']]
        
        print(f"\n=== Top {n} Earners ===")
        print(top.to_string(index=False))
        
        return top
    
    def salary_by_department_chart_data(self):
        """Prepare data for salary by department chart"""
        df = self.get_employee_dataframe()
        
        chart_data = df.groupby('department')['salary'].mean().sort_values(ascending=False)
        
        print("\n=== Average Salary by Department ===")
        for dept, salary in chart_data.items():
            print(f"{dept}: ${salary:,.2f}")
        
        return chart_data
    
    def export_analysis_report(self, filename='analysis_report.csv'):
        """Export comprehensive analysis report"""
        df = self.get_employee_dataframe()
        
        # Create summary statistics
        summary = df.groupby('department').agg({
            'emp_id': 'count',
            'salary': ['mean', 'median', 'std', 'min', 'max'],
            'age': ['mean', 'min', 'max']
        }).round(2)
        
        summary.to_csv(filename)
        print(f"\nAnalysis report exported to {filename}")
    
    def find_outliers(self):
        """Find salary outliers using IQR method"""
        df = self.get_employee_dataframe()
        
        Q1 = df['salary'].quantile(0.25)
        Q3 = df['salary'].quantile(0.75)
        IQR = Q3 - Q1
        
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        outliers = df[(df['salary'] < lower_bound) | (df['salary'] > upper_bound)]
        
        print("\n=== Salary Outliers ===")
        if len(outliers) > 0:
            print(outliers[['name', 'department', 'salary']])
        else:
            print("No outliers found")
        
        return outliers


# Example Usage
if __name__ == "__main__":
    # Setup database
    db = DatabaseManager('company.db')
    db.connect()
    
    # Create analytics instance
    analytics = CompanyAnalytics(db)
    
    # Run analyses
    analytics.analyze_salaries()
    analytics.department_comparison()
    analytics.age_distribution()
    analytics.top_earners(3)
    analytics.salary_by_department_chart_data()
    analytics.find_outliers()
    analytics.export_analysis_report()
    
    db.disconnect()
```

---

## Complete Application

### File: `main.py`

```python
"""
Company Management System
A complete OOP application using Python, SQL, CSV, and Pandas
"""

from models.employee import Employee
from models.department import Department
from database.db_manager import DatabaseManager
from utils.csv_handler import CSVHandler
from analytics import CompanyAnalytics
import os

class CompanyManagementSystem:
    """Main application class"""
    
    def __init__(self):
        """Initialize the system"""
        self.db = DatabaseManager('company.db')
        self.db.connect()
        self.db.create_tables()
        self.analytics = CompanyAnalytics(self.db)
    
    def display_menu(self):
        """Display main menu"""
        print("\n" + "="*50)
        print("    COMPANY MANAGEMENT SYSTEM")
        print("="*50)
        print("1.  Add Employee")
        print("2.  View All Employees")
        print("3.  Search Employee by ID")
        print("4.  Update Employee Salary")
        print("5.  Delete Employee")
        print("6.  Add Department")
        print("7.  View Department Statistics")
        print("8.  Import Employees from CSV")
        print("9.  Export Employees to CSV")
        print("10. Run Salary Analysis")
        print("11. View Top Earners")
        print("12. Department Comparison")
        print("0.  Exit")
        print("="*50)
    
    def add_employee(self):
        """Add a new employee"""
        print("\n--- Add New Employee ---")
        try:
            emp_id = int(input("Employee ID: "))
            name = input("Name: ")
            age = int(input("Age: "))
            department = input("Department: ")
            salary = float(input("Salary: "))
            
            emp = Employee(emp_id, name, age, department, salary)
            self.db.insert_employee(emp)
            
        except ValueError:
            print("Invalid input! Please enter correct data types.")
    
    def view_all_employees(self):
        """View all employees"""
        print("\n--- All Employees ---")
        employees = self.db.get_all_employees()
        
        if not employees:
            print("No employees found")
            return
        
        print(f"\nTotal Employees: {len(employees)}\n")
        print(f"{'ID':<5} {'Name':<20} {'Age':<5} {'Department':<15} {'Salary':<10}")
        print("-" * 70)
        
        for emp in employees:
            print(f"{emp.emp_id:<5} {emp.name:<20} {emp.age:<5} {emp.department:<15} ${emp.salary:<10,.2f}")
    
    def search_employee(self):
        """Search employee by ID"""
        print("\n--- Search Employee ---")
        try:
            emp_id = int(input("Enter Employee ID: "))
            emp = self.db.get_employee_by_id(emp_id)
            
            if emp:
                print(f"\nFound: {emp}")
                print(f"Annual Salary: ${emp.get_annual_salary():,.2f}")
                print(f"Senior Employee: {'Yes' if emp.is_senior() else 'No'}")
            else:
                print(f"Employee with ID {emp_id} not found")
                
        except ValueError:
            print("Invalid ID!")
    
    def update_salary(self):
        """Update employee salary"""
        print("\n--- Update Salary ---")
        try:
            emp_id = int(input("Employee ID: "))
            new_salary = float(input("New Salary: "))
            
            self.db.update_employee_salary(emp_id, new_salary)
            
        except ValueError:
            print("Invalid input!")
    
    def delete_employee(self):
        """Delete an employee"""
        print("\n--- Delete Employee ---")
        try:
            emp_id = int(input("Employee ID to delete: "))
            confirm = input(f"Are you sure you want to delete employee {emp_id}? (yes/no): ")
            
            if confirm.lower() == 'yes':
                self.db.delete_employee(emp_id)
            else:
                print("Deletion cancelled")
                
        except ValueError:
            print("Invalid ID!")
    
    def add_department(self):
        """Add a new department"""
        print("\n--- Add New Department ---")
        try:
            dept_id = int(input("Department ID: "))
            name = input("Department Name: ")
            manager = input("Manager Name: ")
            
            dept = Department(dept_id, name, manager)
            self.db.insert_department(dept)
            
        except ValueError:
            print("Invalid input!")
    
    def view_department_stats(self):
        """View department statistics"""
        print("\n--- Department Statistics ---")
        stats = self.db.get_department_statistics()
        print(stats.to_string(index=False))
    
    def import_from_csv(self):
        """Import employees from CSV"""
        print("\n--- Import from CSV ---")
        filename = input("Enter CSV filename (default: employees.csv): ").strip()
        
        if not filename:
            filename = 'employees.csv'
        
        if not os.path.exists(filename):
            print(f"File {filename} not found!")
            return
        
        employees = CSVHandler.import_employees_pandas(filename)
        
        for emp in employees:
            self.db.insert_employee(emp)
    
    def export_to_csv(self):
        """Export employees to CSV"""
        print("\n--- Export to CSV ---")
        filename = input("Enter CSV filename (default: employees_export.csv): ").strip()
        
        if not filename:
            filename = 'employees_export.csv'
        
        employees = self.db.get_all_employees()
        CSVHandler.export_employees_pandas(employees, filename)
    
    def run_salary_analysis(self):
        """Run salary analysis"""
        self.analytics.analyze_salaries()
    
    def view_top_earners(self):
        """View top earners"""
        try:
            n = int(input("How many top earners to display? (default: 5): ") or 5)
            self.analytics.top_earners(n)
        except ValueError:
            self.analytics.top_earners(5)
    
    def department_comparison(self):
        """Compare departments"""
        self.analytics.department_comparison()
    
    def run(self):
        """Run the application"""
        print("\nWelcome to Company Management System!")
        
        while True:
            self.display_menu()
            choice = input("\nEnter your choice: ").strip()
            
            if choice == '1':
                self.add_employee()
            elif choice == '2':
                self.view_all_employees()
            elif choice == '3':
                self.search_employee()
            elif choice == '4':
                self.update_salary()
            elif choice == '5':
                self.delete_employee()
            elif choice == '6':
                self.add_department()
            elif choice == '7':
                self.view_department_stats()
            elif choice == '8':
                self.import_from_csv()
            elif choice == '9':
                self.export_to_csv()
            elif choice == '10':
                self.run_salary_analysis()
            elif choice == '11':
                self.view_top_earners()
            elif choice == '12':
                self.department_comparison()
            elif choice == '0':
                print("\nThank you for using Company Management System!")
                self.db.disconnect()
                break
            else:
                print("\nInvalid choice! Please try again.")
            
            input("\nPress Enter to continue...")


# Sample data generator
def generate_sample_data():
    """Generate sample data for testing"""
    db = DatabaseManager('company.db')
    db.connect()
    db.create_tables()
    
    # Create departments
    departments = [
        Department(1, "IT", "John Manager"),
        Department(2, "Sales", "Jane Director"),
        Department(3, "HR", "Bob Chief"),
        Department(4, "Marketing", "Alice Head")
    ]
    
    for dept in departments:
        db.insert_department(dept)
    
    # Create employees
    employees = [
        Employee(101, "Alice Johnson", 28, "IT", 75000),
        Employee(102, "Bob Smith", 35, "Sales", 65000),
        Employee(103, "Charlie Brown", 42, "IT", 85000),
        Employee(104, "Diana Prince", 30, "Sales", 70000),
        Employee(105, "Eve Wilson", 26, "HR", 55000),
        Employee(106, "Frank Miller", 38, "IT", 90000),
        Employee(107, "Grace Lee", 33, "Marketing", 68000),
        Employee(108, "Henry Davis", 29, "Sales", 62000),
        Employee(109, "Ivy Chen", 31, "Marketing", 72000),
        Employee(110, "Jack Robinson", 45, "IT", 95000),
    ]
    
    for emp in employees:
        db.insert_employee(emp)
    
    print("Sample data generated successfully!")
    db.disconnect()


if __name__ == "__main__":
    # Uncomment to generate sample data
    # generate_sample_data()
    
    # Run the application
    app = CompanyManagementSystem()
    app.run()
```

---

## Create Sample CSV Files

### File: `create_sample_data.py`

```python
"""
Create sample CSV files for testing
"""

import csv
import os

def create_employees_csv():
    """Create sample employees CSV"""
    employees = [
        ['emp_id', 'name', 'age', 'department', 'salary'],
        [201, 'Sarah Connor', 32, 'IT', 78000],
        [202, 'Kyle Reese', 29, 'Sales', 64000],
        [203, 'John Connor', 25, 'IT', 72000],
        [204, 'Marcus Wright', 40, 'HR', 58000],
        [205, 'Kate Brewster', 34, 'Marketing', 71000],
    ]
    
    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    
    with open('data/employees.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(employees)
    
    print("Created data/employees.csv")

def create_departments_csv():
    """Create sample departments CSV"""
    departments = [
        ['dept_id', 'name', 'manager'],
        [1, 'IT', 'Tech Director'],
        [2, 'Sales', 'Sales VP'],
        [3, 'HR', 'HR Manager'],
        [4, 'Marketing', 'Marketing Head'],
    ]
    
    os.makedirs('data', exist_ok=True)
    
    with open('data/departments.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(departments)
    
    print("Created data/departments.csv")

if __name__ == "__main__":
    create_employees_csv()
    create_departments_csv()
    print("\nSample CSV files created successfully!")
```

---

## Project Files Overview

### File: `models/__init__.py`

```python
"""
Models package for Company Management System
"""

from .employee import Employee
from .department import Department

__all__ = ['Employee', 'Department']
```

### File: `database/__init__.py`

```python
"""
Database package for Company Management System
"""

from .db_manager import DatabaseManager

__all__ = ['DatabaseManager']
```

### File: `utils/__init__.py`

```python
"""
Utilities package for Company Management System
"""

from .csv_handler import CSVHandler

__all__ = ['CSVHandler']
```

---

## How to Run the Project

### Step 1: Create Directory Structure

```bash
mkdir company_project
cd company_project
mkdir models database utils data
```

### Step 2: Create All Python Files

Copy all the code from above into their respective files.

### Step 3: Create `__init__.py` Files

```bash
# Windows PowerShell
New-Item models\__init__.py
New-Item database\__init__.py
New-Item utils\__init__.py
```

### Step 4: Generate Sample Data

```bash
python create_sample_data.py
```

### Step 5: Run the Application

```bash
python main.py
```

---

## Key Learning Points

### OOP Concepts Used

1. **Classes and Objects**
   - `Employee` class represents individual employees
   - `Department` class represents departments
   - Each object has its own state (attributes)

2. **Encapsulation**
   - Data and methods bundled together
   - Private methods (starting with `_`)

3. **Inheritance** (can be extended)
   - Create specialized employee types
   - Example: `Manager(Employee)`, `Developer(Employee)`

4. **Polymorphism**
   - `__str__` and `__repr__` methods
   - Method overriding

5. **Class Methods and Static Methods**
   - `@classmethod` - `from_dict()`
   - `@staticmethod` - `validate_salary()`

### SQL Operations Covered

- CREATE TABLE
- INSERT data
- SELECT queries
- UPDATE records
- DELETE records
- GROUP BY and aggregation
- JOIN operations (relationships)

### CSV Operations

- Reading CSV with `csv` module
- Writing CSV with `csv` module
- Using Pandas for CSV
- Data validation

### Pandas Features

- DataFrames
- Data analysis (`describe()`, `groupby()`)
- Filtering and sorting
- Statistical operations
- Data visualization preparation

---

## Exercises for Practice

### Beginner Level

1. Add a method to calculate employee's years of service
2. Create a method to give bonus to all employees in a department
3. Add validation for employee age (must be 18-70)
4. Create a method to count employees by department

### Intermediate Level

1. Implement a `Manager` class that inherits from `Employee`
2. Add a salary history tracking feature
3. Create a method to transfer employee to another department
4. Implement employee performance rating system

### Advanced Level

1. Add data visualization using matplotlib
2. Implement role-based access control
3. Create automated reports generation
4. Add email notification system for salary updates

---

## Common Errors and Solutions

### Error 1: Module Not Found

```
ModuleNotFoundError: No module named 'models'
```

**Solution:** Make sure you're running from the project root directory and all `__init__.py` files exist.

### Error 2: Database Locked

```
sqlite3.OperationalError: database is locked
```

**Solution:** Close all database connections properly using `db.disconnect()`.

### Error 3: CSV File Not Found

```
FileNotFoundError: [Errno 2] No such file or directory: 'employees.csv'
```

**Solution:** Ensure the CSV file exists in the correct location or create it using `create_sample_data.py`.

---

## Next Steps

1. **Add More Features:**
   - Employee attendance tracking
   - Project assignment system
   - Leave management
   - Performance reviews

2. **Improve UI:**
   - Create a web interface (Flask/Django)
   - Add GUI with Tkinter
   - Build REST API

3. **Advanced Database:**
   - Use PostgreSQL or MySQL
   - Add database migrations
   - Implement database backups

4. **Testing:**
   - Write unit tests
   - Add integration tests
   - Test edge cases

5. **Deployment:**
   - Containerize with Docker
   - Deploy to cloud (AWS/Azure)
   - Add CI/CD pipeline

---

## Resources

- [Python OOP Documentation](https://docs.python.org/3/tutorial/classes.html)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [SQLite Tutorial](https://www.sqlitetutorial.net/)
- [CSV Module](https://docs.python.org/3/library/csv.html)

---

**Congratulations!** You've built a complete Company Management System using OOP Python, SQL, CSV, and Pandas! 🎉
