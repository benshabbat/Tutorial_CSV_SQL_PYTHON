# Pandas Tutorial for Beginners

A simple, practical guide to data analysis with Pandas.

---

## 🎯 What is Pandas?

Pandas is a Python library for working with data in tables (like Excel).

**Install:**
```bash
pip install pandas
```

---

## Step 1: Create a DataFrame

### From Dictionary

```python
import pandas as pd

# Create data
data = {
    'name': ['Alice', 'Bob', 'Charlie', 'Diana'],
    'age': [25, 30, 35, 28],
    'salary': [70000, 60000, 80000, 75000]
}

# Create DataFrame
df = pd.DataFrame(data)
print(df)
```

**Output:**
```
      name  age  salary
0    Alice   25   70000
1      Bob   30   60000
2  Charlie   35   80000
3    Diana   28   75000
```

### From List

```python
import pandas as pd

# Create from list of lists
data = [
    ['Alice', 25, 70000],
    ['Bob', 30, 60000],
    ['Charlie', 35, 80000]
]

df = pd.DataFrame(data, columns=['name', 'age', 'salary'])
print(df)
```

---

## Step 2: Read & Write Files

### Read CSV

```python
import pandas as pd

# Read CSV file
df = pd.read_csv('employees.csv')
print(df)
```

### Write CSV

```python
import pandas as pd

df = pd.DataFrame({
    'name': ['Alice', 'Bob'],
    'salary': [70000, 60000]
})

# Save to CSV
df.to_csv('output.csv', index=False)  # index=False removes row numbers
print("✓ Saved!")
```

### Read Excel

```python
# First install: pip install openpyxl
df = pd.read_excel('data.xlsx')
```

### Write Excel

```python
df.to_excel('output.xlsx', index=False)
```

---

## Step 3: View Data

```python
import pandas as pd

df = pd.read_csv('employees.csv')

# First 5 rows
print(df.head())

# Last 5 rows
print(df.tail())

# First 10 rows
print(df.head(10))

# Basic info
print(df.info())

# Column names
print(df.columns)

# Shape (rows, columns)
print(df.shape)  # (100, 3) = 100 rows, 3 columns

# Data types
print(df.dtypes)
```

---

## Step 4: Select Data

### Select Columns

```python
import pandas as pd

df = pd.read_csv('employees.csv')

# Select one column
names = df['name']
print(names)

# Select multiple columns
subset = df[['name', 'salary']]
print(subset)
```

### Select Rows

```python
# First row
print(df.iloc[0])

# First 3 rows
print(df.iloc[0:3])

# Specific rows
print(df.iloc[[0, 2, 4]])

# Select by condition
high_earners = df[df['salary'] > 65000]
print(high_earners)
```

### Select Specific Cell

```python
# Row 0, Column 'name'
print(df.loc[0, 'name'])

# Row 2, Column 'salary'
print(df.iloc[2, 2])
```

---

## Step 5: Filter Data

```python
import pandas as pd

df = pd.read_csv('employees.csv')

# Filter by condition
it_dept = df[df['department'] == 'IT']
print(it_dept)

# Multiple conditions (AND)
senior_it = df[(df['department'] == 'IT') & (df['salary'] > 70000)]
print(senior_it)

# Multiple conditions (OR)
it_or_sales = df[(df['department'] == 'IT') | (df['department'] == 'Sales')]
print(it_or_sales)

# Filter by list
depts = ['IT', 'HR']
result = df[df['department'].isin(depts)]
print(result)

# String contains
alice_employees = df[df['name'].str.contains('Alice')]
print(alice_employees)
```

---

## Step 6: Sort Data

```python
import pandas as pd

df = pd.read_csv('employees.csv')

# Sort by one column (ascending)
sorted_df = df.sort_values('salary')
print(sorted_df)

# Sort descending
sorted_df = df.sort_values('salary', ascending=False)
print(sorted_df)

# Sort by multiple columns
sorted_df = df.sort_values(['department', 'salary'], ascending=[True, False])
print(sorted_df)
```

---

## Step 7: Add/Modify Columns

