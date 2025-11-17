# OOP Python + SQL Tutorial for Beginners

A simple guide to Object-Oriented Programming with SQL databases.

---

## 🎯 What You'll Learn

- Create classes in Python (OOP)
- Use objects to represent real data
- Connect classes to SQL databases
- Build a simple app with OOP + SQL

---

## What is OOP?

**Object-Oriented Programming (OOP)** organizes code into "objects" that represent real things.

**Example:** Instead of separate variables for each employee:
```python
# Without OOP - messy
employee1_name = "Alice"
employee1_salary = 70000
employee2_name = "Bob"
employee2_salary = 60000
```

Use a **class** to create employee objects:
```python
# With OOP - organized
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

emp1 = Employee("Alice", 70000)
emp2 = Employee("Bob", 60000)
```

---

## Step 1: Basic Class

```python
class Employee:
    """Represents a company employee"""
    
    def __init__(self, name, department, salary):
        """Initialize a new employee"""
        self.name = name
        self.department = department
        self.salary = salary
    
    def give_raise(self, amount):
        """Increase salary"""
        self.salary += amount
    
    def display(self):
        """Show employee info"""
        print(f"{self.name} - {self.department} - ${self.salary:,}")

# Create employee objects
emp1 = Employee("Alice", "IT", 70000)
emp2 = Employee("Bob", "Sales", 60000)

# Use methods
emp1.display()  # Output: Alice - IT - $70,000
emp1.give_raise(5000)
emp1.display()  # Output: Alice - IT - $75,000
```

**Key Concepts:**
- `class` = blueprint for creating objects
- `__init__` = constructor (runs when creating object)
- `self` = refers to the current object
- Methods = functions inside a class

---

## Step 2: Class with Database

```python
import sqlite3

class Employee:
    """Employee with database integration"""
    
    def __init__(self, id, name, department, salary):
        self.id = id
        self.name = name
        self.department = department
        self.salary = salary
    
    def save_to_db(self, conn):
        """Save employee to database"""
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO employees (id, name, department, salary)
            VALUES (?, ?, ?, ?)
        ''', (self.id, self.name, self.department, self.salary))
        conn.commit()
        print(f"✓ Saved {self.name} to database")
    
    def give_raise(self, percent):
        """Increase salary by percentage"""
        self.salary = self.salary * (1 + percent/100)
        print(f"✓ {self.name} got {percent}% raise: ${self.salary:,.0f}")
    
    def __str__(self):
        """String representation"""
        return f"Employee({self.name}, {self.department}, ${self.salary:,})"

# Test it
if __name__ == "__main__":
    # Connect to database
    conn = sqlite3.connect('company.db')
    
    # Create table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY,
            name TEXT,
            department TEXT,
            salary REAL
        )
    ''')
    
    # Create and save employees
    emp1 = Employee(1, "Alice", "IT", 70000)
    emp1.save_to_db(conn)
    
    emp2 = Employee(2, "Bob", "Sales", 60000)
    emp2.save_to_db(conn)
    
    # Give raise and update database
    emp1.give_raise(10)
    emp1.save_to_db(conn)
    
    conn.close()
```

---

## Step 3: Database Manager Class

