# מדריך למתחילים: CSV, MySQL ו-Python

## תוכן עניינים
1. [מבוא](#מבוא)
2. [התקנה והכנה](#התקנה-והכנה)
3. [חלק 1: עבודה עם קבצי CSV](#חלק-1-עבודה-עם-קבצי-csv)
4. [חלק 2: עבודה עם MySQL](#חלק-2-עבודה-עם-mysql)
5. [חלק 3: שילוב CSV ו-MySQL](#חלק-3-שילוב-csv-ו-mysql)
6. [תרגילים מעשיים](#תרגילים-מעשיים)

---

## מבוא

### מה נלמד?
במדריך זה נלמד כיצד:
- לקרוא ולכתוב קבצי CSV עם Python
- להתחבר למסד נתונים MySQL
- להעביר מידע בין קבצי CSV למסד נתונים
- לבצע פעולות בסיסיות על המידע

### למי המדריך מיועד?
- מתחילים בתכנות Python
- מי שרוצה ללמוד עבודה עם מסדי נתונים
- מי שצריך לעבד קבצי CSV

---

## התקנה והכנה

### שלב 1: התקנת Python
ודא ש-Python מותקן במחשב:
```bash
python --version
```

### שלב 2: התקנת הספריות הנדרשות
```bash
pip install mysql-connector-python pandas
```

### שלב 3: התקנת MySQL
1. הורד והתקן MySQL Server מהאתר הרשמי
2. זכור את סיסמת ה-root שהגדרת
3. וודא שהשירות פועל

---

## חלק 1: עבודה עם קבצי CSV

### מה זה CSV?
CSV (Comma Separated Values) הוא פורמט קובץ פשוט לאחסון טבלאות.

**דוגמה לקובץ CSV:**
```
name,age,city
Alice,25,Tel Aviv
Bob,30,Jerusalem
Charlie,35,Haifa
```

### 1.1: קריאת קובץ CSV

#### שיטה 1: שימוש במודול `csv` המובנה

```python
import csv

# קריאת קובץ CSV
with open('employees.csv', 'r', encoding='utf-8') as file:
    csv_reader = csv.reader(file)
    
    # קריאת כותרת
    header = next(csv_reader)
    print(f"כותרות: {header}")
    
    # קריאת כל השורות
    for row in csv_reader:
        print(row)
```

#### שיטה 2: שימוש ב-`DictReader`

```python
import csv

with open('employees.csv', 'r', encoding='utf-8') as file:
    csv_reader = csv.DictReader(file)
    
    for row in csv_reader:
        print(f"שם: {row['name']}, גיל: {row['age']}, עיר: {row['city']}")
```

### 1.2: כתיבה לקובץ CSV

```python
import csv

# נתונים לכתיבה
employees = [
    ['name', 'age', 'city', 'salary'],
    ['Alice', 25, 'Tel Aviv', 10000],
    ['Bob', 30, 'Jerusalem', 12000],
    ['Charlie', 35, 'Haifa', 15000]
]

# כתיבה לקובץ
with open('employees.csv', 'w', newline='', encoding='utf-8') as file:
    csv_writer = csv.writer(file)
    csv_writer.writerows(employees)

print("הקובץ נוצר בהצלחה!")
```

### 1.3: שימוש ב-Pandas (מומלץ למתקדמים)

```python
import pandas as pd

# קריאת קובץ CSV
df = pd.read_csv('employees.csv')
print(df)

# הצגת מידע על הנתונים
print(df.info())
print(df.describe())

# סינון נתונים
young_employees = df[df['age'] < 30]
print(young_employees)

# כתיבה לקובץ CSV
df.to_csv('employees_updated.csv', index=False)
```

---

## חלק 2: עבודה עם MySQL

### 2.1: התחברות למסד נתונים

```python
import mysql.connector

# יצירת חיבור
connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='your_password',  # שנה לסיסמה שלך
    database='company_db'
)

if connection.is_connected():
    print("התחברות הצליחה!")
    
# סגירת חיבור
connection.close()
```

### 2.2: יצירת מסד נתונים וטבלה

```python
import mysql.connector

# התחברות ללא מסד נתונים ספציפי
connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='your_password'
)

cursor = connection.cursor()

# יצירת מסד נתונים
cursor.execute("CREATE DATABASE IF NOT EXISTS company_db")
print("מסד נתונים נוצר!")

# שימוש במסד נתונים
cursor.execute("USE company_db")

# יצירת טבלה
create_table_query = """
CREATE TABLE IF NOT EXISTS employees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    age INT,
    city VARCHAR(100),
    salary DECIMAL(10, 2)
)
"""

cursor.execute(create_table_query)
print("טבלה נוצרה!")

connection.commit()
cursor.close()
connection.close()
```

### 2.3: הוספת נתונים (INSERT)

```python
import mysql.connector

connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='your_password',
    database='company_db'
)

cursor = connection.cursor()

# הוספת שורה אחת
insert_query = "INSERT INTO employees (name, age, city, salary) VALUES (%s, %s, %s, %s)"
employee_data = ("Alice", 25, "Tel Aviv", 10000)

cursor.execute(insert_query, employee_data)

# הוספת מספר שורות
employees_data = [
    ("Bob", 30, "Jerusalem", 12000),
    ("Charlie", 35, "Haifa", 15000),
    ("Diana", 28, "Beer Sheva", 11000)
]

cursor.executemany(insert_query, employees_data)

connection.commit()
print(f"{cursor.rowcount} שורות נוספו!")

cursor.close()
connection.close()
```

### 2.4: קריאת נתונים (SELECT)

```python
import mysql.connector

connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='your_password',
    database='company_db'
)

cursor = connection.cursor()

# קריאת כל הנתונים
cursor.execute("SELECT * FROM employees")

# שליפת כל התוצאות
results = cursor.fetchall()

for row in results:
    print(f"ID: {row[0]}, Name: {row[1]}, Age: {row[2]}, City: {row[3]}, Salary: {row[4]}")

# שימוש ב-dictionary
cursor = connection.cursor(dictionary=True)
cursor.execute("SELECT * FROM employees WHERE age > 25")

for row in cursor.fetchall():
    print(row)

cursor.close()
connection.close()
```

### 2.5: עדכון נתונים (UPDATE)

```python
import mysql.connector

connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='your_password',
    database='company_db'
)

cursor = connection.cursor()

# עדכון משכורת
update_query = "UPDATE employees SET salary = salary * 1.1 WHERE age > 30"
cursor.execute(update_query)

connection.commit()
print(f"{cursor.rowcount} שורות עודכנו!")

cursor.close()
connection.close()
```

### 2.6: מחיקת נתונים (DELETE)

```python
import mysql.connector

connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='your_password',
    database='company_db'
)

cursor = connection.cursor()

# מחיקת עובדים מעיר מסוימת
delete_query = "DELETE FROM employees WHERE city = %s"
cursor.execute(delete_query, ("Haifa",))

connection.commit()
print(f"{cursor.rowcount} שורות נמחקו!")

cursor.close()
connection.close()
```

---

## חלק 3: שילוב CSV ו-MySQL

### 3.1: ייבוא נתונים מ-CSV ל-MySQL

#### דרך 1: שימוש במודול csv

```python
import csv
import mysql.connector

# התחברות למסד נתונים
connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='your_password',
    database='company_db'
)

cursor = connection.cursor()

# קריאת קובץ CSV והכנסה למסד נתונים
with open('employees.csv', 'r', encoding='utf-8') as file:
    csv_reader = csv.DictReader(file)
    
    for row in csv_reader:
        insert_query = """
        INSERT INTO employees (name, age, city, salary) 
        VALUES (%s, %s, %s, %s)
        """
        values = (row['name'], row['age'], row['city'], row['salary'])
        cursor.execute(insert_query, values)

connection.commit()
print(f"{cursor.rowcount} שורות נוספו מקובץ CSV!")

cursor.close()
connection.close()
```

#### דרך 2: שימוש ב-Pandas (מומלץ)

```python
import pandas as pd
import mysql.connector
from sqlalchemy import create_engine

# קריאת CSV
df = pd.read_csv('employees.csv')

# יצירת חיבור עם SQLAlchemy
engine = create_engine('mysql+mysqlconnector://root:your_password@localhost/company_db')

# ייבוא לטבלה
df.to_sql('employees', con=engine, if_exists='append', index=False)

print("כל הנתונים מ-CSV יובאו ל-MySQL!")
```

### 3.2: ייצוא נתונים מ-MySQL ל-CSV

#### דרך 1: שימוש במודול csv

```python
import csv
import mysql.connector

# התחברות
connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='your_password',
    database='company_db'
)

cursor = connection.cursor()

# שליפת נתונים
cursor.execute("SELECT name, age, city, salary FROM employees")
results = cursor.fetchall()

# כתיבה ל-CSV
with open('employees_export.csv', 'w', newline='', encoding='utf-8') as file:
    csv_writer = csv.writer(file)
    
    # כתיבת כותרת
    csv_writer.writerow(['name', 'age', 'city', 'salary'])
    
    # כתיבת נתונים
    csv_writer.writerows(results)

print("הנתונים יוצאו ל-CSV בהצלחה!")

cursor.close()
connection.close()
```

#### דרך 2: שימוש ב-Pandas

```python
import pandas as pd
from sqlalchemy import create_engine

# יצירת חיבור
engine = create_engine('mysql+mysqlconnector://root:your_password@localhost/company_db')

# קריאת נתונים מ-SQL
query = "SELECT * FROM employees WHERE salary > 10000"
df = pd.read_sql(query, engine)

# ייצוא ל-CSV
df.to_csv('high_salary_employees.csv', index=False)

print("הנתונים יוצאו ל-CSV!")
```

### 3.3: סקריפט מלא - ניהול עובדים

```python
import csv
import mysql.connector
from datetime import datetime

class EmployeeManager:
    def __init__(self, host, user, password, database):
        """אתחול מנהל עובדים"""
        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.connection.cursor(dictionary=True)
    
    def import_from_csv(self, filename):
        """ייבוא עובדים מקובץ CSV"""
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file)
                count = 0
                
                for row in csv_reader:
                    query = """
                    INSERT INTO employees (name, age, city, salary) 
                    VALUES (%s, %s, %s, %s)
                    """
                    values = (row['name'], row['age'], row['city'], row['salary'])
                    self.cursor.execute(query, values)
                    count += 1
                
                self.connection.commit()
                print(f"✓ {count} עובדים יובאו בהצלחה!")
                return True
                
        except Exception as e:
            print(f"✗ שגיאה: {e}")
            return False
    
    def export_to_csv(self, filename, query="SELECT * FROM employees"):
        """ייצוא עובדים לקובץ CSV"""
        try:
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            
            if not results:
                print("אין נתונים לייצוא!")
                return False
            
            with open(filename, 'w', newline='', encoding='utf-8') as file:
                # שליפת שמות העמודות
                fieldnames = results[0].keys()
                csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
                
                csv_writer.writeheader()
                csv_writer.writerows(results)
            
            print(f"✓ {len(results)} שורות יוצאו ל-{filename}!")
            return True
            
        except Exception as e:
            print(f"✗ שגיאה: {e}")
            return False
    
    def get_all_employees(self):
        """הצגת כל העובדים"""
        self.cursor.execute("SELECT * FROM employees")
        return self.cursor.fetchall()
    
    def add_employee(self, name, age, city, salary):
        """הוספת עובד חדש"""
        try:
            query = """
            INSERT INTO employees (name, age, city, salary) 
            VALUES (%s, %s, %s, %s)
            """
            self.cursor.execute(query, (name, age, city, salary))
            self.connection.commit()
            print(f"✓ עובד {name} נוסף בהצלחה!")
            return True
        except Exception as e:
            print(f"✗ שגיאה: {e}")
            return False
    
    def search_employees(self, **filters):
        """חיפוש עובדים לפי פילטרים"""
        conditions = []
        values = []
        
        if 'city' in filters:
            conditions.append("city = %s")
            values.append(filters['city'])
        
        if 'min_salary' in filters:
            conditions.append("salary >= %s")
            values.append(filters['min_salary'])
        
        if 'max_age' in filters:
            conditions.append("age <= %s")
            values.append(filters['max_age'])
        
        query = "SELECT * FROM employees"
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        
        self.cursor.execute(query, values)
        return self.cursor.fetchall()
    
    def close(self):
        """סגירת החיבור"""
        self.cursor.close()
        self.connection.close()
        print("החיבור נסגר!")


# דוגמה לשימוש
if __name__ == "__main__":
    # יצירת מנהל עובדים
    manager = EmployeeManager(
        host='localhost',
        user='root',
        password='your_password',
        database='company_db'
    )
    
    # ייבוא מ-CSV
    manager.import_from_csv('employees.csv')
    
    # הצגת כל העובדים
    employees = manager.get_all_employees()
    for emp in employees:
        print(emp)
    
    # חיפוש עובדים
    results = manager.search_employees(city='Tel Aviv', min_salary=10000)
    print(f"\nנמצאו {len(results)} עובדים בתל אביב עם משכורת מעל 10000")
    
    # ייצוא לקובץ חדש
    manager.export_to_csv(
        'tel_aviv_employees.csv',
        "SELECT * FROM employees WHERE city = 'Tel Aviv'"
    )
    
    # סגירת החיבור
    manager.close()
```

---

## תרגילים מעשיים

### תרגיל 1: יצירת קובץ CSV והכנסתו ל-MySQL

**משימה:**
1. צור קובץ CSV בשם `students.csv` עם הנתונים הבאים:
```
name,age,grade,subject
David,20,85,Math
Emma,22,90,Physics
Frank,21,88,Chemistry
```

2. צור טבלה `students` במסד נתונים
3. ייבא את הנתונים מה-CSV לטבלה

**פתרון:**

```python
import csv
import mysql.connector

# שלב 1: יצירת קובץ CSV
students_data = [
    ['name', 'age', 'grade', 'subject'],
    ['David', 20, 85, 'Math'],
    ['Emma', 22, 90, 'Physics'],
    ['Frank', 21, 88, 'Chemistry']
]

with open('students.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerows(students_data)

print("✓ קובץ CSV נוצר!")

# שלב 2: יצירת טבלה
connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='your_password',
    database='company_db'
)

cursor = connection.cursor()

create_table = """
CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    age INT,
    grade INT,
    subject VARCHAR(100)
)
"""

cursor.execute(create_table)
print("✓ טבלה נוצרה!")

# שלב 3: ייבוא נתונים
with open('students.csv', 'r', encoding='utf-8') as file:
    csv_reader = csv.DictReader(file)
    
    for row in csv_reader:
        query = "INSERT INTO students (name, age, grade, subject) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (row['name'], row['age'], row['grade'], row['subject']))

connection.commit()
print(f"✓ {cursor.rowcount} סטודנטים יובאו!")

cursor.close()
connection.close()
```

### תרגיל 2: ניתוח נתונים וייצוא

**משימה:**
1. שלוף מהמסד נתונים את כל הסטודנטים עם ציון מעל 85
2. חשב את ממוצע הגילאים
3. ייצא את התוצאות לקובץ CSV חדש

**פתרון:**

```python
import mysql.connector
import csv

connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='your_password',
    database='company_db'
)

cursor = connection.cursor(dictionary=True)

# שליפת סטודנטים עם ציון גבוה
cursor.execute("SELECT * FROM students WHERE grade > 85")
high_grade_students = cursor.fetchall()

print(f"נמצאו {len(high_grade_students)} סטודנטים עם ציון מעל 85")

# חישוב ממוצע גילאים
if high_grade_students:
    avg_age = sum(s['age'] for s in high_grade_students) / len(high_grade_students)
    print(f"ממוצע גילאים: {avg_age:.2f}")

# ייצוא לקובץ CSV
with open('high_grade_students.csv', 'w', newline='', encoding='utf-8') as file:
    fieldnames = ['id', 'name', 'age', 'grade', 'subject']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    
    writer.writeheader()
    writer.writerows(high_grade_students)

print("✓ הנתונים יוצאו ל-CSV!")

cursor.close()
connection.close()
```

### תרגיל 3: עדכון מסיבי מ-CSV

**משימה:**
יש לך קובץ CSV עם עדכוני משכורות. עדכן את מסד הנתונים בהתאם.

```python
import csv
import mysql.connector

# קובץ עדכונים
updates = [
    ['name', 'new_salary'],
    ['Alice', 11000],
    ['Bob', 13000]
]

# יצירת קובץ
with open('salary_updates.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerows(updates)

# עדכון מסד הנתונים
connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='your_password',
    database='company_db'
)

cursor = connection.cursor()

with open('salary_updates.csv', 'r', encoding='utf-8') as file:
    csv_reader = csv.DictReader(file)
    
    for row in csv_reader:
        update_query = "UPDATE employees SET salary = %s WHERE name = %s"
        cursor.execute(update_query, (row['new_salary'], row['name']))

connection.commit()
print(f"✓ {cursor.rowcount} עובדים עודכנו!")

cursor.close()
connection.close()
```

---

## טיפים וכללי אצבע

### 1. טיפול בשגיאות

תמיד השתמש ב-try-except:

```python
import mysql.connector

try:
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='your_password',
        database='company_db'
    )
    cursor = connection.cursor()
    
    # הפעולות שלך כאן
    
    connection.commit()
    
except mysql.connector.Error as error:
    print(f"שגיאה: {error}")
    
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("החיבור נסגר")
```

### 2. שימוש ב-Context Manager

```python
from contextlib import closing
import mysql.connector

with closing(mysql.connector.connect(
    host='localhost',
    user='root',
    password='your_password',
    database='company_db'
)) as connection:
    with closing(connection.cursor()) as cursor:
        cursor.execute("SELECT * FROM employees")
        results = cursor.fetchall()
        print(results)
# החיבור נסגר אוטומטית
```

### 3. קידוד (Encoding)

תמיד הגדר encoding='utf-8' בעבודה עם קבצי CSV:

```python
with open('file.csv', 'r', encoding='utf-8') as file:
    # הקוד שלך
```

### 4. Parameterized Queries

מניעת SQL Injection - תמיד השתמש ב-parameters:

```python
# ✓ נכון
cursor.execute("SELECT * FROM employees WHERE name = %s", (name,))

# ✗ לא נכון - מסוכן!
cursor.execute(f"SELECT * FROM employees WHERE name = '{name}'")
```

### 5. ביצועים

לייבוא כמויות גדולות של נתונים, השתמש ב-executemany:

```python
data = [(name1, age1), (name2, age2), (name3, age3)]
cursor.executemany("INSERT INTO employees (name, age) VALUES (%s, %s)", data)
```

---

## סיכום

במדריך זה למדת:

✅ **CSV:**
- קריאה וכתיבה של קבצי CSV
- שימוש במודול csv ו-Pandas
- עבודה עם DictReader ו-DictWriter

✅ **MySQL:**
- התחברות למסד נתונים
- יצירת טבלאות
- פעולות CRUD (Create, Read, Update, Delete)
- שאילתות SQL בסיסיות

✅ **שילוב:**
- ייבוא נתונים מ-CSV ל-MySQL
- ייצוא נתונים מ-MySQL ל-CSV
- בניית מערכת ניהול עובדים

### צעדים הבאים

1. תרגל עם נתונים אמיתיים
2. למד שאילתות SQL מתקדמות (JOIN, GROUP BY)
3. התחל לעבוד עם Pandas למניפולציות נתונים מתקדמות
4. למד על ORM כמו SQLAlchemy או SQLModel

---

## משאבים נוספים

- [תיעוד Python CSV](https://docs.python.org/3/library/csv.html)
- [תיעוד MySQL Connector](https://dev.mysql.com/doc/connector-python/en/)
- [תיעוד Pandas](https://pandas.pydata.org/docs/)
- [מדריך SQL](https://www.w3schools.com/sql/)

**בהצלחה! 🚀**
