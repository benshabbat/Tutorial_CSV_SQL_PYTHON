# Python & CSV Tutorial for Beginners

A simple guide to working with CSV files in Python.

---

## 🎯 What You'll Learn

- Read CSV files
- Write CSV files
- Process and analyze data
- Use both `csv` module and `pandas`

---

## What is CSV?

**CSV** = Comma-Separated Values

A simple text file format for storing tabular data.

**Example: `employees.csv`**
```
name,department,salary
Alice,IT,70000
Bob,Sales,60000
Charlie,IT,80000
```

---

## Method 1: Using CSV Module (Built-in)

### Read CSV File

```python
import csv

# Read CSV file
with open('employees.csv', 'r') as file:
    csv_reader = csv.reader(file)
    
    # Skip header row
    header = next(csv_reader)
    print(f"Columns: {header}")
    
    # Read each row
    for row in csv_reader:
        print(row)
```

**Output:**
```
Columns: ['name', 'department', 'salary']
['Alice', 'IT', '70000']
['Bob', 'Sales', '60000']
['Charlie', 'IT', '80000']
```

### Read with DictReader (Better!)

```python
import csv

with open('employees.csv', 'r') as file:
    csv_reader = csv.DictReader(file)
    
    for row in csv_reader:
        print(f"{row['name']} works in {row['department']}")
        print(f"Salary: ${row['salary']}")
        print()
```

**Output:**
```
Alice works in IT
Salary: $70000

Bob works in Sales
Salary: $60000
```

---

### Write CSV File

```python
import csv

# Data to write
employees = [
    ['name', 'department', 'salary'],
    ['Alice', 'IT', 70000],
    ['Bob', 'Sales', 60000],
    ['Charlie', 'IT', 80000]
]

# Write to CSV
with open('employees.csv', 'w', newline='') as file:
    csv_writer = csv.writer(file)
    csv_writer.writerows(employees)

print("✓ File created!")
```

### Write with DictWriter

```python
import csv

employees = [
    {'name': 'Alice', 'department': 'IT', 'salary': 70000},
    {'name': 'Bob', 'department': 'Sales', 'salary': 60000},
    {'name': 'Charlie', 'department': 'IT', 'salary': 80000}
]

with open('employees.csv', 'w', newline='') as file:
    fieldnames = ['name', 'department', 'salary']
    csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
    
    # Write header
    csv_writer.writeheader()
    
    # Write rows
    csv_writer.writerows(employees)

print("✓ File created!")
```

---

## Method 2: Using Pandas (Recommended)

### Install Pandas

```bash
pip install pandas
```

### Read CSV

```python
import pandas as pd

# Read CSV file
df = pd.read_csv('employees.csv')

# Display first 5 rows
print(df.head())

# Display info
print(df.info())

# Display statistics
print(df.describe())
```

**Output:**
```
      name department  salary
0    Alice         IT   70000
1      Bob      Sales   60000
2  Charlie         IT   80000
```

### Write CSV

```python
import pandas as pd

# Create data
data = {
    'name': ['Alice', 'Bob', 'Charlie'],
    'department': ['IT', 'Sales', 'IT'],
    'salary': [70000, 60000, 80000]
}

# Create DataFrame
df = pd.DataFrame(data)

# Save to CSV
df.to_csv('employees.csv', index=False)

print("✓ File saved!")
```

---

## Common Operations

### 1. Filter Data

```python
import pandas as pd

df = pd.read_csv('employees.csv')

# Filter IT employees
it_employees = df[df['department'] == 'IT']
print(it_employees)

# Filter high earners
high_earners = df[df['salary'] > 65000]
print(high_earners)
```

### 2. Add Column

```python
import pandas as pd

df = pd.read_csv('employees.csv')

# Add annual salary column
df['annual_salary'] = df['salary'] * 12

# Add bonus column (10% of salary)
df['bonus'] = df['salary'] * 0.10

print(df)
```

### 3. Sort Data