```python
import sqlite3

class Employee:
    def __init__(self, id, name, department, salary):
        self.id = id
        self.name = name
        self.department = department
        self.salary = salary
    
    def __str__(self):
        return f"{self.name} ({self.department}): ${self.salary:,.0f}"

class EmployeeDatabase:
    """Manages employee database operations"""
    
    def __init__(self, db_name='company.db'):
        self.conn = sqlite3.connect(db_name)
        self.create_table()
    
    def create_table(self):
        """Create employees table"""
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                department TEXT,
                salary REAL
            )
        ''')
        self.conn.commit()
    
    def add_employee(self, employee):
        """Add employee to database"""
        self.conn.execute('''
            INSERT INTO employees (id, name, department, salary)
            VALUES (?, ?, ?, ?)
        ''', (employee.id, employee.name, employee.department, employee.salary))
        self.conn.commit()
        print(f"✓ Added {employee.name}")
    
    def get_all_employees(self):
        """Get all employees as objects"""
        cursor = self.conn.execute('SELECT * FROM employees')
        employees = []
        for row in cursor:
            emp = Employee(row[0], row[1], row[2], row[3])
            employees.append(emp)
        return employees
    
    def get_employee_by_id(self, emp_id):
        """Get specific employee"""
        cursor = self.conn.execute(
            'SELECT * FROM employees WHERE id = ?', (emp_id,)
        )
        row = cursor.fetchone()
        if row:
            return Employee(row[0], row[1], row[2], row[3])
        return None
    
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
    
    def get_department_employees(self, department):
        """Get employees by department"""
        cursor = self.conn.execute(
            'SELECT * FROM employees WHERE department = ?', (department,)
        )
        return [Employee(r[0], r[1], r[2], r[3]) for r in cursor]
    
    def close(self):
        """Close database connection"""
        self.conn.close()

# Test it
if __name__ == "__main__":
    db = EmployeeDatabase()
    
    # Create employee objects
    emp1 = Employee(1, "Alice", "IT", 70000)
    emp2 = Employee(2, "Bob", "Sales", 60000)
    emp3 = Employee(3, "Charlie", "IT", 80000)
    
    # Add to database
    db.add_employee(emp1)
    db.add_employee(emp2)
    db.add_employee(emp3)
    
    # Get all employees
    print("\nAll Employees:")
    for emp in db.get_all_employees():
        print(emp)
    
    # Get IT employees
    print("\nIT Department:")
    for emp in db.get_department_employees("IT"):
        print(emp)
    
    # Update salary
    db.update_salary(1, 75000)
    
    # Get updated employee
    updated = db.get_employee_by_id(1)
    print(f"\nUpdated: {updated}")
    
    db.close()
```

---

## Step 4: Inheritance

```python
class Employee:
    """Base employee class"""
    
    def __init__(self, id, name, salary):
        self.id = id
        self.name = name
        self.salary = salary
    
    def get_annual_salary(self):
        return self.salary * 12
    
    def __str__(self):
        return f"{self.name}: ${self.salary:,}/month"

class Manager(Employee):
    """Manager inherits from Employee"""
    
    def __init__(self, id, name, salary, team_size):
        super().__init__(id, name, salary)  # Call parent constructor
        self.team_size = team_size
    
    def get_bonus(self):
        """Managers get bonus based on team size"""
        return self.team_size * 1000
    
    def __str__(self):
        return f"Manager {self.name}: ${self.salary:,}/month ({self.team_size} team members)"

class Developer(Employee):
    """Developer inherits from Employee"""
    
    def __init__(self, id, name, salary, programming_language):
        super().__init__(id, name, salary)
        self.language = programming_language
    
    def __str__(self):
        return f"Developer {self.name} ({self.language}): ${self.salary:,}/month"

# Test it
emp = Employee(1, "Alice", 60000)
mgr = Manager(2, "Bob", 90000, 5)
dev = Developer(3, "Charlie", 75000, "Python")

print(emp)
print(mgr)
print(dev)

print(f"\nBob's annual salary: ${mgr.get_annual_salary():,}")
print(f"Bob's bonus: ${mgr.get_bonus():,}")
```

**Output:**
```
Alice: $60,000/month
Manager Bob: $90,000/month (5 team members)
Developer Charlie (Python): $75,000/month

Bob's annual salary: $1,080,000
Bob's bonus: $5,000
```

---

## Step 5: Complete Application

