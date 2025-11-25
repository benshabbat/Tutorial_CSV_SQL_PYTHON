# OOP Python + CSV Tutorial for Beginners

A simple guide to using Object-Oriented Programming with CSV files.

---

## 🎯 What You'll Learn

- Create classes to represent data
- Save objects to CSV files
- Load objects from CSV files
- Build a practical application

---

## What is OOP?

**OOP** = Organizing code using "objects" that represent real things.

**Example:** An employee has a name, department, and salary.

```python
# Without OOP - messy
employee1_name = "Alice"
employee1_dept = "IT"
employee1_salary = 70000

# With OOP - organized
class Employee:
    def __init__(self, name, dept, salary):
        self.name = name
        self.dept = dept
        self.salary = salary

emp = Employee("Alice", "IT", 70000)
```

---

## Step 1: Basic Class

```python
class Employee:
    """Represents a company employee"""
    
    def __init__(self, name, department, salary):
        self.name = name
        self.department = department
        self.salary = salary
    
    def give_raise(self, percent):
        """Increase salary by percentage"""
        self.salary *= (1 + percent/100)
    
    def __str__(self):
        """String representation"""
        return f"{self.name} - {self.department} - ${self.salary:,.0f}"

# Create employee
emp = Employee("Alice", "IT", 70000)
print(emp)  # Alice - IT - $70,000

# Give raise
emp.give_raise(10)
print(emp)  # Alice - IT - $77,000
```

---

## Step 2: Save Object to CSV

```python
import csv

class Employee:
    def __init__(self, name, department, salary):
        self.name = name
        self.department = department
        self.salary = salary
    
    def to_list(self):
        """Convert object to list for CSV"""
        return [self.name, self.department, self.salary]
    
    def __str__(self):
        return f"{self.name} - {self.department} - ${self.salary:,.0f}"

# Create employees
employees = [
    Employee("Alice", "IT", 70000),
    Employee("Bob", "Sales", 60000),
    Employee("Charlie", "IT", 80000)
]

# Save to CSV
with open('employees.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    
    # Write header
    writer.writerow(['name', 'department', 'salary'])
    
    # Write employee data
    for emp in employees:
        writer.writerow(emp.to_list())

print("✓ Saved to employees.csv")
```

---

## Step 3: Load Objects from CSV

```python
import csv

class Employee:
    def __init__(self, name, department, salary):
        self.name = name
        self.department = department
        self.salary = float(salary)  # Convert to number
    
    @classmethod
    def from_csv_row(cls, row):
        """Create Employee from CSV row"""
        return cls(row['name'], row['department'], row['salary'])
    
    def __str__(self):
        return f"{self.name} - {self.department} - ${self.salary:,.0f}"

# Load from CSV
employees = []

with open('employees.csv', 'r') as file:
    reader = csv.DictReader(file)
    
    for row in reader:
        emp = Employee.from_csv_row(row)
        employees.append(emp)

# Display loaded employees
print("Loaded Employees:")
for emp in employees:
    print(emp)
```

---

## Step 4: Complete Employee Manager

