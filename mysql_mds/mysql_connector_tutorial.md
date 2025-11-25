# MySQL Connector Python Tutorial for Beginners

A simple guide to connecting Python with MySQL databases.

---

## 🎯 What You'll Learn

- Install and connect to MySQL
- Create databases and tables
- Insert, read, update, and delete data
- Use with real examples

---

## Step 1: Install MySQL Connector

```bash
pip install mysql-connector-python
```

**Verify installation:**
```python
import mysql.connector
print("✓ MySQL Connector installed!")
```

---

## Step 2: Connect to MySQL

```python
import mysql.connector

# Connect to MySQL server
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password"
)

if connection.is_connected():
    print("✓ Connected to MySQL!")

connection.close()
```

**Common connection parameters:**
- `host` - Server address (usually "localhost")
- `user` - MySQL username (default: "root")
- `password` - Your MySQL password
- `database` - Database name (optional)

---

## Step 3: Create Database

```python
import mysql.connector

# Connect to MySQL
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password"
)

cursor = connection.cursor()

# Create database
cursor.execute("CREATE DATABASE IF NOT EXISTS company")
print("✓ Database created!")

# Show all databases
cursor.execute("SHOW DATABASES")
for db in cursor:
    print(db)

cursor.close()
connection.close()
```

---

## Step 4: Create Table

```python
import mysql.connector

# Connect to MySQL with database
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password",
    database="company"
)

cursor = connection.cursor()

# Create table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS employees (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100),
        department VARCHAR(50),
        salary DECIMAL(10, 2)
    )
""")

print("✓ Table created!")

cursor.close()
connection.close()
```

---

## Step 5: Insert Data

### Insert One Record

```python
import mysql.connector

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password",
    database="company"
)

cursor = connection.cursor()

# Insert one employee
sql = "INSERT INTO employees (name, department, salary) VALUES (%s, %s, %s)"
values = ("Alice", "IT", 70000)

cursor.execute(sql, values)
connection.commit()  # Important: Save changes

print(f"✓ Inserted! ID: {cursor.lastrowid}")

cursor.close()
connection.close()
```

### Insert Multiple Records

```python
import mysql.connector

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password",
    database="company"
)

cursor = connection.cursor()

# Insert multiple employees
sql = "INSERT INTO employees (name, department, salary) VALUES (%s, %s, %s)"
values = [
    ("Bob", "Sales", 60000),
    ("Charlie", "IT", 80000),
    ("Diana", "HR", 55000)
]

cursor.executemany(sql, values)
connection.commit()

print(f"✓ Inserted {cursor.rowcount} records!")

cursor.close()
connection.close()
```

---

## Step 6: Read Data (SELECT)

### Get All Records

```python
import mysql.connector

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password",
    database="company"
)

cursor = connection.cursor()

# Select all employees
cursor.execute("SELECT * FROM employees")

# Fetch all results
results = cursor.fetchall()

print("All Employees:")
for row in results:
    print(row)

cursor.close()
connection.close()
```

**Output:**
```
(1, 'Alice', 'IT', 70000.00)
(2, 'Bob', 'Sales', 60000.00)
(3, 'Charlie', 'IT', 80000.00)
```

### Get Specific Columns

```python
cursor.execute("SELECT name, salary FROM employees")

for (name, salary) in cursor:
    print(f"{name}: ${salary:,.2f}")
```

### Get One Record

```python
cursor.execute("SELECT * FROM employees WHERE id = %s", (1,))
result = cursor.fetchone()
print(result)
```

---

## Step 7: Filter Data (WHERE)

```python
import mysql.connector

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password",
    database="company"
)

cursor = connection.cursor()

# Filter by department
cursor.execute("SELECT * FROM employees WHERE department = %s", ("IT",))
print("IT Department:")
for row in cursor:
    print(row)

# Filter by salary
cursor.execute("SELECT name, salary FROM employees WHERE salary > %s", (65000,))
print("\nHigh Earners:")
for (name, salary) in cursor:
    print(f"{name}: ${salary:,.2f}")

# Multiple conditions
cursor.execute("""
    SELECT * FROM employees 
    WHERE department = %s AND salary > %s
""", ("IT", 70000))
print("\nSenior IT:")
for row in cursor:
    print(row)

cursor.close()
connection.close()
```

---

## Step 8: Update Data

```python
import mysql.connector

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password",
    database="company"
)

cursor = connection.cursor()

# Update one employee
sql = "UPDATE employees SET salary = %s WHERE name = %s"
values = (75000, "Alice")

cursor.execute(sql, values)
connection.commit()

print(f"✓ Updated {cursor.rowcount} record(s)")

# Update multiple records (give IT department a raise)
sql = "UPDATE employees SET salary = salary * 1.10 WHERE department = %s"
cursor.execute(sql, ("IT",))
connection.commit()

print(f"✓ Updated {cursor.rowcount} IT employees")

cursor.close()
connection.close()
```

---