```python
import sqlite3

class Employee:
    """Represents an employee"""
    
    def __init__(self, id, name, department, salary):
        self.id = id
        self.name = name
        self.department = department
        self.salary = salary
    
    def give_raise(self, percent):
        self.salary *= (1 + percent/100)
        return self.salary
    
    def to_tuple(self):
        """Convert to tuple for database"""
        return (self.id, self.name, self.department, self.salary)
    
    def __str__(self):
        return f"ID {self.id}: {self.name} - {self.department} - ${self.salary:,.0f}"

class Company:
    """Manages company database and employees"""
    
    def __init__(self, db_name='company.db'):
        self.conn = sqlite3.connect(db_name)
        self.setup_database()
    
    def setup_database(self):
        """Create necessary tables"""
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                department TEXT,
                salary REAL
            )
        ''')
        self.conn.commit()
    
    def hire_employee(self, employee):
        """Hire new employee"""
        self.conn.execute(
            'INSERT INTO employees VALUES (?, ?, ?, ?)',
            employee.to_tuple()
        )
        self.conn.commit()
        print(f"✓ Hired {employee.name}")
    
    def fire_employee(self, emp_id):
        """Fire employee"""
        self.conn.execute('DELETE FROM employees WHERE id = ?', (emp_id,))
        self.conn.commit()
        print(f"✓ Fired employee ID {emp_id}")
    
    def get_all_employees(self):
        """Get all employees"""
        cursor = self.conn.execute('SELECT * FROM employees ORDER BY id')
        return [Employee(*row) for row in cursor]
    
    def find_employee(self, emp_id):
        """Find employee by ID"""
        cursor = self.conn.execute(
            'SELECT * FROM employees WHERE id = ?', (emp_id,)
        )
        row = cursor.fetchone()
        return Employee(*row) if row else None
    
    def give_department_raise(self, department, percent):
        """Give raise to entire department"""
        self.conn.execute('''
            UPDATE employees 
            SET salary = salary * (1 + ? / 100)
            WHERE department = ?
        ''', (percent, department))
        self.conn.commit()
        print(f"✓ Gave {department} department {percent}% raise")
    
    def get_statistics(self):
        """Get company statistics"""
        cursor = self.conn.execute('''
            SELECT 
                COUNT(*) as total,
                AVG(salary) as avg_salary,
                SUM(salary) as total_salary
            FROM employees
        ''')
        return cursor.fetchone()
    
    def list_employees(self):
        """Print all employees"""
        employees = self.get_all_employees()
        print(f"\n{'ID':<5} {'Name':<15} {'Department':<12} {'Salary':<12}")
        print("-" * 50)
        for emp in employees:
            print(f"{emp.id:<5} {emp.name:<15} {emp.department:<12} ${emp.salary:<11,.0f}")
        print(f"\nTotal: {len(employees)} employees")
    
    def close(self):
        """Close database"""
        self.conn.close()

# Main Application
class CompanyApp:
    """Main application"""
    
    def __init__(self):
        self.company = Company()
    
    def menu(self):
        print("\n" + "="*40)
        print("      COMPANY MANAGEMENT")
        print("="*40)
        print("1. Hire Employee")
        print("2. View All Employees")
        print("3. Find Employee")
        print("4. Give Department Raise")
        print("5. Company Statistics")
        print("6. Fire Employee")
        print("0. Exit")
        print("="*40)
    
    def run(self):
        while True:
            self.menu()
            choice = input("\nChoice: ").strip()
            
            if choice == '1':
                self.hire_employee()
            elif choice == '2':
                self.company.list_employees()
            elif choice == '3':
                self.find_employee()
            elif choice == '4':
                self.department_raise()
            elif choice == '5':
                self.show_statistics()
            elif choice == '6':
                self.fire_employee()
            elif choice == '0':
                print("\nGoodbye!")
                self.company.close()
                break
            else:
                print("Invalid choice!")
    
    def hire_employee(self):
        print("\n--- Hire Employee ---")
        try:
            id = int(input("ID: "))
            name = input("Name: ")
            dept = input("Department: ")
            salary = float(input("Salary: "))
            
            emp = Employee(id, name, dept, salary)
            self.company.hire_employee(emp)
        except ValueError:
            print("Invalid input!")
    
    def find_employee(self):
        try:
            emp_id = int(input("\nEmployee ID: "))
            emp = self.company.find_employee(emp_id)
            if emp:
                print(f"\nFound: {emp}")
            else:
                print("Employee not found!")
        except ValueError:
            print("Invalid ID!")
    
    def department_raise(self):
        dept = input("\nDepartment: ")
        try:
            percent = float(input("Raise %: "))
            self.company.give_department_raise(dept, percent)
        except ValueError:
            print("Invalid percentage!")
    
    def show_statistics(self):
        total, avg, total_sal = self.company.get_statistics()
        print(f"\n--- Company Statistics ---")
        print(f"Total Employees: {total}")
        print(f"Average Salary: ${avg:,.0f}")
        print(f"Total Payroll: ${total_sal:,.0f}")
    
    def fire_employee(self):
        try:
            emp_id = int(input("\nEmployee ID to fire: "))
            confirm = input("Are you sure? (yes/no): ")
            if confirm.lower() == 'yes':
                self.company.fire_employee(emp_id)
        except ValueError:
            print("Invalid ID!")

# Run the app
if __name__ == "__main__":
    app = CompanyApp()
    app.run()
```