```python
import csv
import os

class Employee:
    """Represents an employee"""
    
    def __init__(self, id, name, department, salary):
        self.id = id
        self.name = name
        self.department = department
        self.salary = float(salary)
    
    def give_raise(self, percent):
        """Increase salary"""
        self.salary *= (1 + percent/100)
        return self.salary
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'department': self.department,
            'salary': self.salary
        }
    
    def __str__(self):
        return f"ID {self.id}: {self.name} - {self.department} - ${self.salary:,.0f}"

class EmployeeManager:
    """Manages employees and CSV storage"""
    
    def __init__(self, filename='employees.csv'):
        self.filename = filename
        self.employees = []
        self.load_from_csv()
    
    def load_from_csv(self):
        """Load all employees from CSV"""
        if not os.path.exists(self.filename):
            print(f"No existing file found. Starting fresh.")
            return
        
        with open(self.filename, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                emp = Employee(
                    row['id'],
                    row['name'],
                    row['department'],
                    row['salary']
                )
                self.employees.append(emp)
        
        print(f"✓ Loaded {len(self.employees)} employees")
    
    def save_to_csv(self):
        """Save all employees to CSV"""
        with open(self.filename, 'w', newline='') as file:
            fieldnames = ['id', 'name', 'department', 'salary']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            
            writer.writeheader()
            for emp in self.employees:
                writer.writerow(emp.to_dict())
        
        print(f"✓ Saved {len(self.employees)} employees")
    
    def add_employee(self, employee):
        """Add new employee"""
        self.employees.append(employee)
        self.save_to_csv()
        print(f"✓ Added {employee.name}")
    
    def find_by_id(self, emp_id):
        """Find employee by ID"""
        for emp in self.employees:
            if emp.id == emp_id:
                return emp
        return None
    
    def remove_employee(self, emp_id):
        """Remove employee by ID"""
        emp = self.find_by_id(emp_id)
        if emp:
            self.employees.remove(emp)
            self.save_to_csv()
            print(f"✓ Removed {emp.name}")
        else:
            print(f"Employee {emp_id} not found")
    
    def list_all(self):
        """Display all employees"""
        if not self.employees:
            print("No employees found")
            return
        
        print(f"\n{'ID':<5} {'Name':<15} {'Department':<12} {'Salary':<10}")
        print("-" * 50)
        for emp in self.employees:
            print(f"{emp.id:<5} {emp.name:<15} {emp.department:<12} ${emp.salary:<10,.0f}")
        print(f"\nTotal: {len(self.employees)} employees")
    
    def find_by_department(self, department):
        """Get all employees in a department"""
        return [emp for emp in self.employees if emp.department == department]
    
    def give_department_raise(self, department, percent):
        """Give raise to entire department"""
        dept_employees = self.find_by_department(department)
        for emp in dept_employees:
            emp.give_raise(percent)
        self.save_to_csv()
        print(f"✓ Gave {len(dept_employees)} employees in {department} a {percent}% raise")

# Usage Example
if __name__ == "__main__":
    manager = EmployeeManager()
    
    # Add employees
    manager.add_employee(Employee(1, "Alice", "IT", 70000))
    manager.add_employee(Employee(2, "Bob", "Sales", 60000))
    manager.add_employee(Employee(3, "Charlie", "IT", 80000))
    
    # List all
    manager.list_all()
    
    # Find by department
    print("\nIT Department:")
    it_emps = manager.find_by_department("IT")
    for emp in it_emps:
        print(emp)
    
    # Give department raise
    manager.give_department_raise("IT", 10)
    
    # List after raise
    print("\nAfter IT raise:")
    manager.list_all()
```

---

## Step 5: Interactive Application

```python
import csv
import os

class Employee:
    def __init__(self, id, name, department, salary):
        self.id = id
        self.name = name
        self.department = department
        self.salary = float(salary)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'department': self.department,
            'salary': self.salary
        }
    
    def __str__(self):
        return f"{self.name} ({self.department}): ${self.salary:,.0f}"

class EmployeeManager:
    def __init__(self, filename='employees.csv'):
        self.filename = filename
        self.employees = []
        self.load_from_csv()
    
    def load_from_csv(self):
        if not os.path.exists(self.filename):
            return
        
        with open(self.filename, 'r') as file:
            reader = csv.DictReader(file)
            self.employees = [
                Employee(row['id'], row['name'], row['department'], row['salary'])
                for row in reader
            ]
    
    def save_to_csv(self):
        with open(self.filename, 'w', newline='') as file:
            fieldnames = ['id', 'name', 'department', 'salary']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows([emp.to_dict() for emp in self.employees])
    
    def add_employee(self, employee):
        self.employees.append(employee)
        self.save_to_csv()
    
    def list_all(self):
        if not self.employees:
            print("\nNo employees found")
            return
        
        print(f"\n{'ID':<5} {'Name':<15} {'Department':<12} {'Salary':<12}")
        print("-" * 50)
        for emp in self.employees:
            print(f"{emp.id:<5} {emp.name:<15} {emp.department:<12} ${emp.salary:<11,.0f}")

class EmployeeApp:
    """Interactive employee management application"""
    
    def __init__(self):
        self.manager = EmployeeManager()
    
    def menu(self):
        print("\n" + "="*40)
        print("    EMPLOYEE MANAGEMENT SYSTEM")
        print("="*40)
        print("1. Add Employee")
        print("2. View All Employees")
        print("3. Search by Department")
        print("4. Export Report")
        print("0. Exit")
        print("="*40)
    
    def run(self):
        while True:
            self.menu()
            choice = input("\nChoice: ").strip()
            
            if choice == '1':
                self.add_employee()
            elif choice == '2':
                self.manager.list_all()
            elif choice == '3':
                self.search_department()
            elif choice == '4':
                self.export_report()
            elif choice == '0':
                print("\nGoodbye!")
                break
            else:
                print("Invalid choice!")
    
    def add_employee(self):
        print("\n--- Add Employee ---")
        try:
            emp_id = input("ID: ")
            name = input("Name: ")
            dept = input("Department: ")
            salary = float(input("Salary: "))
            
            emp = Employee(emp_id, name, dept, salary)
            self.manager.add_employee(emp)
            print(f"✓ Added {name}")
        except ValueError:
            print("Invalid input!")
    
    def search_department(self):
        dept = input("\nDepartment: ")
        found = [emp for emp in self.manager.employees if emp.department == dept]
        
        if found:
            print(f"\n{dept} Department:")
            for emp in found:
                print(f"  {emp}")
        else:
            print(f"No employees in {dept}")
    
    def export_report(self):
        filename = input("\nExport filename (default: report.csv): ").strip()
        if not filename:
            filename = 'report.csv'
        
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['ID', 'Name', 'Department', 'Salary', 'Annual Salary'])
            
            for emp in self.manager.employees:
                writer.writerow([
                    emp.id,
                    emp.name,
                    emp.department,
                    emp.salary,
                    emp.salary * 12
                ])
        
        print(f"✓ Exported to {filename}")

# Run the app
if __name__ == "__main__":
    app = EmployeeApp()
    app.run()
```