```python
import pandas as pd

df = pd.read_csv('employees.csv')

# Add new column
df['annual_salary'] = df['salary'] * 12
print(df)

# Add column with calculation
df['bonus'] = df['salary'] * 0.10
print(df)

# Add column based on condition
df['senior'] = df['salary'] > 70000
print(df)

# Add column with if-else
df['level'] = df['salary'].apply(lambda x: 'Senior' if x > 70000 else 'Junior')
print(df)

# Modify existing column
df['salary'] = df['salary'] * 1.10  # 10% raise
print(df)

# Rename columns
df = df.rename(columns={'name': 'employee_name', 'salary': 'monthly_salary'})
print(df)
```

---

## Step 8: Delete Data

```python
import pandas as pd

df = pd.read_csv('employees.csv')

# Delete column
df = df.drop('bonus', axis=1)
# or
df = df.drop(columns=['bonus'])

# Delete multiple columns
df = df.drop(['bonus', 'level'], axis=1)

# Delete rows by index
df = df.drop([0, 2, 4])

# Delete rows by condition
df = df[df['salary'] >= 50000]  # Keep only salary >= 50000
```

---

## Step 9: Statistics

```python
import pandas as pd

df = pd.read_csv('employees.csv')

# Summary statistics
print(df.describe())

# Mean
print(df['salary'].mean())

# Median
print(df['salary'].median())

# Min/Max
print(df['salary'].min())
print(df['salary'].max())

# Standard deviation
print(df['salary'].std())

# Count
print(df['department'].value_counts())

# Sum
print(df['salary'].sum())

# Multiple stats
stats = df['salary'].agg(['mean', 'median', 'min', 'max'])
print(stats)
```

---

## Step 10: Group By

```python
import pandas as pd

df = pd.read_csv('employees.csv')

# Group by department, calculate mean
dept_avg = df.groupby('department')['salary'].mean()
print(dept_avg)

# Count employees per department
dept_count = df.groupby('department').size()
print(dept_count)

# Multiple aggregations
dept_stats = df.groupby('department')['salary'].agg(['count', 'mean', 'min', 'max'])
print(dept_stats)

# Group by multiple columns
result = df.groupby(['department', 'level'])['salary'].mean()
print(result)
```

---

## Step 11: Handle Missing Data

```python
import pandas as pd

df = pd.read_csv('employees.csv')

# Check for missing values
print(df.isnull().sum())

# Check if any missing
print(df.isnull().any())

# Drop rows with missing values
df_clean = df.dropna()

# Fill missing values with 0
df['salary'] = df['salary'].fillna(0)

# Fill with mean
df['salary'] = df['salary'].fillna(df['salary'].mean())

# Fill with specific value
df['department'] = df['department'].fillna('Unknown')
```

---

## Step 12: Merge DataFrames

```python
import pandas as pd

# DataFrame 1
employees = pd.DataFrame({
    'emp_id': [1, 2, 3],
    'name': ['Alice', 'Bob', 'Charlie']
})

# DataFrame 2
salaries = pd.DataFrame({
    'emp_id': [1, 2, 3],
    'salary': [70000, 60000, 80000]
})

# Merge (like SQL JOIN)
result = pd.merge(employees, salaries, on='emp_id')
print(result)
```

**Output:**
```
   emp_id     name  salary
0       1    Alice   70000
1       2      Bob   60000
2       3  Charlie   80000
```

---

## Step 13: Complete Example

```python
import pandas as pd

# Create sample data
data = {
    'name': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve', 'Frank'],
    'department': ['IT', 'Sales', 'IT', 'HR', 'Sales', 'IT'],
    'salary': [70000, 60000, 80000, 55000, 65000, 90000],
    'age': [25, 30, 35, 28, 32, 40]
}

df = pd.DataFrame(data)

print("=== Original Data ===")
print(df)

# 1. Add annual salary column
df['annual_salary'] = df['salary'] * 12

# 2. Filter IT department
it_dept = df[df['department'] == 'IT']
print("\n=== IT Department ===")
print(it_dept)

# 3. Calculate average salary by department
print("\n=== Average Salary by Department ===")
avg_salary = df.groupby('department')['salary'].mean()
print(avg_salary)

# 4. Find top 3 earners
print("\n=== Top 3 Earners ===")
top3 = df.nlargest(3, 'salary')[['name', 'salary']]
print(top3)

# 5. Add salary grade
df['grade'] = pd.cut(df['salary'], 
                      bins=[0, 60000, 80000, 100000],
                      labels=['Junior', 'Mid', 'Senior'])
print("\n=== With Grades ===")
print(df[['name', 'salary', 'grade']])

# 6. Export to CSV
df.to_csv('employee_analysis.csv', index=False)
print("\n✓ Exported to employee_analysis.csv")
```

