# Python & SQL Tutorial for Beginners

A simple, practical guide to working with Python and SQL databases.

---

## 🎯 What You'll Learn

- Connect Python to a database
- Create tables
- Insert, read, update, and delete data
- Run queries and analyze results

---

## 📦 Setup

SQLite comes built-in with Python - no installation needed!

```python
import sqlite3  # Already included in Python
```

---

## Step 1: Connect to Database

```python
import sqlite3

# Create/connect to database
conn = sqlite3.connect('mydata.db')
cursor = conn.cursor()

print("✓ Connected to database!")

# Always close when done
conn.close()
```

---

## Step 2: Create a Table

```python
import sqlite3

conn = sqlite3.connect('mydata.db')
cursor = conn.cursor()

# Create employees table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        department TEXT,
        salary REAL
    )
''')

conn.commit()
print("✓ Table created!")

conn.close()
```

**SQL Explained:**
- `INTEGER PRIMARY KEY` - Unique ID number
- `TEXT` - Text/string data
- `REAL` - Decimal numbers
- `NOT NULL` - Field is required

---

## Step 3: Insert Data

```python
import sqlite3

conn = sqlite3.connect('mydata.db')
cursor = conn.cursor()

# Insert one employee
cursor.execute('''
    INSERT INTO employees (id, name, department, salary)
    VALUES (1, 'Alice', 'IT', 75000)
''')

# Insert multiple employees
employees = [
    (2, 'Bob', 'Sales', 60000),
    (3, 'Charlie', 'IT', 80000),
    (4, 'Diana', 'HR', 55000)
]

cursor.executemany('''
    INSERT INTO employees (id, name, department, salary)
    VALUES (?, ?, ?, ?)
''', employees)

conn.commit()
print("✓ Data inserted!")

conn.close()
```

**Important:** 
- Use `?` placeholders to prevent SQL injection
- Call `conn.commit()` to save changes

---

## Step 4: Read Data (SELECT)

```python
import sqlite3

conn = sqlite3.connect('mydata.db')
cursor = conn.cursor()

# Get all employees
cursor.execute('SELECT * FROM employees')
rows = cursor.fetchall()

print("All Employees:")
for row in rows:
    print(row)

# Get specific columns
cursor.execute('SELECT name, salary FROM employees')
results = cursor.fetchall()

print("\nNames and Salaries:")
for name, salary in results:
    print(f"{name}: ${salary:,.0f}")

conn.close()
```

**Output:**
```
All Employees:
(1, 'Alice', 'IT', 75000.0)
(2, 'Bob', 'Sales', 60000.0)
(3, 'Charlie', 'IT', 80000.0)
(4, 'Diana', 'HR', 55000.0)

Names and Salaries:
Alice: $75,000
Bob: $60,000
Charlie: $80,000
Diana: $55,000
```

---

## Step 5: Filter Data (WHERE)

```python
import sqlite3

conn = sqlite3.connect('mydata.db')
cursor = conn.cursor()

# Find IT employees
cursor.execute('''
    SELECT * FROM employees 
    WHERE department = 'IT'
''')

print("IT Department:")
for row in cursor.fetchall():
    print(row)

# Find high earners
cursor.execute('''
    SELECT name, salary FROM employees 
    WHERE salary > 65000
''')

print("\nHigh Earners (>$65k):")
for name, salary in cursor.fetchall():
    print(f"{name}: ${salary:,.0f}")

# Find by name pattern
cursor.execute('''
    SELECT * FROM employees 
    WHERE name LIKE 'A%'
''')

print("\nNames starting with 'A':")
for row in cursor.fetchall():
    print(row[1])  # row[1] is the name

conn.close()
```

---

## Step 6: Update Data

```python
import sqlite3

conn = sqlite3.connect('mydata.db')
cursor = conn.cursor()

# Give Alice a raise
cursor.execute('''
    UPDATE employees 
    SET salary = 82000 
    WHERE name = 'Alice'
''')

# Give IT department 10% raise
cursor.execute('''
    UPDATE employees 
    SET salary = salary * 1.10 
    WHERE department = 'IT'
''')

conn.commit()
print("✓ Data updated!")

# Verify changes
cursor.execute('SELECT name, salary FROM employees WHERE department = "IT"')
print("\nIT Department after raises:")
for name, salary in cursor.fetchall():
    print(f"{name}: ${salary:,.0f}")

conn.close()
```

---

## Step 7: Delete Data

```python
import sqlite3

conn = sqlite3.connect('mydata.db')
cursor = conn.cursor()

# Delete specific employee
cursor.execute('''
    DELETE FROM employees 
    WHERE id = 4
''')

# Delete all low earners (example - be careful!)
cursor.execute('''
    DELETE FROM employees 
    WHERE salary < 50000
''')

conn.commit()
print("✓ Data deleted!")

# Count remaining employees
cursor.execute('SELECT COUNT(*) FROM employees')
count = cursor.fetchone()[0]
print(f"Remaining employees: {count}")

conn.close()
```

**⚠️ Warning:** DELETE is permanent! Always test with WHERE clause first.

---

## Step 8: Aggregate Functions

