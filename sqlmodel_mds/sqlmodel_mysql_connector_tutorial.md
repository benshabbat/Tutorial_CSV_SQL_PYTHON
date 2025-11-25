# מדריך למתחילים - SQLModel עם MySQL Connector

## מבוא
במדריך זה נלמד כיצד לעבוד עם שתי ספריות חשובות:
- **SQLModel** - ORM מודרני לעבודה עם בסיסי נתונים
- **MySQL Connector** - חיבור ישיר לבסיס נתונים MySQL

נלמד מתי להשתמש בכל אחת ואיך לשלב ביניהן.

---

## חלק 1: התקנה

### שלב 1.1: התקנת הספריות

```bash
pip install sqlmodel
pip install mysql-connector-python
```

### שלב 1.2: התקנת MySQL Server

אם עדיין אין לך MySQL מותקן:
1. הורד מ-[MySQL Downloads](https://dev.mysql.com/downloads/mysql/)
2. התקן עם הסיסמה שלך (זכור אותה!)
3. ברירת המחדל: `localhost:3306`

---

## חלק 2: MySQL Connector - חיבור ישיר

### שלב 2.1: חיבור בסיסי למשתמש root

```python
import mysql.connector
from mysql.connector import Error

def create_connection():
    """יצירת חיבור לשרת MySQL"""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='your_password'  # שנה לסיסמה שלך!
        )
        
        if connection.is_connected():
            print("✓ התחברנו בהצלחה ל-MySQL!")
            return connection
            
    except Error as e:
        print(f"✗ שגיאה: {e}")
        return None

# שימוש
connection = create_connection()
if connection:
    connection.close()
    print("החיבור נסגר")
```

### שלב 2.2: יצירת בסיס נתונים

```python
import mysql.connector

def create_database():
    """יצירת בסיס נתונים חדש"""
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='your_password'
    )
    
    cursor = connection.cursor()
    
    try:
        # יצירת בסיס נתונים
        cursor.execute("CREATE DATABASE IF NOT EXISTS school_db")
        print("✓ בסיס הנתונים 'school_db' נוצר בהצלחה!")
        
        # הצגת כל בסיסי הנתונים
        cursor.execute("SHOW DATABASES")
        print("\nבסיסי נתונים קיימים:")
        for db in cursor:
            print(f"  - {db[0]}")
            
    except mysql.connector.Error as e:
        print(f"✗ שגיאה: {e}")
        
    finally:
        cursor.close()
        connection.close()

create_database()
```

### שלב 2.3: יצירת טבלה עם MySQL Connector

```python
import mysql.connector

def create_table():
    """יצירת טבלת תלמידים"""
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='your_password',
        database='school_db'  # מתחברים לבסיס הנתונים
    )
    
    cursor = connection.cursor()
    
    # SQL ליצירת טבלה
    create_table_query = """
    CREATE TABLE IF NOT EXISTS students (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        age INT NOT NULL,
        grade FLOAT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
    
    try:
        cursor.execute(create_table_query)
        print("✓ טבלת students נוצרה בהצלחה!")
        
    except mysql.connector.Error as e:
        print(f"✗ שגיאה: {e}")
        
    finally:
        cursor.close()
        connection.close()

create_table()
```

### שלב 2.4: הוספת נתונים עם MySQL Connector

```python
import mysql.connector

def insert_student(name, age, grade):
    """הוספת תלמיד חדש"""
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='your_password',
        database='school_db'
    )
    
    cursor = connection.cursor()
    
    insert_query = """
    INSERT INTO students (name, age, grade) 
    VALUES (%s, %s, %s)
    """
    
    try:
        cursor.execute(insert_query, (name, age, grade))
        connection.commit()
        print(f"✓ התלמיד {name} נוסף בהצלחה! ID: {cursor.lastrowid}")
        
    except mysql.connector.Error as e:
        print(f"✗ שגיאה: {e}")
        
    finally:
        cursor.close()
        connection.close()

# הוספת תלמידים
insert_student("יוסי כהן", 15, 88.5)
insert_student("שרה לוי", 16, 92.0)
insert_student("דני מזרחי", 15, 78.0)
```

### שלב 2.5: קריאת נתונים עם MySQL Connector

```python
import mysql.connector

def get_all_students():
    """קריאת כל התלמידים"""
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='your_password',
        database='school_db'
    )
    
    cursor = connection.cursor()
    
    try:
        cursor.execute("SELECT * FROM students")
        students = cursor.fetchall()
        
        print("\n=== רשימת התלמידים ===")
        for student in students:
            print(f"ID: {student[0]} | שם: {student[1]} | גיל: {student[2]} | ציון: {student[3]}")
            
    except mysql.connector.Error as e:
        print(f"✗ שגיאה: {e}")
        
    finally:
        cursor.close()
        connection.close()

def get_student_by_id(student_id):
    """קריאת תלמיד ספציפי"""
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='your_password',
        database='school_db'
    )
    
    cursor = connection.cursor()
    
    try:
        cursor.execute("SELECT * FROM students WHERE id = %s", (student_id,))
        student = cursor.fetchone()
        
        if student:
            print(f"נמצא: {student[1]}, גיל {student[2]}, ציון {student[3]}")
        else:
            print("תלמיד לא נמצא")
            
    except mysql.connector.Error as e:
        print(f"✗ שגיאה: {e}")
        
    finally:
        cursor.close()
        connection.close()

get_all_students()
get_student_by_id(1)
```

### שלב 2.6: עדכון ומחיקה עם MySQL Connector

```python
import mysql.connector

def update_grade(student_id, new_grade):
    """עדכון ציון תלמיד"""
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='your_password',
        database='school_db'
    )
    
    cursor = connection.cursor()
    
    try:
        cursor.execute(
            "UPDATE students SET grade = %s WHERE id = %s",
            (new_grade, student_id)
        )
        connection.commit()
        print(f"✓ הציון עודכן! {cursor.rowcount} שורות הושפעו")
        
    except mysql.connector.Error as e:
        print(f"✗ שגיאה: {e}")
        
    finally:
        cursor.close()
        connection.close()

def delete_student(student_id):
    """מחיקת תלמיד"""
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='your_password',
        database='school_db'
    )
    
    cursor = connection.cursor()
    
    try:
        cursor.execute("DELETE FROM students WHERE id = %s", (student_id,))
        connection.commit()
        print(f"✓ התלמיד נמחק! {cursor.rowcount} שורות נמחקו")
        
    except mysql.connector.Error as e:
        print(f"✗ שגיאה: {e}")
        
    finally:
        cursor.close()
        connection.close()

# שימוש
update_grade(1, 95.0)
delete_student(3)
```

---

## חלק 3: SQLModel עם MySQL

### שלב 3.1: הגדרת המודלים

```python
from sqlmodel import SQLModel, Field, create_engine, Session, select
from typing import Optional
from datetime import datetime

class Student(SQLModel, table=True):
    """מודל תלמיד - ייצוג אובייקטי של טבלת students"""
    __tablename__ = "students_sqlmodel"  # שם טבלה שונה כדי לא להתנגש
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100)
    age: int = Field(ge=5, le=120)
    grade: float = Field(ge=0, le=100)
    created_at: Optional[str] = None

# יצירת חיבור ל-MySQL
DATABASE_URL = "mysql+pymysql://root:your_password@localhost/school_db"

# התקנת pymysql אם צריך: pip install pymysql
engine = create_engine(DATABASE_URL, echo=True)  # echo=True להצגת SQL
```

### שלב 3.2: יצירת טבלאות עם SQLModel

```python
from sqlmodel import SQLModel, create_engine

# יצירת כל הטבלאות
SQLModel.metadata.create_all(engine)
print("✓ הטבלאות נוצרו בהצלחה!")
```

### שלב 3.3: CRUD עם SQLModel

```python
from sqlmodel import Session, select
from datetime import datetime

# CREATE - הוספה
def add_student_sqlmodel(name: str, age: int, grade: float):
    """הוספת תלמיד עם SQLModel"""
    with Session(engine) as session:
        student = Student(
            name=name,
            age=age,
            grade=grade,
            created_at=str(datetime.now())
        )
        session.add(student)
        session.commit()
        session.refresh(student)
        print(f"✓ התלמיד {student.name} נוסף! ID: {student.id}")
        return student

# READ - קריאה
def get_all_students_sqlmodel():
    """קריאת כל התלמידים"""
    with Session(engine) as session:
        statement = select(Student)
        students = session.exec(statement).all()
        
        print("\n=== רשימת תלמידים (SQLModel) ===")
        for student in students:
            print(f"ID: {student.id} | שם: {student.name} | גיל: {student.age} | ציון: {student.grade}")
        
        return students

# UPDATE - עדכון
def update_student_grade_sqlmodel(student_id: int, new_grade: float):
    """עדכון ציון"""
    with Session(engine) as session:
        student = session.get(Student, student_id)
        if student:
            student.grade = new_grade
            session.add(student)
            session.commit()
            print(f"✓ הציון של {student.name} עודכן ל-{new_grade}")
        else:
            print("✗ תלמיד לא נמצא")

# DELETE - מחיקה
def delete_student_sqlmodel(student_id: int):
    """מחיקת תלמיד"""
    with Session(engine) as session:
        student = session.get(Student, student_id)
        if student:
            name = student.name
            session.delete(student)
            session.commit()
            print(f"✓ התלמיד {name} נמחק")
        else:
            print("✗ תלמיד לא נמצא")

# שימוש
add_student_sqlmodel("אבי גולן", 17, 89.0)
add_student_sqlmodel("רונית שמש", 16, 94.5)
get_all_students_sqlmodel()
update_student_grade_sqlmodel(1, 96.0)
```

---

## חלק 4: שילוב MySQL Connector ו-SQLModel

### שלב 4.1: מתי להשתמש בכל אחד?

**MySQL Connector - חיבור ישיר:**
- ✅ שאילתות SQL מורכבות
- ✅ פעולות Bulk (הכנסה/עדכון המוני)
- ✅ פרוצדורות מאוחסנות (Stored Procedures)
- ✅ שליטה מלאה על ה-SQL

**SQLModel - ORM:**
- ✅ קוד Python נקי וקריא
- ✅ אימות נתונים אוטומטי
- ✅ קשרים בין טבלאות
- ✅ Type Safety (בטיחות טיפוסים)

### שלב 4.2: דוגמה משולבת

```python
import mysql.connector
from sqlmodel import SQLModel, Field, create_engine, Session, select
from typing import Optional, List

# מודל SQLModel
class Student(SQLModel, table=True):
    __tablename__ = "students"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    age: int
    grade: float

class DatabaseManager:
    """מנהל בסיס נתונים משולב"""
    
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        
        # חיבור MySQL Connector
        self.mysql_config = {
            'host': host,
            'user': user,
            'password': password,
            'database': database
        }
        
        # חיבור SQLModel
        self.engine = create_engine(
            f"mysql+pymysql://{user}:{password}@{host}/{database}"
        )
    
    def execute_raw_sql(self, query, params=None):
        """הרצת SQL ישיר עם MySQL Connector"""
        connection = mysql.connector.connect(**self.mysql_config)
        cursor = connection.cursor()
        
        try:
            cursor.execute(query, params or ())
            
            if query.strip().upper().startswith("SELECT"):
                results = cursor.fetchall()
                return results
            else:
                connection.commit()
                return cursor.rowcount
                
        finally:
            cursor.close()
            connection.close()
    
    def add_student_orm(self, name: str, age: int, grade: float):
        """הוספת תלמיד עם SQLModel"""
        with Session(self.engine) as session:
            student = Student(name=name, age=age, grade=grade)
            session.add(student)
            session.commit()
            session.refresh(student)
            return student
    
    def get_students_orm(self) -> List[Student]:
        """קריאת תלמידים עם SQLModel"""
        with Session(self.engine) as session:
            return session.exec(select(Student)).all()
    
    def get_top_students_raw(self, limit=5):
        """שימוש ב-SQL ישיר לשאילתא מורכבת"""
        query = """
        SELECT name, grade 
        FROM students 
        ORDER BY grade DESC 
        LIMIT %s
        """
        return self.execute_raw_sql(query, (limit,))
    
    def bulk_update_grades_raw(self, bonus_points):
        """עדכון המוני עם SQL ישיר"""
        query = "UPDATE students SET grade = grade + %s WHERE grade < 100"
        rows_affected = self.execute_raw_sql(query, (bonus_points,))
        return rows_affected

# שימוש במנהל
db = DatabaseManager('localhost', 'root', 'your_password', 'school_db')

# הוספה עם ORM
student = db.add_student_orm("מיכל דהן", 16, 87.5)
print(f"נוסף: {student.name}")

# קריאה עם ORM
students = db.get_students_orm()
print(f"\nסך הכל {len(students)} תלמידים")

# שאילתא מורכבת עם SQL ישיר
top_students = db.get_top_students_raw(3)
print("\nתלמידים מצטיינים:")
for name, grade in top_students:
    print(f"  {name}: {grade}")

# עדכון המוני עם SQL ישיר
updated = db.bulk_update_grades_raw(5)
print(f"\n{updated} תלמידים קיבלו בונוס!")
```

---

## חלק 5: דוגמה מלאה - מערכת ניהול בית ספר

```python
import mysql.connector
from sqlmodel import SQLModel, Field, Relationship, create_engine, Session, select
from typing import Optional, List
from datetime import datetime

# ========== מודלים ==========

class Classroom(SQLModel, table=True):
    """כיתה"""
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=50, unique=True)
    teacher_name: str = Field(max_length=100)
    
    students: List["Student"] = Relationship(back_populates="classroom")

class Student(SQLModel, table=True):
    """תלמיד"""
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100)
    age: int = Field(ge=5, le=120)
    grade: float = Field(ge=0, le=100)
    
    classroom_id: Optional[int] = Field(default=None, foreign_key="classroom.id")
    classroom: Optional[Classroom] = Relationship(back_populates="students")

# ========== התחברות ==========

DATABASE_URL = "mysql+pymysql://root:your_password@localhost/school_db"
engine = create_engine(DATABASE_URL, echo=False)

# יצירת טבלאות
SQLModel.metadata.create_all(engine)

# ========== פונקציות ==========

def create_classroom(name: str, teacher_name: str):
    """יצירת כיתה חדשה"""
    with Session(engine) as session:
        classroom = Classroom(name=name, teacher_name=teacher_name)
        session.add(classroom)
        session.commit()
        session.refresh(classroom)
        print(f"✓ כיתה {name} נוצרה עם המורה {teacher_name}")
        return classroom

def add_student_to_classroom(name: str, age: int, grade: float, classroom_id: int):
    """הוספת תלמיד לכיתה"""
    with Session(engine) as session:
        student = Student(
            name=name,
            age=age,
            grade=grade,
            classroom_id=classroom_id
        )
        session.add(student)
        session.commit()
        print(f"✓ התלמיד {name} נוסף לכיתה")
        return student

def show_classroom_details(classroom_id: int):
    """הצגת פרטי כיתה עם כל התלמידים"""
    with Session(engine) as session:
        classroom = session.get(Classroom, classroom_id)
        
        if not classroom:
            print("✗ כיתה לא נמצאה")
            return
        
        print(f"\n{'='*50}")
        print(f"כיתה: {classroom.name}")
        print(f"מורה: {classroom.teacher_name}")
        print(f"{'='*50}")
        
        if classroom.students:
            print(f"\nתלמידים ({len(classroom.students)}):")
            total_grade = 0
            for student in classroom.students:
                print(f"  • {student.name} (גיל {student.age}) - ציון: {student.grade}")
                total_grade += student.grade
            
            avg_grade = total_grade / len(classroom.students)
            print(f"\nממוצע כיתה: {avg_grade:.2f}")
        else:
            print("אין תלמידים בכיתה")

def get_class_statistics():
    """סטטיסטיקות כלליות עם SQL ישיר"""
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='your_password',
        database='school_db'
    )
    
    cursor = connection.cursor()
    
    query = """
    SELECT 
        c.name as classroom,
        COUNT(s.id) as student_count,
        AVG(s.grade) as avg_grade,
        MAX(s.grade) as max_grade,
        MIN(s.grade) as min_grade
    FROM classroom c
    LEFT JOIN student s ON c.id = s.classroom_id
    GROUP BY c.id, c.name
    """
    
    cursor.execute(query)
    results = cursor.fetchall()
    
    print("\n" + "="*70)
    print("סטטיסטיקות בית הספר")
    print("="*70)
    print(f"{'כיתה':<15} {'מס׳ תלמידים':<15} {'ממוצע':<10} {'מקסימום':<10} {'מינימום':<10}")
    print("-"*70)
    
    for row in results:
        classroom, count, avg, max_g, min_g = row
        avg_str = f"{avg:.1f}" if avg else "N/A"
        max_str = f"{max_g:.1f}" if max_g else "N/A"
        min_str = f"{min_g:.1f}" if min_g else "N/A"
        print(f"{classroom:<15} {count:<15} {avg_str:<10} {max_str:<10} {min_str:<10}")
    
    cursor.close()
    connection.close()

# ========== הרצה ==========

if __name__ == "__main__":
    # יצירת כיתות
    class_a = create_classroom("כיתה א'", "גב' שרה כהן")
    class_b = create_classroom("כיתה ב'", "מר דוד לוי")
    
    # הוספת תלמידים לכיתה א'
    add_student_to_classroom("יוסי אברהם", 15, 88.5, class_a.id)
    add_student_to_classroom("מיכל דהן", 15, 92.0, class_a.id)
    add_student_to_classroom("רון שמש", 16, 78.0, class_a.id)
    
    # הוספת תלמידים לכיתה ב'
    add_student_to_classroom("שרה גולן", 16, 95.5, class_b.id)
    add_student_to_classroom("דני מזרחי", 17, 89.0, class_b.id)
    
    # הצגת פרטי כיתות
    show_classroom_details(class_a.id)
    show_classroom_details(class_b.id)
    
    # סטטיסטיקות
    get_class_statistics()
```

---

## חלק 6: טיפים ושגיאות נפוצות

### טיפ 1: ניהול חיבורים

```python
# ❌ לא טוב - חיבור נשאר פתוח
connection = mysql.connector.connect(...)
cursor = connection.cursor()
# אם יש שגיאה, החיבור לא ייסגר!

# ✅ טוב - שימוש ב-try/finally
connection = mysql.connector.connect(...)
cursor = connection.cursor()
try:
    cursor.execute(query)
finally:
    cursor.close()
    connection.close()

# ✅ הכי טוב - Context Manager (SQLModel)
with Session(engine) as session:
    # החיבור ייסגר אוטומטית
    pass
```

### טיפ 2: מניעת SQL Injection

```python
# ❌ מסוכן!
name = "'; DROP TABLE students; --"
query = f"SELECT * FROM students WHERE name = '{name}'"

# ✅ בטוח - שימוש ב-Parameterized Queries
query = "SELECT * FROM students WHERE name = %s"
cursor.execute(query, (name,))
```

### טיפ 3: טיפול בשגיאות

```python
from mysql.connector import Error

try:
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='wrong_password',
        database='school_db'
    )
except Error as e:
    if e.errno == 1045:
        print("שגיאת אימות - סיסמה שגויה")
    elif e.errno == 2003:
        print("לא ניתן להתחבר לשרת")
    else:
        print(f"שגיאה: {e}")
```

### טיפ 4: Migrations עם SQLModel

```python
# כשמשנים מודל, לפעמים צריך למחוק ולייצר מחדש
from sqlmodel import SQLModel

# מחיקת טבלאות (זהירות! מוחק נתונים!)
SQLModel.metadata.drop_all(engine)

# יצירה מחדש
SQLModel.metadata.create_all(engine)
```

---

## חלק 7: תרגילים

### תרגיל 1: מערכת ספרייה
צור מערכת עם:
- טבלת Books (ספרים)
- טבלת Members (חברים)
- טבלת Loans (השאלות)

השתמש ב-SQLModel לניהול הנתונים וב-MySQL Connector לדוחות.

### תרגיל 2: מערכת חנות
צור:
- Products (מוצרים)
- Customers (לקוחות)
- Orders (הזמנות)
- OrderItems (פריטי הזמנה)

### תרגיל 3: שאילתות מורכבות
כתוב פונקציה שמשתמשת ב-MySQL Connector ל:
1. חישוב הכנסות חודשיות
2. מציאת הלקוח הכי פעיל
3. מוצרים שלא הוזמנו ב-30 יום האחרונים

---

## סיכום

| **היבט** | **MySQL Connector** | **SQLModel** |
|-----------|-------------------|--------------|
| **קלות שימוש** | דורש SQL ידני | קוד Python פשוט |
| **ביצועים** | מהיר לפעולות המוניות | טוב לפעולות רגילות |
| **אימות נתונים** | ידני | אוטומטי |
| **Type Safety** | אין | יש |
| **שאילתות מורכבות** | מצוין | מוגבל |
| **קריאות קוד** | SQL גולמי | Python אובייקטי |

### המלצות:
- 🎯 למתחילים: התחל עם **SQLModel**
- 🚀 לפעולות מורכבות: השתמש ב-**MySQL Connector**
- 💡 בפרויקט אמיתי: שלב בין שניהם!

---

## משאבים נוספים

- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)
- [MySQL Connector Python](https://dev.mysql.com/doc/connector-python/en/)
- [MySQL Reference](https://dev.mysql.com/doc/)

בהצלחה! 🎓🚀