---

## Common Operations Cheat Sheet

### Read/Write
```python
df = pd.read_csv('file.csv')
df.to_csv('output.csv', index=False)
```

### View Data
```python
df.head()          # First 5 rows
df.tail()          # Last 5 rows
df.info()          # Data info
df.describe()      # Statistics
```

### Select
```python
df['column']                    # One column
df[['col1', 'col2']]           # Multiple columns
df.iloc[0]                      # First row
df[df['salary'] > 50000]       # Filter
```

### Modify
```python
df['new_col'] = value          # Add column
df = df.drop('col', axis=1)    # Delete column
df = df.sort_values('col')     # Sort
```

### Analyze
```python
df['col'].mean()               # Average
df['col'].sum()                # Total
df.groupby('col').mean()       # Group by
df['col'].value_counts()       # Count values
```

---

## Practice Exercises

### Easy
1. Create DataFrame with 5 products (name, price, quantity)
2. Calculate total value (price × quantity)
3. Find products with price > 100

### Medium
1. Read CSV file
2. Filter products by category
3. Calculate average price per category
4. Export filtered data

### Challenge
1. Load sales data CSV
2. Add profit column (price - cost)
3. Find top 5 products by profit
4. Create summary by category
5. Export analysis to Excel

---

## Real-World Example: Sales Analysis

```python
import pandas as pd

# Sample sales data
sales = pd.DataFrame({
    'date': ['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-01', '2024-01-02'],
    'product': ['Laptop', 'Mouse', 'Laptop', 'Keyboard', 'Mouse'],
    'quantity': [2, 5, 1, 3, 10],
    'price': [1000, 25, 1000, 75, 25]
})

# Convert date to datetime
sales['date'] = pd.to_datetime(sales['date'])

# Add total column
sales['total'] = sales['quantity'] * sales['price']

print("=== Sales Data ===")
print(sales)

# Total sales
print(f"\nTotal Revenue: ${sales['total'].sum():,}")

# Sales by product
print("\n=== Sales by Product ===")
by_product = sales.groupby('product').agg({
    'quantity': 'sum',
    'total': 'sum'
}).sort_values('total', ascending=False)
print(by_product)

# Sales by date
print("\n=== Sales by Date ===")
by_date = sales.groupby('date')['total'].sum()
print(by_date)

# Best selling product
best = sales.groupby('product')['quantity'].sum().idxmax()
print(f"\nBest Selling Product: {best}")

# Export report
sales.to_csv('sales_report.csv', index=False)
print("\n✓ Report saved!")
```

---

## Tips

💡 **Always use `index=False`** when saving CSV to avoid extra column

💡 **Use `head()` first** to preview data before processing

💡 **Chain operations** for cleaner code:
```python
result = df.sort_values('salary').head(5)
```

💡 **Copy DataFrame** before modifying:
```python
df_copy = df.copy()
```

💡 **Use `describe()`** to quickly understand your data

---

## Common Errors

### KeyError: 'column'
```python
# Check column names first
print(df.columns)
```

### AttributeError
```python
# Make sure you imported pandas
import pandas as pd
```

### File Not Found
```python
# Check file path
import os
print(os.getcwd())  # Current directory
```

---

## What's Next?

1. 📊 Learn **data visualization** with matplotlib/seaborn
2. 🧹 Practice **data cleaning** techniques
3. 🔗 Combine with **SQL** databases
4. 📈 Learn **time series** analysis
5. 🤖 Use pandas for **machine learning** preprocessing

---

**You now know Pandas! 🎉**

Practice with real datasets:
- Sales data
- Weather data
- Sports statistics
- Financial data