```python
import pandas as pd

df = pd.read_csv('employees.csv')

# Sort by salary (descending)
df_sorted = df.sort_values('salary', ascending=False)
print(df_sorted)

# Sort by multiple columns
df_sorted = df.sort_values(['department', 'salary'])
print(df_sorted)
```

### 4. Group Data

```python
import pandas as pd

df = pd.read_csv('employees.csv')

# Average salary by department
avg_by_dept = df.groupby('department')['salary'].mean()
print(avg_by_dept)

# Count employees by department
count_by_dept = df.groupby('department').size()
print(count_by_dept)
```

### 5. Select Columns

```python
import pandas as pd

df = pd.read_csv('employees.csv')

# Select single column
names = df['name']
print(names)

# Select multiple columns
subset = df[['name', 'salary']]
print(subset)
```

---

## Complete Example: Employee Manager

```python
import csv

class EmployeeManager:
    """Manage employee data in CSV"""
    
    def __init__(self, filename='employees.csv'):
        self.filename = filename
    
    def add_employee(self, name, department, salary):
        """Add new employee to CSV"""
        with open(self.filename, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([name, department, salary])
        print(f"✓ Added {name}")
    
    def read_all(self):
        """Read all employees"""
        try:
            with open(self.filename, 'r') as file:
                reader = csv.DictReader(file)
                employees = list(reader)
                return employees
        except FileNotFoundError:
            return []
    
    def display_all(self):
        """Display all employees"""
        employees = self.read_all()
        
        if not employees:
            print("No employees found")
            return
        
        print(f"\n{'Name':<15} {'Department':<12} {'Salary':<10}")
        print("-" * 40)
        
        for emp in employees:
            print(f"{emp['name']:<15} {emp['department']:<12} ${float(emp['salary']):>9,.0f}")
    
    def find_by_department(self, department):
        """Find employees by department"""
        employees = self.read_all()
        found = [e for e in employees if e['department'] == department]
        return found
    
    def calculate_total_salary(self):
        """Calculate total salary cost"""
        employees = self.read_all()
        total = sum(float(e['salary']) for e in employees)
        return total
    
    def create_file(self):
        """Create CSV file with header"""
        with open(self.filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['name', 'department', 'salary'])
        print(f"✓ Created {self.filename}")

# Usage
if __name__ == "__main__":
    manager = EmployeeManager()
    
    # Create file with header
    manager.create_file()
    
    # Add employees
    manager.add_employee("Alice", "IT", 70000)
    manager.add_employee("Bob", "Sales", 60000)
    manager.add_employee("Charlie", "IT", 80000)
    
    # Display all
    manager.display_all()
    
    # Find IT employees
    print("\nIT Department:")
    it_emps = manager.find_by_department("IT")
    for emp in it_emps:
        print(f"  {emp['name']}: ${float(emp['salary']):,.0f}")
    
    # Total salary
    total = manager.calculate_total_salary()
    print(f"\nTotal Salary Cost: ${total:,.0f}")
```

---

## Pandas Analysis Example

```python
import pandas as pd

# Read data
df = pd.read_csv('employees.csv')

print("=== Employee Analysis ===\n")

# Basic info
print(f"Total Employees: {len(df)}")
print(f"Departments: {df['department'].nunique()}")

# Salary statistics
print(f"\nSalary Statistics:")
print(f"Average: ${df['salary'].mean():,.0f}")
print(f"Median: ${df['salary'].median():,.0f}")
print(f"Min: ${df['salary'].min():,.0f}")
print(f"Max: ${df['salary'].max():,.0f}")

# By department
print("\nBy Department:")
dept_stats = df.groupby('department').agg({
    'name': 'count',
    'salary': ['mean', 'sum']
})
print(dept_stats)

# Top earners
print("\nTop 3 Earners:")
top3 = df.nlargest(3, 'salary')[['name', 'salary']]
print(top3.to_string(index=False))

# Export analysis
summary = df.groupby('department').agg({
    'salary': ['count', 'mean', 'min', 'max']
})
summary.to_csv('salary_analysis.csv')
print("\n✓ Analysis saved to salary_analysis.csv")
```

---

## Handling Common Issues