## Step 9: Delete Data

```python
import mysql.connector

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password",
    database="company"
)

cursor = connection.cursor()

# Delete specific employee
sql = "DELETE FROM employees WHERE id = %s"
cursor.execute(sql, (4,))
connection.commit()

print(f"✓ Deleted {cursor.rowcount} record(s)")

cursor.close()
connection.close()
```

**⚠️ Warning:** Always use WHERE clause! Without it, all records will be deleted.

---

## Step 10: Using Dictionary Cursor

```python
import mysql.connector

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password",
    database="company"
)

# Use dictionary cursor for easier access
cursor = connection.cursor(dictionary=True)

cursor.execute("SELECT * FROM employees")

for row in cursor:
    print(f"Name: {row['name']}")
    print(f"Department: {row['department']}")
    print(f"Salary: ${row['salary']:,.2f}")
    print()

cursor.close()
connection.close()
```

---

## Step 11: Error Handling

```python
import mysql.connector
from mysql.connector import Error

try:
    # Connect to MySQL
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="your_password",
        database="company"
    )
    
    if connection.is_connected():
        cursor = connection.cursor()
        
        # Execute query
        cursor.execute("SELECT * FROM employees")
        results = cursor.fetchall()
        
        for row in results:
            print(row)
        
except Error as e:
    print(f"Error: {e}")

finally:
    # Always close connection
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("✓ Connection closed")
```

---

## Step 12: Complete Example - Employee Manager

```python
import mysql.connector
from mysql.connector import Error

class EmployeeDB:
    """Manages employee database operations"""
    
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
    
    def connect(self):
        """Connect to MySQL database"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if self.connection.is_connected():
                print("✓ Connected to MySQL")
        except Error as e:
            print(f"Error: {e}")
    
    def create_table(self):
        """Create employees table"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS employees (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    department VARCHAR(50),
                    salary DECIMAL(10, 2)
                )
            """)
            print("✓ Table ready")
        except Error as e:
            print(f"Error: {e}")
    
    def add_employee(self, name, department, salary):
        """Add new employee"""
        try:
            cursor = self.connection.cursor()
            sql = "INSERT INTO employees (name, department, salary) VALUES (%s, %s, %s)"
            cursor.execute(sql, (name, department, salary))
            self.connection.commit()
            print(f"✓ Added {name} (ID: {cursor.lastrowid})")
            return cursor.lastrowid
        except Error as e:
            print(f"Error: {e}")
            return None
    
    def get_all_employees(self):
        """Get all employees"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM employees")
            return cursor.fetchall()
        except Error as e:
            print(f"Error: {e}")
            return []
    
    def get_employee_by_id(self, emp_id):
        """Get employee by ID"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM employees WHERE id = %s", (emp_id,))
            return cursor.fetchone()
        except Error as e:
            print(f"Error: {e}")
            return None
    
    def update_salary(self, emp_id, new_salary):
        """Update employee salary"""
        try:
            cursor = self.connection.cursor()
            sql = "UPDATE employees SET salary = %s WHERE id = %s"
            cursor.execute(sql, (new_salary, emp_id))
            self.connection.commit()
            print(f"✓ Updated salary for employee {emp_id}")
        except Error as e:
            print(f"Error: {e}")
    
    def delete_employee(self, emp_id):
        """Delete employee"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("DELETE FROM employees WHERE id = %s", (emp_id,))
            self.connection.commit()
            print(f"✓ Deleted employee {emp_id}")
        except Error as e:
            print(f"Error: {e}")
    
    def get_department_employees(self, department):
        """Get employees by department"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM employees WHERE department = %s", (department,))
            return cursor.fetchall()
        except Error as e:
            print(f"Error: {e}")
            return []
    
    def close(self):
        """Close database connection"""
        if self.connection.is_connected():
            self.connection.close()
            print("✓ Connection closed")

# Usage Example
if __name__ == "__main__":
    # Create database manager
    db = EmployeeDB(
        host="localhost",
        user="root",
        password="your_password",
        database="company"
    )
    
    # Connect and setup
    db.connect()
    db.create_table()
    
    # Add employees
    db.add_employee("Alice", "IT", 70000)
    db.add_employee("Bob", "Sales", 60000)
    db.add_employee("Charlie", "IT", 80000)
    
    # Get all employees
    print("\n=== All Employees ===")
    employees = db.get_all_employees()
    for emp in employees:
        print(f"ID {emp['id']}: {emp['name']} - {emp['department']} - ${emp['salary']:,.2f}")
    
    # Get IT department
    print("\n=== IT Department ===")
    it_emps = db.get_department_employees("IT")
    for emp in it_emps:
        print(f"{emp['name']}: ${emp['salary']:,.2f}")
    
    # Update salary
    db.update_salary(1, 75000)
    
    # Close connection
    db.close()
```

---

## Step 13: Using with Context Manager

