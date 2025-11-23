# מדריך MySQL עם Python למתחילים

מדריך מקיף בעברית לעבודה עם MySQL ו-Python מהבסיס.

---

## 📚 חלק א': הסבר מושגים

### מה זה MySQL?

**MySQL** היא מערכת לניהול מסדי נתונים יחסיים (RDBMS - Relational Database Management System).

**למה להשתמש ב-MySQL?**
- 🆓 חינמי וקוד פתוח
- ⚡ מהיר ויעיל
- 🔒 אמין ובטוח
- 🌍 הכי פופולרי בעולם

### מושגי יסוד

#### 1. מסד נתונים (Database)
מקום לאחסון מידע מאורגן. כמו תיקייה שמכילה קבצים.

**דוגמה:**
- מסד נתונים: `חברה`
- מכיל: עובדים, מחלקות, משכורות

#### 2. טבלה (Table)
מבנה לאחסון נתונים בשורות ועמודות. כמו גיליון Excel.

**דוגמה - טבלת עובדים:**
```
+----+-----------+-----------+---------+
| id | שם        | מחלקה     | משכורת  |
+----+-----------+-----------+---------+
| 1  | דני       | פיתוח     | 15000   |
| 2  | שרה       | שיווק     | 12000   |
+----+-----------+-----------+---------+
```

#### 3. שורה (Row/Record)
רשומה בודדת בטבלה. כל שורה מייצגת ישות אחת.

**דוגמה:** `1, דני, פיתוח, 15000` - רשומת עובד אחד

#### 4. עמודה (Column/Field)
סוג נתון ספציפי. כל עמודה מחזיקה מידע מסוים.

**דוגמה:** עמודת "שם" מכילה רק שמות

#### 5. מפתח ראשי (Primary Key)
מזהה ייחודי לכל שורה. לא יכול להיות כפול.

**דוגמה:** עמודת `id` - כל עובד מקבל מספר ייחודי

#### 6. סוגי נתונים (Data Types)
- **INT** - מספר שלם (גיל, כמות)
- **VARCHAR(100)** - טקסט עד 100 תווים (שם, כתובת)
- **DECIMAL(10,2)** - מספר עשרוני (משכורת, מחיר)
- **DATE** - תאריך (תאריך לידה)
- **TEXT** - טקסט ארוך (תיאור)

#### 7. פקודות SQL בסיסיות

- **CREATE** - יוצר מסד נתונים או טבלה
- **INSERT** - מוסיף נתונים חדשים
- **SELECT** - קורא נתונים
- **UPDATE** - מעדכן נתונים קיימים
- **DELETE** - מוחק נתונים

---

## 🔧 חלק ב': התקנה והגדרה

### שלב 1: התקנת MySQL

