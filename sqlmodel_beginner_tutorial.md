# מדריך למתחילים - SQLModel

## מהו SQLModel?
SQLModel הוא ספרייה של Python המשלבת בין SQLAlchemy (לעבודה עם בסיסי נתונים) ל-Pydantic (לאימות נתונים). הוא מאפשר לנו לעבוד עם בסיסי נתונים בצורה קלה ובטוחה, תוך שימוש בקוד Python פשוט.

---

## שלב 1: התקנה

ראשית, נתקין את SQLModel:

```bash
pip install sqlmodel
```

---

## שלב 2: יצירת מודל ראשון

מודל הוא מחלקה שמייצגת טבלה בבסיס הנתונים.

**דוגמה - מחלקת Student:**

```python
from sqlmodel import SQLModel, Field
from typing import Optional

class Student(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    age: int
    grade: float
```

**הסבר:**
- `SQLModel` - המחלקה הבסיסית
- `table=True` - אומר לSQLModel שזו טבלה בבסיס הנתונים
- `Field(default=None, primary_key=True)` - מגדיר מפתח ראשי שמתמלא אוטומטית
- `Optional[int]` - אומר שהשדה יכול להיות None (לפני שנשמור)

---

## שלב 3: יצירת בסיס נתונים והתחברות

```python
from sqlmodel import SQLModel, create_engine

# יצירת מנוע התחברות (SQLite בדוגמה זו)
engine = create_engine("sqlite:///students.db")

# יצירת כל הטבלאות
SQLModel.metadata.create_all(engine)
```

**הסבר:**
- `create_engine` - יוצר חיבור לבסיס הנתונים
- `sqlite:///students.db` - בסיס נתונים מקומי (קובץ)
- `create_all` - יוצר את כל הטבלאות שהגדרנו

---

## שלב 4: הוספת נתונים (Create)

```python
from sqlmodel import Session

# יצירת תלמיד חדש
student1 = Student(name="יוסי כהן", age=15, grade=85.5)
student2 = Student(name="שרה לוי", age=16, grade=92.0)

# שמירה בבסיס הנתונים
with Session(engine) as session:
    session.add(student1)
    session.add(student2)
    session.commit()
    print("התלמידים נוספו בהצלחה!")
```

**הסבר:**
- `Session` - פותח חיבור לבסיס הנתונים
- `add` - מוסיף אובייקט לסשן
- `commit` - שומר את השינויים בפועל

---

## שלב 5: קריאת נתונים (Read)

### קריאת כל התלמידים:

```python
from sqlmodel import Session, select

with Session(engine) as session:
    statement = select(Student)
    students = session.exec(statement).all()
    
    for student in students:
        print(f"ID: {student.id}, שם: {student.name}, גיל: {student.age}, ציון: {student.grade}")
```

### קריאת תלמיד ספציפי לפי ID:

```python
with Session(engine) as session:
    student = session.get(Student, 1)  # ID = 1
    if student:
        print(f"נמצא: {student.name}")
```

### סינון תלמידים:

```python
with Session(engine) as session:
    # תלמידים מעל גיל 15
    statement = select(Student).where(Student.age > 15)
    students = session.exec(statement).all()
    
    for student in students:
        print(student.name)
```

---

## שלב 6: עדכון נתונים (Update)

```python
with Session(engine) as session:
    # מוצאים תלמיד
    student = session.get(Student, 1)
    
    if student:
        # משנים את הציון
        student.grade = 95.0
        
        # שומרים את השינוי
        session.add(student)
        session.commit()
        print(f"הציון של {student.name} עודכן!")
```

---

## שלב 7: מחיקת נתונים (Delete)

```python
with Session(engine) as session:
    # מוצאים תלמיד
    student = session.get(Student, 1)
    
    if student:
        # מחיקה
        session.delete(student)
        session.commit()
        print(f"{student.name} נמחק מהמערכת")
```

---

## שלב 8: דוגמה מלאה - מערכת ניהול תלמידים

```python
from sqlmodel import SQLModel, Field, create_engine, Session, select
from typing import Optional

# הגדרת המודל
class Student(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    age: int
    grade: float

# יצירת בסיס נתונים
engine = create_engine("sqlite:///school.db")
SQLModel.metadata.create_all(engine)

# פונקציה להוספת תלמיד
def add_student(name: str, age: int, grade: float):
    with Session(engine) as session:
        student = Student(name=name, age=age, grade=grade)
        session.add(student)
        session.commit()
        print(f"✓ התלמיד {name} נוסף בהצלחה!")

# פונקציה להצגת כל התלמידים
def show_all_students():
    with Session(engine) as session:
        students = session.exec(select(Student)).all()
        print("\n=== רשימת התלמידים ===")
        for student in students:
            print(f"ID: {student.id} | שם: {student.name} | גיל: {student.age} | ציון: {student.grade}")

# פונקציה לעדכון ציון
def update_grade(student_id: int, new_grade: float):
    with Session(engine) as session:
        student = session.get(Student, student_id)
        if student:
            student.grade = new_grade
            session.add(student)
            session.commit()
            print(f"✓ הציון של {student.name} עודכן ל-{new_grade}")
        else:
            print("✗ תלמיד לא נמצא")

# פונקציה למחיקת תלמיד
def delete_student(student_id: int):
    with Session(engine) as session:
        student = session.get(Student, student_id)
        if student:
            name = student.name
            session.delete(student)
            session.commit()
            print(f"✓ התלמיד {name} נמחק")
        else:
            print("✗ תלמיד לא נמצא")

# שימוש במערכת
if __name__ == "__main__":
    # הוספת תלמידים
    add_student("דני כהן", 15, 88.5)
    add_student("מיכל לוי", 16, 95.0)
    add_student("עומר מזרחי", 15, 78.0)
    
    # הצגת כולם
    show_all_students()
    
    # עדכון ציון
    update_grade(1, 92.0)
    
    # הצגה אחרי עדכון
    show_all_students()
    
    # מחיקת תלמיד
    delete_student(2)
    
    # הצגה אחרי מחיקה
    show_all_students()
```