---

## Using Pandas (Easier!)

```python
import pandas as pd

class Employee:
    def __init__(self, id, name, department, salary):
        self.id = id
        self.name = name
        self.department = department
        self.salary = salary
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'department': self.department,
            'salary': self.salary
        }

class EmployeeManagerPandas:
    """Employee manager using Pandas"""
    
    def __init__(self, filename='employees.csv'):
        self.filename = filename
        self.employees = []
        self.load_from_csv()
    
    def load_from_csv(self):
        """Load employees using pandas"""
        try:
            df = pd.read_csv(self.filename)
            self.employees = [
                Employee(row['id'], row['name'], row['department'], row['salary'])
                for _, row in df.iterrows()
            ]
            print(f"✓ Loaded {len(self.employees)} employees")
        except FileNotFoundError:
            print("No existing file. Starting fresh.")
    
    def save_to_csv(self):
        """Save using pandas"""
        data = [emp.to_dict() for emp in self.employees]
        df = pd.DataFrame(data)
        df.to_csv(self.filename, index=False)
        print(f"✓ Saved {len(self.employees)} employees")
    
    def add_employee(self, employee):
        self.employees.append(employee)
        self.save_to_csv()
    
    def get_dataframe(self):
        """Get employees as DataFrame for analysis"""
        data = [emp.to_dict() for emp in self.employees]
        return pd.DataFrame(data)
    
    def analyze(self):
        """Analyze employee data"""
        df = self.get_dataframe()
        
        print("\n=== Employee Analysis ===")
        print(f"Total Employees: {len(df)}")
        print(f"Average Salary: ${df['salary'].mean():,.0f}")
        print(f"\nBy Department:")
        print(df.groupby('department')['salary'].agg(['count', 'mean']))

# Usage
if __name__ == "__main__":
    manager = EmployeeManagerPandas()
    
    # Add employees
    manager.add_employee(Employee(1, "Alice", "IT", 70000))
    manager.add_employee(Employee(2, "Bob", "Sales", 60000))
    manager.add_employee(Employee(3, "Charlie", "IT", 80000))
    
    # Analyze
    manager.analyze()
```

---

## Real-World Example: Product Inventory