**Windows:**
1. הורד מ-[mysql.com](https://dev.mysql.com/downloads/installer/)
2. הרץ את ה-Installer
3. בחר "Developer Default"
4. הגדר סיסמה ל-root

**בדיקה:**
```bash
mysql --version
```

### שלב 2: התקנת MySQL Connector לPython

```bash
pip install mysql-connector-python
```

**בדיקה:**
```python
import mysql.connector
print("✓ ההתקנה הצליחה!")
```

---

## 📖 חלק ג': טוטוריאל שלב אחר שלב

### שלב 1: התחברות ראשונית

```python
import mysql.connector

# התחבר לשרת MySQL
connection = mysql.connector.connect(
    host="localhost",        # כתובת השרת
    user="root",            # שם משתמש
    password="your_password"   # הסיסמה שהגדרת
)

if connection.is_connected():
    print("✓ התחברנו בהצלחה ל-MySQL!")

connection.close()
```

**הסבר:**
- `host` - כתובת שרת MySQL (בדרך כלל localhost)
- `user` - שם משתמש (ברירת מחדל: root)
- `password` - הסיסמה שהגדרת
- `is_connected()` - בודק אם החיבור הצליח
- `close()` - סוגר את החיבור

---

### שלב 2: יצירת מסד נתונים

```python
import mysql.connector

# התחבר ל-MySQL
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password"
)

cursor = connection.cursor()

# צור מסד נתונים חדש
cursor.execute("CREATE DATABASE IF NOT EXISTS company")
print("✓ מסד הנתונים נוצר!")

# הצג את כל מסדי הנתונים
cursor.execute("SHOW DATABASES")
print("\nמסדי נתונים קיימים:")
for db in cursor:
    print(f"  - {db[0]}")

cursor.close()
connection.close()
```

**הסבר:**
- `cursor()` - יוצר "סמן" לביצוע פקודות SQL
- `CREATE DATABASE` - יוצר מסד נתונים חדש
- `IF NOT EXISTS` - רק אם לא קיים (למנוע שגיאות)
- `SHOW DATABASES` - מציג את כל מסדי הנתונים

---

### שלב 3: יצירת טבלה

```python
import mysql.connector

# התחבר למסד הנתונים
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password",
    database="company"  # מתחבר ישירות למסד הנתונים
)

cursor = connection.cursor()

# צור טבלת עובדים
cursor.execute("""
    CREATE TABLE IF NOT EXISTS employees (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        department VARCHAR(50),
        salary DECIMAL(10, 2)
    )
""")

print("✓ הטבלה נוצרה בהצלחה!")

cursor.close()
connection.close()
```

**הסבר על המבנה:**
- `id INT AUTO_INCREMENT PRIMARY KEY` - מספר זיהוי ייחודי שעולה אוטומטית
- `שם VARCHAR(100) NOT NULL` - שם עד 100 תווים, חובה למלא
- `מחלקה VARCHAR(50)` - מחלקה עד 50 תווים
- `משכורת DECIMAL(10, 2)` - משכורת עם 2 ספרות אחרי הנקודה

---

### שלב 4: הוספת נתונים

#### הוספת רשומה אחת

```python
import mysql.connector

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password",
    database="company"
)

cursor = connection.cursor()

# הוסף עובד אחד
sql = "INSERT INTO employees (name, department, salary) VALUES (%s, %s, %s)"
values = ("Danny Cohen", "Development", 15000)

cursor.execute(sql, values)
connection.commit()  # חשוב! שומר את השינויים

print(f"✓ עובד נוסף! מספר זיהוי: {cursor.lastrowid}")

cursor.close()
connection.close()
```

**הסבר חשוב:**
- `%s` - מקום שומר (placeholder) לערכים
- `VALUES (%s, %s, %s)` - 3 ערכים בסדר: שם, מחלקה, משכורת
- `commit()` - **חובה!** שומר את השינויים למסד הנתונים
- `lastrowid` - מחזיר את מספר הזיהוי של הרשומה שנוספה

#### הוספת מספר רשומות

```python
import mysql.connector

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password",
    database="company"
)

cursor = connection.cursor()

# הוסף כמה עובדים בבת אחת
sql = "INSERT INTO employees (name, department, salary) VALUES (%s, %s, %s)"
employees = [
    ("Sarah Levi", "Marketing", 12000),
    ("Yossi Cohen", "Development", 16000),
    ("Michal Israeli", "HR", 11000),
    ("Ron Abraham", "Sales", 13000)
]

cursor.executemany(sql, employees)
connection.commit()

print(f"✓ נוספו {cursor.rowcount} עובדים!")

cursor.close()
connection.close()
```

**הסבר:**
- `executemany()` - מבצע את אותה פקודה על רשימה של ערכים
- `rowcount` - כמה שורות הושפעו מהפעולה

---

### שלב 5: קריאת נתונים (SELECT)

#### קריאת כל הנתונים

```python
import mysql.connector

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password",
    database="company"
)

cursor = connection.cursor()

# בחר את כל העובדים
cursor.execute("SELECT * FROM employees")

# קרא את כל התוצאות
results = cursor.fetchall()

print("כל העובדים:")
print(f"{'ID':<8} {'Name':<20} {'Department':<15} {'Salary':<10}")
print("-" * 60)

for row in results:
    print(f"{row[0]:<8} {row[1]:<20} {row[2]:<15} {row[3]:<10}")

print(f"\nסה\"כ: {len(results)} עובדים")

cursor.close()
connection.close()
```

#### קריאת עמודות ספציפיות

```python
cursor.execute("SELECT name, salary FROM employees")

for (name, salary) in cursor:
    print(f"{name}: ₪{salary:,.2f}")
```

#### קריאת רשומה אחת

```python
cursor.execute("SELECT * FROM employees WHERE id = %s", (1,))
result = cursor.fetchone()

if result:
    print(f"נמצא: {result}")
else:
    print("לא נמצא")
```

**הסבר:**
- `SELECT *` - בחר את כל העמודות
- `fetchall()` - מחזיר את כל התוצאות כרשימה
- `fetchone()` - מחזיר רשומה אחת בלבד

---

### שלב 6: סינון נתונים (WHERE)

```python
import mysql.connector

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password",
    database="company"
)

cursor = connection.cursor()

# סנן לפי מחלקה
print("עובדי פיתוח:")
cursor.execute("SELECT * FROM employees WHERE department = %s", ("Development",))
for row in cursor:
    print(f"  {row[1]} - ₪{row[3]:,.2f}")

# סנן לפי משכורת
print("\nעובדים עם משכורת מעל 13,000:")
cursor.execute("SELECT name, salary FROM employees WHERE salary > %s", (13000,))
for (name, salary) in cursor:
    print(f"  {name}: ₪{salary:,.2f}")

# תנאי מרובה
print("\nעובדי פיתוח בכירים:")
cursor.execute("""
    SELECT name, salary 
    FROM employees 
    WHERE department = %s AND salary > %s
""", ("Development", 14000))
for (name, salary) in cursor:
    print(f"  {name}: ₪{salary:,.2f}")

cursor.close()
connection.close()
```

**תנאים נפוצים:**
- `WHERE salary > 10000` - גדול מ
- `WHERE salary >= 10000` - גדול או שווה
- `WHERE salary < 10000` - קטן מ
- `WHERE salary BETWEEN 10000 AND 15000` - בטווח
- `WHERE department IN ('Development', 'Marketing')` - אחד מהרשימה
- `WHERE name LIKE '%Cohen%'` - מכיל טקסט

---

### שלב 7: עדכון נתונים (UPDATE)

```python
import mysql.connector

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password",
    database="company"
)

cursor = connection.cursor()

# עדכן עובד ספציפי
sql = "UPDATE employees SET salary = %s WHERE name = %s"
cursor.execute(sql, (17000, "Danny Cohen"))
connection.commit()

print(f"✓ עודכנו {cursor.rowcount} עובדים")

# תן העלאה לכל המחלקה
sql = "UPDATE employees SET salary = salary * 1.10 WHERE department = %s"
cursor.execute(sql, ("Development",))
connection.commit()

print(f"✓ ניתנה העלאה ל-{cursor.rowcount} עובדי פיתוח")

cursor.close()
connection.close()
```

**⚠️ אזהרה:** תמיד השתמש ב-WHERE! בלי WHERE כל הרשומות יתעדכנו!

---

### שלב 8: מחיקת נתונים (DELETE)

```python
import mysql.connector

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password",
    database="company"
)

cursor = connection.cursor()

# מחק עובד ספציפי
sql = "DELETE FROM employees WHERE id = %s"
cursor.execute(sql, (5,))
connection.commit()

print(f"✓ נמחקו {cursor.rowcount} רשומות")

cursor.close()
connection.close()
```

**⚠️ אזהרה חמורה:** 
```python
# זה ימחק את כל הטבלה!
DELETE FROM employees  # ללא WHERE = מחיקת הכל!!!
```

---

### שלב 9: שימוש ב-Dictionary Cursor

```python
import mysql.connector

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password",
    database="company"
)

# שימוש ב-dictionary cursor - קל יותר לקריאה!
cursor = connection.cursor(dictionary=True)

cursor.execute("SELECT * FROM employees")

for row in cursor:
    print(f"שם: {row['name']}")
    print(f"מחלקה: {row['department']}")
    print(f"משכורת: ₪{row['salary']:,.2f}")
    print()

cursor.close()
connection.close()
```

**יתרון:** במקום `row[1]` אפשר לכתוב `row['name']` - הרבה יותר ברור!

---

### שלב 10: טיפול בשגיאות

```python
import mysql.connector
from mysql.connector import Error

try:
    # נסה להתחבר
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="your_password",
        database="company"
    )
    
    if connection.is_connected():
        print("✓ התחברנו בהצלחה!")
        
        cursor = connection.cursor()
        
        # נסה לבצע פעולה
        cursor.execute("SELECT * FROM employees")
        results = cursor.fetchall()
        
        for row in results:
            print(row)
        
except Error as e:
    print(f"❌ שגיאה: {e}")

finally:
    # תמיד סגור את החיבור
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("✓ החיבור נסגר")
```

**הסבר:**
- `try` - נסה לבצע את הקוד
- `except Error` - אם יש שגיאה, טפל בה
- `finally` - תמיד הרץ (לסגור חיבור)

---

### שלב 11: דוגמה מלאה - מערכת ניהול עובדים

```python
import mysql.connector
from mysql.connector import Error

class EmployeeManager:
    """מחלקה לניהול עובדים במסד הנתונים"""
    
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
    
    def connect(self):
        """התחבר למסד הנתונים"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if self.connection.is_connected():
                print("✓ התחברנו למסד הנתונים")
        except Error as e:
            print(f"❌ שגיאה בהתחברות: {e}")
    
    def create_table(self):
        """צור את טבלת העובדים"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS employees (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    department VARCHAR(50),
                    salary DECIMAL(10, 2),
                    start_date DATE
                )
            """)
            print("✓ הטבלה מוכנה")
        except Error as e:
            print(f"❌ שגיאה: {e}")
    
    def add_employee(self, name, department, salary, start_date=None):
        """הוסף עובד חדש"""
        try:
            cursor = self.connection.cursor()
            if start_date:
                sql = """INSERT INTO employees 
                        (name, department, salary, start_date) 
                        VALUES (%s, %s, %s, %s)"""
                cursor.execute(sql, (name, department, salary, start_date))
            else:
                sql = """INSERT INTO employees 
                        (name, department, salary) 
                        VALUES (%s, %s, %s)"""
                cursor.execute(sql, (name, department, salary))
            
            self.connection.commit()
            print(f"✓ {name} נוסף בהצלחה! (מזהה: {cursor.lastrowid})")
            return cursor.lastrowid
        except Error as e:
            print(f"❌ שגיאה: {e}")
            return None
    
    def show_all_employees(self):
        """הצג את כל העובדים"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM employees ORDER BY id")
            employees = cursor.fetchall()
            
            if not employees:
                print("אין עובדים במערכת")
                return
            
            print("\n" + "="*70)
            print(f"{'ID':<8} {'Name':<20} {'Department':<15} {'Salary':<12}")
            print("="*70)
            
            for emp in employees:
                print(f"{emp['id']:<8} {emp['name']:<20} "
                      f"{emp['department']:<15} ₪{emp['salary']:<11,.2f}")
            
            print("="*70)
            print(f"סה\"כ: {len(employees)} עובדים\n")
            
        except Error as e:
            print(f"❌ שגיאה: {e}")
    
    def search_employee(self, emp_id):
        """חפש עובד לפי מזהה"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM employees WHERE id = %s", (emp_id,))
            employee = cursor.fetchone()
            
            if employee:
                print(f"\nנמצא עובד:")
                print(f"  מזהה: {employee['id']}")
                print(f"  שם: {employee['name']}")
                print(f"  מחלקה: {employee['department']}")
                print(f"  משכורת: ₪{employee['salary']:,.2f}")
                return employee
            else:
                print(f"עובד עם מזהה {emp_id} לא נמצא")
                return None
                
        except Error as e:
            print(f"❌ שגיאה: {e}")
            return None
    
    def update_salary(self, emp_id, new_salary):
        """עדכן משכורת עובד"""
        try:
            cursor = self.connection.cursor()
            sql = "UPDATE employees SET salary = %s WHERE id = %s"
            cursor.execute(sql, (new_salary, emp_id))
            self.connection.commit()
            
            if cursor.rowcount > 0:
                print(f"✓ משכורת עובד {emp_id} עודכנה ל-₪{new_salary:,.2f}")
            else:
                print(f"עובד {emp_id} לא נמצא")
                
        except Error as e:
            print(f"❌ שגיאה: {e}")
    
    def delete_employee(self, emp_id):
        """מחק עובד"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("DELETE FROM employees WHERE id = %s", (emp_id,))
            self.connection.commit()
            
            if cursor.rowcount > 0:
                print(f"✓ עובד {emp_id} נמחק")
            else:
                print(f"עובד {emp_id} לא נמצא")
                
        except Error as e:
            print(f"❌ שגיאה: {e}")
    
    def employees_by_department(self, department):
        """הצג עובדים לפי מחלקה"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT * FROM employees 
                WHERE department = %s 
                ORDER BY salary DESC
            """, (department,))
            
            employees = cursor.fetchall()
            
            if employees:
                print(f"\nעובדי {department}:")
                for emp in employees:
                    print(f"  {emp['name']}: ₪{emp['salary']:,.2f}")
            else:
                print(f"אין עובדים במחלקת {department}")
                
            return employees
            
        except Error as e:
            print(f"❌ שגיאה: {e}")
            return []
    
    def get_statistics(self):
        """הצג סטטיסטיקות"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            
            # סטטיסטיקות כלליות
            cursor.execute("""
                SELECT 
                    COUNT(*) as total_employees,
                    AVG(salary) as avg_salary,
                    MIN(salary) as min_salary,
                    MAX(salary) as max_salary
                FROM employees
            """)
            
            stats = cursor.fetchone()
            
            print("\n=== סטטיסטיקות ===")
            print(f"סך עובדים: {stats['total_employees']}")
            print(f"משכורת ממוצעת: ₪{stats['avg_salary']:,.2f}")
            print(f"משכורת מינימלית: ₪{stats['min_salary']:,.2f}")
            print(f"משכורת מקסימלית: ₪{stats['max_salary']:,.2f}")
            
            # לפי מחלקה
            cursor.execute("""
                SELECT 
                    department,
                    COUNT(*) as emp_count,
                    AVG(salary) as avg_salary
                FROM employees
                GROUP BY department
            """)
            
            print("\nלפי מחלקה:")
            for row in cursor:
                print(f"  {row['department']}: "
                      f"{row['emp_count']} עובדים, "
                      f"ממוצע ₪{row['avg_salary']:,.2f}")
            
        except Error as e:
            print(f"❌ שגיאה: {e}")
    
    def close(self):
        """סגור את החיבור"""
        if self.connection.is_connected():
            self.connection.close()
            print("✓ החיבור נסגר")

# דוגמת שימוש
if __name__ == "__main__":
    # צור מערכת
    manager = EmployeeManager(
        host="localhost",
        user="root",
        password="your_password",
        database="company"
    )
    
    # התחבר
    manager.connect()
    manager.create_table()
    
    # הוסף עובדים
    manager.add_employee("Danny Cohen", "Development", 15000)
    manager.add_employee("Sarah Levi", "Marketing", 12000)
    manager.add_employee("Yossi Abraham", "Development", 16000)
    manager.add_employee("Michal Israeli", "HR", 11000)
    
    # הצג כולם
    manager.show_all_employees()
    
    # חפש עובד
    manager.search_employee(1)
    
    # עדכן משכורת
    manager.update_salary(1, 17000)
    
    # הצג לפי מחלקה
    manager.employees_by_department("Development")
    
    # הצג סטטיסטיקות
    manager.get_statistics()
    
    # סגור חיבור
    manager.close()
```

---

## 📊 מדריך מהיר לפקודות

### התחברות
```python
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="database_name"
)
```

### יצירה
```python
cursor.execute("CREATE DATABASE database_name")
cursor.execute("CREATE TABLE table_name (id INT, name VARCHAR(100))")
```

### הוספה
```python
cursor.execute("INSERT INTO table_name (column) VALUES (%s)", (value,))
connection.commit()
```

### קריאה
```python
cursor.execute("SELECT * FROM table_name")
results = cursor.fetchall()
```

### עדכון
```python
cursor.execute("UPDATE table_name SET column = %s WHERE id = %s", (value, id))
connection.commit()
```

### מחיקה
```python
cursor.execute("DELETE FROM table_name WHERE id = %s", (id,))
connection.commit()
```

### סגירה
```python
cursor.close()
connection.close()
```

---

## ⚠️ טעויות נפוצות

### 1. שכחתי commit()
```python
# ❌ לא עובד - השינויים לא נשמרים
cursor.execute("INSERT INTO ...")
# חסר: connection.commit()

# ✅ נכון
cursor.execute("INSERT INTO ...")
connection.commit()
```

### 2. לא סגרתי את החיבור
```python
# ❌ זליגת חיבורים
connection = mysql.connector.connect(...)
# חסר: connection.close()

# ✅ נכון
try:
    connection = mysql.connector.connect(...)
    # עשה משהו
finally:
    connection.close()
```

### 3. SQL Injection (חור אבטחה!)
```python
# ❌ מסוכן מאוד!
name = input("הכנס שם: ")
cursor.execute(f"SELECT * FROM users WHERE name = '{name}'")

# ✅ בטוח
name = input("הכנס שם: ")
cursor.execute("SELECT * FROM users WHERE name = %s", (name,))
```

### 4. לא בדקתי אם התחבר
```python
# ❌ עלול לקרוס
connection = mysql.connector.connect(...)
cursor = connection.cursor()

# ✅ נכון
connection = mysql.connector.connect(...)
if connection.is_connected():
    cursor = connection.cursor()
```

---

## 💡 טיפים חשובים

### 1. תמיד השתמש ב-%s
```python
# ✅ נכון - מוגן מפני SQL Injection
cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
```

### 2. תמיד עשה commit() אחרי שינויים
```python
cursor.execute("INSERT/UPDATE/DELETE ...")
connection.commit()  # חובה!
```

### 3. השתמש ב-dictionary cursor לנוחות
```python
cursor = connection.cursor(dictionary=True)
# עכשיו: row['name'] במקום row[1]
```

### 4. סגור תמיד חיבורים
```python
try:
    # עבודה עם מסד נתונים
finally:
    connection.close()
```

### 5. טפל בשגיאות
```python
try:
    cursor.execute(...)
except mysql.connector.Error as e:
    print(f"שגיאה: {e}")
```

---

## 🎯 תרגילים לתרגול

### קל
1. צור מסד נתונים בשם "בית_ספר"
2. צור טבלת "תלמידים" עם: מזהה, שם, כיתה, ציון
3. הוסף 5 תלמידים
4. הצג את כולם

### בינוני
1. מצא את כל התלמידים בכיתה א'
2. חשב את ממוצע הציונים
3. עדכן ציון לתלמיד ספציפי
4. הצג את 3 התלמידים עם הציונים הגבוהים ביותר

### מתקדם
1. צור מערכת ניהול ספרייה עם טבלאות: ספרים, לקוחות, השאלות
2. הוסף אפשרות להשאיל והחזר ספר
3. הצג דוח של ספרים מושאלים
4. מצא לקוחות שלא החזירו ספרים

---

## 📚 משאבים נוספים

- [תיעוד MySQL Connector](https://dev.mysql.com/doc/connector-python/en/)
- [מדריך SQL בעברית](https://www.w3schools.com/sql/)
- [MySQL Workbench](https://www.mysql.com/products/workbench/) - כלי ויזואלי לניהול

---

**בהצלחה! 🚀**

כעת אתה יודע לעבוד עם MySQL ו-Python!