### 1. File Not Found

```python
import csv
import os

filename = 'employees.csv'

if os.path.exists(filename):
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            print(row)
else:
    print(f"File {filename} not found!")
```

### 2. Encoding Issues

```python
import pandas as pd

# Try different encodings
try:
    df = pd.read_csv('data.csv', encoding='utf-8')
except:
    df = pd.read_csv('data.csv', encoding='latin-1')
```

### 3. Different Delimiters

```python
import pandas as pd

# Semicolon separated
df = pd.read_csv('data.csv', sep=';')

# Tab separated
df = pd.read_csv('data.tsv', sep='\t')

# Auto-detect
df = pd.read_csv('data.csv', sep=None, engine='python')
```

### 4. Skip Rows

```python
import pandas as pd

# Skip first 2 rows
df = pd.read_csv('data.csv', skiprows=2)

# Skip specific rows
df = pd.read_csv('data.csv', skiprows=[0, 2, 5])
```

### 5. Handle Missing Data

```python
import pandas as pd

df = pd.read_csv('employees.csv')

# Check for missing values
print(df.isnull().sum())

# Fill missing values
df['salary'].fillna(0, inplace=True)

# Drop rows with missing values
df.dropna(inplace=True)
```

---

## Quick Reference

### CSV Module

```python
import csv

# Read
with open('file.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row['column_name'])

# Write
with open('file.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['col1', 'col2'])
    writer.writeheader()
    writer.writerow({'col1': 'value1', 'col2': 'value2'})
```

### Pandas

```python
import pandas as pd

# Read
df = pd.read_csv('file.csv')

# Write
df.to_csv('file.csv', index=False)

# Filter
filtered = df[df['column'] > 100]

# Sort
sorted_df = df.sort_values('column')

# Group
grouped = df.groupby('column')['value'].mean()

# Select
subset = df[['col1', 'col2']]
```

---

## Practice Exercises

### Easy
1. Create a CSV file with 5 products (name, price, quantity)
2. Read the file and print all products
3. Calculate total value (price × quantity)

### Medium
1. Read CSV and filter products with price > 100
2. Add a new column for discounted price (10% off)
3. Export filtered data to new CSV

### Challenge
1. Read sales data CSV
2. Calculate total sales per month
3. Find best-selling product
4. Create a summary report CSV

---

## Sample Data Generator

```python
import csv
import random

# Generate sample employee data
departments = ['IT', 'Sales', 'HR', 'Marketing', 'Finance']
names = ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve', 'Frank', 'Grace', 'Henry']

with open('employees.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['name', 'department', 'salary'])
    
    for name in names:
        dept = random.choice(departments)
        salary = random.randint(50000, 100000)
        writer.writerow([name, dept, salary])

print("✓ Sample data generated!")
```

---

## Tips

💡 **Use `pandas` for analysis** - Much more powerful than `csv` module

💡 **Always use `newline=''`** - When writing CSV files

💡 **Use `DictReader/DictWriter`** - Easier to work with than plain reader/writer

💡 **Set `index=False`** - When saving with pandas to avoid extra column

💡 **Check file exists first** - Use `os.path.exists()` to avoid errors

---

## CSV vs Excel

| Feature | CSV | Excel |
|---------|-----|-------|
| File size | Small | Large |
| Speed | Fast | Slower |
| Formulas | No | Yes |
| Multiple sheets | No | Yes |
| Formatting | No | Yes |
| Compatibility | Universal | Needs Excel/library |

**Use CSV when:** You need simple, fast, universal data storage  
**Use Excel when:** You need formatting, formulas, or multiple sheets

---

## Next Steps

1. 📊 Learn data visualization with **matplotlib**
2. 🗄️ Combine CSV with **SQL databases**
3. 🌐 Build a web app that uploads/downloads CSV
4. 🤖 Automate CSV reports with **schedule**
5. 📈 Learn advanced pandas (merge, pivot, etc.)

---

**You now know how to work with CSV files in Python! 🎉**

Practice by building:
- Budget tracker
- Contact manager
- Sales report generator
- Inventory system
