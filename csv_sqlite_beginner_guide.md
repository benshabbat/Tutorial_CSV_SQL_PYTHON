# מדריך מקיף: CSV עם SQLite לרמת מתחילים

## תוכן עניינים
1. [מבוא](#מבוא)
2. [התקנה והכנה](#התקנה-והכנה)
3. [יצירת קובץ CSV ראשון](#יצירת-קובץ-csv-ראשון)
4. [קריאת נתונים מקובץ CSV](#קריאת-נתונים-מקובץ-csv)
5. [יצירת מסד נתונים SQLite](#יצירת-מסד-נתונים-sqlite)
6. [העברת נתונים מ-CSV ל-SQLite](#העברת-נתונים-מ-csv-ל-sqlite)
7. [שאילתות בסיסיות](#שאילתות-בסיסיות)
8. [ייצוא נתונים מ-SQLite ל-CSV](#ייצוא-נתונים-מ-sqlite-ל-csv)
9. [תרגילים מעשיים](#תרגילים-מעשיים)

---

## מבוא

### מה זה CSV?
CSV (Comma-Separated Values) הוא פורמט קובץ פשוט לאחסון נתונים בטבלה. כל שורה מייצגת רשומה, והערכים מופרדים בפסיקים.

**דוגמה לקובץ CSV:**
```csv
name,age,city
Alice,25,Tel Aviv
Bob,30,Jerusalem
Charlie,35,Haifa
```

### מה זה SQLite?
SQLite הוא מסד נתונים רלציוני קל משקל שלא דורש שרת נפרד. הוא מושלם למתחילים ולפרויקטים קטנים-בינוניים.

### למה לשלב בין CSV ל-SQLite?
- **CSV**: קל לעריכה, קריא לבני אדם, תואם לאקסל
- **SQLite**: מאפשר שאילתות מורכבות, קשרים בין טבלאות, ביצועים טובים

---

## התקנה והכנה

### דרישות מקדימות
Python כבר מותקן במחשב שלך (גרסה 3.6 ומעלה).

### בדיקת גרסת Python
```bash
python --version
```

### ספריות נדרשות
Python מגיע עם הספריות הבאות מובנות:
- `csv` - לעבודה עם קבצי CSV
- `sqlite3` - לעבודה עם מסדי נתונים SQLite

**אין צורך בהתקנה נוספת!**

---

## יצירת קובץ CSV ראשון

### שלב 1: יצירת קובץ CSV באופן ידני

צור קובץ בשם `students.csv` עם התוכן הבא:

```csv
id,name,age,grade,city
1,דני,20,85,תל אביב
2,שרה,22,92,ירושלים
3,יוסי,21,78,חיפה
4,רחל,23,88,באר שבע
5,משה,20,95,נתניה
```

### שלב 2: יצירת קובץ CSV עם Python

```python
import csv

# נתונים לדוגמה
students_data = [
    ['id', 'name', 'age', 'grade', 'city'],
    [1, 'דני', 20, 85, 'תל אביב'],
    [2, 'שרה', 22, 92, 'ירושלים'],
    [3, 'יוסי', 21, 78, 'חיפה'],
    [4, 'רחל', 23, 88, 'באר שבע'],
    [5, 'משה', 20, 95, 'נתניה']
]

# כתיבה לקובץ CSV
with open('students.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerows(students_data)

print("קובץ CSV נוצר בהצלחה!")
```

**הסבר:**
- `open('students.csv', 'w')` - פותח קובץ לכתיבה
- `newline=''` - מונע שורות ריקות בין רשומות
- `encoding='utf-8'` - תמיכה בעברית
- `csv.writer()` - יצירת אובייקט לכתיבת CSV
- `writerows()` - כתיבת כל השורות בבת אחת

---

## קריאת נתונים מקובץ CSV

### שלב 1: קריאה בסיסית

```python
import csv

# קריאת קובץ CSV
with open('students.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    
    for row in reader:
        print(row)
```

**פלט:**
```
['id', 'name', 'age', 'grade', 'city']
['1', 'דני', '20', '85', 'תל אביב']
['2', 'שרה', '22', '92', 'ירושלים']
...
```

### שלב 2: קריאה עם DictReader (מומלץ)

```python
import csv

with open('students.csv', 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    
    for row in reader:
        print(f"שם: {row['name']}, גיל: {row['age']}, ציון: {row['grade']}")
```

**פלט:**
```
שם: דני, גיל: 20, ציון: 85
שם: שרה, גיל: 22, ציון: 92
שם: יוסי, גיל: 21, ציון: 78
...
```

**יתרון DictReader:**
- גישה לערכים לפי שם העמודה במקום אינדקס
- קוד קריא וברור יותר

---

## יצירת מסד נתונים SQLite

### שלב 1: חיבור למסד נתונים

```python
import sqlite3

# יצירת חיבור (אם הקובץ לא קיים, הוא ייוצר)
conn = sqlite3.connect('school.db')

# יצירת cursor לביצוע פקודות
cursor = conn.cursor()

print("חיבור למסד הנתונים בוצע בהצלחה!")

# סגירת החיבור
conn.close()
```

**הסבר:**
- `sqlite3.connect()` - יוצר/פותח קובץ מסד נתונים
- `cursor()` - מאפשר ביצוע פקודות SQL
- `conn.close()` - סוגר את החיבור (חשוב!)

### שלב 2: יצירת טבלה

```python
import sqlite3

conn = sqlite3.connect('school.db')
cursor = conn.cursor()

# יצירת טבלת תלמידים
cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        age INTEGER,
        grade INTEGER,
        city TEXT
    )
''')

# שמירת השינויים
conn.commit()

print("טבלה נוצרה בהצלחה!")
conn.close()
```

**הסבר על סוגי נתונים ב-SQLite:**
- `INTEGER` - מספרים שלמים
- `TEXT` - טקסט
- `REAL` - מספרים עשרוניים
- `BLOB` - נתונים בינאריים
- `PRIMARY KEY` - מפתח ראשי (ייחודי)
- `NOT NULL` - שדה חובה

---

## העברת נתונים מ-CSV ל-SQLite

### שלב 1: קריאה מ-CSV והכנסה ל-SQLite

```python
import csv
import sqlite3

# חיבור למסד נתונים
conn = sqlite3.connect('school.db')
cursor = conn.cursor()

# יצירת טבלה
cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        age INTEGER,
        grade INTEGER,
        city TEXT
    )
''')

# קריאת הנתונים מ-CSV והכנסה ל-SQLite
with open('students.csv', 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    
    for row in reader:
        cursor.execute('''
            INSERT INTO students (id, name, age, grade, city)
            VALUES (?, ?, ?, ?, ?)
        ''', (row['id'], row['name'], row['age'], row['grade'], row['city']))

# שמירת השינויים
conn.commit()

# בדיקה - כמה רשומות הוכנסו
cursor.execute('SELECT COUNT(*) FROM students')
count = cursor.fetchone()[0]
print(f"הוכנסו {count} תלמידים למסד הנתונים")

conn.close()
```

**הסבר:**
- `?` - placeholders למניעת SQL Injection
- `commit()` - שומר את השינויים במסד הנתונים
- `fetchone()` - מחזיר רשומה אחת

### שלב 2: גרסה משופרת עם טיפול בשגיאות

```python
import csv
import sqlite3

def import_csv_to_sqlite(csv_file, db_file, table_name):
    """
    מייבא נתונים מ-CSV ל-SQLite
    """
    try:
        # חיבור למסד נתונים
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        
        # יצירת טבלה
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {table_name} (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                age INTEGER,
                grade INTEGER,
                city TEXT
            )
        ''')
        
        # ניקוי הטבלה (אופציונלי)
        cursor.execute(f'DELETE FROM {table_name}')
        
        # קריאה והכנסת נתונים
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                cursor.execute(f'''
                    INSERT INTO {table_name} (id, name, age, grade, city)
                    VALUES (?, ?, ?, ?, ?)
                ''', (row['id'], row['name'], row['age'], row['grade'], row['city']))
        
        conn.commit()
        
        # בדיקה
        cursor.execute(f'SELECT COUNT(*) FROM {table_name}')
        count = cursor.fetchone()[0]
        print(f"✓ הצלחה! {count} רשומות יובאו לטבלת {table_name}")
        
    except FileNotFoundError:
        print(f"✗ שגיאה: הקובץ {csv_file} לא נמצא")
    except sqlite3.Error as e:
        print(f"✗ שגיאת SQLite: {e}")
    except Exception as e:
        print(f"✗ שגיאה כללית: {e}")
    finally:
        if conn:
            conn.close()

# שימוש בפונקציה
import_csv_to_sqlite('students.csv', 'school.db', 'students')
```

---

## שאילתות בסיסיות

### 1. בחירת כל הנתונים (SELECT)

```python
import sqlite3

conn = sqlite3.connect('school.db')
cursor = conn.cursor()

# שאילתה בסיסית
cursor.execute('SELECT * FROM students')
results = cursor.fetchall()

print("כל התלמידים:")
for row in results:
    print(row)

conn.close()
```

### 2. בחירת עמודות ספציפיות

```python
import sqlite3

conn = sqlite3.connect('school.db')
cursor = conn.cursor()

# בחירת שם וציון בלבד
cursor.execute('SELECT name, grade FROM students')
results = cursor.fetchall()

print("שמות וציונים:")
for name, grade in results:
    print(f"{name}: {grade}")

conn.close()
```

### 3. סינון נתונים (WHERE)

```python
import sqlite3

conn = sqlite3.connect('school.db')
cursor = conn.cursor()

# תלמידים עם ציון מעל 85
cursor.execute('SELECT name, grade FROM students WHERE grade > 85')
results = cursor.fetchall()

print("תלמידים מצטיינים (ציון מעל 85):")
for name, grade in results:
    print(f"{name}: {grade}")

conn.close()
```

### 4. מיון תוצאות (ORDER BY)

```python
import sqlite3

conn = sqlite3.connect('school.db')
cursor = conn.cursor()

# מיון לפי ציון בסדר יורד
cursor.execute('SELECT name, grade FROM students ORDER BY grade DESC')
results = cursor.fetchall()

print("תלמידים לפי ציונים (מהגבוה לנמוך):")
for i, (name, grade) in enumerate(results, 1):
    print(f"{i}. {name}: {grade}")

conn.close()
```

### 5. חישובים סטטיסטיים

```python
import sqlite3

conn = sqlite3.connect('school.db')
cursor = conn.cursor()

# ממוצע ציונים
cursor.execute('SELECT AVG(grade) FROM students')
avg = cursor.fetchone()[0]
print(f"ממוצע הציונים: {avg:.2f}")

# ציון מקסימלי
cursor.execute('SELECT MAX(grade) FROM students')
max_grade = cursor.fetchone()[0]
print(f"הציון הגבוה ביותר: {max_grade}")

# ציון מינימלי
cursor.execute('SELECT MIN(grade) FROM students')
min_grade = cursor.fetchone()[0]
print(f"הציון הנמוך ביותר: {min_grade}")

# ספירת תלמידים
cursor.execute('SELECT COUNT(*) FROM students')
count = cursor.fetchone()[0]
print(f"מספר התלמידים: {count}")

conn.close()
```

### 6. קיבוץ נתונים (GROUP BY)

```python
import sqlite3

conn = sqlite3.connect('school.db')
cursor = conn.cursor()

# מספר תלמידים בכל עיר
cursor.execute('SELECT city, COUNT(*) as count FROM students GROUP BY city')
results = cursor.fetchall()

print("מספר תלמידים לפי עיר:")
for city, count in results:
    print(f"{city}: {count} תלמידים")

conn.close()
```

---

## ייצוא נתונים מ-SQLite ל-CSV

### שלב 1: ייצוא בסיסי

```python
import sqlite3
import csv

conn = sqlite3.connect('school.db')
cursor = conn.cursor()

# שאילתה
cursor.execute('SELECT * FROM students')
results = cursor.fetchall()

# קבלת שמות העמודות
column_names = [description[0] for description in cursor.description]

# כתיבה ל-CSV
with open('students_export.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    
    # כתיבת כותרות
    writer.writerow(column_names)
    
    # כתיבת הנתונים
    writer.writerows(results)

print("הנתונים יוצאו בהצלחה ל-students_export.csv")
conn.close()
```

### שלב 2: ייצוא עם סינון

```python
import sqlite3
import csv

def export_to_csv(db_file, query, output_file):
    """
    מייצא תוצאות שאילתה ל-CSV
    """
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    cursor.execute(query)
    results = cursor.fetchall()
    column_names = [description[0] for description in cursor.description]
    
    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(column_names)
        writer.writerows(results)
    
    print(f"✓ {len(results)} רשומות יוצאו ל-{output_file}")
    conn.close()

# דוגמאות שימוש:

# ייצוא תלמידים מצטיינים
export_to_csv('school.db', 
              'SELECT * FROM students WHERE grade >= 90',
              'excellent_students.csv')

# ייצוא תלמידים מעיר מסוימת
export_to_csv('school.db',
              "SELECT * FROM students WHERE city = 'תל אביב'",
              'tel_aviv_students.csv')

# ייצוא עם מיון
export_to_csv('school.db',
              'SELECT name, grade FROM students ORDER BY grade DESC',
              'students_by_grade.csv')
```

---

## תרגילים מעשיים

### תרגיל 1: מערכת ניהול ספרייה

```python
import csv
import sqlite3

# 1. צור קובץ CSV עם ספרים
books_data = [
    ['id', 'title', 'author', 'year', 'genre'],
    [1, 'הארי פוטר', 'ג.ק. רולינג', 1997, 'פנטזיה'],
    [2, '1984', 'ג\'ורג\' אורוול', 1949, 'מדע בדיוני'],
    [3, 'גאווה ודעה קדומה', 'ג\'יין אוסטין', 1813, 'רומנטיקה'],
    [4, 'הארי פוטר 2', 'ג.ק. רולינג', 1998, 'פנטזיה']
]

with open('books.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerows(books_data)

# 2. יצירת מסד נתונים והכנסת הספרים
conn = sqlite3.connect('library.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        year INTEGER,
        genre TEXT
    )
''')

with open('books.csv', 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        cursor.execute('''
            INSERT OR REPLACE INTO books (id, title, author, year, genre)
            VALUES (?, ?, ?, ?, ?)
        ''', (row['id'], row['title'], row['author'], row['year'], row['genre']))

conn.commit()

# 3. שאילתות שונות
print("=== כל הספרים ===")
cursor.execute('SELECT title, author FROM books')
for title, author in cursor.fetchall():
    print(f"- {title} מאת {author}")

print("\n=== ספרי פנטזיה ===")
cursor.execute('SELECT title FROM books WHERE genre = "פנטזיה"')
for (title,) in cursor.fetchall():
    print(f"- {title}")

print("\n=== ספרים לפי מחבר ===")
cursor.execute('SELECT author, COUNT(*) FROM books GROUP BY author')
for author, count in cursor.fetchall():
    print(f"{author}: {count} ספרים")

conn.close()
```

### תרגיל 2: מערכת עובדים ומשכורות

```python
import csv
import sqlite3

# יצירת קובץ עובדים
employees_data = [
    ['id', 'name', 'department', 'salary', 'hire_date'],
    [1, 'יוסי כהן', 'IT', 15000, '2020-01-15'],
    [2, 'שרה לוי', 'HR', 12000, '2019-03-20'],
    [3, 'דוד ישראלי', 'IT', 18000, '2018-06-10'],
    [4, 'רחל אברהם', 'Sales', 14000, '2021-02-01'],
    [5, 'משה דוד', 'IT', 16000, '2020-08-15']
]

with open('employees.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerows(employees_data)

# יצירת מסד נתונים
conn = sqlite3.connect('company.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        department TEXT,
        salary INTEGER,
        hire_date TEXT
    )
''')

# ייבוא נתונים
with open('employees.csv', 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        cursor.execute('''
            INSERT OR REPLACE INTO employees VALUES (?, ?, ?, ?, ?)
        ''', (row['id'], row['name'], row['department'], 
              row['salary'], row['hire_date']))

conn.commit()

# שאילתות מעניינות
print("=== משכורת ממוצעת לפי מחלקה ===")
cursor.execute('''
    SELECT department, AVG(salary) as avg_salary 
    FROM employees 
    GROUP BY department
''')
for dept, avg_sal in cursor.fetchall():
    print(f"{dept}: ₪{avg_sal:,.0f}")

print("\n=== עובדי IT ===")
cursor.execute('SELECT name, salary FROM employees WHERE department = "IT"')
for name, salary in cursor.fetchall():
    print(f"{name}: ₪{salary:,}")

print("\n=== משכורת מקסימלית ומינימלית ===")
cursor.execute('SELECT MAX(salary), MIN(salary) FROM employees')
max_sal, min_sal = cursor.fetchone()
print(f"מקסימום: ₪{max_sal:,}")
print(f"מינימום: ₪{min_sal:,}")

conn.close()
```

### תרגיל 3: פרויקט מלא - מערכת ניהול סטודנטים

```python
import csv
import sqlite3
from datetime import datetime

class StudentManagementSystem:
    """
    מערכת ניהול סטודנטים עם SQLite
    """
    
    def __init__(self, db_file='students_system.db'):
        self.db_file = db_file
        self.create_table()
    
    def create_table(self):
        """יצירת טבלת סטודנטים"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER,
                grade REAL,
                city TEXT,
                enrollment_date TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def import_from_csv(self, csv_file):
        """ייבוא סטודנטים מקובץ CSV"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        try:
            with open(csv_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                count = 0
                
                for row in reader:
                    cursor.execute('''
                        INSERT INTO students (name, age, grade, city, enrollment_date)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (row.get('name'), row.get('age'), row.get('grade'),
                          row.get('city'), row.get('enrollment_date', datetime.now().strftime('%Y-%m-%d'))))
                    count += 1
                
                conn.commit()
                print(f"✓ יובאו {count} סטודנטים בהצלחה")
        except Exception as e:
            print(f"✗ שגיאה בייבוא: {e}")
        finally:
            conn.close()
    
    def add_student(self, name, age, grade, city):
        """הוספת סטודנט חדש"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO students (name, age, grade, city, enrollment_date)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, age, grade, city, datetime.now().strftime('%Y-%m-%d')))
        
        conn.commit()
        print(f"✓ הסטודנט {name} נוסף בהצלחה")
        conn.close()
    
    def get_all_students(self):
        """הצגת כל הסטודנטים"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM students')
        students = cursor.fetchall()
        
        print("\n=== רשימת כל הסטודנטים ===")
        for student in students:
            print(f"ID: {student[0]}, שם: {student[1]}, גיל: {student[2]}, "
                  f"ציון: {student[3]}, עיר: {student[4]}")
        
        conn.close()
        return students
    
    def search_by_city(self, city):
        """חיפוש סטודנטים לפי עיר"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM students WHERE city = ?', (city,))
        students = cursor.fetchall()
        
        print(f"\n=== סטודנטים מ{city} ===")
        for student in students:
            print(f"{student[1]} - ציון: {student[3]}")
        
        conn.close()
        return students
    
    def get_statistics(self):
        """סטטיסטיקות כלליות"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*), AVG(grade), MAX(grade), MIN(grade) FROM students')
        count, avg, max_g, min_g = cursor.fetchone()
        
        print("\n=== סטטיסטיקות ===")
        print(f"מספר סטודנטים: {count}")
        print(f"ממוצע ציונים: {avg:.2f}")
        print(f"ציון מקסימלי: {max_g}")
        print(f"ציון מינימלי: {min_g}")
        
        conn.close()
    
    def export_to_csv(self, output_file='students_export.csv'):
        """ייצוא כל הסטודנטים ל-CSV"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM students')
        students = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]
        
        with open(output_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(column_names)
            writer.writerows(students)
        
        print(f"✓ {len(students)} סטודנטים יוצאו ל-{output_file}")
        conn.close()

# שימוש במערכת
if __name__ == "__main__":
    # יצירת המערכת
    system = StudentManagementSystem()
    
    # הוספת סטודנטים
    system.add_student('אלי כהן', 21, 88, 'תל אביב')
    system.add_student('מיכל לוי', 22, 92, 'חיפה')
    system.add_student('דני ישראלי', 20, 85, 'תל אביב')
    
    # הצגת כל הסטודנטים
    system.get_all_students()
    
    # חיפוש לפי עיר
    system.search_by_city('תל אביב')
    
    # סטטיסטיקות
    system.get_statistics()
    
    # ייצוא ל-CSV
    system.export_to_csv()
```

---

## טיפים וטריקים מתקדמים

### 1. שימוש ב-Context Manager

```python
import sqlite3

class DatabaseConnection:
    """Context manager לחיבור מסד נתונים"""
    
    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = None
    
    def __enter__(self):
        self.conn = sqlite3.connect(self.db_file)
        return self.conn.cursor()
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            if exc_type is None:
                self.conn.commit()
            else:
                self.conn.rollback()
            self.conn.close()

# שימוש
with DatabaseConnection('school.db') as cursor:
    cursor.execute('SELECT * FROM students')
    results = cursor.fetchall()
    for row in results:
        print(row)
```

### 2. Bulk Insert מהיר יותר

```python
import csv
import sqlite3

conn = sqlite3.connect('school.db')
cursor = conn.cursor()

# קריאת כל הנתונים מ-CSV
with open('students.csv', 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    data = [(row['id'], row['name'], row['age'], row['grade'], row['city']) 
            for row in reader]

# הכנסה מהירה של כל הנתונים בבת אחת
cursor.executemany('''
    INSERT INTO students (id, name, age, grade, city)
    VALUES (?, ?, ?, ?, ?)
''', data)

conn.commit()
conn.close()
```

### 3. שאילתות פרמטריות בטוחות

```python
import sqlite3

def safe_search(name_pattern):
    """חיפוש בטוח עם פרמטרים"""
    conn = sqlite3.connect('school.db')
    cursor = conn.cursor()
    
    # שימוש נכון ב-parameters
    cursor.execute('SELECT * FROM students WHERE name LIKE ?', (f'%{name_pattern}%',))
    results = cursor.fetchall()
    
    conn.close()
    return results

# שימוש
results = safe_search('דני')
for row in results:
    print(row)
```

---

## שגיאות נפוצות ופתרונות

### שגיאה 1: UnicodeDecodeError
**בעיה:** טקסט בעברית לא מוצג כראוי

**פתרון:**
```python
# תמיד להוסיף encoding='utf-8'
with open('file.csv', 'r', encoding='utf-8') as file:
    # קוד...
```

### שגיאה 2: sqlite3.OperationalError: table already exists
**בעיה:** ניסיון ליצור טבלה קיימת

**פתרון:**
```python
# שימוש ב-IF NOT EXISTS
cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (...)
''')
```

### שגיאה 3: נתונים לא נשמרים
**בעיה:** שכחתם לקרוא ל-commit()

**פתרון:**
```python
conn = sqlite3.connect('school.db')
cursor = conn.cursor()
cursor.execute('INSERT INTO ...')
conn.commit()  # חובה!
conn.close()
```

---

## סיכום ומה הלאה

### מה למדנו:
✓ עבודה עם קבצי CSV (קריאה וכתיבה)  
✓ יצירת מסד נתונים SQLite  
✓ העברת נתונים בין CSV ל-SQLite  
✓ שאילתות SQL בסיסיות  
✓ ייצוא נתונים  
✓ טיפול בשגיאות  

### צעדים הבאים:
1. למד על יחסים בין טבלאות (Foreign Keys)
2. התנסה עם Pandas לניתוח נתונים מתקדם
3. למד על SQLAlchemy או SQLModel לעבודה מתקדמת
4. בנה פרויקט אמיתי משלך

### משאבים נוספים:
- [תיעוד Python CSV](https://docs.python.org/3/library/csv.html)
- [תיעוד Python SQLite3](https://docs.python.org/3/library/sqlite3.html)
- [SQLite Tutorial](https://www.sqlitetutorial.net/)

---

**בהצלחה! 🚀**