---

## שלב 9: קשרים בין טבלאות (Relationships)

### דוגמה - תלמידים וכיתות:

```python
from sqlmodel import SQLModel, Field, Relationship, create_engine, Session
from typing import Optional, List

class Classroom(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    
    # קשר לתלמידים
    students: List["Student"] = Relationship(back_populates="classroom")

class Student(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    age: int
    grade: float
    
    # מפתח זר לכיתה
    classroom_id: Optional[int] = Field(default=None, foreign_key="classroom.id")
    
    # קשר לכיתה
    classroom: Optional[Classroom] = Relationship(back_populates="students")

# יצירת בסיס נתונים
engine = create_engine("sqlite:///school_with_classes.db")
SQLModel.metadata.create_all(engine)

# שימוש
with Session(engine) as session:
    # יצירת כיתה
    class_a = Classroom(name="כיתה א'")
    session.add(class_a)
    session.commit()
    session.refresh(class_a)  # לקבל את ה-ID
    
    # הוספת תלמידים לכיתה
    student1 = Student(name="יוסי", age=15, grade=85.5, classroom_id=class_a.id)
    student2 = Student(name="שרה", age=15, grade=92.0, classroom_id=class_a.id)
    
    session.add(student1)
    session.add(student2)
    session.commit()
    
    # קריאת כיתה עם התלמידים שלה
    classroom = session.get(Classroom, class_a.id)
    print(f"\nכיתה: {classroom.name}")
    print("תלמידים:")
    for student in classroom.students:
        print(f"  - {student.name}, ציון: {student.grade}")
```

---

## שלב 10: טיפים חשובים

### 1. שימוש ב-Optional
```python
# שדה שחייב להיות (לא יכול להיות None)
name: str

# שדה שיכול להיות None
email: Optional[str] = None
```

### 2. ערכי ברירת מחדל
```python
class Student(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    is_active: bool = True  # ברירת מחדל
    created_at: str = Field(default_factory=lambda: str(datetime.now()))
```

### 3. אילוצים על שדות
```python
from sqlmodel import Field

class Student(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(min_length=2, max_length=50)
    age: int = Field(ge=5, le=120)  # גיל בין 5 ל-120
    grade: float = Field(ge=0, le=100)  # ציון בין 0 ל-100
```

### 4. אינדקסים למהירות
```python
class Student(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)  # אינדקס לחיפוש מהיר
    email: str = Field(unique=True)  # ערך ייחודי
```

---

## שלב 11: בסיסי נתונים שונים

### SQLite (קובץ מקומי):
```python
engine = create_engine("sqlite:///database.db")
```

### MySQL:
```python
engine = create_engine("mysql://user:password@localhost/dbname")
```

### PostgreSQL:
```python
engine = create_engine("postgresql://user:password@localhost/dbname")
```

---

## תרגילים לתרגול

### תרגיל 1: מערכת ספרייה
צור מערכת לניהול ספרים עם השדות הבאים:
- id
- title (שם הספר)
- author (מחבר)
- year (שנת הוצאה)
- is_available (האם זמין להשאלה)

יישם פונקציות להוספה, עדכון, מחיקה וחיפוש ספרים.

### תרגיל 2: מערכת משימות
צור מערכת TODO עם:
- id
- title (כותרת המשימה)
- description (תיאור)
- is_completed (האם הושלמה)
- due_date (תאריך יעד)

### תרגיל 3: מערכת עם קשרים
צור מערכת עם שתי טבלאות:
- Authors (מחברים)
- Books (ספרים)

כל מחבר יכול לכתוב כמה ספרים, וצור קשר ביניהם.

---

## סיכום

SQLModel מאפשר לנו:
- ✅ להגדיר טבלאות בקלות עם מחלקות Python
- ✅ לאמת נתונים אוטומטית
- ✅ לבצע פעולות CRUD פשוטות
- ✅ ליצור קשרים בין טבלאות
- ✅ לעבוד עם בסיסי נתונים שונים

**זכור:** תמיד השתמש ב-`with Session(engine)` כדי להבטיח סגירה נכונה של החיבור!

---

## משאבים נוספים

- [תיעוד רשמי של SQLModel](https://sqlmodel.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Pydantic Documentation](https://docs.pydantic.dev/)

בהצלחה! 🚀
