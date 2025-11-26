# מדריך OOP עם CSV ו-SQLite למתחילים

## תוכן עניינים
1. [מבוא](#מבוא)
2. [התקנה והכנה](#התקנה-והכנה)
3. [יסודות OOP בפייתון](#יסודות-oop-בפייתון)
4. [יצירת מחלקות בסיסיות](#יצירת-מחלקות-בסיסיות)
5. [עבודה עם CSV](#עבודה-עם-csv)
6. [עבודה עם SQLite](#עבודה-עם-sqlite)
7. [שילוב הכל ביחד](#שילוב-הכל-ביחד)
8. [תרגילים מעשיים](#תרגילים-מעשיים)

---

## מבוא

### מה זה OOP?
תכנות מונחה עצמים (Object-Oriented Programming) הוא גישה לתכנות שמארגנת קוד סביב **אובייקטים** ו**מחלקות**.

**יתרונות:**
- קוד מאורגן וקריא יותר
- קל לתחזוקה ושימוש חוזר
- מדמה את העולם האמיתי

### מה נלמד?
- איך ליצור מחלקות (Classes)
- איך לקרוא ולכתוב קבצי CSV
- איך לעבוד עם SQLite
- איך לשלב הכל לפרויקט שלם

---

## התקנה והכנה

### ספריות נדרשות
```bash
# אין צורך להתקין - כל הספריות מובנות בפייתון
```

### ספריות שנשתמש בהן:
```python
import csv        # לעבודה עם קבצי CSV
import sqlite3    # לעבודה עם מסד נתונים SQLite
from typing import List, Optional  # לסוגי נתונים
```

---

## יסודות OOP בפייתון

### 1. מחלקה פשוטה (Class)

```python
class Student:
    """מחלקה שמייצגת סטודנט"""
    
    def __init__(self, name, age, grade):
        """פונקציית בנאי - רצה כשיוצרים אובייקט חדש"""
        self.name = name      # שם הסטודנט
        self.age = age        # גיל
        self.grade = grade    # ציון
    
    def display_info(self):
        """מציג את פרטי הסטודנט"""
        print(f"שם: {self.name}, גיל: {self.age}, ציון: {self.grade}")
    
    def is_passed(self):
        """בודק אם הסטודנט עבר"""
        return self.grade >= 60
```

### 2. שימוש במחלקה

```python
# יצירת אובייקט
student1 = Student("יוסי", 20, 85)

# שימוש במתודות
student1.display_info()  # שם: יוסי, גיל: 20, ציון: 85
print(student1.is_passed())  # True
```

### 3. מושגי יסוד חשובים

**Attributes (תכונות):**
```python
self.name = name  # תכונה של האובייקט
```

**Methods (מתודות):**
```python
def display_info(self):  # פונקציה של המחלקה
    pass
```

**Constructor (בנאי):**
```python
def __init__(self):  # מתבצע בעת יצירת אובייקט
    pass
```

---

## יצירת מחלקות בסיסיות

### דוגמה 1: מחלקת תלמיד מלאה

```python
class Student:
    """מחלקה מלאה לניהול סטודנט"""
    
    # משתנה סטטי - משותף לכל הסטודנטים
    total_students = 0
    
    def __init__(self, student_id, name, age, grade):
        self.student_id = student_id
        self.name = name
        self.age = age
        self.grade = grade
        Student.total_students += 1
    
    def __str__(self):
        """מחזיר ייצוג טקסט של האובייקט"""
        return f"Student({self.student_id}, {self.name}, {self.grade})"
    
    def __repr__(self):
        """מחזיר ייצוג טכני של האובייקט"""
        return f"Student(id={self.student_id}, name='{self.name}', age={self.age}, grade={self.grade})"
    
    def to_dict(self):
        """המר לדיקשנרי"""
        return {
            'student_id': self.student_id,
            'name': self.name,
            'age': self.age,
            'grade': self.grade
        }
    
    @classmethod
    def from_dict(cls, data):
        """יצירת אובייקט מדיקשנרי"""
        return cls(
            data['student_id'],
            data['name'],
            data['age'],
            data['grade']
        )
    
    def update_grade(self, new_grade):
        """עדכון ציון"""
        if 0 <= new_grade <= 100:
            self.grade = new_grade
            return True
        return False
```

### שימוש:

```python
# יצירת סטודנט
student = Student(1, "דני", 22, 88)

# הדפסה
print(student)  # Student(1, דני, 88)

# המרה לדיקשנרי
data = student.to_dict()
print(data)  # {'student_id': 1, 'name': 'דני', ...}

# יצירה מדיקשנרי
new_student = Student.from_dict(data)

# עדכון ציון
student.update_grade(95)
```

---

## עבודה עם CSV

### מחלקה לניהול CSV

```python
import csv
from typing import List

class CSVManager:
    """מחלקה לניהול קבצי CSV"""
    
    def __init__(self, filename):
        self.filename = filename
    
    def write_students(self, students: List[Student]):
        """כתיבת רשימת סטודנטים ל-CSV"""
        with open(self.filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['student_id', 'name', 'age', 'grade'])
            writer.writeheader()  # כתיבת שורת כותרת
            
            for student in students:
                writer.writerow(student.to_dict())
    
    def read_students(self) -> List[Student]:
        """קריאת סטודנטים מ-CSV"""
        students = []
        
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                for row in reader:
                    student = Student(
                        int(row['student_id']),
                        row['name'],
                        int(row['age']),
                        float(row['grade'])
                    )
                    students.append(student)
        
        except FileNotFoundError:
            print(f"הקובץ {self.filename} לא נמצא")
        
        return students
    
    def append_student(self, student: Student):
        """הוספת סטודנט לקובץ קיים"""
        with open(self.filename, 'a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['student_id', 'name', 'age', 'grade'])
            writer.writerow(student.to_dict())
```

### דוגמת שימוש:

```python
# יצירת סטודנטים
students = [
    Student(1, "אבי", 20, 85),
    Student(2, "בני", 21, 92),
    Student(3, "גלי", 19, 78)
]

# כתיבה ל-CSV
csv_manager = CSVManager('students.csv')
csv_manager.write_students(students)

# קריאה מ-CSV
loaded_students = csv_manager.read_students()
for student in loaded_students:
    print(student)

# הוספת סטודנט
new_student = Student(4, "דנה", 22, 88)
csv_manager.append_student(new_student)
```

---

## עבודה עם SQLite

### מחלקה לניהול SQLite

```python
import sqlite3
from typing import List, Optional

class DatabaseManager:
    """מחלקה לניהול מסד נתונים SQLite"""
    
    def __init__(self, db_name='students.db'):
        self.db_name = db_name
        self.connection = None
        self.cursor = None
    
    def connect(self):
        """התחברות למסד נתונים"""
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
    
    def disconnect(self):
        """ניתוק ממסד נתונים"""
        if self.connection:
            self.connection.close()
    
    def create_table(self):
        """יצירת טבלת סטודנטים"""
        query = """
        CREATE TABLE IF NOT EXISTS students (
            student_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER,
            grade REAL
        )
        """
        self.cursor.execute(query)
        self.connection.commit()
    
    def insert_student(self, student: Student):
        """הוספת סטודנט למסד נתונים"""
        query = """
        INSERT INTO students (student_id, name, age, grade)
        VALUES (?, ?, ?, ?)
        """
        self.cursor.execute(query, (
            student.student_id,
            student.name,
            student.age,
            student.grade
        ))
        self.connection.commit()
    
    def insert_many_students(self, students: List[Student]):
        """הוספת מספר סטודנטים"""
        query = """
        INSERT INTO students (student_id, name, age, grade)
        VALUES (?, ?, ?, ?)
        """
        data = [(s.student_id, s.name, s.age, s.grade) for s in students]
        self.cursor.executemany(query, data)
        self.connection.commit()
    
    def get_all_students(self) -> List[Student]:
        """קבלת כל הסטודנטים"""
        query = "SELECT * FROM students"
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        
        students = []
        for row in rows:
            student = Student(row[0], row[1], row[2], row[3])
            students.append(student)
        
        return students
    
    def get_student_by_id(self, student_id: int) -> Optional[Student]:
        """קבלת סטודנט לפי ID"""
        query = "SELECT * FROM students WHERE student_id = ?"
        self.cursor.execute(query, (student_id,))
        row = self.cursor.fetchone()
        
        if row:
            return Student(row[0], row[1], row[2], row[3])
        return None
    
    def update_student(self, student: Student):
        """עדכון סטודנט"""
        query = """
        UPDATE students 
        SET name = ?, age = ?, grade = ?
        WHERE student_id = ?
        """
        self.cursor.execute(query, (
            student.name,
            student.age,
            student.grade,
            student.student_id
        ))
        self.connection.commit()
    
    def delete_student(self, student_id: int):
        """מחיקת סטודנט"""
        query = "DELETE FROM students WHERE student_id = ?"
        self.cursor.execute(query, (student_id,))
        self.connection.commit()
    
    def get_students_by_grade(self, min_grade: float) -> List[Student]:
        """קבלת סטודנטים לפי ציון מינימלי"""
        query = "SELECT * FROM students WHERE grade >= ?"
        self.cursor.execute(query, (min_grade,))
        rows = self.cursor.fetchall()
        
        return [Student(row[0], row[1], row[2], row[3]) for row in rows]
```

### דוגמת שימוש:

```python
# התחברות
db = DatabaseManager('students.db')
db.connect()

# יצירת טבלה
db.create_table()

# הוספת סטודנט
student = Student(1, "משה", 23, 90)
db.insert_student(student)

# הוספת מספר סטודנטים
students = [
    Student(2, "שרה", 21, 85),
    Student(3, "יעל", 22, 95)
]
db.insert_many_students(students)

# שליפת כל הסטודנטים
all_students = db.get_all_students()
for s in all_students:
    print(s)

# שליפת סטודנט ספציפי
student = db.get_student_by_id(1)
print(student)

# עדכון
student.grade = 95
db.update_student(student)

# מחיקה
db.delete_student(3)

# ניתוק
db.disconnect()
```

---

## שילוב הכל ביחד

### מערכת שלמה לניהול סטודנטים

```python
import csv
import sqlite3
from typing import List, Optional

class Student:
    """מחלקת סטודנט"""
    
    def __init__(self, student_id, name, age, grade):
        self.student_id = student_id
        self.name = name
        self.age = age
        self.grade = grade
    
    def __str__(self):
        return f"Student(ID: {self.student_id}, Name: {self.name}, Age: {self.age}, Grade: {self.grade})"
    
    def to_dict(self):
        return {
            'student_id': self.student_id,
            'name': self.name,
            'age': self.age,
            'grade': self.grade
        }


class StudentManager:
    """מחלקה מרכזית לניהול סטודנטים עם CSV ו-SQLite"""
    
    def __init__(self, csv_file='students.csv', db_file='students.db'):
        self.csv_file = csv_file
        self.db_file = db_file
        self.connection = None
        self.cursor = None
    
    # ======= פונקציות מסד נתונים =======
    
    def connect_db(self):
        """התחברות למסד נתונים"""
        self.connection = sqlite3.connect(self.db_file)
        self.cursor = self.connection.cursor()
    
    def disconnect_db(self):
        """ניתוק ממסד נתונים"""
        if self.connection:
            self.connection.close()
    
    def create_table(self):
        """יצירת טבלה"""
        query = """
        CREATE TABLE IF NOT EXISTS students (
            student_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER,
            grade REAL
        )
        """
        self.cursor.execute(query)
        self.connection.commit()
    
    # ======= פונקציות CSV =======
    
    def export_to_csv(self):
        """ייצוא מסד נתונים ל-CSV"""
        query = "SELECT * FROM students"
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        
        with open(self.csv_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['student_id', 'name', 'age', 'grade'])
            writer.writerows(rows)
        
        print(f"✅ נתונים יוצאו ל-{self.csv_file}")
    
    def import_from_csv(self):
        """ייבוא נתונים מ-CSV למסד נתונים"""
        try:
            with open(self.csv_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                for row in reader:
                    student = Student(
                        int(row['student_id']),
                        row['name'],
                        int(row['age']),
                        float(row['grade'])
                    )
                    self.add_student(student)
            
            print(f"✅ נתונים יובאו מ-{self.csv_file}")
        
        except FileNotFoundError:
            print(f"❌ הקובץ {self.csv_file} לא נמצא")
    
    # ======= CRUD Operations =======
    
    def add_student(self, student: Student):
        """הוספת סטודנט (Create)"""
        query = """
        INSERT OR REPLACE INTO students (student_id, name, age, grade)
        VALUES (?, ?, ?, ?)
        """
        self.cursor.execute(query, (
            student.student_id,
            student.name,
            student.age,
            student.grade
        ))
        self.connection.commit()
        print(f"✅ סטודנט {student.name} נוסף בהצלחה")
    
    def get_all_students(self) -> List[Student]:
        """קבלת כל הסטודנטים (Read)"""
        query = "SELECT * FROM students"
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        
        return [Student(row[0], row[1], row[2], row[3]) for row in rows]
    
    def get_student(self, student_id: int) -> Optional[Student]:
        """קבלת סטודנט בודד (Read)"""
        query = "SELECT * FROM students WHERE student_id = ?"
        self.cursor.execute(query, (student_id,))
        row = self.cursor.fetchone()
        
        if row:
            return Student(row[0], row[1], row[2], row[3])
        return None
    
    def update_student(self, student: Student):
        """עדכון סטודנט (Update)"""
        query = """
        UPDATE students 
        SET name = ?, age = ?, grade = ?
        WHERE student_id = ?
        """
        self.cursor.execute(query, (
            student.name,
            student.age,
            student.grade,
            student.student_id
        ))
        self.connection.commit()
        print(f"✅ סטודנט {student.name} עודכן בהצלחה")
    
    def delete_student(self, student_id: int):
        """מחיקת סטודנט (Delete)"""
        query = "DELETE FROM students WHERE student_id = ?"
        self.cursor.execute(query, (student_id,))
        self.connection.commit()
        print(f"✅ סטודנט עם ID {student_id} נמחק")
    
    # ======= פונקציות עזר =======
    
    def display_all_students(self):
        """הצגת כל הסטודנטים"""
        students = self.get_all_students()
        
        if not students:
            print("אין סטודנטים במערכת")
            return
        
        print("\n" + "="*60)
        print("רשימת סטודנטים:")
        print("="*60)
        for student in students:
            print(student)
        print("="*60 + "\n")
    
    def get_statistics(self):
        """סטטיסטיקות"""
        students = self.get_all_students()
        
        if not students:
            print("אין נתונים")
            return
        
        grades = [s.grade for s in students]
        
        print("\n" + "="*40)
        print("סטטיסטיקות:")
        print("="*40)
        print(f"מספר סטודנטים: {len(students)}")
        print(f"ציון ממוצע: {sum(grades) / len(grades):.2f}")
        print(f"ציון מקסימלי: {max(grades)}")
        print(f"ציון מינימלי: {min(grades)}")
        print("="*40 + "\n")


def main():
    """תוכנית ראשית"""
    
    # יצירת מנהל סטודנטים
    manager = StudentManager()
    
    # התחברות למסד נתונים
    manager.connect_db()
    manager.create_table()
    
    # הוספת סטודנטים
    students = [
        Student(1, "אבי כהן", 20, 85),
        Student(2, "בת-שבע לוי", 21, 92),
        Student(3, "גיל מזרחי", 19, 78),
        Student(4, "דנה ישראלי", 22, 88),
        Student(5, "הדר חכים", 20, 95)
    ]
    
    for student in students:
        manager.add_student(student)
    
    # הצגת כל הסטודנטים
    manager.display_all_students()
    
    # ייצוא ל-CSV
    manager.export_to_csv()
    
    # עדכון סטודנט
    student = manager.get_student(1)
    if student:
        student.grade = 90
        manager.update_student(student)
    
    # סטטיסטיקות
    manager.get_statistics()
    
    # ניתוק
    manager.disconnect_db()
    
    print("✅ התוכנית הסתיימה בהצלחה!")


if __name__ == "__main__":
    main()
```

### הרצת התוכנית:

```bash
python student_management_system.py
```

### פלט לדוגמה:

```
✅ סטודנט אבי כהן נוסף בהצלחה
✅ סטודנט בת-שבע לוי נוסף בהצלחה
...

============================================================
רשימת סטודנטים:
============================================================
Student(ID: 1, Name: אבי כהן, Age: 20, Grade: 85)
Student(ID: 2, Name: בת-שבע לוי, Age: 21, Grade: 92)
...
============================================================

✅ נתונים יוצאו ל-students.csv
✅ סטודנט אבי כהן עודכן בהצלחה

========================================
סטטיסטיקות:
========================================
מספר סטודנטים: 5
ציון ממוצע: 87.60
ציון מקסימלי: 95
ציון מינימלי: 78
========================================

✅ התוכנית הסתיימה בהצלחה!
```

---

## תרגילים מעשיים

### תרגיל 1: מערכת ניהול ספרים

צור מערכת לניהול ספרים עם:
- מחלקת `Book` (מזהה, שם, מחבר, שנה, מחיר)
- מחלקת `BookManager` לניהול CSV ו-SQLite
- פונקציות CRUD
- חיפוש לפי מחבר
- סינון לפי טווח מחירים

```python
class Book:
    def __init__(self, book_id, title, author, year, price):
        # הוסף את הקוד שלך כאן
        pass

class BookManager:
    def __init__(self, csv_file='books.csv', db_file='books.db'):
        # הוסף את הקוד שלך כאן
        pass
    
    def add_book(self, book):
        # הוסף את הקוד שלך כאן
        pass
    
    def search_by_author(self, author):
        # הוסף את הקוד שלך כאן
        pass
```

### תרגיל 2: מערכת ניהול משימות

צור מערכת TODO עם:
- מחלקת `Task` (מזהה, כותרת, תיאור, סטטוס, תאריך יעד)
- שמירה ב-CSV ו-SQLite
- סינון משימות לפי סטטוס
- עדכון סטטוס משימה
- מחיקת משימות שהושלמו

### תרגיל 3: מערכת ניהול עובדים

צור מערכת HR עם:
- מחלקת `Employee` (מזהה, שם, תפקיד, משכורת, מחלקה)
- חישוב משכורת ממוצעת למחלקה
- העלאת שכר לעובד
- דוח עובדים למחלקה
- ייצוא לדוח Excel (CSV)

---

## טיפים וטריקים

### 1. שימוש ב-Context Manager

```python
class DatabaseManager:
    def __enter__(self):
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

# שימוש:
with DatabaseManager() as db:
    db.create_table()
    # הקוד שלך
# הניתוק אוטומטי!
```

### 2. Validation במחלקה

```python
class Student:
    def __init__(self, student_id, name, age, grade):
        if not isinstance(student_id, int):
            raise ValueError("ID חייב להיות מספר שלם")
        
        if not 0 <= grade <= 100:
            raise ValueError("ציון חייב להיות בין 0 ל-100")
        
        self.student_id = student_id
        self.name = name
        self.age = age
        self.grade = grade
```

### 3. Logging

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StudentManager:
    def add_student(self, student):
        logger.info(f"מוסיף סטודנט: {student.name}")
        # קוד...
        logger.info("סטודנט נוסף בהצלחה")
```

### 4. טיפול בשגיאות

```python
def get_student(self, student_id):
    try:
        query = "SELECT * FROM students WHERE student_id = ?"
        self.cursor.execute(query, (student_id,))
        row = self.cursor.fetchone()
        
        if row:
            return Student(*row)
        else:
            raise ValueError(f"סטודנט עם ID {student_id} לא נמצא")
    
    except sqlite3.Error as e:
        print(f"שגיאת מסד נתונים: {e}")
        return None
```

---

## סיכום

### מה למדנו?

✅ יסודות OOP בפייתון  
✅ יצירת מחלקות ומתודות  
✅ קריאה וכתיבה ל-CSV  
✅ עבודה עם SQLite  
✅ שילוב CSV ו-SQLite במערכת אחת  
✅ CRUD Operations  
✅ ארגון קוד מקצועי  

### המשך לימוד מומלץ

1. **Inheritance** - הורשה בין מחלקות
2. **Polymorphism** - פולימורפיזם
3. **Design Patterns** - תבניות עיצוב
4. **SQLAlchemy** - ORM מתקדם
5. **Pandas** - ניתוח נתונים
6. **FastAPI** - בניית API

---

## משאבים נוספים

- [Python OOP Documentation](https://docs.python.org/3/tutorial/classes.html)
- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [CSV Module Documentation](https://docs.python.org/3/library/csv.html)

---

**בהצלחה! 🚀**