```python
import mysql.connector
from mysql.connector import Error

class Database:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
    
    def __enter__(self):
        """Connect when entering context"""
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        return self.connection
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close when exiting context"""
        if self.connection.is_connected():
            self.connection.close()

# Usage with 'with' statement (automatically closes connection)
with Database("localhost", "root", "your_password", "company") as conn:
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM employees")
    
    for row in cursor:
        print(row)
    
    cursor.close()
# Connection automatically closed here
```

---

## Step 14: Connection Pool (For Multiple Queries)

```python
import mysql.connector
from mysql.connector import pooling

# Create connection pool
pool = pooling.MySQLConnectionPool(
    pool_name="mypool",
    pool_size=5,
    host="localhost",
    user="root",
    password="your_password",
    database="company"
)

# Get connection from pool
connection = pool.get_connection()
cursor = connection.cursor()

cursor.execute("SELECT * FROM employees")
for row in cursor:
    print(row)

cursor.close()
connection.close()  # Returns connection to pool

print("✓ Connection returned to pool")
```

---

## Quick Reference

### Connect to MySQL
```python
import mysql.connector

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="dbname"
)
```

### Execute Query
```python
cursor = connection.cursor()
cursor.execute("SELECT * FROM table")
results = cursor.fetchall()
```

### Insert Data
```python
sql = "INSERT INTO table (col1, col2) VALUES (%s, %s)"
cursor.execute(sql, (val1, val2))
connection.commit()
```

### Update Data
```python
sql = "UPDATE table SET col = %s WHERE id = %s"
cursor.execute(sql, (value, id))
connection.commit()
```

### Delete Data
```python
sql = "DELETE FROM table WHERE id = %s"
cursor.execute(sql, (id,))
connection.commit()
```

### Close Connection
```python
cursor.close()
connection.close()
```

---

## Common Operations

### Check if Connected
```python
if connection.is_connected():
    print("Connected!")
```

### Get Last Inserted ID
```python
cursor.execute("INSERT INTO ...")
last_id = cursor.lastrowid
```

### Get Row Count
```python
cursor.execute("UPDATE ...")
print(f"Updated {cursor.rowcount} rows")
```

### Show Tables
```python
cursor.execute("SHOW TABLES")
for table in cursor:
    print(table)
```

### Describe Table
```python
cursor.execute("DESCRIBE employees")
for column in cursor:
    print(column)
```

---

## Practice Exercises

### Easy
1. Create a database called "school"
2. Create a "students" table with id, name, grade
3. Insert 5 students
4. Display all students

### Medium
1. Create a products table
2. Insert 10 products with prices
3. Update prices (increase by 10%)
4. Find products with price > 100
5. Calculate average price

### Challenge
1. Create a library system with books and members tables
2. Implement borrow/return functionality
3. Create reports (most borrowed books, member activity)
4. Export data to CSV

---

## Common Errors & Solutions

### Error: Access denied
```python
# Solution: Check username and password
connection = mysql.connector.connect(
    user="root",
    password="correct_password"
)
```

### Error: Unknown database
```python
# Solution: Create database first
cursor.execute("CREATE DATABASE IF NOT EXISTS company")
```

### Error: Table doesn't exist
```python
# Solution: Create table first
cursor.execute("CREATE TABLE IF NOT EXISTS ...")
```

### Error: Connection lost
```python
# Solution: Add error handling and reconnect
try:
    cursor.execute("SELECT ...")
except mysql.connector.Error as e:
    if e.errno == 2006:  # MySQL server has gone away
        connection.reconnect()
```

---

## Best Practices

✅ **Always use parameterized queries** - Prevents SQL injection
```python
# GOOD
cursor.execute("SELECT * FROM users WHERE name = %s", (name,))

# BAD (vulnerable to SQL injection)
cursor.execute(f"SELECT * FROM users WHERE name = '{name}'")
```

✅ **Always commit changes** - For INSERT, UPDATE, DELETE
```python
cursor.execute("INSERT ...")
connection.commit()
```

✅ **Always close connections**
```python
cursor.close()
connection.close()
```

✅ **Use try-except-finally**
```python
try:
    # Database operations
except Error as e:
    print(f"Error: {e}")
finally:
    connection.close()
```

✅ **Use connection pooling** for multiple queries

---

## Configuration File (Recommended)

Create `config.py`:
```python
# config.py
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'your_password',
    'database': 'company'
}
```

Use in your code:
```python
# main.py
import mysql.connector
from config import DB_CONFIG

connection = mysql.connector.connect(**DB_CONFIG)
```

---

## What's Next?

1. 🔐 Learn about **database security** and user permissions
2. 📊 Combine with **Pandas** for data analysis
3. 🌐 Build a **web application** with Flask/Django
4. ⚡ Learn about **database optimization** and indexes
5. 🔄 Explore **database transactions** and rollback

---

**You now know how to use MySQL with Python! 🎉**

Build projects like:
- User management system
- E-commerce database
- Blog with MySQL backend
- Inventory tracking system
