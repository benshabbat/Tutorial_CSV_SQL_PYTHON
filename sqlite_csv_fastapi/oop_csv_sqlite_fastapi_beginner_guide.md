# מדריך מקיף: OOP, CSV, SQLite ו-FastAPI לרמה מתחילה

## תוכן עניינים
1. [הקדמה](#הקדמה)
2. [התקנת הסביבה](#התקנת-הסביבה)
3. [חלק 1: עבודה עם CSV באמצעות OOP](#חלק-1-עבודה-עם-csv-באמצעות-oop)
4. [חלק 2: SQLite עם OOP](#חלק-2-sqlite-עם-oop)
5. [חלק 3: העברת נתונים מ-CSV ל-SQLite](#חלק-3-העברת-נתונים-מ-csv-ל-sqlite)
6. [חלק 4: בניית API עם FastAPI](#חלק-4-בניית-api-עם-fastapi)
7. [חלק 5: פרויקט מלא](#חלק-5-פרויקט-מלא)

---

## הקדמה

### מה נלמד במדריך?
- **OOP (Object-Oriented Programming)**: תכנות מונחה עצמים
- **CSV**: קבצי טקסט לאחסון נתונים בפורמט טבלאי
- **SQLite**: מסד נתונים קל ומהיר
- **FastAPI**: פריימוורק מודרני לבניית API

### מושגי יסוד ב-OOP
- **Class (מחלקה)**: תבנית ליצירת אובייקטים
- **Object (אובייקט)**: מופע של מחלקה
- **Attributes (תכונות)**: משתנים בתוך אובייקט
- **Methods (מתודות)**: פונקציות בתוך מחלקה
- **Encapsulation (אינקפסולציה)**: הסתרת פרטים פנימיים
- **Inheritance (ירושה)**: יצירת מחלקות מבוססות על מחלקות קיימות

---

## התקנת הסביבה

### שלב 1: וידוא התקנת Python
```bash
python --version
```

### שלב 2: התקנת הספריות הנדרשות
```bash
pip install fastapi uvicorn
```

---

## חלק 1: עבודה עם CSV באמצעות OOP

### שלב 1.1: הבנת מבנה קובץ CSV

קובץ CSV (Comma-Separated Values) הוא קובץ טקסט שבו כל שורה מייצגת רשומה, והערכים מופרדים בפסיקים.

**דוגמה לקובץ students.csv:**
```csv
id,name,age,grade
1,דני,20,85
2,רונית,22,90
3,יוסי,21,78
```

### שלב 1.2: יצירת מחלקה לניהול תלמיד

```python
# student.py
class Student:
    """מחלקה המייצגת תלמיד"""
    
    def __init__(self, id: int, name: str, age: int, grade: float):
        """
        בנאי המחלקה - יוצר תלמיד חדש
        
        Args:
            id: מספר מזהה של התלמיד
            name: שם התלמיד
            age: גיל התלמיד
            grade: ציון התלמיד
        """
        self.id = id
        self.name = name
        self.age = age
        self.grade = grade
    
    def __str__(self):
        """מחזיר ייצוג טקסטואלי של התלמיד"""
        return f"תלמיד {self.name} (ID: {self.id}), גיל: {self.age}, ציון: {self.grade}"
    
    def __repr__(self):
        """מחזיר ייצוג טכני של התלמיד"""
        return f"Student(id={self.id}, name='{self.name}', age={self.age}, grade={self.grade})"
    
    def is_passing(self, passing_grade: float = 60) -> bool:
        """
        בודק אם התלמיד עבר
        
        Args:
            passing_grade: ציון המינימום למעבר (ברירת מחדל: 60)
            
        Returns:
            True אם התלמיד עבר, False אחרת
        """
        return self.grade >= passing_grade
    
    def to_dict(self) -> dict:
        """
        ממיר את התלמיד למילון
        
        Returns:
            מילון עם פרטי התלמיד
        """
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'grade': self.grade
        }
```

### שלב 1.3: יצירת מחלקה לניהול CSV

```python
# csv_manager.py
import csv
from typing import List
from student import Student

class CSVManager:
    """מחלקה לניהול קבצי CSV"""
    
    def __init__(self, filename: str):
        """
        בנאי המחלקה
        
        Args:
            filename: שם קובץ ה-CSV
        """
        self.filename = filename
    
    def read_students(self) -> List[Student]:
        """
        קורא תלמידים מקובץ CSV
        
        Returns:
            רשימת אובייקטי Student
        """
        students = []
        
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file)
                
                for row in csv_reader:
                    student = Student(
                        id=int(row['id']),
                        name=row['name'],
                        age=int(row['age']),
                        grade=float(row['grade'])
                    )
                    students.append(student)
            
            print(f"✓ נקראו {len(students)} תלמידים מהקובץ {self.filename}")
            
        except FileNotFoundError:
            print(f"✗ הקובץ {self.filename} לא נמצא")
        except Exception as e:
            print(f"✗ שגיאה בקריאת הקובץ: {e}")
        
        return students
    
    def write_students(self, students: List[Student]) -> bool:
        """
        כותב תלמידים לקובץ CSV
        
        Args:
            students: רשימת אובייקטי Student
            
        Returns:
            True אם הכתיבה הצליחה, False אחרת
        """
        try:
            with open(self.filename, 'w', encoding='utf-8', newline='') as file:
                fieldnames = ['id', 'name', 'age', 'grade']
                csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
                
                csv_writer.writeheader()
                
                for student in students:
                    csv_writer.writerow(student.to_dict())
            
            print(f"✓ נכתבו {len(students)} תלמידים לקובץ {self.filename}")
            return True
            
        except Exception as e:
            print(f"✗ שגיאה בכתיבת הקובץ: {e}")
            return False
    
    def append_student(self, student: Student) -> bool:
        """
        מוסיף תלמיד לקובץ CSV קיים
        
        Args:
            student: אובייקט Student להוספה
            
        Returns:
            True אם ההוספה הצליחה, False אחרת
        """
        try:
            with open(self.filename, 'a', encoding='utf-8', newline='') as file:
                fieldnames = ['id', 'name', 'age', 'grade']
                csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
                csv_writer.writerow(student.to_dict())
            
            print(f"✓ התלמיד {student.name} נוסף בהצלחה")
            return True
            
        except Exception as e:
            print(f"✗ שגיאה בהוספת התלמיד: {e}")
            return False
```

### שלב 1.4: דוגמה לשימוש

```python
# example_csv_usage.py
from student import Student
from csv_manager import CSVManager

def main():
    # יצירת מנהל CSV
    csv_manager = CSVManager('students.csv')
    
    # קריאת תלמידים מהקובץ
    students = csv_manager.read_students()
    
    # הצגת כל התלמידים
    print("\n=== רשימת תלמידים ===")
    for student in students:
        print(student)
        print(f"  עבר את הקורס: {'כן' if student.is_passing() else 'לא'}")
    
    # חישוב ממוצע
    if students:
        average = sum(s.grade for s in students) / len(students)
        print(f"\nממוצע הכיתה: {average:.2f}")
    
    # הוספת תלמיד חדש
    new_student = Student(id=4, name='מיכל', age=23, grade=88)
    csv_manager.append_student(new_student)

if __name__ == "__main__":
    main()
```

---

## חלק 2: SQLite עם OOP

### שלב 2.1: הבנת SQLite

SQLite הוא מסד נתונים:
- **קל משקל**: לא דורש שרת נפרד
- **מהיר**: מתאים לפרויקטים קטנים ובינוניים
- **מובנה ב-Python**: אין צורך בהתקנות נוספות

### שלב 2.2: יצירת מחלקה לניהול מסד הנתונים

```python
# database_manager.py
import sqlite3
from typing import List, Optional
from student import Student

class DatabaseManager:
    """מחלקה לניהול מסד נתונים SQLite"""
    
    def __init__(self, db_name: str = "students.db"):
        """
        בנאי המחלקה
        
        Args:
            db_name: שם קובץ מסד הנתונים
        """
        self.db_name = db_name
        self.connection = None
        self.cursor = None
    
    def connect(self):
        """יצירת חיבור למסד הנתונים"""
        try:
            self.connection = sqlite3.connect(self.db_name)
            self.cursor = self.connection.cursor()
            print(f"✓ התחברות מוצלחת למסד הנתונים {self.db_name}")
        except sqlite3.Error as e:
            print(f"✗ שגיאה בהתחברות למסד הנתונים: {e}")
    
    def disconnect(self):
        """סגירת החיבור למסד הנתונים"""
        if self.connection:
            self.connection.close()
            print("✓ החיבור למסד הנתונים נסגר")
    
    def create_table(self):
        """יצירת טבלת תלמידים"""
        try:
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    age INTEGER NOT NULL,
                    grade REAL NOT NULL
                )
            ''')
            self.connection.commit()
            print("✓ טבלת students נוצרה בהצלחה")
        except sqlite3.Error as e:
            print(f"✗ שגיאה ביצירת הטבלה: {e}")
    
    def insert_student(self, student: Student) -> bool:
        """
        הוספת תלמיד למסד הנתונים
        
        Args:
            student: אובייקט Student להוספה
            
        Returns:
            True אם ההוספה הצליחה, False אחרת
        """
        try:
            self.cursor.execute('''
                INSERT INTO students (id, name, age, grade)
                VALUES (?, ?, ?, ?)
            ''', (student.id, student.name, student.age, student.grade))
            
            self.connection.commit()
            print(f"✓ התלמיד {student.name} נוסף למסד הנתונים")
            return True
            
        except sqlite3.IntegrityError:
            print(f"✗ תלמיד עם ID {student.id} כבר קיים")
            return False
        except sqlite3.Error as e:
            print(f"✗ שגיאה בהוספת התלמיד: {e}")
            return False
    
    def get_all_students(self) -> List[Student]:
        """
        קבלת כל התלמידים ממסד הנתונים
        
        Returns:
            רשימת אובייקטי Student
        """
        try:
            self.cursor.execute('SELECT id, name, age, grade FROM students')
            rows = self.cursor.fetchall()
            
            students = [
                Student(id=row[0], name=row[1], age=row[2], grade=row[3])
                for row in rows
            ]
            
            print(f"✓ נמצאו {len(students)} תלמידים במסד הנתונים")
            return students
            
        except sqlite3.Error as e:
            print(f"✗ שגיאה בקבלת התלמידים: {e}")
            return []
    
    def get_student_by_id(self, student_id: int) -> Optional[Student]:
        """
        חיפוש תלמיד לפי ID
        
        Args:
            student_id: מזהה התלמיד
            
        Returns:
            אובייקט Student אם נמצא, None אחרת
        """
        try:
            self.cursor.execute(
                'SELECT id, name, age, grade FROM students WHERE id = ?',
                (student_id,)
            )
            row = self.cursor.fetchone()
            
            if row:
                student = Student(id=row[0], name=row[1], age=row[2], grade=row[3])
                print(f"✓ נמצא תלמיד: {student.name}")
                return student
            else:
                print(f"✗ תלמיד עם ID {student_id} לא נמצא")
                return None
                
        except sqlite3.Error as e:
            print(f"✗ שגיאה בחיפוש התלמיד: {e}")
            return None
    
    def update_student(self, student: Student) -> bool:
        """
        עדכון פרטי תלמיד
        
        Args:
            student: אובייקט Student עם הנתונים המעודכנים
            
        Returns:
            True אם העדכון הצליח, False אחרת
        """
        try:
            self.cursor.execute('''
                UPDATE students
                SET name = ?, age = ?, grade = ?
                WHERE id = ?
            ''', (student.name, student.age, student.grade, student.id))
            
            self.connection.commit()
            
            if self.cursor.rowcount > 0:
                print(f"✓ התלמיד עם ID {student.id} עודכן בהצלחה")
                return True
            else:
                print(f"✗ תלמיד עם ID {student.id} לא נמצא")
                return False
                
        except sqlite3.Error as e:
            print(f"✗ שגיאה בעדכון התלמיד: {e}")
            return False
    
    def delete_student(self, student_id: int) -> bool:
        """
        מחיקת תלמיד
        
        Args:
            student_id: מזהה התלמיד למחיקה
            
        Returns:
            True אם המחיקה הצליחה, False אחרת
        """
        try:
            self.cursor.execute('DELETE FROM students WHERE id = ?', (student_id,))
            self.connection.commit()
            
            if self.cursor.rowcount > 0:
                print(f"✓ התלמיד עם ID {student_id} נמחק בהצלחה")
                return True
            else:
                print(f"✗ תלמיד עם ID {student_id} לא נמצא")
                return False
                
        except sqlite3.Error as e:
            print(f"✗ שגיאה במחיקת התלמיד: {e}")
            return False
    
    def get_students_by_min_grade(self, min_grade: float) -> List[Student]:
        """
        קבלת תלמידים עם ציון מינימלי
        
        Args:
            min_grade: ציון מינימלי
            
        Returns:
            רשימת תלמידים
        """
        try:
            self.cursor.execute(
                'SELECT id, name, age, grade FROM students WHERE grade >= ?',
                (min_grade,)
            )
            rows = self.cursor.fetchall()
            
            students = [
                Student(id=row[0], name=row[1], age=row[2], grade=row[3])
                for row in rows
            ]
            
            print(f"✓ נמצאו {len(students)} תלמידים עם ציון מעל {min_grade}")
            return students
            
        except sqlite3.Error as e:
            print(f"✗ שגיאה בחיפוש התלמידים: {e}")
            return []
```

### שלב 2.3: דוגמה לשימוש במסד הנתונים

```python
# example_database_usage.py
from student import Student
from database_manager import DatabaseManager

def main():
    # יצירת מנהל מסד נתונים
    db = DatabaseManager("students.db")
    
    # התחברות ויצירת טבלה
    db.connect()
    db.create_table()
    
    # הוספת תלמידים
    print("\n=== הוספת תלמידים ===")
    students = [
        Student(1, "דני", 20, 85),
        Student(2, "רונית", 22, 90),
        Student(3, "יוסי", 21, 78),
        Student(4, "מיכל", 23, 88)
    ]
    
    for student in students:
        db.insert_student(student)
    
    # קבלת כל התלמידים
    print("\n=== כל התלמידים ===")
    all_students = db.get_all_students()
    for student in all_students:
        print(student)
    
    # חיפוש תלמיד לפי ID
    print("\n=== חיפוש תלמיד ===")
    student = db.get_student_by_id(2)
    if student:
        print(student)
    
    # עדכון תלמיד
    print("\n=== עדכון תלמיד ===")
    if student:
        student.grade = 95
        db.update_student(student)
    
    # חיפוש תלמידים עם ציון גבוה
    print("\n=== תלמידים מצטיינים ===")
    top_students = db.get_students_by_min_grade(85)
    for student in top_students:
        print(student)
    
    # מחיקת תלמיד
    print("\n=== מחיקת תלמיד ===")
    db.delete_student(3)
    
    # סגירת החיבור
    db.disconnect()

if __name__ == "__main__":
    main()
```

---

## חלק 3: העברת נתונים מ-CSV ל-SQLite

### שלב 3.1: מחלקה לניהול המרת נתונים

```python
# data_migrator.py
from csv_manager import CSVManager
from database_manager import DatabaseManager

class DataMigrator:
    """מחלקה להעברת נתונים מ-CSV למסד נתונים"""
    
    def __init__(self, csv_filename: str, db_name: str = "students.db"):
        """
        בנאי המחלקה
        
        Args:
            csv_filename: שם קובץ ה-CSV
            db_name: שם מסד הנתונים
        """
        self.csv_manager = CSVManager(csv_filename)
        self.db_manager = DatabaseManager(db_name)
    
    def migrate_csv_to_db(self) -> bool:
        """
        מעביר נתונים מ-CSV למסד נתונים
        
        Returns:
            True אם ההעברה הצליחה, False אחרת
        """
        print("=== התחלת העברת נתונים ===\n")
        
        # קריאת נתונים מ-CSV
        students = self.csv_manager.read_students()
        
        if not students:
            print("✗ לא נמצאו תלמידים להעברה")
            return False
        
        # התחברות למסד נתונים
        self.db_manager.connect()
        self.db_manager.create_table()
        
        # הוספת התלמידים למסד הנתונים
        success_count = 0
        for student in students:
            if self.db_manager.insert_student(student):
                success_count += 1
        
        # סגירת החיבור
        self.db_manager.disconnect()
        
        print(f"\n✓ העברה הושלמה: {success_count}/{len(students)} תלמידים הועברו")
        return success_count > 0
    
    def migrate_db_to_csv(self) -> bool:
        """
        מעביר נתונים ממסד נתונים ל-CSV
        
        Returns:
            True אם ההעברה הצליחה, False אחרת
        """
        print("=== התחלת העברת נתונים ממסד נתונים ל-CSV ===\n")
        
        # קבלת נתונים ממסד הנתונים
        self.db_manager.connect()
        students = self.db_manager.get_all_students()
        self.db_manager.disconnect()
        
        if not students:
            print("✗ לא נמצאו תלמידים להעברה")
            return False
        
        # כתיבה ל-CSV
        success = self.csv_manager.write_students(students)
        
        if success:
            print(f"✓ {len(students)} תלמידים הועברו בהצלחה ל-CSV")
        
        return success
```

### שלב 3.2: דוגמה לשימוש

```python
# example_migration.py
from data_migrator import DataMigrator

def main():
    # יצירת מעביר נתונים
    migrator = DataMigrator('students.csv', 'students.db')
    
    # העברה מ-CSV למסד נתונים
    print("=== העברה מ-CSV למסד נתונים ===")
    migrator.migrate_csv_to_db()
    
    print("\n" + "="*50 + "\n")
    
    # העברה ממסד נתונים ל-CSV
    print("=== העברה ממסד נתונים ל-CSV ===")
    migrator.migrate_db_to_csv()

if __name__ == "__main__":
    main()
```

---

## חלק 4: בניית API עם FastAPI

### שלב 4.1: הבנת FastAPI

FastAPI הוא פריימוורק מודרני ל-Python:
- **מהיר**: ביצועים גבוהים
- **קל ללמידה**: תחביר פשוט ואינטואיטיבי
- **מתועד אוטומטית**: יוצר דוקומנטציה אוטומטית
- **בדיקות מובנות**: כלים לבדיקת ה-API

### שלב 4.2: מודלים ב-Pydantic

```python
# models.py
from pydantic import BaseModel, Field
from typing import Optional

class StudentBase(BaseModel):
    """מודל בסיס לתלמיד"""
    name: str = Field(..., min_length=1, max_length=100, description="שם התלמיד")
    age: int = Field(..., gt=0, lt=120, description="גיל התלמיד")
    grade: float = Field(..., ge=0, le=100, description="ציון התלמיד")

class StudentCreate(StudentBase):
    """מודל ליצירת תלמיד חדש"""
    pass

class StudentUpdate(BaseModel):
    """מודל לעדכון תלמיד"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    age: Optional[int] = Field(None, gt=0, lt=120)
    grade: Optional[float] = Field(None, ge=0, le=100)

class StudentResponse(StudentBase):
    """מודל לתגובה עם תלמיד"""
    id: int = Field(..., description="מזהה ייחודי של התלמיד")
    
    class Config:
        from_attributes = True

class MessageResponse(BaseModel):
    """מודל להודעת תגובה"""
    message: str
    
class StatisticsResponse(BaseModel):
    """מודל לסטטיסטיקות"""
    total_students: int
    average_grade: float
    highest_grade: float
    lowest_grade: float
    passing_students: int
    failing_students: int
```

### שלב 4.3: שכבת שירותים

```python
# services.py
from typing import List, Optional
from student import Student
from database_manager import DatabaseManager
from models import StudentCreate, StudentUpdate, StatisticsResponse

class StudentService:
    """שכבת שירותים לניהול תלמידים"""
    
    def __init__(self, db_name: str = "students.db"):
        """
        בנאי המחלקה
        
        Args:
            db_name: שם מסד הנתונים
        """
        self.db = DatabaseManager(db_name)
        self.db.connect()
        self.db.create_table()
    
    def create_student(self, student_data: StudentCreate) -> Optional[Student]:
        """
        יצירת תלמיד חדש
        
        Args:
            student_data: נתוני התלמיד החדש
            
        Returns:
            אובייקט Student אם נוצר בהצלחה, None אחרת
        """
        # מציאת ID הבא
        all_students = self.db.get_all_students()
        next_id = max([s.id for s in all_students], default=0) + 1
        
        # יצירת תלמיד חדש
        student = Student(
            id=next_id,
            name=student_data.name,
            age=student_data.age,
            grade=student_data.grade
        )
        
        # הוספה למסד הנתונים
        if self.db.insert_student(student):
            return student
        return None
    
    def get_all_students(self) -> List[Student]:
        """קבלת כל התלמידים"""
        return self.db.get_all_students()
    
    def get_student(self, student_id: int) -> Optional[Student]:
        """קבלת תלמיד לפי ID"""
        return self.db.get_student_by_id(student_id)
    
    def update_student(self, student_id: int, student_data: StudentUpdate) -> Optional[Student]:
        """
        עדכון תלמיד
        
        Args:
            student_id: מזהה התלמיד
            student_data: נתונים לעדכון
            
        Returns:
            אובייקט Student מעודכן אם הצליח, None אחרת
        """
        # קבלת התלמיד הנוכחי
        student = self.db.get_student_by_id(student_id)
        if not student:
            return None
        
        # עדכון הערכים שנשלחו
        if student_data.name is not None:
            student.name = student_data.name
        if student_data.age is not None:
            student.age = student_data.age
        if student_data.grade is not None:
            student.grade = student_data.grade
        
        # עדכון במסד הנתונים
        if self.db.update_student(student):
            return student
        return None
    
    def delete_student(self, student_id: int) -> bool:
        """מחיקת תלמיד"""
        return self.db.delete_student(student_id)
    
    def get_statistics(self) -> Optional[StatisticsResponse]:
        """
        קבלת סטטיסטיקות על התלמידים
        
        Returns:
            אובייקט StatisticsResponse עם הנתונים
        """
        students = self.db.get_all_students()
        
        if not students:
            return None
        
        grades = [s.grade for s in students]
        
        return StatisticsResponse(
            total_students=len(students),
            average_grade=sum(grades) / len(grades),
            highest_grade=max(grades),
            lowest_grade=min(grades),
            passing_students=len([s for s in students if s.is_passing()]),
            failing_students=len([s for s in students if not s.is_passing()])
        )
    
    def get_top_students(self, limit: int = 5) -> List[Student]:
        """
        קבלת התלמידים המצטיינים
        
        Args:
            limit: מספר התלמידים להחזיר
            
        Returns:
            רשימת תלמידים ממוינת לפי ציון
        """
        students = self.db.get_all_students()
        return sorted(students, key=lambda s: s.grade, reverse=True)[:limit]
    
    def close(self):
        """סגירת החיבור למסד הנתונים"""
        self.db.disconnect()
```

### שלב 4.4: יצירת ה-API

```python
# main.py
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from typing import List
from models import (
    StudentCreate, StudentUpdate, StudentResponse,
    MessageResponse, StatisticsResponse
)
from services import StudentService
from student import Student

# יצירת האפליקציה
app = FastAPI(
    title="Students Management API",
    description="API לניהול תלמידים עם SQLite",
    version="1.0.0"
)

# יצירת שירות התלמידים
service = StudentService()

# פונקציה להמרת Student ל-StudentResponse
def student_to_response(student: Student) -> StudentResponse:
    """המרת אובייקט Student למודל StudentResponse"""
    return StudentResponse(
        id=student.id,
        name=student.name,
        age=student.age,
        grade=student.grade
    )

@app.get("/", response_model=MessageResponse)
async def root():
    """נקודת קצה ראשית"""
    return MessageResponse(message="ברוכים הבאים ל-Students Management API")

@app.post("/students/", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
async def create_student(student: StudentCreate):
    """
    יצירת תלמיד חדש
    
    - **name**: שם התלמיד
    - **age**: גיל התלמיד
    - **grade**: ציון התלמיד
    """
    new_student = service.create_student(student)
    
    if not new_student:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="שגיאה ביצירת התלמיד"
        )
    
    return student_to_response(new_student)

@app.get("/students/", response_model=List[StudentResponse])
async def get_all_students():
    """קבלת כל התלמידים"""
    students = service.get_all_students()
    return [student_to_response(s) for s in students]

@app.get("/students/{student_id}", response_model=StudentResponse)
async def get_student(student_id: int):
    """קבלת תלמיד לפי ID"""
    student = service.get_student(student_id)
    
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"תלמיד עם ID {student_id} לא נמצא"
        )
    
    return student_to_response(student)

@app.put("/students/{student_id}", response_model=StudentResponse)
async def update_student(student_id: int, student_data: StudentUpdate):
    """עדכון פרטי תלמיד"""
    updated_student = service.update_student(student_id, student_data)
    
    if not updated_student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"תלמיד עם ID {student_id} לא נמצא"
        )
    
    return student_to_response(updated_student)

@app.delete("/students/{student_id}", response_model=MessageResponse)
async def delete_student(student_id: int):
    """מחיקת תלמיד"""
    success = service.delete_student(student_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"תלמיד עם ID {student_id} לא נמצא"
        )
    
    return MessageResponse(message=f"תלמיד עם ID {student_id} נמחק בהצלחה")

@app.get("/statistics/", response_model=StatisticsResponse)
async def get_statistics():
    """קבלת סטטיסטיקות על התלמידים"""
    stats = service.get_statistics()
    
    if not stats:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="אין תלמידים במערכת"
        )
    
    return stats

@app.get("/students/top/{limit}", response_model=List[StudentResponse])
async def get_top_students(limit: int = 5):
    """קבלת התלמידים המצטיינים"""
    if limit < 1 or limit > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="הגבלה חייבת להיות בין 1 ל-100"
        )
    
    top_students = service.get_top_students(limit)
    return [student_to_response(s) for s in top_students]

# סגירת החיבור למסד הנתונים בסיום
@app.on_event("shutdown")
async def shutdown_event():
    """סגירת החיבור למסד הנתונים"""
    service.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### שלב 4.5: הרצת ה-API

```bash
# הרצה מהטרמינל
uvicorn main:app --reload

# או הרצה ישירה
python main.py
```

### שלב 4.6: גישה לדוקומנטציה

לאחר הרצת ה-API:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## חלק 5: פרויקט מלא

### שלב 5.1: מבנה הפרויקט

```
student_management_system/
│
├── models/
│   ├── __init__.py
│   ├── student.py          # מחלקת Student
│   └── api_models.py       # מודלי Pydantic
│
├── managers/
│   ├── __init__.py
│   ├── csv_manager.py      # ניהול CSV
│   └── database_manager.py # ניהול SQLite
│
├── services/
│   ├── __init__.py
│   ├── student_service.py  # שכבת שירותים
│   └── migration_service.py # שירות העברת נתונים
│
├── api/
│   ├── __init__.py
│   └── routes.py           # נקודות קצה של ה-API
│
├── data/
│   ├── students.csv        # קובץ CSV
│   └── students.db         # מסד נתונים
│
├── main.py                 # נקודת כניסה לאפליקציה
├── config.py               # הגדרות
└── requirements.txt        # תלויות
```

### שלב 5.2: קובץ requirements.txt

```
fastapi==0.104.1
uvicorn==0.24.0
pydantic==2.5.0
```

### שלב 5.3: קובץ config.py

```python
# config.py
from pathlib import Path

# נתיבי בסיס
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"

# הגדרות מסד נתונים
DATABASE_NAME = "students.db"
DATABASE_PATH = DATA_DIR / DATABASE_NAME

# הגדרות CSV
CSV_FILENAME = "students.csv"
CSV_PATH = DATA_DIR / CSV_FILENAME

# הגדרות API
API_TITLE = "Students Management API"
API_VERSION = "1.0.0"
API_DESCRIPTION = "API לניהול תלמידים עם SQLite ו-CSV"

# הגדרות כלליות
PASSING_GRADE = 60.0
```

### שלב 5.4: דוגמה לשימוש מלא

```python
# full_example.py
from pathlib import Path
from models.student import Student
from managers.csv_manager import CSVManager
from managers.database_manager import DatabaseManager
from services.migration_service import DataMigrator

def main():
    print("="*60)
    print("מערכת ניהול תלמידים - דוגמה מלאה")
    print("="*60)
    
    # יצירת תיקיית data אם לא קיימת
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    csv_path = data_dir / "students.csv"
    db_path = data_dir / "students.db"
    
    # שלב 1: יצירת תלמידים ושמירה ל-CSV
    print("\n📝 שלב 1: יצירת קובץ CSV")
    csv_manager = CSVManager(str(csv_path))
    
    students = [
        Student(1, "דני כהן", 20, 85.5),
        Student(2, "רונית לוי", 22, 92.0),
        Student(3, "יוסי אברהם", 21, 78.5),
        Student(4, "מיכל דוד", 23, 88.0),
        Student(5, "עומר שלום", 19, 95.5)
    ]
    
    csv_manager.write_students(students)
    
    # שלב 2: העברה ממסד נתונים
    print("\n🔄 שלב 2: העברת נתונים מ-CSV למסד נתונים")
    migrator = DataMigrator(str(csv_path), str(db_path))
    migrator.migrate_csv_to_db()
    
    # שלב 3: עבודה עם מסד הנתונים
    print("\n💾 שלב 3: פעולות על מסד הנתונים")
    db = DatabaseManager(str(db_path))
    db.connect()
    
    # הוספת תלמיד חדש
    new_student = Student(6, "שרה מזרחי", 24, 91.0)
    db.insert_student(new_student)
    
    # קבלת תלמידים מצטיינים
    print("\n🌟 תלמידים מצטיינים (ציון מעל 85):")
    top_students = db.get_students_by_min_grade(85)
    for student in top_students:
        print(f"  • {student}")
    
    # חישוב סטטיסטיקות
    all_students = db.get_all_students()
    if all_students:
        avg_grade = sum(s.grade for s in all_students) / len(all_students)
        print(f"\n📊 סטטיסטיקות:")
        print(f"  • סך התלמידים: {len(all_students)}")
        print(f"  • ממוצע ציונים: {avg_grade:.2f}")
        print(f"  • ציון הכי גבוה: {max(s.grade for s in all_students):.2f}")
        print(f"  • ציון הכי נמוך: {min(s.grade for s in all_students):.2f}")
    
    db.disconnect()
    
    print("\n✅ הדוגמה הושלמה בהצלחה!")
    print(f"📁 הקבצים נשמרו ב: {data_dir.absolute()}")
    print("\n💡 להרצת ה-API, הפעל: uvicorn main:app --reload")

if __name__ == "__main__":
    main()
```

---

## תרגילים לתרגול

### תרגיל 1: הרחבת מודל התלמיד
הוסף למחלקת `Student`:
- שדה `email`
- שדה `phone`
- מתודה `get_grade_letter()` שמחזירה A/B/C/D/F

### תרגיל 2: חיפושים מתקדמים
הוסף למחלקת `DatabaseManager`:
- חיפוש תלמידים לפי טווח גילאים
- חיפוש תלמידים לפי טווח ציונים
- מיון תלמידים לפי שם

### תרגיל 3: ולידציות
הוסף ולידציות:
- וידוא שהשם מכיל רק אותיות
- וידוא שהגיל הגיוני (16-99)
- וידוא שהציון בטווח 0-100

### תרגיל 4: נקודות קצה נוספות ל-API
הוסף נקודות קצה:
- `GET /students/search?name=xxx` - חיפוש לפי שם
- `GET /students/grade-range?min=X&max=Y` - חיפוש לפי טווח ציונים
- `POST /students/bulk` - הוספת מספר תלמידים בבת אחת

### תרגיל 5: ייצוא נתונים
צור שירות לייצוא נתונים:
- ייצוא ל-JSON
- ייצוא ל-Excel
- ייצוא ל-PDF

---

## סיכום

במדריך זה למדת:

✅ **OOP בסיס**: מחלקות, אובייקטים, מתודות  
✅ **עבודה עם CSV**: קריאה, כתיבה, ניהול נתונים  
✅ **SQLite**: יצירת טבלאות, CRUD operations  
✅ **העברת נתונים**: מ-CSV למסד נתונים ולהיפך  
✅ **FastAPI**: בניית REST API מלא  
✅ **ארכיטקטורה**: הפרדת שכבות, שירותים, מודלים  

### המשך לימוד מומלץ
- אימות משתמשים ב-FastAPI (JWT)
- טסטים אוטומטיים (pytest)
- Docker containerization
- פריסה לענן (Heroku, AWS, Azure)

---

**בהצלחה! 🚀**
