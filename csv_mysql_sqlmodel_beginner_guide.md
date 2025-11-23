# מדריך למתחילים: CSV, MySQL, SQLModel ו-Python

## תוכן עניינים
1. [מבוא](#מבוא)
2. [התקנה והכנה](#התקנה-והכנה)
3. [חלק 1: מבוא ל-SQLModel](#חלק-1-מבוא-ל-sqlmodel)
4. [חלק 2: עבודה עם CSV](#חלק-2-עבודה-עם-csv)
5. [חלק 3: SQLModel עם MySQL](#חלק-3-sqlmodel-עם-mysql)
6. [חלק 4: שילוב CSV, SQLModel ו-MySQL](#חלק-4-שילוב-csv-sqlmodel-ו-mysql)
7. [חלק 5: פרויקט מלא](#חלק-5-פרויקט-מלא)
8. [תרגילים מעשיים](#תרגילים-מעשיים)

---

## מבוא

### מה נלמד?
במדריך זה נלמד כיצד:
- לעבוד עם SQLModel - ספרייה מודרנית לעבודה עם מסדי נתונים
- לקרוא ולכתוב קבצי CSV
- להתחבר למסד נתונים MySQL דרך SQLModel
- להעביר מידע בין CSV למסד נתונים
- לבנות אפליקציה מלאה לניהול נתונים

### מה זה SQLModel?
SQLModel היא ספרייה מודרנית ש:
- משלבת את Pydantic (לוולידציה) ו-SQLAlchemy (למסדי נתונים)
- מאפשרת להגדיר מודלים עם Type Hints
- מספקת בטיחות טיפוסים
- קלה ללמידה ושימוש

### למי המדריך מיועד?
- מתחילים בתכנות Python
- מי שרוצה ללמוד ORM מודרני
- מי שמעוניין בקוד נקי ובטיחותי

---

## התקנה והכנה

### שלב 1: ודא ש-Python מותקן
```bash
python --version
```

אמור להציג Python 3.7 ומעלה.

### שלב 2: התקנת הספריות הנדרשות

```bash
pip install sqlmodel pymysql pandas
```

**הסבר:**
- `sqlmodel` - הספרייה העיקרית
- `pymysql` - דרייבר MySQL לעבודה עם SQLModel
- `pandas` - לעבודה עם CSV (אופציונלי אך מומלץ)

### שלב 3: התקנת MySQL

1. הורד MySQL Server מ-[mysql.com](https://dev.mysql.com/downloads/)
2. התקן והגדר סיסמת root
3. וודא שהשירות פועל:
```bash
mysql --version
```

---

## חלק 1: מבוא ל-SQLModel

### 1.1: המודל הראשון שלך

```python
from sqlmodel import SQLModel, Field
from typing import Optional

class Employee(SQLModel, table=True):
    """מודל עובד - מייצג שורה בטבלה"""
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    age: int
    city: str
    salary: float
    
    class Config:
        # הגדרות נוספות
        arbitrary_types_allowed = True

# יצירת אובייקט עובד
employee = Employee(
    name="Alice",
    age=25,
    city="Tel Aviv",
    salary=10000.0
)

print(employee)
print(f"שם: {employee.name}, גיל: {employee.age}")
```

### 1.2: הבנת המודל

**הסבר מפורט:**

```python
from sqlmodel import SQLModel, Field
from typing import Optional

class Employee(SQLModel, table=True):
    # table=True אומר שזו טבלה במסד נתונים
    
    # id - מזהה ייחודי, אוטומטי (AUTO_INCREMENT)
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # שדות חובה
    name: str  # טקסט חובה
    age: int   # מספר שלם חובה
    city: str  # טקסט חובה
    salary: float  # מספר עשרוני חובה
    
    # שדה אופציונלי
    department: Optional[str] = None
```

### 1.3: וולידציה אוטומטית

SQLModel בודק את הטיפוסים אוטומטית:

```python
from sqlmodel import SQLModel, Field
from typing import Optional

class Employee(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(min_length=2, max_length=100)
    age: int = Field(gt=0, lt=120)  # גדול מ-0, קטן מ-120
    salary: float = Field(gt=0)  # חייב להיות חיובי
    email: str = Field(regex=r"^[\w\.-]+@[\w\.-]+\.\w+$")

# ינסה ליצור עובד תקין
try:
    employee = Employee(
        name="Alice",
        age=25,
        salary=10000.0,
        email="alice@example.com"
    )
    print("✓ עובד תקין נוצר!")
except Exception as e:
    print(f"✗ שגיאה: {e}")

# ינסה ליצור עובד עם נתונים לא תקינים
try:
    invalid_employee = Employee(
        name="A",  # שם קצר מדי
        age=-5,    # גיל שלילי
        salary=-1000,  # משכורת שלילית
        email="invalid-email"  # אימייל לא תקין
    )
except Exception as e:
    print(f"✗ שגיאת וולידציה: {e}")
```

---

## חלק 2: עבודה עם CSV

### 2.1: יצירת קובץ CSV פשוט

```python
import csv

# נתונים ליצירת CSV
employees_data = [
    ['name', 'age', 'city', 'salary'],
    ['Alice', 25, 'Tel Aviv', 10000],
    ['Bob', 30, 'Jerusalem', 12000],
    ['Charlie', 35, 'Haifa', 15000],
    ['Diana', 28, 'Beer Sheva', 11000]
]

# כתיבה לקובץ
with open('employees.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerows(employees_data)

print("✓ קובץ employees.csv נוצר!")
```

### 2.2: קריאת CSV עם Pandas

```python
import pandas as pd

# קריאת קובץ
df = pd.read_csv('employees.csv')

print("=== כל הנתונים ===")
print(df)

print("\n=== מידע על הנתונים ===")
print(df.info())

print("\n=== סטטיסטיקות ===")
print(df.describe())

# סינון
print("\n=== עובדים מתל אביב ===")
tel_aviv = df[df['city'] == 'Tel Aviv']
print(tel_aviv)

# חישובים
avg_salary = df['salary'].mean()
print(f"\nממוצע משכורות: {avg_salary:.2f} ₪")
```

### 2.3: קריאת CSV ויצירת מודלים

```python
import csv
from sqlmodel import SQLModel, Field
from typing import Optional, List

class Employee(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    age: int
    city: str
    salary: float

def read_employees_from_csv(filename: str) -> List[Employee]:
    """קריאת עובדים מקובץ CSV והמרה למודלים"""
    employees = []
    
    with open(filename, 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        
        for row in csv_reader:
            employee = Employee(
                name=row['name'],
                age=int(row['age']),
                city=row['city'],
                salary=float(row['salary'])
            )
            employees.append(employee)
    
    return employees

# שימוש
employees = read_employees_from_csv('employees.csv')
print(f"נקראו {len(employees)} עובדים:")
for emp in employees:
    print(f"  - {emp.name}, {emp.age}, {emp.city}")
```

---

## חלק 3: SQLModel עם MySQL

### 3.1: יצירת חיבור למסד נתונים

```python
from sqlmodel import SQLModel, create_engine

# יצירת מנוע חיבור
# פורמט: mysql+pymysql://username:password@host:port/database
DATABASE_URL = "mysql+pymysql://root:your_password@localhost:3306/company_db"

engine = create_engine(DATABASE_URL, echo=True)
# echo=True מציג את כל פקודות SQL שמתבצעות

print("✓ מנוע חיבור נוצר!")
```

### 3.2: יצירת מסד נתונים וטבלאות

```python
from sqlmodel import SQLModel, Field, create_engine
from typing import Optional

# הגדרת מודל
class Employee(SQLModel, table=True):
    __tablename__ = "employees"  # שם הטבלה במסד הנתונים
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100)
    age: int
    city: str = Field(max_length=100)
    salary: float

# חיבור למסד נתונים
DATABASE_URL = "mysql+pymysql://root:your_password@localhost:3306/company_db"
engine = create_engine(DATABASE_URL, echo=True)

# יצירת כל הטבלאות
SQLModel.metadata.create_all(engine)
print("✓ טבלה employees נוצרה!")
```

**הערה:** אם מסד הנתונים לא קיים, צור אותו קודם:

```python
from sqlmodel import create_engine
from sqlalchemy import text

# חיבור ללא מסד נתונים ספציפי
temp_engine = create_engine("mysql+pymysql://root:your_password@localhost:3306")

with temp_engine.connect() as connection:
    connection.execute(text("CREATE DATABASE IF NOT EXISTS company_db"))
    connection.commit()

print("✓ מסד נתונים company_db נוצר!")
```

### 3.3: הוספת נתונים (Create)

```python
from sqlmodel import SQLModel, Field, create_engine, Session
from typing import Optional

class Employee(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    age: int
    city: str
    salary: float

DATABASE_URL = "mysql+pymysql://root:your_password@localhost:3306/company_db"
engine = create_engine(DATABASE_URL)

# הוספת עובד אחד
employee = Employee(
    name="Alice",
    age=25,
    city="Tel Aviv",
    salary=10000.0
)

with Session(engine) as session:
    session.add(employee)
    session.commit()
    session.refresh(employee)  # מעדכן את ה-id
    print(f"✓ עובד נוסף עם ID: {employee.id}")

# הוספת מספר עובדים
employees = [
    Employee(name="Bob", age=30, city="Jerusalem", salary=12000),
    Employee(name="Charlie", age=35, city="Haifa", salary=15000),
    Employee(name="Diana", age=28, city="Beer Sheva", salary=11000)
]

with Session(engine) as session:
    for emp in employees:
        session.add(emp)
    session.commit()
    print(f"✓ {len(employees)} עובדים נוספו!")
```

### 3.4: קריאת נתונים (Read)

```python
from sqlmodel import Session, select

# קריאת כל העובדים
with Session(engine) as session:
    statement = select(Employee)
    results = session.exec(statement).all()
    
    print(f"נמצאו {len(results)} עובדים:")
    for emp in results:
        print(f"  {emp.id}. {emp.name}, {emp.age}, {emp.city} - {emp.salary} ₪")

# קריאת עובד אחד לפי ID
with Session(engine) as session:
    employee = session.get(Employee, 1)  # מביא עובד עם ID=1
    if employee:
        print(f"✓ נמצא: {employee.name}")
    else:
        print("✗ עובד לא נמצא")

# סינון עובדים
with Session(engine) as session:
    statement = select(Employee).where(Employee.city == "Tel Aviv")
    tel_aviv_employees = session.exec(statement).all()
    print(f"עובדים בתל אביב: {len(tel_aviv_employees)}")

# סינון מורכב
with Session(engine) as session:
    statement = select(Employee).where(
        Employee.age > 25,
        Employee.salary >= 11000
    )
    filtered = session.exec(statement).all()
    print(f"עובדים מעל גיל 25 עם משכורת מעל 11000: {len(filtered)}")
```

### 3.5: עדכון נתונים (Update)

```python
from sqlmodel import Session, select

# עדכון עובד אחד
with Session(engine) as session:
    employee = session.get(Employee, 1)
    if employee:
        employee.salary = 11000
        employee.city = "Ramat Gan"
        session.add(employee)
        session.commit()
        session.refresh(employee)
        print(f"✓ עובד {employee.name} עודכן!")

# עדכון מסיבי
with Session(engine) as session:
    statement = select(Employee).where(Employee.city == "Tel Aviv")
    employees = session.exec(statement).all()
    
    for emp in employees:
        emp.salary *= 1.1  # העלאת שכר של 10%
        session.add(emp)
    
    session.commit()
    print(f"✓ {len(employees)} עובדים מתל אביב קיבלו העלאת שכר!")
```

### 3.6: מחיקת נתונים (Delete)

```python
from sqlmodel import Session, select

# מחיקת עובד אחד
with Session(engine) as session:
    employee = session.get(Employee, 1)
    if employee:
        session.delete(employee)
        session.commit()
        print(f"✓ עובד {employee.name} נמחק!")

# מחיקת מספר עובדים
with Session(engine) as session:
    statement = select(Employee).where(Employee.salary < 10000)
    employees_to_delete = session.exec(statement).all()
    
    for emp in employees_to_delete:
        session.delete(emp)
    
    session.commit()
    print(f"✓ {len(employees_to_delete)} עובדים נמחקו!")
```

---

## חלק 4: שילוב CSV, SQLModel ו-MySQL

### 4.1: ייבוא נתונים מ-CSV למסד נתונים

#### גרסה פשוטה

```python
import csv
from sqlmodel import SQLModel, Field, create_engine, Session
from typing import Optional

class Employee(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    age: int
    city: str
    salary: float

DATABASE_URL = "mysql+pymysql://root:your_password@localhost:3306/company_db"
engine = create_engine(DATABASE_URL)

# יצירת טבלה
SQLModel.metadata.create_all(engine)

# קריאה מ-CSV והכנסה למסד נתונים
with open('employees.csv', 'r', encoding='utf-8') as file:
    csv_reader = csv.DictReader(file)
    
    with Session(engine) as session:
        count = 0
        for row in csv_reader:
            employee = Employee(
                name=row['name'],
                age=int(row['age']),
                city=row['city'],
                salary=float(row['salary'])
            )
            session.add(employee)
            count += 1
        
        session.commit()
        print(f"✓ {count} עובדים יובאו מ-CSV למסד נתונים!")
```

#### גרסה מתקדמת עם Pandas

```python
import pandas as pd
from sqlmodel import SQLModel, Field, create_engine, Session
from typing import Optional, List

class Employee(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    age: int
    city: str
    salary: float

def import_csv_to_db(csv_file: str, database_url: str) -> int:
    """ייבוא נתונים מ-CSV למסד נתונים"""
    
    # קריאת CSV
    df = pd.read_csv(csv_file)
    print(f"נקראו {len(df)} שורות מ-{csv_file}")
    
    # יצירת מנוע וטבלה
    engine = create_engine(database_url)
    SQLModel.metadata.create_all(engine)
    
    # המרה למודלים והכנסה למסד נתונים
    with Session(engine) as session:
        for _, row in df.iterrows():
            employee = Employee(
                name=row['name'],
                age=int(row['age']),
                city=row['city'],
                salary=float(row['salary'])
            )
            session.add(employee)
        
        session.commit()
    
    print(f"✓ {len(df)} עובדים יובאו בהצלחה!")
    return len(df)

# שימוש
DATABASE_URL = "mysql+pymysql://root:your_password@localhost:3306/company_db"
count = import_csv_to_db('employees.csv', DATABASE_URL)
```

### 4.2: ייצוא נתונים ממסד נתונים ל-CSV

#### גרסה פשוטה

```python
import csv
from sqlmodel import Session, select

with Session(engine) as session:
    # שליפת כל העובדים
    statement = select(Employee)
    employees = session.exec(statement).all()
    
    # כתיבה ל-CSV
    with open('employees_export.csv', 'w', newline='', encoding='utf-8') as file:
        fieldnames = ['id', 'name', 'age', 'city', 'salary']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        
        writer.writeheader()
        
        for emp in employees:
            writer.writerow({
                'id': emp.id,
                'name': emp.name,
                'age': emp.age,
                'city': emp.city,
                'salary': emp.salary
            })
    
    print(f"✓ {len(employees)} עובדים יוצאו ל-CSV!")
```

#### גרסה מתקדמת עם Pandas

```python
import pandas as pd
from sqlmodel import Session, select

def export_db_to_csv(
    database_url: str, 
    output_file: str, 
    filter_city: str = None
) -> int:
    """ייצוא נתונים ממסד נתונים ל-CSV"""
    
    engine = create_engine(database_url)
    
    with Session(engine) as session:
        # בניית שאילתה
        statement = select(Employee)
        if filter_city:
            statement = statement.where(Employee.city == filter_city)
        
        employees = session.exec(statement).all()
        
        # המרה ל-DataFrame
        data = []
        for emp in employees:
            data.append({
                'id': emp.id,
                'name': emp.name,
                'age': emp.age,
                'city': emp.city,
                'salary': emp.salary
            })
        
        df = pd.DataFrame(data)
        
        # שמירה ל-CSV
        df.to_csv(output_file, index=False, encoding='utf-8')
        print(f"✓ {len(employees)} עובדים יוצאו ל-{output_file}!")
        
        return len(employees)

# שימוש
DATABASE_URL = "mysql+pymysql://root:your_password@localhost:3306/company_db"

# ייצוא כל העובדים
export_db_to_csv(DATABASE_URL, 'all_employees.csv')

# ייצוא רק עובדים מתל אביב
export_db_to_csv(DATABASE_URL, 'tel_aviv_employees.csv', filter_city='Tel Aviv')
```

### 4.3: סנכרון דו-כיווני

```python
import csv
from sqlmodel import SQLModel, Field, create_engine, Session, select
from typing import Optional
from datetime import datetime

class Employee(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    age: int
    city: str
    salary: float
    last_updated: Optional[str] = None

class DataSync:
    """מחלקה לסנכרון נתונים בין CSV למסד נתונים"""
    
    def __init__(self, database_url: str):
        self.engine = create_engine(database_url)
        SQLModel.metadata.create_all(self.engine)
    
    def csv_to_db(self, csv_file: str) -> int:
        """ייבוא מ-CSV למסד נתונים"""
        count = 0
        
        with open(csv_file, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            
            with Session(self.engine) as session:
                for row in csv_reader:
                    employee = Employee(
                        name=row['name'],
                        age=int(row['age']),
                        city=row['city'],
                        salary=float(row['salary']),
                        last_updated=datetime.now().isoformat()
                    )
                    session.add(employee)
                    count += 1
                
                session.commit()
        
        print(f"✓ CSV → DB: {count} רכומות")
        return count
    
    def db_to_csv(self, csv_file: str, where_clause=None) -> int:
        """ייצוא ממסד נתונים ל-CSV"""
        with Session(self.engine) as session:
            statement = select(Employee)
            if where_clause:
                statement = statement.where(where_clause)
            
            employees = session.exec(statement).all()
            
            with open(csv_file, 'w', newline='', encoding='utf-8') as file:
                fieldnames = ['id', 'name', 'age', 'city', 'salary', 'last_updated']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                
                writer.writeheader()
                for emp in employees:
                    writer.writerow({
                        'id': emp.id,
                        'name': emp.name,
                        'age': emp.age,
                        'city': emp.city,
                        'salary': emp.salary,
                        'last_updated': emp.last_updated
                    })
            
            print(f"✓ DB → CSV: {len(employees)} רכומות")
            return len(employees)
    
    def update_from_csv(self, csv_file: str) -> tuple:
        """עדכון מסד נתונים מקובץ CSV (לפי name)"""
        updated = 0
        added = 0
        
        with open(csv_file, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            
            with Session(self.engine) as session:
                for row in csv_reader:
                    # חיפוש עובד קיים
                    statement = select(Employee).where(Employee.name == row['name'])
                    existing = session.exec(statement).first()
                    
                    if existing:
                        # עדכון עובד קיים
                        existing.age = int(row['age'])
                        existing.city = row['city']
                        existing.salary = float(row['salary'])
                        existing.last_updated = datetime.now().isoformat()
                        session.add(existing)
                        updated += 1
                    else:
                        # הוספת עובד חדש
                        new_employee = Employee(
                            name=row['name'],
                            age=int(row['age']),
                            city=row['city'],
                            salary=float(row['salary']),
                            last_updated=datetime.now().isoformat()
                        )
                        session.add(new_employee)
                        added += 1
                
                session.commit()
        
        print(f"✓ עודכנו: {updated}, נוספו: {added}")
        return updated, added

# שימוש
DATABASE_URL = "mysql+pymysql://root:your_password@localhost:3306/company_db"
sync = DataSync(DATABASE_URL)

# ייבוא ראשוני
sync.csv_to_db('employees.csv')

# ייצוא
sync.db_to_csv('backup.csv')

# עדכון מ-CSV (מעדכן קיימים ומוסיף חדשים)
sync.update_from_csv('employees_updated.csv')
```

---

## חלק 5: פרויקט מלא

### 5.1: מערכת ניהול עובדים מלאה

```python
import csv
from sqlmodel import SQLModel, Field, create_engine, Session, select
from typing import Optional, List
from datetime import datetime
import pandas as pd

# ============= מודלים =============

class Employee(SQLModel, table=True):
    """מודל עובד"""
    __tablename__ = "employees"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(min_length=2, max_length=100)
    age: int = Field(gt=18, lt=120)
    city: str = Field(max_length=100)
    salary: float = Field(gt=0)
    department: Optional[str] = Field(default=None, max_length=100)
    hire_date: Optional[str] = None
    
    class Config:
        arbitrary_types_allowed = True

# ============= מחלקת ניהול =============

class EmployeeManager:
    """מנהל עובדים - פעולות CRUD ועבודה עם CSV"""
    
    def __init__(self, database_url: str):
        """אתחול"""
        self.engine = create_engine(database_url, echo=False)
        SQLModel.metadata.create_all(self.engine)
        print("✓ מנהל עובדים הופעל!")
    
    # ========== פעולות CRUD ==========
    
    def add_employee(self, **kwargs) -> Employee:
        """הוספת עובד חדש"""
        employee = Employee(**kwargs)
        
        with Session(self.engine) as session:
            session.add(employee)
            session.commit()
            session.refresh(employee)
            print(f"✓ עובד {employee.name} נוסף (ID: {employee.id})")
            return employee
    
    def get_employee(self, employee_id: int) -> Optional[Employee]:
        """שליפת עובד לפי ID"""
        with Session(self.engine) as session:
            employee = session.get(Employee, employee_id)
            if employee:
                return employee
            else:
                print(f"✗ עובד עם ID {employee_id} לא נמצא")
                return None
    
    def get_all_employees(self) -> List[Employee]:
        """שליפת כל העובדים"""
        with Session(self.engine) as session:
            statement = select(Employee)
            return session.exec(statement).all()
    
    def update_employee(self, employee_id: int, **kwargs) -> bool:
        """עדכון עובד"""
        with Session(self.engine) as session:
            employee = session.get(Employee, employee_id)
            
            if not employee:
                print(f"✗ עובד עם ID {employee_id} לא נמצא")
                return False
            
            for key, value in kwargs.items():
                setattr(employee, key, value)
            
            session.add(employee)
            session.commit()
            print(f"✓ עובד {employee.name} עודכן!")
            return True
    
    def delete_employee(self, employee_id: int) -> bool:
        """מחיקת עובד"""
        with Session(self.engine) as session:
            employee = session.get(Employee, employee_id)
            
            if not employee:
                print(f"✗ עובד עם ID {employee_id} לא נמצא")
                return False
            
            session.delete(employee)
            session.commit()
            print(f"✓ עובד {employee.name} נמחק!")
            return True
    
    # ========== חיפוס וסינון ==========
    
    def search_employees(self, **filters) -> List[Employee]:
        """חיפוש עובדים לפי פילטרים"""
        with Session(self.engine) as session:
            statement = select(Employee)
            
            if 'city' in filters:
                statement = statement.where(Employee.city == filters['city'])
            
            if 'department' in filters:
                statement = statement.where(Employee.department == filters['department'])
            
            if 'min_salary' in filters:
                statement = statement.where(Employee.salary >= filters['min_salary'])
            
            if 'max_salary' in filters:
                statement = statement.where(Employee.salary <= filters['max_salary'])
            
            if 'min_age' in filters:
                statement = statement.where(Employee.age >= filters['min_age'])
            
            if 'max_age' in filters:
                statement = statement.where(Employee.age <= filters['max_age'])
            
            return session.exec(statement).all()
    
    # ========== סטטיסטיקות ==========
    
    def get_statistics(self) -> dict:
        """קבלת סטטיסטיקות"""
        employees = self.get_all_employees()
        
        if not employees:
            return {}
        
        salaries = [emp.salary for emp in employees]
        ages = [emp.age for emp in employees]
        
        # ספירת עובדים לפי עיר
        cities = {}
        for emp in employees:
            cities[emp.city] = cities.get(emp.city, 0) + 1
        
        # ספירת עובדים לפי מחלקה
        departments = {}
        for emp in employees:
            dept = emp.department or "ללא מחלקה"
            departments[dept] = departments.get(dept, 0) + 1
        
        stats = {
            'total_employees': len(employees),
            'avg_salary': sum(salaries) / len(salaries),
            'min_salary': min(salaries),
            'max_salary': max(salaries),
            'avg_age': sum(ages) / len(ages),
            'min_age': min(ages),
            'max_age': max(ages),
            'cities': cities,
            'departments': departments
        }
        
        return stats
    
    def print_statistics(self):
        """הדפסת סטטיסטיקות"""
        stats = self.get_statistics()
        
        if not stats:
            print("אין נתונים להצגה")
            return
        
        print("\n" + "="*50)
        print("סטטיסטיקות עובדים")
        print("="*50)
        print(f"סך כל עובדים: {stats['total_employees']}")
        print(f"\nמשכורות:")
        print(f"  ממוצע: {stats['avg_salary']:.2f} ₪")
        print(f"  מינימום: {stats['min_salary']:.2f} ₪")
        print(f"  מקסימום: {stats['max_salary']:.2f} ₪")
        print(f"\nגילאים:")
        print(f"  ממוצע: {stats['avg_age']:.1f}")
        print(f"  מינימום: {stats['min_age']}")
        print(f"  מקסימום: {stats['max_age']}")
        print(f"\nפילוח לפי ערים:")
        for city, count in stats['cities'].items():
            print(f"  {city}: {count}")
        print(f"\nפילוח לפי מחלקות:")
        for dept, count in stats['departments'].items():
            print(f"  {dept}: {count}")
        print("="*50 + "\n")
    
    # ========== עבודה עם CSV ==========
    
    def import_from_csv(self, filename: str, clear_existing: bool = False) -> int:
        """ייבוא עובדים מ-CSV"""
        
        if clear_existing:
            with Session(self.engine) as session:
                session.exec(select(Employee)).all()
                for emp in session.exec(select(Employee)).all():
                    session.delete(emp)
                session.commit()
            print("✓ טבלה נוקתה")
        
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file)
                count = 0
                
                with Session(self.engine) as session:
                    for row in csv_reader:
                        employee = Employee(
                            name=row['name'],
                            age=int(row['age']),
                            city=row['city'],
                            salary=float(row['salary']),
                            department=row.get('department'),
                            hire_date=row.get('hire_date')
                        )
                        session.add(employee)
                        count += 1
                    
                    session.commit()
                
                print(f"✓ {count} עובדים יובאו מ-{filename}")
                return count
                
        except Exception as e:
            print(f"✗ שגיאה בייבוא: {e}")
            return 0
    
    def export_to_csv(self, filename: str, **filters) -> int:
        """ייצוא עובדים ל-CSV"""
        
        try:
            if filters:
                employees = self.search_employees(**filters)
            else:
                employees = self.get_all_employees()
            
            if not employees:
                print("אין עובדים לייצוא")
                return 0
            
            with open(filename, 'w', newline='', encoding='utf-8') as file:
                fieldnames = ['id', 'name', 'age', 'city', 'salary', 'department', 'hire_date']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                
                writer.writeheader()
                
                for emp in employees:
                    writer.writerow({
                        'id': emp.id,
                        'name': emp.name,
                        'age': emp.age,
                        'city': emp.city,
                        'salary': emp.salary,
                        'department': emp.department,
                        'hire_date': emp.hire_date
                    })
            
            print(f"✓ {len(employees)} עובדים יוצאו ל-{filename}")
            return len(employees)
            
        except Exception as e:
            print(f"✗ שגיאה בייצוא: {e}")
            return 0
    
    def export_to_excel(self, filename: str, **filters) -> int:
        """ייצוא עובדים ל-Excel"""
        
        try:
            if filters:
                employees = self.search_employees(**filters)
            else:
                employees = self.get_all_employees()
            
            if not employees:
                print("אין עובדים לייצוא")
                return 0
            
            data = []
            for emp in employees:
                data.append({
                    'ID': emp.id,
                    'שם': emp.name,
                    'גיל': emp.age,
                    'עיר': emp.city,
                    'משכורת': emp.salary,
                    'מחלקה': emp.department,
                    'תאריך קבלה': emp.hire_date
                })
            
            df = pd.DataFrame(data)
            df.to_excel(filename, index=False, engine='openpyxl')
            
            print(f"✓ {len(employees)} עובדים יוצאו ל-{filename}")
            return len(employees)
            
        except Exception as e:
            print(f"✗ שגיאה בייצוא ל-Excel: {e}")
            print("אולי צריך להתקין: pip install openpyxl")
            return 0
    
    # ========== פעולות מיוחדות ==========
    
    def give_raise(self, employee_id: int, percentage: float) -> bool:
        """העלאת שכר באחוזים"""
        with Session(self.engine) as session:
            employee = session.get(Employee, employee_id)
            
            if not employee:
                print(f"✗ עובד עם ID {employee_id} לא נמצא")
                return False
            
            old_salary = employee.salary
            employee.salary *= (1 + percentage / 100)
            
            session.add(employee)
            session.commit()
            
            print(f"✓ {employee.name}: {old_salary:.2f} → {employee.salary:.2f} ₪ (+{percentage}%)")
            return True
    
    def mass_raise(self, percentage: float, **filters) -> int:
        """העלאת שכר קבוצתית"""
        employees = self.search_employees(**filters)
        
        if not employees:
            print("לא נמצאו עובדים התואמים את הקריטריונים")
            return 0
        
        with Session(self.engine) as session:
            for emp in employees:
                db_emp = session.get(Employee, emp.id)
                db_emp.salary *= (1 + percentage / 100)
                session.add(db_emp)
            
            session.commit()
        
        print(f"✓ {len(employees)} עובדים קיבלו העלאה של {percentage}%")
        return len(employees)


# ============= דוגמאות שימוש =============

if __name__ == "__main__":
    # יצירת מנהל
    DATABASE_URL = "mysql+pymysql://root:your_password@localhost:3306/company_db"
    manager = EmployeeManager(DATABASE_URL)
    
    # הוספת עובדים
    manager.add_employee(
        name="Alice",
        age=25,
        city="Tel Aviv",
        salary=10000,
        department="IT",
        hire_date="2024-01-15"
    )
    
    manager.add_employee(
        name="Bob",
        age=30,
        city="Jerusalem",
        salary=12000,
        department="Sales",
        hire_date="2023-06-01"
    )
    
    # הצגת סטטיסטיקות
    manager.print_statistics()
    
    # חיפוש עובדים
    it_employees = manager.search_employees(department="IT")
    print(f"\nעובדי IT: {len(it_employees)}")
    
    # העלאת שכר
    manager.mass_raise(10, department="IT")
    
    # ייצוא ל-CSV
    manager.export_to_csv('employees_backup.csv')
    
    # ייצוא עובדי IT בלבד
    manager.export_to_csv('it_employees.csv', department="IT")
```

---

## תרגילים מעשיים

### תרגיל 1: יצירת מסד נתונים לסטודנטים

**משימה:**
1. צור מודל `Student` עם השדות: name, age, grade, subject
2. צור קובץ CSV עם 5 סטודנטים
3. ייבא אותם למסד נתונים
4. הצג את כל הסטודנטים עם ציון מעל 80

**פתרון:**

```python
from sqlmodel import SQLModel, Field, create_engine, Session, select
from typing import Optional
import csv

# שלב 1: יצירת מודל
class Student(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    age: int
    grade: float = Field(ge=0, le=100)
    subject: str

# שלב 2: יצירת CSV
students_data = [
    ['name', 'age', 'grade', 'subject'],
    ['David', 20, 85, 'Math'],
    ['Emma', 22, 90, 'Physics'],
    ['Frank', 21, 88, 'Chemistry'],
    ['Grace', 23, 95, 'Biology'],
    ['Henry', 19, 75, 'Math']
]

with open('students.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerows(students_data)

print("✓ קובץ CSV נוצר!")

# שלב 3: ייבוא למסד נתונים
DATABASE_URL = "mysql+pymysql://root:your_password@localhost:3306/school_db"
engine = create_engine(DATABASE_URL)
SQLModel.metadata.create_all(engine)

with open('students.csv', 'r', encoding='utf-8') as file:
    csv_reader = csv.DictReader(file)
    
    with Session(engine) as session:
        for row in csv_reader:
            student = Student(
                name=row['name'],
                age=int(row['age']),
                grade=float(row['grade']),
                subject=row['subject']
            )
            session.add(student)
        session.commit()

print("✓ סטודנטים יובאו!")

# שלב 4: הצגת סטודנטים עם ציון מעל 80
with Session(engine) as session:
    statement = select(Student).where(Student.grade > 80)
    high_achievers = session.exec(statement).all()
    
    print(f"\nסטודנטים עם ציון מעל 80:")
    for student in high_achievers:
        print(f"  {student.name}: {student.grade} ב-{student.subject}")
```

### תרגיל 2: ניתוח ועדכון נתונים

**משימה:**
1. חשב את ממוצע הציונים לכל מקצוע
2. העלה את הציונים במתמטיקה ב-5%
3. ייצא את התוצאות ל-CSV חדש

**פתרון:**

```python
from collections import defaultdict

with Session(engine) as session:
    # שליפת כל הסטודנטים
    students = session.exec(select(Student)).all()
    
    # חישוב ממוצע לפי מקצוע
    subject_grades = defaultdict(list)
    
    for student in students:
        subject_grades[student.subject].append(student.grade)
    
    print("\nממוצע ציונים לפי מקצוע:")
    for subject, grades in subject_grades.items():
        avg = sum(grades) / len(grades)
        print(f"  {subject}: {avg:.2f}")
    
    # העלאת ציונים במתמטיקה
    math_students = session.exec(
        select(Student).where(Student.subject == "Math")
    ).all()
    
    for student in math_students:
        old_grade = student.grade
        student.grade = min(100, student.grade * 1.05)  # מקסימום 100
        session.add(student)
        print(f"  {student.name}: {old_grade:.1f} → {student.grade:.1f}")
    
    session.commit()
    
    # ייצוא לקובץ חדש
    all_students = session.exec(select(Student)).all()
    
    with open('students_updated.csv', 'w', newline='', encoding='utf-8') as file:
        fieldnames = ['id', 'name', 'age', 'grade', 'subject']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        
        writer.writeheader()
        for student in all_students:
            writer.writerow({
                'id': student.id,
                'name': student.name,
                'age': student.age,
                'grade': student.grade,
                'subject': student.subject
            })
    
    print("\n✓ הקובץ students_updated.csv נוצר!")
```

### תרגיל 3: מערכת דוחות

**משימה:**
צור דוח Excel המכיל:
1. סטטיסטיקות כלליות
2. רשימת מצטיינים (ציון מעל 90)
3. רשימה לפי מקצוע

**פתרון:**

```python
import pandas as pd
from sqlmodel import Session, select

def create_report(database_url: str, output_file: str):
    """יצירת דוח Excel מפורט"""
    
    engine = create_engine(database_url)
    
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        
        with Session(engine) as session:
            # גיליון 1: כל הסטודנטים
            students = session.exec(select(Student)).all()
            
            data = [{
                'ID': s.id,
                'שם': s.name,
                'גיל': s.age,
                'ציון': s.grade,
                'מקצוע': s.subject
            } for s in students]
            
            df_all = pd.DataFrame(data)
            df_all.to_excel(writer, sheet_name='כל הסטודנטים', index=False)
            
            # גיליון 2: מצטיינים
            high_achievers = session.exec(
                select(Student).where(Student.grade >= 90)
            ).all()
            
            data_ha = [{
                'שם': s.name,
                'ציון': s.grade,
                'מקצוע': s.subject
            } for s in high_achievers]
            
            df_ha = pd.DataFrame(data_ha)
            df_ha.to_excel(writer, sheet_name='מצטיינים', index=False)
            
            # גיליון 3: סטטיסטיקות
            stats = df_all.groupby('מקצוע').agg({
                'ציון': ['mean', 'min', 'max', 'count']
            }).round(2)
            
            stats.to_excel(writer, sheet_name='סטטיסטיקות')
    
    print(f"✓ דוח נוצר: {output_file}")

# שימוש
DATABASE_URL = "mysql+pymysql://root:your_password@localhost:3306/school_db"
create_report(DATABASE_URL, 'students_report.xlsx')
```

---

## טיפים למתחילים

### 1. בטיחות טיפוסים

SQLModel משתמש ב-Type Hints - תמיד הגדר טיפוסים:

```python
# ✓ נכון
def get_employee(employee_id: int) -> Optional[Employee]:
    pass

# ✗ לא מומלץ
def get_employee(employee_id):
    pass
```

### 2. טיפול בשגיאות

```python
from sqlmodel import Session
from sqlalchemy.exc import IntegrityError

try:
    with Session(engine) as session:
        # הפעולות שלך
        session.commit()
except IntegrityError as e:
    print(f"שגיאת אילוץ: {e}")
except Exception as e:
    print(f"שגיאה כללית: {e}")
```

### 3. שימוש ב-Context Manager

תמיד השתמש ב-`with` לניהול Sessions:

```python
# ✓ נכון
with Session(engine) as session:
    # הקוד שלך
    session.commit()
# ה-session נסגר אוטומטית

# ✗ לא מומלץ
session = Session(engine)
# קוד...
session.close()  # קל לשכוח!
```

### 4. Refresh אחרי Commit

```python
employee = Employee(name="Alice", age=25, city="Tel Aviv", salary=10000)

with Session(engine) as session:
    session.add(employee)
    session.commit()
    session.refresh(employee)  # מעדכן את ה-id
    print(f"ID חדש: {employee.id}")
```

### 5. אופטימיזציה לייבוא מסיבי

```python
# לייבוא כמויות גדולות
with Session(engine) as session:
    employees = []
    
    for row in csv_reader:
        employees.append(Employee(**row))
        
        # Commit כל 1000 שורות
        if len(employees) >= 1000:
            session.add_all(employees)
            session.commit()
            employees = []
    
    # Commit שארית
    if employees:
        session.add_all(employees)
        session.commit()
```

---

## סיכום

במדריך זה למדת:

✅ **SQLModel:**
- יצירת מודלים עם Type Hints
- וולידציה אוטומטית
- פעולות CRUD מלאות
- שאילתות עם select

✅ **CSV:**
- קריאה וכתיבה
- שימוש ב-Pandas
- המרה למודלים

✅ **MySQL:**
- התחברות דרך SQLModel
- יצירת טבלאות אוטומטית
- ניהול נתונים

✅ **שילוב:**
- ייבוא/ייצוא CSV ↔ MySQL
- סנכרון נתונים
- פרויקט מלא

### צעדים הבאים

1. למד על Relationships (קשרים בין טבלאות)
2. התנסה עם FastAPI + SQLModel
3. למד Alembic למיגרציות
4. בנה פרויקט אמיתי

---

## משאבים נוספים

- [תיעוד SQLModel](https://sqlmodel.tiangolo.com/)
- [תיעוד Pydantic](https://docs.pydantic.dev/)
- [תיעוד SQLAlchemy](https://docs.sqlalchemy.org/)
- [MySQL Connector](https://dev.mysql.com/doc/connector-python/en/)

**בהצלחה! 🚀**