```python
import sqlite3

conn = sqlite3.connect('mydata.db')
cursor = conn.cursor()

# Count employees
cursor.execute('SELECT COUNT(*) FROM employees')
total = cursor.fetchone()[0]
print(f"Total employees: {total}")

# Average salary
cursor.execute('SELECT AVG(salary) FROM employees')
avg_salary = cursor.fetchone()[0]
print(f"Average salary: ${avg_salary:,.2f}")

# Min and Max salary
cursor.execute('SELECT MIN(salary), MAX(salary) FROM employees')
min_sal, max_sal = cursor.fetchone()
print(f"Salary range: ${min_sal:,.0f} - ${max_sal:,.0f}")

# Sum of all salaries
cursor.execute('SELECT SUM(salary) FROM employees')
total_cost = cursor.fetchone()[0]
print(f"Total salary cost: ${total_cost:,.0f}")

conn.close()
```

---

## Step 9: Group By

```python
import sqlite3

conn = sqlite3.connect('mydata.db')
cursor = conn.cursor()

# Count employees per department
cursor.execute('''
    SELECT department, COUNT(*) as employee_count
    FROM employees
    GROUP BY department
''')

print("Employees per Department:")
for dept, count in cursor.fetchall():
    print(f"{dept}: {count} employees")

# Average salary per department
cursor.execute('''
    SELECT department, AVG(salary) as avg_salary
    FROM employees
    GROUP BY department
    ORDER BY avg_salary DESC
''')

print("\nAverage Salary by Department:")
for dept, avg in cursor.fetchall():
    print(f"{dept}: ${avg:,.0f}")

conn.close()
```

---

## Step 10: Complete Example - Simple App

```python
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
```

---

## Quick Reference

### Connect to Database
```python
conn = sqlite3.connect('database.db')
cursor = conn.cursor()
```

### Create Table
```python
cursor.execute('CREATE TABLE table_name (id INTEGER PRIMARY KEY, name TEXT)')
conn.commit()
```

### Insert Data
```python
cursor.execute('INSERT INTO table_name VALUES (?, ?)', (value1, value2))
conn.commit()
```

### Select Data
```python
cursor.execute('SELECT * FROM table_name')
rows = cursor.fetchall()
```

### Update Data
```python
cursor.execute('UPDATE table_name SET column = ? WHERE id = ?', (new_value, id))
conn.commit()
```

### Delete Data
```python
cursor.execute('DELETE FROM table_name WHERE id = ?', (id,))
conn.commit()
```

### Close Connection
```python
conn.close()
```

---

## Common SQL Commands

| Command | Purpose | Example |
|---------|---------|---------|
| `SELECT` | Get data | `SELECT * FROM employees` |
| `WHERE` | Filter results | `WHERE salary > 50000` |
| `ORDER BY` | Sort results | `ORDER BY name ASC` |
| `GROUP BY` | Group data | `GROUP BY department` |
| `COUNT()` | Count rows | `SELECT COUNT(*) FROM employees` |
| `AVG()` | Average | `SELECT AVG(salary) FROM employees` |
| `SUM()` | Total | `SELECT SUM(salary) FROM employees` |
| `MIN()` | Minimum | `SELECT MIN(salary) FROM employees` |
| `MAX()` | Maximum | `SELECT MAX(salary) FROM employees` |

---

## Practice Exercises

### Easy
1. Create a table for products with name and price
2. Insert 5 products
3. Select all products under $50

### Medium
1. Calculate average product price
2. Update prices - increase all by 10%
3. Find the most expensive product

### Challenge
1. Create a customers table
2. Create an orders table linking to customers
3. Query to show customer names with their total orders

---

## Common Mistakes

❌ **Forgetting to commit**
```python
cursor.execute('INSERT ...')
# Missing: conn.commit()
```

❌ **Not using placeholders (SQL injection risk)**
```python
# BAD:
cursor.execute(f"SELECT * FROM users WHERE name = '{user_input}'")

# GOOD:
cursor.execute("SELECT * FROM users WHERE name = ?", (user_input,))
```

❌ **Not closing connection**
```python
conn = sqlite3.connect('db.db')
# ... do work ...
# Missing: conn.close()
```

✅ **Better: Use context manager**
```python
with sqlite3.connect('db.db') as conn:
    cursor = conn.cursor()
    # ... do work ...
    # Automatically commits and closes
```

---

## Tips

💡 **Always use placeholders (?)** - Prevents SQL injection attacks

💡 **Commit after changes** - `INSERT`, `UPDATE`, `DELETE` need `conn.commit()`

💡 **Close connections** - Use `conn.close()` or context managers

💡 **Test queries first** - Run `SELECT` before `DELETE` to verify what will be deleted

💡 **Use AUTOINCREMENT** - Let database handle ID numbers automatically

---

## What's Next?

1. 📊 Learn **pandas** to analyze SQL data as DataFrames
2. 🗄️ Try **PostgreSQL** or **MySQL** for production apps
3. 🔒 Learn about database **indexes** for faster queries
4. 🌐 Build a web app with **Flask** + SQL
5. 📈 Create visualizations from your database data

---

**You now know the basics of Python + SQL! 🎉**

Keep practicing by building small projects like:
- Todo list app
- Contact manager
- Personal expense tracker
- Inventory system
