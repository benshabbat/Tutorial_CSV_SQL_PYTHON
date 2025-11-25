# מדריך מקיף: CSV, SQLite ו-FastAPI לרמת מתחילים

## תוכן עניינים
1. [מבוא](#מבוא)
2. [התקנה והכנה](#התקנה-והכנה)
3. [חלק 1: עבודה עם CSV](#חלק-1-עבודה-עם-csv)
4. [חלק 2: SQLite - מסד נתונים](#חלק-2-sqlite---מסד-נתונים)
5. [חלק 3: FastAPI - בניית API](#חלק-3-fastapi---בניית-api)
6. [חלק 4: פרויקט מלא - מערכת ניהול תלמידים](#חלק-4-פרויקט-מלא---מערכת-ניהול-תלמידים)
7. [חלק 5: פרויקט מתקדם - מערכת ניהול מוצרים](#חלק-5-פרויקט-מתקדם---מערכת-ניהול-מוצרים)
8. [טיפים ושגיאות נפוצות](#טיפים-ושגיאות-נפוצות)

---

## מבוא

### מה נלמד במדריך זה?

במדריך זה נלמד איך לבנות API מלא שמאפשר:
- ✅ קריאת נתונים מקובץ CSV
- ✅ שמירת נתונים במסד נתונים SQLite
- ✅ יצירת API עם FastAPI לניהול הנתונים
- ✅ פעולות CRUD (Create, Read, Update, Delete)
- ✅ ייצוא נתונים חזרה ל-CSV

### טכנולוגיות שנשתמש בהן:

**1. CSV (Comma-Separated Values)**
- פורמט קובץ פשוט לאחסון נתונים
- קל לעריכה ולקריאה
- תואם לאקסל וכלי ניתוח נתונים

**2. SQLite**
- מסד נתונים רלציוני קל משקל
- לא דורש שרת נפרד
- מושלם לפרויקטים קטנים-בינוניים

**3. FastAPI**
- פריימוורק מודרני לבניית API
- מהיר וקל ללמידה
- תיעוד אוטומטי
- תמיכה בטיפוסים (Type Hints)

---

## התקנה והכנה

### שלב 1: בדיקת Python

ודא ש-Python 3.7+ מותקן במחשב:

```bash
python --version
```

### שלב 2: יצירת תיקיית פרויקט

צור תיקייה חדשה לפרויקט:

```bash
mkdir student_management_api
cd student_management_api
```

### שלב 3: יצירת סביבה וירטואלית (מומלץ)

```bash
# יצירת סביבה וירטואלית
python -m venv venv

# הפעלת הסביבה
# ב-Windows:
venv\Scripts\activate

# ב-Mac/Linux:
source venv/bin/activate
```

### שלב 4: התקנת הספריות הנדרשות

```bash
pip install fastapi uvicorn
```

**הסבר הספריות:**
- `fastapi` - הפריימוורק לבניית ה-API
- `uvicorn` - שרת ASGI להרצת FastAPI
- `csv` ו-`sqlite3` - מובנות ב-Python, אין צורך בהתקנה

### שלב 5: יצירת קובץ requirements.txt

```bash
pip freeze > requirements.txt
```

---

## חלק 1: עבודה עם CSV

### 1.1 יצירת קובץ CSV לדוגמה

צור קובץ `students.csv`:

```csv
id,name,age,grade,email,city
1,דני כהן,20,85,dani@example.com,תל אביב
2,שרה לוי,22,92,sara@example.com,ירושלים
3,יוסי ישראלי,21,78,yossi@example.com,חיפה
4,רחל אברהם,23,88,rachel@example.com,באר שבע
5,משה דוד,20,95,moshe@example.com,נתניה
```

### 1.2 קריאת CSV עם Python

צור קובץ `csv_reader.py`:

```python
import csv

def read_students_csv(filename='students.csv'):
    """קריאת קובץ CSV של תלמידים"""
    students = []
    
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                students.append(row)
        
        print(f"✓ נקראו {len(students)} תלמידים מהקובץ")
        return students
    
    except FileNotFoundError:
        print(f"✗ הקובץ {filename} לא נמצא")
        return []
    except Exception as e:
        print(f"✗ שגיאה: {e}")
        return []

# בדיקה
if __name__ == "__main__":
    students = read_students_csv()
    
    # הדפסת התלמידים
    for student in students:
        print(f"{student['name']} - ציון: {student['grade']}")
```

**הרץ את הקובץ:**
```bash
python csv_reader.py
```

### 1.3 כתיבת CSV

צור קובץ `csv_writer.py`:

```python
import csv

def write_students_csv(students, filename='students_new.csv'):
    """כתיבת רשימת תלמידים ל-CSV"""
    
    if not students:
        print("אין תלמידים לכתוב")
        return
    
    fieldnames = ['id', 'name', 'age', 'grade', 'email', 'city']
    
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(students)
        
        print(f"✓ {len(students)} תלמידים נשמרו בקובץ {filename}")
    
    except Exception as e:
        print(f"✗ שגיאה בשמירה: {e}")

# דוגמה לשימוש
if __name__ == "__main__":
    students = [
        {'id': 1, 'name': 'אלי', 'age': 21, 'grade': 90, 'email': 'eli@example.com', 'city': 'רמת גן'},
        {'id': 2, 'name': 'מיכל', 'age': 22, 'grade': 87, 'email': 'michal@example.com', 'city': 'פתח תקווה'}
    ]
    
    write_students_csv(students)
```

---

## חלק 2: SQLite - מסד נתונים

### 2.1 יצירת מסד נתונים ראשון

צור קובץ `database.py`:

```python
import sqlite3

def create_database():
    """יצירת מסד נתונים וטבלת תלמידים"""
    
    # חיבור למסד נתונים (ייווצר אם לא קיים)
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    
    # יצירת טבלה
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            grade INTEGER,
            email TEXT UNIQUE,
            city TEXT
        )
    ''')
    
    conn.commit()
    conn.close()
    
    print("✓ מסד נתונים נוצר בהצלחה")

if __name__ == "__main__":
    create_database()
```

**הסבר על הטבלה:**
- `id` - מזהה ייחודי (מתעדכן אוטומטית)
- `PRIMARY KEY` - מפתח ראשי
- `AUTOINCREMENT` - עלייה אוטומטית
- `NOT NULL` - שדה חובה
- `UNIQUE` - ערך ייחודי (אין שני אימיילים זהים)

### 2.2 פעולות CRUD בסיסיות

צור קובץ `db_operations.py`:

```python
import sqlite3

class StudentDB:
    """מחלקה לניהול מסד נתונים של תלמידים"""
    
    def __init__(self, db_name='students.db'):
        self.db_name = db_name
        self.create_table()
    
    def create_table(self):
        """יצירת הטבלה"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER,
                grade INTEGER,
                email TEXT UNIQUE,
                city TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_student(self, name, age, grade, email, city):
        """הוספת תלמיד חדש"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO students (name, age, grade, email, city)
                VALUES (?, ?, ?, ?, ?)
            ''', (name, age, grade, email, city))
            
            conn.commit()
            student_id = cursor.lastrowid
            print(f"✓ תלמיד נוסף בהצלחה (ID: {student_id})")
            return student_id
        
        except sqlite3.IntegrityError:
            print(f"✗ האימייל {email} כבר קיים במערכת")
            return None
        
        finally:
            conn.close()
    
    def get_all_students(self):
        """קבלת כל התלמידים"""
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row  # להחזיר כמילון
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM students')
        students = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        return students
    
    def get_student_by_id(self, student_id):
        """קבלת תלמיד לפי ID"""
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM students WHERE id = ?', (student_id,))
        student = cursor.fetchone()
        
        conn.close()
        return dict(student) if student else None
    
    def update_student(self, student_id, name=None, age=None, grade=None, email=None, city=None):
        """עדכון פרטי תלמיד"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # בניית שאילתת UPDATE דינמית
        updates = []
        params = []
        
        if name:
            updates.append("name = ?")
            params.append(name)
        if age:
            updates.append("age = ?")
            params.append(age)
        if grade:
            updates.append("grade = ?")
            params.append(grade)
        if email:
            updates.append("email = ?")
            params.append(email)
        if city:
            updates.append("city = ?")
            params.append(city)
        
        if not updates:
            print("אין מה לעדכן")
            conn.close()
            return False
        
        params.append(student_id)
        query = f"UPDATE students SET {', '.join(updates)} WHERE id = ?"
        
        cursor.execute(query, params)
        conn.commit()
        
        updated = cursor.rowcount > 0
        conn.close()
        
        if updated:
            print(f"✓ תלמיד {student_id} עודכן בהצלחה")
        else:
            print(f"✗ תלמיד {student_id} לא נמצא")
        
        return updated
    
    def delete_student(self, student_id):
        """מחיקת תלמיד"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM students WHERE id = ?', (student_id,))
        conn.commit()
        
        deleted = cursor.rowcount > 0
        conn.close()
        
        if deleted:
            print(f"✓ תלמיד {student_id} נמחק")
        else:
            print(f"✗ תלמיד {student_id} לא נמצא")
        
        return deleted

# בדיקה
if __name__ == "__main__":
    db = StudentDB()
    
    # הוספת תלמידים
    db.add_student('דני', 20, 85, 'dani@example.com', 'תל אביב')
    db.add_student('שרה', 22, 92, 'sara@example.com', 'ירושלים')
    
    # הצגת כל התלמידים
    students = db.get_all_students()
    print(f"\nסה\"כ תלמידים: {len(students)}")
    for s in students:
        print(f"- {s['name']}, גיל {s['age']}, ציון {s['grade']}")
    
    # עדכון תלמיד
    db.update_student(1, grade=90)
    
    # מחיקת תלמיד
    # db.delete_student(2)
```

### 2.3 ייבוא נתונים מ-CSV ל-SQLite

צור קובץ `csv_to_db.py`:

```python
import csv
import sqlite3
from db_operations import StudentDB

def import_csv_to_db(csv_file='students.csv'):
    """ייבוא נתונים מ-CSV למסד נתונים"""
    
    db = StudentDB()
    
    try:
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            count = 0
            for row in reader:
                student_id = db.add_student(
                    name=row['name'],
                    age=int(row['age']),
                    grade=int(row['grade']),
                    email=row['email'],
                    city=row['city']
                )
                if student_id:
                    count += 1
            
            print(f"\n✓ סה\"כ יובאו {count} תלמידים")
    
    except FileNotFoundError:
        print(f"✗ הקובץ {csv_file} לא נמצא")
    except Exception as e:
        print(f"✗ שגיאה: {e}")

if __name__ == "__main__":
    import_csv_to_db()
```

### 2.4 ייצוא נתונים מ-SQLite ל-CSV

צור קובץ `db_to_csv.py`:

```python
import csv
from db_operations import StudentDB

def export_db_to_csv(output_file='students_export.csv'):
    """ייצוא נתונים ממסד הנתונים ל-CSV"""
    
    db = StudentDB()
    students = db.get_all_students()
    
    if not students:
        print("אין תלמידים לייצא")
        return
    
    fieldnames = ['id', 'name', 'age', 'grade', 'email', 'city']
    
    try:
        with open(output_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(students)
        
        print(f"✓ {len(students)} תלמידים יוצאו ל-{output_file}")
    
    except Exception as e:
        print(f"✗ שגיאה: {e}")

if __name__ == "__main__":
    export_db_to_csv()
```

---

## חלק 3: FastAPI - בניית API

### 3.1 FastAPI בסיסי - Hello World

צור קובץ `main.py`:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "שלום! ברוך הבא ל-API של ניהול תלמידים"}

@app.get("/hello/{name}")
def say_hello(name: str):
    return {"message": f"שלום {name}!"}
```

**הרץ את השרת:**
```bash
uvicorn main:app --reload
```

**בדוק ב-דפדפן:**
- `http://localhost:8000` - עמוד הבית
- `http://localhost:8000/docs` - תיעוד אוטומטי (Swagger UI)
- `http://localhost:8000/redoc` - תיעוד חלופי

### 3.2 הוספת מודלים (Pydantic)

עדכן את `main.py`:

```python
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr
from typing import Optional

app = FastAPI(title="Student Management API", version="1.0")

# מודל לתלמיד
class Student(BaseModel):
    name: str
    age: int
    grade: int
    email: str
    city: str

class StudentUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    grade: Optional[int] = None
    email: Optional[str] = None
    city: Optional[str] = None

@app.get("/")
def read_root():
    return {"message": "Student Management API", "version": "1.0"}

# נבדוק שהמודל עובד
@app.post("/test-student")
def test_student(student: Student):
    return {
        "message": "קיבלתי את הנתונים",
        "student": student
    }
```

**בדיקה:**
גש ל-`http://localhost:8000/docs` ונסה להוסיף תלמיד דרך ממשק ה-Swagger.

### 3.3 חיבור FastAPI ל-SQLite

צור קובץ `main.py` מלא:

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from db_operations import StudentDB

app = FastAPI(
    title="Student Management API",
    description="API לניהול תלמידים עם SQLite",
    version="1.0"
)

# יצירת מופע של מסד הנתונים
db = StudentDB()

# מודלים
class StudentCreate(BaseModel):
    name: str
    age: int
    grade: int
    email: str
    city: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "דני כהן",
                "age": 20,
                "grade": 85,
                "email": "dani@example.com",
                "city": "תל אביב"
            }
        }

class StudentUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    grade: Optional[int] = None
    email: Optional[str] = None
    city: Optional[str] = None

class StudentResponse(BaseModel):
    id: int
    name: str
    age: int
    grade: int
    email: str
    city: str

# נתיבי API

@app.get("/", tags=["General"])
def read_root():
    """עמוד הבית"""
    return {
        "message": "Student Management API",
        "version": "1.0",
        "endpoints": {
            "docs": "/docs",
            "students": "/students"
        }
    }

@app.post("/students", response_model=dict, tags=["Students"])
def create_student(student: StudentCreate):
    """הוספת תלמיד חדש"""
    student_id = db.add_student(
        name=student.name,
        age=student.age,
        grade=student.grade,
        email=student.email,
        city=student.city
    )
    
    if student_id:
        return {
            "message": "תלמיד נוסף בהצלחה",
            "student_id": student_id
        }
    else:
        raise HTTPException(status_code=400, detail="האימייל כבר קיים במערכת")

@app.get("/students", response_model=List[StudentResponse], tags=["Students"])
def get_all_students():
    """קבלת כל התלמידים"""
    students = db.get_all_students()
    return students

@app.get("/students/{student_id}", response_model=StudentResponse, tags=["Students"])
def get_student(student_id: int):
    """קבלת תלמיד לפי ID"""
    student = db.get_student_by_id(student_id)
    
    if student:
        return student
    else:
        raise HTTPException(status_code=404, detail="תלמיד לא נמצא")

@app.put("/students/{student_id}", tags=["Students"])
def update_student(student_id: int, student: StudentUpdate):
    """עדכון פרטי תלמיד"""
    updated = db.update_student(
        student_id=student_id,
        name=student.name,
        age=student.age,
        grade=student.grade,
        email=student.email,
        city=student.city
    )
    
    if updated:
        return {"message": "תלמיד עודכן בהצלחה"}
    else:
        raise HTTPException(status_code=404, detail="תלמיד לא נמצא")

@app.delete("/students/{student_id}", tags=["Students"])
def delete_student(student_id: int):
    """מחיקת תלמיד"""
    deleted = db.delete_student(student_id)
    
    if deleted:
        return {"message": "תלמיד נמחק בהצלחה"}
    else:
        raise HTTPException(status_code=404, detail="תלמיד לא נמצא")
```

**הרץ את השרת:**
```bash
uvicorn main:app --reload
```

**נסה את ה-API:**
1. גש ל-`http://localhost:8000/docs`
2. נסה להוסיף תלמידים
3. קבל רשימת תלמידים
4. עדכן תלמיד
5. מחק תלמיד

---

## חלק 4: פרויקט מלא - מערכת ניהול תלמידים

### 4.1 מבנה הפרויקט

```
student_management_api/
│
├── main.py              # נתיבי FastAPI
├── database.py          # הגדרת מסד הנתונים
├── models.py            # מודלי Pydantic
├── crud.py              # פעולות CRUD
├── csv_utils.py         # עזרים ל-CSV
├── students.csv         # קובץ CSV לדוגמה
├── students.db          # מסד נתונים SQLite
└── requirements.txt     # תלויות
```

### 4.2 קובץ `models.py` - מודלים

```python
from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class StudentBase(BaseModel):
    """מודל בסיס לתלמיד"""
    name: str = Field(..., min_length=2, max_length=100)
    age: int = Field(..., ge=18, le=100)
    grade: int = Field(..., ge=0, le=100)
    email: str
    city: str = Field(..., min_length=2)

class StudentCreate(StudentBase):
    """מודל ליצירת תלמיד חדש"""
    pass

class StudentUpdate(BaseModel):
    """מודל לעדכון תלמיד"""
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    age: Optional[int] = Field(None, ge=18, le=100)
    grade: Optional[int] = Field(None, ge=0, le=100)
    email: Optional[str] = None
    city: Optional[str] = Field(None, min_length=2)

class StudentResponse(StudentBase):
    """מודל לתגובה"""
    id: int
    
    class Config:
        from_attributes = True
```

### 4.3 קובץ `crud.py` - פעולות מסד נתונים

```python
import sqlite3
from typing import List, Optional

class StudentCRUD:
    """מחלקה לפעולות CRUD על תלמידים"""
    
    def __init__(self, db_name: str = "students.db"):
        self.db_name = db_name
        self.init_db()
    
    def init_db(self):
        """אתחול מסד הנתונים"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                grade INTEGER NOT NULL,
                email TEXT UNIQUE NOT NULL,
                city TEXT NOT NULL
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def create(self, name: str, age: int, grade: int, email: str, city: str) -> Optional[int]:
        """יצירת תלמיד חדש"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO students (name, age, grade, email, city)
                VALUES (?, ?, ?, ?, ?)
            ''', (name, age, grade, email, city))
            
            conn.commit()
            return cursor.lastrowid
        
        except sqlite3.IntegrityError:
            return None
        
        finally:
            conn.close()
    
    def get_all(self) -> List[dict]:
        """קבלת כל התלמידים"""
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM students ORDER BY id')
        students = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        return students
    
    def get_by_id(self, student_id: int) -> Optional[dict]:
        """קבלת תלמיד לפי ID"""
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM students WHERE id = ?', (student_id,))
        student = cursor.fetchone()
        
        conn.close()
        return dict(student) if student else None
    
    def update(self, student_id: int, **kwargs) -> bool:
        """עדכון תלמיד"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # סינון ערכים None
        updates = {k: v for k, v in kwargs.items() if v is not None}
        
        if not updates:
            conn.close()
            return False
        
        # בניית שאילתה
        set_clause = ', '.join([f"{k} = ?" for k in updates.keys()])
        values = list(updates.values()) + [student_id]
        
        cursor.execute(f'UPDATE students SET {set_clause} WHERE id = ?', values)
        conn.commit()
        
        updated = cursor.rowcount > 0
        conn.close()
        
        return updated
    
    def delete(self, student_id: int) -> bool:
        """מחיקת תלמיד"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM students WHERE id = ?', (student_id,))
        conn.commit()
        
        deleted = cursor.rowcount > 0
        conn.close()
        
        return deleted
    
    def search(self, **criteria) -> List[dict]:
        """חיפוש תלמידים לפי קריטריונים"""
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        conditions = []
        values = []
        
        for key, value in criteria.items():
            if value is not None:
                conditions.append(f"{key} = ?")
                values.append(value)
        
        if conditions:
            query = f"SELECT * FROM students WHERE {' AND '.join(conditions)}"
            cursor.execute(query, values)
        else:
            cursor.execute('SELECT * FROM students')
        
        students = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return students
```

### 4.4 קובץ `csv_utils.py` - פונקציות CSV

```python
import csv
from typing import List
from crud import StudentCRUD

def import_csv(filename: str = "students.csv") -> dict:
    """ייבוא נתונים מ-CSV"""
    crud = StudentCRUD()
    
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            success = 0
            failed = 0
            
            for row in reader:
                student_id = crud.create(
                    name=row['name'],
                    age=int(row['age']),
                    grade=int(row['grade']),
                    email=row['email'],
                    city=row['city']
                )
                
                if student_id:
                    success += 1
                else:
                    failed += 1
            
            return {
                "success": success,
                "failed": failed,
                "total": success + failed
            }
    
    except FileNotFoundError:
        return {"error": f"הקובץ {filename} לא נמצא"}
    except Exception as e:
        return {"error": str(e)}

def export_csv(filename: str = "students_export.csv") -> dict:
    """ייצוא נתונים ל-CSV"""
    crud = StudentCRUD()
    students = crud.get_all()
    
    if not students:
        return {"error": "אין תלמידים לייצא"}
    
    try:
        fieldnames = ['id', 'name', 'age', 'grade', 'email', 'city']
        
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(students)
        
        return {
            "success": True,
            "count": len(students),
            "filename": filename
        }
    
    except Exception as e:
        return {"error": str(e)}
```

### 4.5 קובץ `main.py` המלא

```python
from fastapi import FastAPI, HTTPException, Query
from typing import List, Optional
from models import StudentCreate, StudentUpdate, StudentResponse
from crud import StudentCRUD
from csv_utils import import_csv, export_csv

app = FastAPI(
    title="Student Management API",
    description="מערכת ניהול תלמידים עם CSV ו-SQLite",
    version="2.0"
)

crud = StudentCRUD()

# ===== נתיבי API בסיסיים =====

@app.get("/", tags=["General"])
def root():
    """עמוד הבית"""
    return {
        "message": "Student Management API v2.0",
        "features": [
            "ניהול תלמידים (CRUD)",
            "ייבוא מ-CSV",
            "ייצוא ל-CSV",
            "חיפוש מתקדם"
        ],
        "docs": "/docs"
    }

# ===== ניהול תלמידים =====

@app.post("/students", response_model=dict, status_code=201, tags=["Students"])
def create_student(student: StudentCreate):
    """יצירת תלמיד חדש"""
    student_id = crud.create(
        name=student.name,
        age=student.age,
        grade=student.grade,
        email=student.email,
        city=student.city
    )
    
    if student_id:
        return {
            "message": "תלמיד נוסף בהצלחה",
            "id": student_id
        }
    else:
        raise HTTPException(
            status_code=400,
            detail="האימייל כבר קיים במערכת"
        )

@app.get("/students", response_model=List[StudentResponse], tags=["Students"])
def get_students(
    city: Optional[str] = Query(None, description="סינון לפי עיר"),
    min_grade: Optional[int] = Query(None, ge=0, le=100, description="ציון מינימלי")
):
    """קבלת כל התלמידים (עם אפשרות סינון)"""
    students = crud.get_all()
    
    # סינון לפי עיר
    if city:
        students = [s for s in students if s['city'] == city]
    
    # סינון לפי ציון מינימלי
    if min_grade is not None:
        students = [s for s in students if s['grade'] >= min_grade]
    
    return students

@app.get("/students/{student_id}", response_model=StudentResponse, tags=["Students"])
def get_student(student_id: int):
    """קבלת תלמיד לפי ID"""
    student = crud.get_by_id(student_id)
    
    if not student:
        raise HTTPException(status_code=404, detail="תלמיד לא נמצא")
    
    return student

@app.put("/students/{student_id}", tags=["Students"])
def update_student(student_id: int, student: StudentUpdate):
    """עדכון פרטי תלמיד"""
    updated = crud.update(
        student_id,
        name=student.name,
        age=student.age,
        grade=student.grade,
        email=student.email,
        city=student.city
    )
    
    if not updated:
        raise HTTPException(status_code=404, detail="תלמיד לא נמצא")
    
    return {"message": "תלמיד עודכן בהצלחה"}

@app.delete("/students/{student_id}", tags=["Students"])
def delete_student(student_id: int):
    """מחיקת תלמיד"""
    deleted = crud.delete(student_id)
    
    if not deleted:
        raise HTTPException(status_code=404, detail="תלמיד לא נמצא")
    
    return {"message": "תלמיד נמחק בהצלחה"}

# ===== פעולות CSV =====

@app.post("/import-csv", tags=["CSV"])
def import_from_csv(filename: str = Query("students.csv", description="שם קובץ ה-CSV")):
    """ייבוא תלמידים מקובץ CSV"""
    result = import_csv(filename)
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    
    return result

@app.get("/export-csv", tags=["CSV"])
def export_to_csv(filename: str = Query("students_export.csv", description="שם קובץ היעד")):
    """ייצוא תלמידים לקובץ CSV"""
    result = export_csv(filename)
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    
    return result

# ===== סטטיסטיקות =====

@app.get("/statistics", tags=["Statistics"])
def get_statistics():
    """סטטיסטיקות כלליות"""
    students = crud.get_all()
    
    if not students:
        return {"message": "אין תלמידים במערכת"}
    
    grades = [s['grade'] for s in students]
    cities = {}
    
    for student in students:
        city = student['city']
        cities[city] = cities.get(city, 0) + 1
    
    return {
        "total_students": len(students),
        "average_grade": sum(grades) / len(grades),
        "max_grade": max(grades),
        "min_grade": min(grades),
        "students_by_city": cities
    }
```

### 4.6 הרצת הפרויקט המלא

```bash
# וודא שכל הקבצים במקום
# הרץ את השרת
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**בדיקת ה-API:**

1. **גש לתיעוד:** `http://localhost:8000/docs`

2. **ייבא נתונים מ-CSV:**
   - POST `/import-csv?filename=students.csv`

3. **הצג תלמידים:**
   - GET `/students`

4. **הוסף תלמיד חדש:**
   - POST `/students`
   ```json
   {
     "name": "אלי כהן",
     "age": 21,
     "grade": 90,
     "email": "eli@example.com",
     "city": "רמת גן"
   }
   ```

5. **סטטיסטיקות:**
   - GET `/statistics`

6. **ייצא ל-CSV:**
   - GET `/export-csv?filename=output.csv`

---

## חלק 5: פרויקט מתקדם - מערכת ניהול מוצרים

### 5.1 מבנה המוצר

צור קובץ `products.csv`:

```csv
id,name,price,quantity,category,supplier
1,לפטופ Dell,3500.00,10,מחשבים,Dell Inc
2,עכבר Logitech,80.00,50,אביזרים,Logitech
3,מקלדת מכנית,350.00,25,אביזרים,Corsair
4,מסך 27 אינץ,1200.00,15,מסכים,LG
5,כבל HDMI,45.00,100,כבלים,AmazonBasics
```

### 5.2 API למוצרים - `products_api.py`

```python
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from typing import List, Optional
import sqlite3
import csv

app = FastAPI(title="Product Management API", version="1.0")

# === מודלים ===

class Product(BaseModel):
    name: str = Field(..., min_length=2)
    price: float = Field(..., gt=0)
    quantity: int = Field(..., ge=0)
    category: str
    supplier: str

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    quantity: Optional[int] = Field(None, ge=0)
    category: Optional[str] = None
    supplier: Optional[str] = None

class ProductResponse(Product):
    id: int

# === מסד נתונים ===

def init_db():
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            quantity INTEGER NOT NULL,
            category TEXT NOT NULL,
            supplier TEXT NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()

init_db()

# === נתיבי API ===

@app.post("/products", status_code=201)
def create_product(product: Product):
    """הוספת מוצר חדש"""
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO products (name, price, quantity, category, supplier)
        VALUES (?, ?, ?, ?, ?)
    ''', (product.name, product.price, product.quantity, product.category, product.supplier))
    
    conn.commit()
    product_id = cursor.lastrowid
    conn.close()
    
    return {"message": "מוצר נוסף בהצלחה", "id": product_id}

@app.get("/products", response_model=List[ProductResponse])
def get_products(
    category: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None
):
    """קבלת כל המוצרים עם סינון"""
    conn = sqlite3.connect('products.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    query = "SELECT * FROM products WHERE 1=1"
    params = []
    
    if category:
        query += " AND category = ?"
        params.append(category)
    
    if min_price is not None:
        query += " AND price >= ?"
        params.append(min_price)
    
    if max_price is not None:
        query += " AND price <= ?"
        params.append(max_price)
    
    cursor.execute(query, params)
    products = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return products

@app.get("/products/low-stock")
def get_low_stock(threshold: int = Query(10, description="סף מלאי נמוך")):
    """מוצרים עם מלאי נמוך"""
    conn = sqlite3.connect('products.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM products WHERE quantity < ?', (threshold,))
    products = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return {
        "threshold": threshold,
        "count": len(products),
        "products": products
    }

@app.put("/products/{product_id}/quantity")
def update_quantity(product_id: int, quantity: int):
    """עדכון כמות במלאי"""
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    
    cursor.execute('UPDATE products SET quantity = ? WHERE id = ?', (quantity, product_id))
    conn.commit()
    
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="מוצר לא נמצא")
    
    conn.close()
    return {"message": "כמות עודכנה בהצלחה"}

@app.get("/products/categories")
def get_categories():
    """קבלת רשימת קטגוריות"""
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT DISTINCT category FROM products')
    categories = [row[0] for row in cursor.fetchall()]
    conn.close()
    
    return {"categories": categories}

@app.post("/import-csv")
def import_products_csv(filename: str = "products.csv"):
    """ייבוא מוצרים מ-CSV"""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            conn = sqlite3.connect('products.db')
            cursor = conn.cursor()
            
            count = 0
            for row in reader:
                cursor.execute('''
                    INSERT INTO products (name, price, quantity, category, supplier)
                    VALUES (?, ?, ?, ?, ?)
                ''', (row['name'], float(row['price']), int(row['quantity']), 
                      row['category'], row['supplier']))
                count += 1
            
            conn.commit()
            conn.close()
            
            return {"message": f"{count} מוצרים יובאו בהצלחה"}
    
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"הקובץ {filename} לא נמצא")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/export-csv")
def export_products_csv(filename: str = "products_export.csv"):
    """ייצוא מוצרים ל-CSV"""
    conn = sqlite3.connect('products.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM products')
    products = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    if not products:
        raise HTTPException(status_code=404, detail="אין מוצרים לייצא")
    
    fieldnames = ['id', 'name', 'price', 'quantity', 'category', 'supplier']
    
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(products)
    
    return {
        "message": f"{len(products)} מוצרים יוצאו ל-{filename}",
        "count": len(products)
    }

@app.get("/statistics")
def get_statistics():
    """סטטיסטיקות מוצרים"""
    conn = sqlite3.connect('products.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM products')
    products = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    if not products:
        return {"message": "אין מוצרים במערכת"}
    
    total_value = sum(p['price'] * p['quantity'] for p in products)
    categories = {}
    
    for p in products:
        cat = p['category']
        if cat not in categories:
            categories[cat] = {'count': 0, 'value': 0}
        categories[cat]['count'] += 1
        categories[cat]['value'] += p['price'] * p['quantity']
    
    return {
        "total_products": len(products),
        "total_inventory_value": round(total_value, 2),
        "categories": categories,
        "average_price": round(sum(p['price'] for p in products) / len(products), 2)
    }
```

**הרץ:**
```bash
uvicorn products_api:app --reload --port 8001
```

**גש ל:** `http://localhost:8001/docs`

---

## טיפים ושגיאות נפוצות

### שגיאות נפוצות ופתרונות

#### 1. UnicodeDecodeError
**בעיה:** קידוד לא נכון לעברית

**פתרון:**
```python
with open('file.csv', 'r', encoding='utf-8') as file:
    # תמיד להשתמש ב-utf-8
```

#### 2. ModuleNotFoundError: No module named 'fastapi'
**בעיה:** FastAPI לא מותקן

**פתרון:**
```bash
pip install fastapi uvicorn
```

#### 3. sqlite3.IntegrityError
**בעיה:** ניסיון להכניס ערך כפול (UNIQUE)

**פתרון:**
```python
try:
    cursor.execute("INSERT ...")
except sqlite3.IntegrityError:
    print("הערך כבר קיים")
```

#### 4. שרת FastAPI לא עולה
**בעיה:** פורט תפוס

**פתרון:**
```bash
# שנה את הפורט
uvicorn main:app --reload --port 8001
```

### טיפים לביצועים

1. **השתמש ב-executemany להכנסות מרובות:**
```python
cursor.executemany("INSERT INTO students VALUES (?, ?, ?)", data)
```

2. **סגור חיבורים תמיד:**
```python
try:
    conn = sqlite3.connect('db.db')
    # עבודה...
finally:
    conn.close()
```

3. **השתמש ב-Context Manager:**
```python
with sqlite3.connect('db.db') as conn:
    cursor = conn.cursor()
    # עבודה...
    # commit אוטומטי
```

### Best Practices

1. **Validation עם Pydantic:**
```python
class Student(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    age: int = Field(..., ge=18, le=120)
```

2. **Error Handling:**
```python
@app.get("/students/{id}")
def get_student(id: int):
    student = db.get(id)
    if not student:
        raise HTTPException(status_code=404, detail="לא נמצא")
    return student
```

3. **תיעוד API:**
```python
@app.post("/students", tags=["Students"], summary="הוספת תלמיד")
def create_student(student: Student):
    """
    הוספת תלמיד חדש למערכת.
    
    - **name**: שם מלא
    - **age**: גיל (18-120)
    - **grade**: ציון (0-100)
    """
    pass
```

---

## סיכום

### מה למדנו:
✅ עבודה עם קבצי CSV  
✅ ניהול מסד נתונים SQLite  
✅ בניית REST API עם FastAPI  
✅ פעולות CRUD מלאות  
✅ ייבוא/ייצוא נתונים  
✅ סינון וחיפוש  
✅ סטטיסטיקות וניתוח נתונים  

### צעדים הבאים:
1. הוסף אימות משתמשים (JWT)
2. הוסף pagination לרשימות גדולות
3. שדרג ל-PostgreSQL/MySQL לפרודקשן
4. הוסף Logging
5. כתוב בדיקות (Tests)
6. Deploy ל-Cloud (Heroku, AWS, etc.)

### משאבים נוספים:
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLite Tutorial](https://www.sqlitetutorial.net/)
- [Python CSV Documentation](https://docs.python.org/3/library/csv.html)

**בהצלחה! 🚀**