---

## Quick Start

### 1. Add sample data

```python
# setup_data.py
from step5 import Company, Employee

company = Company()

employees = [
    Employee(1, "Alice Johnson", "IT", 70000),
    Employee(2, "Bob Smith", "Sales", 60000),
    Employee(3, "Charlie Brown", "IT", 80000),
    Employee(4, "Diana Prince", "HR", 55000),
]

for emp in employees:
    company.hire_employee(emp)

company.close()
print("✓ Sample data added!")
```

### 2. Run the app

```bash
python step5.py
```

---

## OOP Concepts Summary

| Concept | What It Is | Example |
|---------|-----------|---------|
| **Class** | Blueprint for objects | `class Employee:` |
| **Object** | Instance of a class | `emp = Employee(...)` |
| **`__init__`** | Constructor method | Runs when creating object |
| **`self`** | Reference to current object | `self.name = name` |
| **Method** | Function inside a class | `def give_raise(self):` |
| **Inheritance** | Class inherits from another | `class Manager(Employee):` |
| **`super()`** | Call parent class method | `super().__init__(...)` |

---

## Why Use OOP with SQL?

✅ **Organized:** Each table = one class  
✅ **Reusable:** Create/modify objects easily  
✅ **Maintainable:** Change logic in one place  
✅ **Readable:** Code makes sense  

**Example:**
```python
# OOP way - clear and simple
emp = Employee(1, "Alice", "IT", 70000)
emp.give_raise(10)
emp.save_to_db(conn)

# vs. Without OOP - repetitive
cursor.execute('SELECT * FROM employees WHERE id = 1')
row = cursor.fetchone()
new_salary = row[3] * 1.10
cursor.execute('UPDATE employees SET salary = ? WHERE id = 1', (new_salary,))
```

---

## Practice Exercises

### Easy
1. Add a method `get_annual_salary()` to Employee class
2. Add a method to check if salary > 70000
3. Create a `Product` class with name and price

### Medium
1. Add a `Department` class that stores employees
2. Create a method to calculate total department salary
3. Add validation: salary must be > 0

### Challenge
1. Create `Manager` class that inherits from `Employee`
2. Add a `Project` class and link employees to projects
3. Generate a report of all managers and their teams

---

## Common Patterns

### Pattern 1: Class represents table row
```python
class Employee:  # → employees table
    def __init__(self, id, name, salary):
        self.id = id        # → id column
        self.name = name    # → name column
        self.salary = salary # → salary column
```

### Pattern 2: Database manager class
```python
class EmployeeDB:
    def __init__(self):
        self.conn = sqlite3.connect('db.db')
    
    def add_employee(self, employee):
        # SQL INSERT
    
    def get_employee(self, id):
        # SQL SELECT
        return Employee(...)
```

### Pattern 3: Convert between object and tuple
```python
class Employee:
    def to_tuple(self):
        """For INSERT"""
        return (self.id, self.name, self.salary)
    
    @classmethod
    def from_tuple(cls, data):
        """For SELECT"""
        return cls(data[0], data[1], data[2])
```

---

## Tips

💡 **One class per table** - Makes code organized  
💡 **Use `__str__`** - Makes printing objects easy  
💡 **Methods for common tasks** - Like `save()`, `delete()`  
💡 **Separate DB logic** - Use a manager class  
💡 **Use inheritance** - For similar types (Employee → Manager)

---

## What's Next?

1. 📚 Learn more OOP: properties, class variables, static methods
2. 🗄️ Try ORMs like **SQLAlchemy** (handles SQL for you)
3. 🌐 Build a web app with **Flask** + OOP
4. 📊 Add data validation and error handling
5. 🧪 Write unit tests for your classes

---

**You now know OOP with SQL! 🎉**

Build projects like:
- Task management system
- Student grade tracker  
- Inventory management
- Library system
