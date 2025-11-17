# Beginner's Guide to Python, SQL, and CSV

## Table of Contents
1. [Introduction](#introduction)
2. [Python Basics](#python-basics)
3. [Working with CSV Files](#working-with-csv-files)
4. [SQL Fundamentals](#sql-fundamentals)
5. [Connecting Python with SQL](#connecting-python-with-sql)
6. [Practical Examples](#practical-examples)

---

## Introduction

This guide will help you understand how to work with Python, SQL databases, and CSV files. These are essential skills for data analysis, automation, and backend development.

**What you'll learn:**
- Python programming basics
- Reading and writing CSV files
- SQL database operations
- Integrating Python with SQL databases

---

## Python Basics

### Installing Python

Download Python from [python.org](https://www.python.org/) and install it. Verify installation:

```bash
python --version
```

### Basic Python Syntax

```python
# Variables
name = "John"
age = 25
price = 19.99

# Lists
fruits = ["apple", "banana", "cherry"]

# Dictionaries
person = {
    "name": "Alice",
    "age": 30,
    "city": "New York"
}

# Functions
def greet(name):
    return f"Hello, {name}!"

print(greet("World"))

# Loops
for fruit in fruits:
    print(fruit)

# Conditionals
if age >= 18:
    print("Adult")
else:
    print("Minor")
```

### Installing Libraries

```bash
pip install pandas
pip install sqlite3
```

---

## Working with CSV Files

CSV (Comma-Separated Values) files are simple text files used to store tabular data.

### Reading CSV Files

#### Using the built-in `csv` module:

```python
import csv

# Reading a CSV file
with open('data.csv', 'r') as file:
    csv_reader = csv.reader(file)
    
    # Skip header
    next(csv_reader)
    
    for row in csv_reader:
        print(row)
```

#### Using `pandas` (recommended):

```python
import pandas as pd

# Read CSV file
df = pd.read_csv('data.csv')

# Display first 5 rows
print(df.head())

# Display basic information
print(df.info())

# Display statistics
print(df.describe())
```

### Writing CSV Files

#### Using `csv` module:

```python
import csv

data = [
    ['Name', 'Age', 'City'],
    ['Alice', 25, 'New York'],
    ['Bob', 30, 'London'],
    ['Charlie', 35, 'Paris']
]

with open('output.csv', 'w', newline='') as file:
    csv_writer = csv.writer(file)
    csv_writer.writerows(data)
```

#### Using `pandas`:

```python
import pandas as pd

data = {
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Age': [25, 30, 35],
    'City': ['New York', 'London', 'Paris']
}

df = pd.DataFrame(data)
df.to_csv('output.csv', index=False)
```

### Manipulating CSV Data

```python
import pandas as pd

# Read CSV
df = pd.read_csv('data.csv')

# Filter rows
filtered = df[df['Age'] > 25]

# Select specific columns
names = df['Name']

# Add a new column
df['Country'] = 'USA'

# Sort data
sorted_df = df.sort_values('Age', ascending=False)

# Group and aggregate
grouped = df.groupby('City')['Age'].mean()

# Save changes
df.to_csv('modified_data.csv', index=False)
```

---

## SQL Fundamentals

SQL (Structured Query Language) is used to manage and query relational databases.

### Basic SQL Commands

#### Creating a Table

```sql
CREATE TABLE employees (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    age INTEGER,
    department TEXT,
    salary REAL
);
```

#### Inserting Data

```sql
INSERT INTO employees (name, age, department, salary)
VALUES ('Alice', 25, 'IT', 60000);

INSERT INTO employees (name, age, department, salary)
VALUES 
    ('Bob', 30, 'Sales', 55000),
    ('Charlie', 35, 'IT', 70000);
```

#### Querying Data

```sql
-- Select all columns
SELECT * FROM employees;

-- Select specific columns
SELECT name, salary FROM employees;

-- Filter with WHERE
SELECT * FROM employees WHERE age > 25;

-- Sort results
SELECT * FROM employees ORDER BY salary DESC;

-- Aggregate functions
SELECT department, AVG(salary) as avg_salary
FROM employees
GROUP BY department;

-- Count records
SELECT COUNT(*) FROM employees;
```

#### Updating Data

```sql
UPDATE employees
SET salary = 65000
WHERE name = 'Alice';
```

#### Deleting Data

```sql
DELETE FROM employees
WHERE age < 25;
```

#### Joining Tables

```sql
-- Assuming we have two tables
SELECT e.name, d.department_name
FROM employees e
INNER JOIN departments d ON e.department = d.id;
```

---

## Connecting Python with SQL

### Using SQLite (Built-in)

SQLite is a lightweight database that comes with Python.

```python
import sqlite3

# Connect to database (creates file if doesn't exist)
conn = sqlite3.connect('mydatabase.db')
cursor = conn.cursor()

# Create table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER,
        department TEXT,
        salary REAL
    )
''')

# Insert data
cursor.execute('''
    INSERT INTO employees (name, age, department, salary)
    VALUES (?, ?, ?, ?)
''', ('Alice', 25, 'IT', 60000))

# Insert multiple records
employees = [
    ('Bob', 30, 'Sales', 55000),
    ('Charlie', 35, 'IT', 70000),
    ('Diana', 28, 'HR', 58000)
]
cursor.executemany('''
    INSERT INTO employees (name, age, department, salary)
    VALUES (?, ?, ?, ?)
''', employees)

# Commit changes
conn.commit()

# Query data
cursor.execute('SELECT * FROM employees')
rows = cursor.fetchall()

for row in rows:
    print(row)

# Query with parameters
cursor.execute('SELECT * FROM employees WHERE department = ?', ('IT',))
it_employees = cursor.fetchall()

# Close connection
conn.close()
```

### Using Pandas with SQL

```python
import pandas as pd
import sqlite3

# Connect to database
conn = sqlite3.connect('mydatabase.db')

# Read SQL query into DataFrame
df = pd.read_sql_query('SELECT * FROM employees', conn)
print(df)

# Write DataFrame to SQL table
new_data = pd.DataFrame({
    'name': ['Eve', 'Frank'],
    'age': [32, 29],
    'department': ['Marketing', 'IT'],
    'salary': [62000, 67000]
})

new_data.to_sql('employees', conn, if_exists='append', index=False)

conn.close()
```

---

## Practical Examples

### Example 1: CSV to SQL Database

```python
import pandas as pd
import sqlite3

# Read CSV file
df = pd.read_csv('employees.csv')

# Connect to SQLite database
conn = sqlite3.connect('company.db')

# Write DataFrame to SQL table
df.to_sql('employees', conn, if_exists='replace', index=False)

# Verify data was inserted
result = pd.read_sql_query('SELECT * FROM employees', conn)
print(result)

conn.close()
```

### Example 2: SQL Database to CSV

```python
import pandas as pd
import sqlite3

# Connect to database
conn = sqlite3.connect('company.db')

# Query data
query = '''
    SELECT department, AVG(salary) as avg_salary, COUNT(*) as count
    FROM employees
    GROUP BY department
'''

df = pd.read_sql_query(query, conn)

# Export to CSV
df.to_csv('department_summary.csv', index=False)

conn.close()
```

### Example 3: Data Processing Pipeline

```python
import pandas as pd
import sqlite3

# Step 1: Read CSV
sales_data = pd.read_csv('sales.csv')

# Step 2: Clean data
sales_data = sales_data.dropna()  # Remove rows with missing values
sales_data['date'] = pd.to_datetime(sales_data['date'])  # Convert to datetime

# Step 3: Add calculated columns
sales_data['total'] = sales_data['quantity'] * sales_data['price']

# Step 4: Store in database
conn = sqlite3.connect('sales.db')
sales_data.to_sql('sales', conn, if_exists='replace', index=False)

# Step 5: Perform analysis
query = '''
    SELECT 
        product,
        SUM(total) as total_revenue,
        SUM(quantity) as total_quantity
    FROM sales
    GROUP BY product
    ORDER BY total_revenue DESC
'''

analysis = pd.read_sql_query(query, conn)

# Step 6: Export results
analysis.to_csv('sales_analysis.csv', index=False)

conn.close()

print("Pipeline completed!")
print(analysis)
```

### Example 4: Interactive Database Application

```python
import sqlite3

def create_database():
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            status TEXT DEFAULT 'pending',
            created_date TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_task(task):
    from datetime import datetime
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO tasks (task, created_date)
        VALUES (?, ?)
    ''', (task, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    conn.commit()
    conn.close()
    print(f"Task added: {task}")

def view_tasks():
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks ORDER BY id')
    tasks = cursor.fetchall()
    conn.close()
    
    print("\n--- Task List ---")
    for task in tasks:
        print(f"ID: {task[0]} | Task: {task[1]} | Status: {task[2]} | Date: {task[3]}")

def complete_task(task_id):
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE tasks
        SET status = 'completed'
        WHERE id = ?
    ''', (task_id,))
    conn.commit()
    conn.close()
    print(f"Task {task_id} marked as completed")

# Usage
create_database()
add_task("Learn Python")
add_task("Master SQL")
add_task("Work with CSV files")
view_tasks()
complete_task(1)
view_tasks()
```

---

## Best Practices

### For CSV Files
- Always close files or use `with` statement
- Handle encoding issues: `pd.read_csv('file.csv', encoding='utf-8')`
- Use `index=False` when saving to avoid extra index column
- Validate data before processing

### For SQL
- Use parameterized queries to prevent SQL injection
- Always commit changes: `conn.commit()`
- Close connections when done: `conn.close()`
- Create indexes for frequently queried columns
- Use transactions for multiple related operations

### For Python
- Follow PEP 8 style guide
- Use meaningful variable names
- Add comments for complex logic
- Handle exceptions with try-except blocks
- Use virtual environments for projects

---

## Common Errors and Solutions

### CSV Errors

**FileNotFoundError**
```python
# Solution: Check file path
import os
if os.path.exists('data.csv'):
    df = pd.read_csv('data.csv')
else:
    print("File not found!")
```

**Encoding Issues**
```python
# Solution: Specify encoding
df = pd.read_csv('data.csv', encoding='utf-8')
# or
df = pd.read_csv('data.csv', encoding='latin-1')
```

### SQL Errors

**Table already exists**
```python
# Solution: Use IF NOT EXISTS
cursor.execute('CREATE TABLE IF NOT EXISTS employees (...)')
```

**SQL Injection Prevention**
```python
# BAD - Vulnerable to SQL injection
name = input("Enter name: ")
cursor.execute(f"SELECT * FROM users WHERE name = '{name}'")

# GOOD - Use parameterized queries
cursor.execute("SELECT * FROM users WHERE name = ?", (name,))
```

---

## Next Steps

1. **Practice Projects:**
   - Create a personal expense tracker
   - Build a student grade management system
   - Develop a simple inventory system

2. **Advanced Topics:**
   - Learn about database normalization
   - Explore pandas advanced features (merge, pivot, etc.)
   - Study database indexing and optimization
   - Learn about ORMs (SQLAlchemy)

3. **Resources:**
   - [Python Documentation](https://docs.python.org/)
   - [Pandas Documentation](https://pandas.pydata.org/docs/)
   - [SQLite Tutorial](https://www.sqlitetutorial.net/)
   - [W3Schools SQL](https://www.w3schools.com/sql/)

---

## Quick Reference

### Python CSV Operations
```python
import pandas as pd

# Read
df = pd.read_csv('file.csv')

# Write
df.to_csv('file.csv', index=False)

# Filter
filtered = df[df['column'] > 10]

# Sort
sorted_df = df.sort_values('column')
```

### SQL Commands
```sql
-- Create
CREATE TABLE table_name (column type);

-- Insert
INSERT INTO table_name (col1, col2) VALUES (val1, val2);

-- Select
SELECT * FROM table_name WHERE condition;

-- Update
UPDATE table_name SET col1 = val1 WHERE condition;

-- Delete
DELETE FROM table_name WHERE condition;
```

### Python + SQL
```python
import sqlite3

conn = sqlite3.connect('db.db')
cursor = conn.cursor()
cursor.execute('SQL QUERY HERE')
conn.commit()
conn.close()
```

---

**Happy Coding! 🚀**