```python
import csv
import os

class Product:
    """Represents a product in inventory"""
    
    def __init__(self, id, name, price, quantity):
        self.id = id
        self.name = name
        self.price = float(price)
        self.quantity = int(quantity)
    
    def total_value(self):
        """Calculate total value of stock"""
        return self.price * self.quantity
    
    def restock(self, amount):
        """Add stock"""
        self.quantity += amount
    
    def sell(self, amount):
        """Reduce stock"""
        if amount <= self.quantity:
            self.quantity -= amount
            return True
        return False
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'quantity': self.quantity
        }
    
    def __str__(self):
        return f"{self.name}: ${self.price:.2f} x {self.quantity} = ${self.total_value():.2f}"

class Inventory:
    """Manages product inventory with CSV storage"""
    
    def __init__(self, filename='inventory.csv'):
        self.filename = filename
        self.products = []
        self.load()
    
    def load(self):
        """Load inventory from CSV"""
        if not os.path.exists(self.filename):
            return
        
        with open(self.filename, 'r') as file:
            reader = csv.DictReader(file)
            self.products = [
                Product(row['id'], row['name'], row['price'], row['quantity'])
                for row in reader
            ]
    
    def save(self):
        """Save inventory to CSV"""
        with open(self.filename, 'w', newline='') as file:
            fieldnames = ['id', 'name', 'price', 'quantity']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows([p.to_dict() for p in self.products])
    
    def add_product(self, product):
        """Add product to inventory"""
        self.products.append(product)
        self.save()
        print(f"✓ Added {product.name}")
    
    def find_by_id(self, product_id):
        """Find product by ID"""
        for p in self.products:
            if p.id == product_id:
                return p
        return None
    
    def list_all(self):
        """Display all products"""
        if not self.products:
            print("No products in inventory")
            return
        
        print(f"\n{'ID':<5} {'Name':<20} {'Price':<10} {'Qty':<8} {'Value':<12}")
        print("-" * 60)
        for p in self.products:
            print(f"{p.id:<5} {p.name:<20} ${p.price:<9.2f} {p.quantity:<8} ${p.total_value():<11.2f}")
        
        total = sum(p.total_value() for p in self.products)
        print(f"\nTotal Inventory Value: ${total:,.2f}")
    
    def low_stock(self, threshold=10):
        """Find products with low stock"""
        return [p for p in self.products if p.quantity < threshold]

# Usage
if __name__ == "__main__":
    inventory = Inventory()
    
    # Add products
    inventory.add_product(Product("P001", "Laptop", 999.99, 15))
    inventory.add_product(Product("P002", "Mouse", 29.99, 50))
    inventory.add_product(Product("P003", "Keyboard", 79.99, 5))
    
    # List all
    inventory.list_all()
    
    # Check low stock
    print("\nLow Stock Items:")
    for p in inventory.low_stock():
        print(f"  {p.name}: {p.quantity} left")
    
    # Sell item
    product = inventory.find_by_id("P001")
    if product.sell(3):
        print(f"\n✓ Sold 3 {product.name}s")
        inventory.save()
```

---

## Quick Reference

### Basic Class with CSV

```python
import csv

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def to_dict(self):
        return {'name': self.name, 'age': self.age}

# Save
people = [Person("Alice", 25), Person("Bob", 30)]
with open('people.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['name', 'age'])
    writer.writeheader()
    writer.writerows([p.to_dict() for p in people])

# Load
people = []
with open('people.csv', 'r') as f:
    reader = csv.DictReader(f)
    people = [Person(row['name'], row['age']) for row in reader]
```

---

## Practice Exercises

### Easy
1. Create a `Book` class with title, author, price
2. Save 5 books to CSV
3. Load and display all books

### Medium
1. Create a `Student` class with name, grades (list)
2. Add methods to calculate average grade
3. Save/load students with CSV
4. Find students with average > 80

### Challenge
1. Create a library system with `Book` and `Member` classes
2. Members can borrow books
3. Save both books and members to separate CSV files
4. Create a report of borrowed books

---

## Tips

💡 **Use `to_dict()` method** - Makes CSV writing easier

💡 **Use `@classmethod`** - For creating objects from CSV rows

💡 **Save after changes** - Always save to CSV after modifications

💡 **Handle missing files** - Use `os.path.exists()` to check

💡 **Use Pandas for analysis** - Much easier than plain CSV

---

## Common Patterns

### Pattern 1: Object to CSV row
```python
def to_dict(self):
    return {'col1': self.attr1, 'col2': self.attr2}
```

### Pattern 2: CSV row to Object
```python
@classmethod
def from_dict(cls, data):
    return cls(data['col1'], data['col2'])
```

### Pattern 3: Manager class
```python
class Manager:
    def __init__(self, filename):
        self.filename = filename
        self.items = []
        self.load()
    
    def load(self):
        # Load from CSV
    
    def save(self):
        # Save to CSV
```

---

**You now know OOP with CSV! 🎉**

Build projects like:
- Todo list manager
- Contact book
- Expense tracker
- Inventory system
