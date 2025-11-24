# מדריך מהיר: CSV, SQL ו-MySQL למתחילים

## מה זה CSV?
CSV (Comma Separated Values) - קובץ טקסט פשוט שבו כל שורה מייצגת רשומה, והערכים מופרדים בפסיקים.

**דוגמה לקובץ CSV:**
```csv
id,name,age,city
1,דני,25,תל אביב
2,שרה,30,חיפה
3,יוסי,28,ירושלים
```

## מה זה SQL?
SQL (Structured Query Language) - שפה לניהול ושאילתות במסדי נתונים.

## מה זה MySQL?
MySQL - מערכת לניהול מסדי נתונים פופולרית ובחינם.

---

## התקנה מהירה

### 1. התקן MySQL
```bash
# הורד מהאתר הרשמי:
https://dev.mysql.com/downloads/mysql/
```

### 2. התקן Python ו-MySQL Connector
```bash
pip install mysql-connector-python
```

---

## דוגמה מעשית מלאה

### שלב 1: צור קובץ CSV
**employees.csv:**
```csv
id,name,position,salary
1,דוד כהן,מתכנת,15000
2,רחל לוי,מעצבת,12000
3,משה ישראלי,מנהל,20000
```

### שלב 2: צור טבלה ב-MySQL
```python
import mysql.connector

# התחבר ל-MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password"
)
cursor = conn.cursor()

# צור מסד נתונים
cursor.execute("CREATE DATABASE IF NOT EXISTS company")
cursor.execute("USE company")

# צור טבלה
cursor.execute("""
    CREATE TABLE IF NOT EXISTS employees (
        id INT PRIMARY KEY,
        name VARCHAR(100),
        position VARCHAR(100),
        salary INT
    )
""")

conn.commit()
cursor.close()
conn.close()
print("טבלה נוצרה בהצלחה!")
```

### שלב 3: העלה CSV ל-MySQL
```python
import csv
import mysql.connector

# התחבר למסד הנתונים
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password",
    database="company"
)
cursor = conn.cursor()

# קרא את קובץ ה-CSV והכנס לטבלה
with open('employees.csv', 'r', encoding='utf-8') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        cursor.execute("""
            INSERT INTO employees (id, name, position, salary)
            VALUES (%s, %s, %s, %s)
        """, (row['id'], row['name'], row['position'], row['salary']))

conn.commit()
cursor.close()
conn.close()
print("הנתונים הועלו בהצלחה!")
```

### שלב 4: שאילתות בסיסיות
```python
import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password",
    database="company"
)
cursor = conn.cursor()

# הצג את כל העובדים
cursor.execute("SELECT * FROM employees")
print("כל העובדים:")
for row in cursor.fetchall():
    print(row)

# הצג עובדים עם משכורת מעל 13000
cursor.execute("SELECT name, salary FROM employees WHERE salary > 13000")
print("\nעובדים עם משכורת מעל 13000:")
for row in cursor.fetchall():
    print(f"{row[0]}: {row[1]} ש״ח")

# עדכן משכורת
cursor.execute("UPDATE employees SET salary = 16000 WHERE name = 'דוד כהן'")
conn.commit()

# מחק עובד
cursor.execute("DELETE FROM employees WHERE id = 3")
conn.commit()

cursor.close()
conn.close()
```

---

## פקודות SQL בסיסיות

### SELECT - קריאת נתונים
```sql
SELECT * FROM employees;                    -- כל העובדים
SELECT name, salary FROM employees;         -- עמודות ספציפיות
SELECT * FROM employees WHERE salary > 15000;  -- עם תנאי
```

### INSERT - הוספת נתונים
```sql
INSERT INTO employees (id, name, position, salary)
VALUES (4, 'אנה', 'מנהלת פרויקטים', 18000);
```

### UPDATE - עדכון נתונים
```sql
UPDATE employees SET salary = 17000 WHERE id = 1;
```

### DELETE - מחיקת נתונים
```sql
DELETE FROM employees WHERE id = 2;
```

---

## ייצא מ-MySQL ל-CSV
```python
import csv
import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password",
    database="company"
)
cursor = conn.cursor()

# שלוף נתונים
cursor.execute("SELECT * FROM employees")
rows = cursor.fetchall()

# כתוב ל-CSV
with open('export_employees.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['id', 'name', 'position', 'salary'])  # כותרות
    writer.writerows(rows)

cursor.close()
conn.close()
print("הנתונים יוצאו ל-CSV!")
```

---

## טיפים חשובים

1. **תמיד סגור חיבורים:**
   ```python
   cursor.close()
   conn.close()
   ```

2. **השתמש ב-commit לשמירת שינויים:**
   ```python
   conn.commit()
   ```

3. **הגנה מפני SQL Injection:**
   ```python
   # נכון ✓
   cursor.execute("SELECT * FROM employees WHERE id = %s", (user_id,))
   
   # לא נכון ✗
   cursor.execute(f"SELECT * FROM employees WHERE id = {user_id}")
   ```

4. **טיפול בשגיאות:**
   ```python
   try:
       cursor.execute("SELECT * FROM employees")
       results = cursor.fetchall()
   except mysql.connector.Error as err:
       print(f"שגיאה: {err}")
   finally:
       cursor.close()
       conn.close()
   ```

---

## סיכום מהיר

| פעולה | כלי |
|-------|-----|
| אחסון נתונים פשוטים | CSV |
| שאילתות מורכבות | SQL |
| ניהול מסד נתונים | MySQL |
| חיבור Python ל-MySQL | mysql-connector-python |

**זרימת עבודה טיפוסית:**
1. צור/קרא קובץ CSV
2. התחבר ל-MySQL
3. צור טבלה
4. העלה נתונים מ-CSV
5. בצע שאילתות SQL
6. סגור חיבור

זהו! עכשיו אתה יכול להתחיל לעבוד עם CSV, SQL ו-MySQL בצורה מעשית.
