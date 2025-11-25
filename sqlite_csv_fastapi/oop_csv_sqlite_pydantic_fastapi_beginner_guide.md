# מדריך מקיף: OOP, CSV, SQLite, Pydantic ו-FastAPI למתחילים

## תוכן עניינים
1. [מבוא](#מבוא)
2. [הכנת הסביבה](#הכנת-הסביבה)
3. [שלב 1: יסודות OOP בפייתון](#שלב-1-יסודות-oop-בפייתון)
4. [שלב 2: עבודה עם קבצי CSV](#שלב-2-עבודה-עם-קבצי-csv)
5. [שלב 3: SQLite - מסד נתונים מקומי](#שלב-3-sqlite---מסד-נתונים-מקומי)
6. [שלב 4: Pydantic - וולידציה ומודלים](#שלב-4-pydantic---וולידציה-ומודלים)
7. [שלב 5: FastAPI - בניית API](#שלב-5-fastapi---בניית-api)
8. [שלב 6: פרויקט מלא - מערכת ניהול סטודנטים](#שלב-6-פרויקט-מלא---מערכת-ניהול-סטודנטים)
9. [תרגילים](#תרגילים)

---

## מבוא

במדריך זה נלמד לבנות אפליקציית API מקצועית המשלבת:
- **OOP (Object-Oriented Programming)** - תכנות מונחה עצמים
- **CSV** - עבודה עם קבצי נתונים
- **SQLite** - מסד נתונים מקומי
- **Pydantic** - וולידציה של נתונים
- **FastAPI** - פריימוורק לבניית API מהיר ויעיל

---

## הכנת הסביבה

### התקנת חבילות נדרשות:

```bash
pip install fastapi uvicorn pydantic sqlite3
```

או שמור בקובץ `requirements.txt`:
```
fastapi==0.104.1
uvicorn==0.24.0
pydantic==2.5.0
```

והתקן:
```bash
pip install -r requirements.txt
```

---

## שלב 1: יסודות OOP בפייתון

### מה זה OOP?

תכנות מונחה עצמים הוא גישה לארגון קוד באמצעות "עצמים" שמכילים נתונים (attributes) ופעולות (methods).

### דוגמה בסיסית - מחלקת Student:

```python
# student_basic.py

class Student:
    """מחלקה המייצגת סטודנט"""
    
    def __init__(self, id: int, name: str, age: int, grade: float):
        """
        Constructor - פונקציה שרצה כשיוצרים אובייקט חדש
        
        Args:
            id: מספר מזהה של הסטודנט
            name: שם הסטודנט
            age: גיל הסטודנט
            grade: ציון ממוצע
        """
        self.id = id
        self.name = name
        self.age = age
        self.grade = grade
    
    def display_info(self):
        """מציג מידע על הסטודנט"""
        print(f"ID: {self.id}")
        print(f"Name: {self.name}")
        print(f"Age: {self.age}")
        print(f"Grade: {self.grade}")
    
    def is_passing(self) -> bool:
        """בודק אם הסטודנט עובר (ציון מעל 60)"""
        return self.grade >= 60
    
    def __str__(self) -> str:
        """מחזיר ייצוג טקסטואלי של הסטודנט"""
        return f"Student({self.name}, Grade: {self.grade})"


# שימוש במחלקה
if __name__ == "__main__":
    # יצירת אובייקט סטודנט
    student1 = Student(1, "יוסי כהן", 20, 85.5)
    
    # שימוש במתודות
    student1.display_info()
    print(f"\nהאם עובר? {student1.is_passing()}")
    print(student1)
```

### הסבר מושגים:

- **Class (מחלקה)**: תבנית ליצירת אובייקטים
- **Object (אובייקט)**: מופע ספציפי של מחלקה
- **`__init__`**: Constructor - פונקציה שרצה כשיוצרים אובייקט
- **`self`**: התייחסות לאובייקט הנוכחי
- **Methods (מתודות)**: פונקציות שמוגדרות בתוך מחלקה
- **Attributes (תכונות)**: משתנים שמוגדרים בתוך מחלקה

---

## שלב 2: עבודה עם קבצי CSV

### מה זה CSV?

CSV (Comma-Separated Values) הוא פורמט קובץ לאחסון נתונים בצורת טבלה.

### קריאה וכתיבה של CSV:

```python
# csv_handler.py

import csv
from typing import List, Dict

class CSVHandler:
    """מחלקה לניהול קבצי CSV"""
    
    @staticmethod
    def read_csv(filename: str) -> List[Dict]:
        """
        קורא קובץ CSV ומחזיר רשימת מילונים
        
        Args:
            filename: נתיב לקובץ CSV
            
        Returns:
            רשימה של מילונים, כל מילון מייצג שורה
        """
        data = []
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    data.append(row)
            print(f"✓ נקראו {len(data)} שורות מהקובץ {filename}")
            return data
        except FileNotFoundError:
            print(f"✗ הקובץ {filename} לא נמצא")
            return []
        except Exception as e:
            print(f"✗ שגיאה בקריאת הקובץ: {e}")
            return []
    
    @staticmethod
    def write_csv(filename: str, data: List[Dict], fieldnames: List[str]):
        """
        כותב נתונים לקובץ CSV
        
        Args:
            filename: נתיב לקובץ CSV
            data: רשימת מילונים לכתיבה
            fieldnames: שמות העמודות
        """
        try:
            with open(filename, 'w', encoding='utf-8', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
            print(f"✓ נכתבו {len(data)} שורות לקובץ {filename}")
        except Exception as e:
            print(f"✗ שגיאה בכתיבת הקובץ: {e}")


# דוגמה לשימוש
if __name__ == "__main__":
    # יצירת קובץ CSV לדוגמה
    students_data = [
        {'id': '1', 'name': 'יוסי כהן', 'age': '20', 'grade': '85.5'},
        {'id': '2', 'name': 'שרה לevi', 'age': '22', 'grade': '92.0'},
        {'id': '3', 'name': 'דוד משה', 'age': '21', 'grade': '78.5'}
    ]
    
    # כתיבה
    CSVHandler.write_csv(
        'students.csv',
        students_data,
        ['id', 'name', 'age', 'grade']
    )
    
    # קריאה
    data = CSVHandler.read_csv('students.csv')
    for student in data:
        print(student)
```

---

## שלב 3: SQLite - מסד נתונים מקומי

### מה זה SQLite?

SQLite הוא מסד נתונים קל משקל שלא דורש שרת נפרד. מעולה ללימוד ופרויקטים קטנים.

### מחלקת Database בסיסית:

```python
# database.py

import sqlite3
from typing import List, Tuple, Optional

class Database:
    """מחלקה לניהול מסד נתונים SQLite"""
    
    def __init__(self, db_name: str = "students.db"):
        """
        יוצר חיבור למסד נתונים
        
        Args:
            db_name: שם קובץ מסד הנתונים
        """
        self.db_name = db_name
        self.connection = None
        self.cursor = None
        
    def connect(self):
        """יוצר חיבור למסד הנתונים"""
        try:
            self.connection = sqlite3.connect(self.db_name)
            self.cursor = self.connection.cursor()
            print(f"✓ חיבור למסד הנתונים {self.db_name} הצליח")
        except sqlite3.Error as e:
            print(f"✗ שגיאה בחיבור למסד הנתונים: {e}")
    
    def disconnect(self):
        """מנתק חיבור למסד הנתונים"""
        if self.connection:
            self.connection.close()
            print("✓ החיבור למסד הנתונים נסגר")
    
    def create_table(self):
        """יוצר טבלת students אם היא לא קיימת"""
        query = """
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            grade REAL NOT NULL
        )
        """
        try:
            self.cursor.execute(query)
            self.connection.commit()
            print("✓ טבלת students נוצרה בהצלחה")
        except sqlite3.Error as e:
            print(f"✗ שגיאה ביצירת הטבלה: {e}")
    
    def insert_student(self, id: int, name: str, age: int, grade: float):
        """
        מוסיף סטודנט חדש למסד הנתונים
        
        Args:
            id: מספר מזהה
            name: שם הסטודנט
            age: גיל
            grade: ציון
        """
        query = "INSERT INTO students (id, name, age, grade) VALUES (?, ?, ?, ?)"
        try:
            self.cursor.execute(query, (id, name, age, grade))
            self.connection.commit()
            print(f"✓ הסטודנט {name} נוסף בהצלחה")
        except sqlite3.IntegrityError:
            print(f"✗ סטודנט עם ID {id} כבר קיים")
        except sqlite3.Error as e:
            print(f"✗ שגיאה בהוספת סטודנט: {e}")
    
    def get_all_students(self) -> List[Tuple]:
        """
        מחזיר את כל הסטודנטים
        
        Returns:
            רשימת tuples, כל tuple מכיל את פרטי הסטודנט
        """
        query = "SELECT * FROM students"
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"✗ שגיאה בשליפת נתונים: {e}")
            return []
    
    def get_student_by_id(self, student_id: int) -> Optional[Tuple]:
        """
        מחזיר סטודנט לפי ID
        
        Args:
            student_id: מספר מזהה של הסטודנט
            
        Returns:
            tuple עם פרטי הסטודנט או None אם לא נמצא
        """
        query = "SELECT * FROM students WHERE id = ?"
        try:
            self.cursor.execute(query, (student_id,))
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            print(f"✗ שגיאה בשליפת נתונים: {e}")
            return None
    
    def update_student(self, student_id: int, name: str, age: int, grade: float):
        """עדכון פרטי סטודנט"""
        query = "UPDATE students SET name=?, age=?, grade=? WHERE id=?"
        try:
            self.cursor.execute(query, (name, age, grade, student_id))
            self.connection.commit()
            print(f"✓ הסטודנט עם ID {student_id} עודכן בהצלחה")
        except sqlite3.Error as e:
            print(f"✗ שגיאה בעדכון: {e}")
    
    def delete_student(self, student_id: int):
        """מחיקת סטודנט"""
        query = "DELETE FROM students WHERE id = ?"
        try:
            self.cursor.execute(query, (student_id,))
            self.connection.commit()
            print(f"✓ הסטודנט עם ID {student_id} נמחק בהצלחה")
        except sqlite3.Error as e:
            print(f"✗ שגיאה במחיקה: {e}")


# דוגמה לשימוש
if __name__ == "__main__":
    # יצירת מסד נתונים
    db = Database("students.db")
    db.connect()
    db.create_table()
    
    # הוספת סטודנטים
    db.insert_student(1, "יוסי כהן", 20, 85.5)
    db.insert_student(2, "שרה לוי", 22, 92.0)
    db.insert_student(3, "דוד משה", 21, 78.5)
    
    # שליפת כל הסטודנטים
    students = db.get_all_students()
    print("\nכל הסטודנטים:")
    for student in students:
        print(student)
    
    # שליפת סטודנט ספציפי
    student = db.get_student_by_id(1)
    print(f"\nסטודנט עם ID 1: {student}")
    
    db.disconnect()
```

---

## שלב 4: Pydantic - וולידציה ומודלים

### מה זה Pydantic?

Pydantic היא ספרייה לוולידציה של נתונים ויצירת מודלים עם type hints.

### יתרונות:
- וולידציה אוטומטית של טייפים
- המרת טייפים אוטומטית
- הודעות שגיאה ברורות
- תמיכה מלאה ב-FastAPI

### מודל Student עם Pydantic:

```python
# models.py

from pydantic import BaseModel, Field, field_validator
from typing import Optional

class StudentBase(BaseModel):
    """מודל בסיס לסטודנט"""
    name: str = Field(..., min_length=2, max_length=100, description="שם הסטודנט")
    age: int = Field(..., ge=16, le=120, description="גיל הסטודנט")
    grade: float = Field(..., ge=0, le=100, description="ציון ממוצע")
    
    @field_validator('name')
    @classmethod
    def name_must_not_be_empty(cls, v: str) -> str:
        """ולידטור מותאם אישית לשם"""
        if not v.strip():
            raise ValueError('שם לא יכול להיות רק רווחים')
        return v.strip()
    
    @field_validator('grade')
    @classmethod
    def grade_must_be_valid(cls, v: float) -> float:
        """ולידטור לציון"""
        if v < 0 or v > 100:
            raise ValueError('ציון חייב להיות בין 0 ל-100')
        return round(v, 2)


class StudentCreate(StudentBase):
    """מודל ליצירת סטודנט חדש (בלי ID)"""
    pass


class StudentUpdate(BaseModel):
    """מודל לעדכון סטודנט (כל השדות אופציונליים)"""
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    age: Optional[int] = Field(None, ge=16, le=120)
    grade: Optional[float] = Field(None, ge=0, le=100)


class Student(StudentBase):
    """מודל מלא של סטודנט (כולל ID)"""
    id: int = Field(..., description="מספר מזהה ייחודי")
    
    class Config:
        """קונפיגורציה של המודל"""
        from_attributes = True  # מאפשר יצירה מאובייקטים של ORM
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "יוסי כהן",
                "age": 20,
                "grade": 85.5
            }
        }


class StudentResponse(BaseModel):
    """מודל לתשובה עם מידע נוסף"""
    student: Student
    is_passing: bool
    status: str
    
    @staticmethod
    def from_student(student: Student) -> "StudentResponse":
        """יוצר StudentResponse מאובייקט Student"""
        is_passing = student.grade >= 60
        status = "עובר" if is_passing else "נכשל"
        return StudentResponse(
            student=student,
            is_passing=is_passing,
            status=status
        )


# דוגמאות שימוש
if __name__ == "__main__":
    # יצירת סטודנט תקין
    try:
        student_data = {
            "name": "יוסי כהן",
            "age": 20,
            "grade": 85.5
        }
        student = StudentCreate(**student_data)
        print("✓ סטודנט תקין נוצר:")
        print(student.model_dump_json(indent=2))
    except Exception as e:
        print(f"✗ שגיאה: {e}")
    
    # ניסיון ליצור סטודנט עם נתונים לא תקינים
    try:
        invalid_student = StudentCreate(
            name="",  # שם ריק - לא תקין
            age=15,   # גיל נמוך מדי
            grade=150  # ציון מעל 100
        )
    except Exception as e:
        print(f"\n✗ וולידציה נכשלה כצפוי: {e}")
    
    # המרת טייפים אוטומטית
    student2 = StudentCreate(
        name="שרה לוי",
        age="22",  # מחרוזת - תומר אוטומטית למספר
        grade="92.5"  # מחרוזת - תומר אוטומטית למספר
    )
    print(f"\n✓ המרת טייפים אוטומטית:")
    print(f"age type: {type(student2.age)}, grade type: {type(student2.grade)}")
```

### הסבר על Field:

- `...` = שדה חובה
- `min_length/max_length` = אורך מינימלי/מקסימלי למחרוזות
- `ge/le` = גדול או שווה / קטן או שווה (greater/less or equal)
- `description` = תיאור השדה (יופיע בתיעוד האוטומטי)

---

## שלב 5: FastAPI - בניית API

### מה זה FastAPI?

FastAPI הוא פריימוורק מודרני לבניית API ב-Python, מהיר במיוחד ועם תיעוד אוטומטי.

### יתרונות:
- מהיר ביותר
- תיעוד אוטומטי (Swagger UI)
- וולידציה אוטומטית עם Pydantic
- תמיכה ב-async/await
- קל ללמידה

### API בסיסי:

```python
# main.py

from fastapi import FastAPI, HTTPException, status
from typing import List
from models import Student, StudentCreate, StudentUpdate, StudentResponse
from database import Database

# יצירת אפליקציית FastAPI
app = FastAPI(
    title="Student Management API",
    description="API לניהול סטודנטים",
    version="1.0.0"
)

# יצירת מסד נתונים גלובלי
db = Database("students.db")

@app.on_event("startup")
async def startup_event():
    """רץ כשהאפליקציה עולה"""
    db.connect()
    db.create_table()
    print("🚀 API מוכן לשימוש!")

@app.on_event("shutdown")
async def shutdown_event():
    """רץ כשהאפליקציה נסגרת"""
    db.disconnect()
    print("👋 API נסגר")


# ========== Endpoints ==========

@app.get("/", tags=["General"])
async def root():
    """נקודת קצה בסיסית"""
    return {
        "message": "ברוך הבא ל-Student Management API",
        "docs": "/docs",
        "version": "1.0.0"
    }


@app.post("/students/", response_model=Student, status_code=status.HTTP_201_CREATED, tags=["Students"])
async def create_student(student: StudentCreate):
    """
    יוצר סטודנט חדש
    
    - **name**: שם הסטודנט (2-100 תווים)
    - **age**: גיל (16-120)
    - **grade**: ציון (0-100)
    """
    # מציאת ID הבא
    all_students = db.get_all_students()
    next_id = max([s[0] for s in all_students], default=0) + 1
    
    # הוספה למסד הנתונים
    db.insert_student(next_id, student.name, student.age, student.grade)
    
    # החזרת הסטודנט שנוצר
    return Student(
        id=next_id,
        name=student.name,
        age=student.age,
        grade=student.grade
    )


@app.get("/students/", response_model=List[Student], tags=["Students"])
async def get_all_students():
    """מחזיר את כל הסטודנטים"""
    students = db.get_all_students()
    return [
        Student(id=s[0], name=s[1], age=s[2], grade=s[3])
        for s in students
    ]


@app.get("/students/{student_id}", response_model=StudentResponse, tags=["Students"])
async def get_student(student_id: int):
    """מחזיר סטודנט לפי ID"""
    student_data = db.get_student_by_id(student_id)
    
    if not student_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"סטודנט עם ID {student_id} לא נמצא"
        )
    
    student = Student(
        id=student_data[0],
        name=student_data[1],
        age=student_data[2],
        grade=student_data[3]
    )
    
    return StudentResponse.from_student(student)


@app.put("/students/{student_id}", response_model=Student, tags=["Students"])
async def update_student(student_id: int, student_update: StudentUpdate):
    """מעדכן את פרטי הסטודנט"""
    # בדיקה שהסטודנט קיים
    existing = db.get_student_by_id(student_id)
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"סטודנט עם ID {student_id} לא נמצא"
        )
    
    # עדכון רק השדות שסופקו
    current_name = existing[1]
    current_age = existing[2]
    current_grade = existing[3]
    
    new_name = student_update.name if student_update.name is not None else current_name
    new_age = student_update.age if student_update.age is not None else current_age
    new_grade = student_update.grade if student_update.grade is not None else current_grade
    
    db.update_student(student_id, new_name, new_age, new_grade)
    
    return Student(id=student_id, name=new_name, age=new_age, grade=new_grade)


@app.delete("/students/{student_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Students"])
async def delete_student(student_id: int):
    """מחק סטודנט"""
    # בדיקה שהסטודנט קיים
    existing = db.get_student_by_id(student_id)
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"סטודנט עם ID {student_id} לא נמצא"
        )
    
    db.delete_student(student_id)
    return None


@app.get("/students/filter/passing", response_model=List[Student], tags=["Students"])
async def get_passing_students():
    """מחזיר רק סטודנטים עם ציון מעל 60"""
    all_students = db.get_all_students()
    passing = [
        Student(id=s[0], name=s[1], age=s[2], grade=s[3])
        for s in all_students
        if s[3] >= 60
    ]
    return passing


@app.get("/statistics/", tags=["Statistics"])
async def get_statistics():
    """מחזיר סטטיסטיקות על הסטודנטים"""
    students = db.get_all_students()
    
    if not students:
        return {
            "total_students": 0,
            "average_grade": 0,
            "passing_rate": 0
        }
    
    grades = [s[3] for s in students]
    passing = sum(1 for g in grades if g >= 60)
    
    return {
        "total_students": len(students),
        "average_grade": round(sum(grades) / len(grades), 2),
        "passing_rate": round((passing / len(students)) * 100, 2),
        "highest_grade": max(grades),
        "lowest_grade": min(grades)
    }


# הרצה: uvicorn main:app --reload
```

### הרצת השרת:

```bash
uvicorn main:app --reload
```

- `main` = שם הקובץ (main.py)
- `app` = שם המשתנה של FastAPI
- `--reload` = טעינה מחדש אוטומטית כשמשנים קוד

### גישה לתיעוד:

- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

---

## שלב 6: פרויקט מלא - מערכת ניהול סטודנטים

### מבנה הפרויקט:

```
student_management/
│
├── main.py                 # נקודת הכניסה של ה-API
├── models.py              # מודלים של Pydantic
├── database.py            # ניהול מסד נתונים
├── csv_handler.py         # עבודה עם CSV
├── requirements.txt       # תלויות
├── students.csv          # קובץ CSV לדוגמה
└── students.db           # מסד נתונים (נוצר אוטומטית)
```

### פיצ'רים מתקדמים - קובץ main.py משופר:

```python
# main_advanced.py

from fastapi import FastAPI, HTTPException, status, UploadFile, File
from fastapi.responses import FileResponse
from typing import List
import csv
import io
from models import Student, StudentCreate, StudentUpdate, StudentResponse
from database import Database
from csv_handler import CSVHandler

app = FastAPI(
    title="Student Management API - Advanced",
    description="API מתקדם לניהול סטודנטים עם תמיכה ב-CSV",
    version="2.0.0"
)

db = Database("students.db")

@app.on_event("startup")
async def startup_event():
    db.connect()
    db.create_table()

@app.on_event("shutdown")
async def shutdown_event():
    db.disconnect()


# ========== CSV Operations ==========

@app.post("/upload-csv/", tags=["CSV"])
async def upload_csv(file: UploadFile = File(...)):
    """
    מעלה קובץ CSV ומייבא את הסטודנטים למסד הנתונים
    
    הקובץ צריך להכיל את העמודות: name, age, grade
    """
    if not file.filename.endswith('.csv'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="הקובץ חייב להיות CSV"
        )
    
    try:
        # קריאת הקובץ
        contents = await file.read()
        decoded = contents.decode('utf-8')
        csv_reader = csv.DictReader(io.StringIO(decoded))
        
        added_count = 0
        errors = []
        
        for row in csv_reader:
            try:
                # ולידציה עם Pydantic
                student = StudentCreate(
                    name=row['name'],
                    age=int(row['age']),
                    grade=float(row['grade'])
                )
                
                # מציאת ID הבא
                all_students = db.get_all_students()
                next_id = max([s[0] for s in all_students], default=0) + 1
                
                # הוספה למסד נתונים
                db.insert_student(next_id, student.name, student.age, student.grade)
                added_count += 1
                
            except Exception as e:
                errors.append(f"שורה {csv_reader.line_num}: {str(e)}")
        
        return {
            "message": f"הועלו {added_count} סטודנטים",
            "added": added_count,
            "errors": errors
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"שגיאה בעיבוד הקובץ: {str(e)}"
        )


@app.get("/download-csv/", tags=["CSV"])
async def download_csv():
    """מוריד את כל הסטודנטים כקובץ CSV"""
    students = db.get_all_students()
    
    # יצירת קובץ CSV בזיכרון
    output = io.StringIO()
    writer = csv.writer(output)
    
    # כתיבת כותרות
    writer.writerow(['id', 'name', 'age', 'grade'])
    
    # כתיבת נתונים
    for student in students:
        writer.writerow(student)
    
    # שמירה לקובץ זמני
    with open("students_export.csv", "w", encoding='utf-8', newline='') as f:
        f.write(output.getvalue())
    
    return FileResponse(
        "students_export.csv",
        media_type="text/csv",
        filename="students.csv"
    )


# ========== Advanced Filters ==========

@app.get("/students/filter/", response_model=List[Student], tags=["Students"])
async def filter_students(
    min_grade: float = 0,
    max_grade: float = 100,
    min_age: int = 0,
    max_age: int = 120
):
    """
    מסנן סטודנטים לפי ציון וגיל
    
    - **min_grade**: ציון מינימלי (ברירת מחדל: 0)
    - **max_grade**: ציון מקסימלי (ברירת מחדל: 100)
    - **min_age**: גיל מינימלי (ברירת מחדל: 0)
    - **max_age**: גיל מקסימלי (ברירת מחדל: 120)
    """
    all_students = db.get_all_students()
    
    filtered = [
        Student(id=s[0], name=s[1], age=s[2], grade=s[3])
        for s in all_students
        if min_grade <= s[3] <= max_grade and min_age <= s[2] <= max_age
    ]
    
    return filtered


@app.get("/students/search/", response_model=List[Student], tags=["Students"])
async def search_students(name: str):
    """
    מחפש סטודנטים לפי שם (חיפוש חלקי)
    
    - **name**: חלק מהשם לחיפוש
    """
    all_students = db.get_all_students()
    
    results = [
        Student(id=s[0], name=s[1], age=s[2], grade=s[3])
        for s in all_students
        if name.lower() in s[1].lower()
    ]
    
    return results


# ========== Batch Operations ==========

@app.post("/students/batch/", response_model=List[Student], tags=["Students"])
async def create_multiple_students(students: List[StudentCreate]):
    """יוצר מספר סטודנטים בבת אחת"""
    created_students = []
    
    for student in students:
        all_students = db.get_all_students()
        next_id = max([s[0] for s in all_students], default=0) + 1
        
        db.insert_student(next_id, student.name, student.age, student.grade)
        
        created_students.append(
            Student(id=next_id, name=student.name, age=student.age, grade=student.grade)
        )
    
    return created_students


@app.delete("/students/batch/", status_code=status.HTTP_204_NO_CONTENT, tags=["Students"])
async def delete_multiple_students(student_ids: List[int]):
    """מוחק מספר סטודנטים בבת אחת"""
    for student_id in student_ids:
        db.delete_student(student_id)
    
    return None
```

### קובץ דוגמה - students.csv:

```csv
name,age,grade
יוסי כהן,20,85.5
שרה לוי,22,92.0
דוד משה,21,78.5
רחל אברהם,19,88.0
מיכאל דוד,23,95.5
```

---

## תרגילים

### תרגיל 1: הוספת שדה "מחלקה"

הוסף שדה `department` (מחלקה) למודל Student ולמסד הנתונים.

**רמז**: 
1. עדכן את מחלקת Student ב-models.py
2. עדכן את הטבלה ב-database.py
3. עדכן את כל הפונקציות הרלוונטיות

### תרגיל 2: סטטיסטיקות מתקדמות

צור endpoint שמחזיר:
- כמה סטודנטים בכל טווח ציונים (0-60, 61-70, 71-80, 81-90, 91-100)
- הגיל הממוצע של הסטודנטים
- רשימת 3 הסטודנטים עם הציונים הגבוהים ביותר

### תרגיל 3: Authentication

הוסף authentication בסיסי ל-API באמצעות API Key.

**רמז**: השתמש ב-`Header` של FastAPI

### תרגיל 4: עדכון מרובה מ-CSV

צור endpoint שמאפשר לעדכן סטודנטים קיימים על ידי העלאת קובץ CSV (על בסיס ID).

### תרגיל 5: Pagination

הוסף pagination ל-endpoint של כל הסטודנטים (דפים של 10 סטודנטים).

**רמז**: השתמש ב-Query parameters: `skip` ו-`limit`

---

## סיכום

במדריך זה למדנו:

✅ **OOP** - יצירת מחלקות ואובייקטים  
✅ **CSV** - קריאה וכתיבה של קבצי נתונים  
✅ **SQLite** - ניהול מסד נתונים מקומי  
✅ **Pydantic** - וולידציה של נתונים  
✅ **FastAPI** - בניית API מקצועי  

### המלצות להמשך:

1. **למד על SQLAlchemy/SQLModel** - ORM מתקדם
2. **הוסף Frontend** - בנה ממשק משתמש עם React/Vue
3. **Docker** - למד לעטוף את האפליקציה ב-Container
4. **Testing** - כתוב בדיקות אוטומטיות עם pytest
5. **Deploy** - העלה את ה-API לענן (Heroku, AWS, etc.)

---

## משאבים נוספים

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [SQLite Tutorial](https://www.sqlitetutorial.net/)
- [Python OOP Tutorial](https://realpython.com/python3-object-oriented-programming/)

---

**בהצלחה! 🚀**
