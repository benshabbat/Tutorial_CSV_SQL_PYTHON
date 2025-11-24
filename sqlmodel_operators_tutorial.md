# מדריך מקיף לאופרטורים ב-SQLModel

## תוכן עניינים
1. [הקדמה](#הקדמה)
2. [התקנה והגדרה](#התקנה-והגדרה)
3. [אופרטורי השוואה](#אופרטורי-השוואה)
4. [אופרטורים לוגיים](#אופרטורים-לוגיים)
5. [אופרטורי טקסט](#אופרטורי-טקסט)
6. [אופרטורים מתקדמים](#אופרטורים-מתקדמים)
7. [דוגמאות מעשיות](#דוגמאות-מעשיות)

---

## הקדמה

SQLModel מאפשר לנו לעבוד עם מסדי נתונים בצורה פיתונית (Pythonic) תוך שימוש באופרטורים שונים לסינון ושאילתות. במדריך זה נלמד את כל האופרטורים הזמינים.

---

## התקנה והגדרה

### התקנת החבילות הנדרשות

```bash
pip install sqlmodel
```

### יצירת מודל בסיסי

```python
from sqlmodel import SQLModel, Field, Session, create_engine, select
from typing import Optional
from datetime import date

class Employee(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    age: int
    salary: float
    department: str
    hire_date: date
    is_active: bool = True
    email: Optional[str] = None

# יצירת מנוע מסד נתונים
engine = create_engine("sqlite:///database.db")
SQLModel.metadata.create_all(engine)
```

---

## אופרטורי השוואה

### 1. שווה ל- (`==`)

```python
# מציאת עובדים בשם "יוסי"
with Session(engine) as session:
    statement = select(Employee).where(Employee.name == "יוסי")
    employees = session.exec(statement).all()
    for emp in employees:
        print(f"{emp.name} - {emp.department}")
```

**תוצאה SQL:**
```sql
SELECT * FROM employee WHERE name = 'יוסי'
```

### 2. לא שווה ל- (`!=`)

```python
# מציאת עובדים שלא במחלקת מכירות
with Session(engine) as session:
    statement = select(Employee).where(Employee.department != "מכירות")
    employees = session.exec(statement).all()
```

**תוצאה SQL:**
```sql
SELECT * FROM employee WHERE department != 'מכירות'
```

### 3. גדול מ- (`>`)

```python
# מציאת עובדים עם שכר מעל 10,000
with Session(engine) as session:
    statement = select(Employee).where(Employee.salary > 10000)
    employees = session.exec(statement).all()
```

**תוצאה SQL:**
```sql
SELECT * FROM employee WHERE salary > 10000
```

### 4. גדול או שווה ל- (`>=`)

```python
# מציאת עובדים בגיל 30 ומעלה
with Session(engine) as session:
    statement = select(Employee).where(Employee.age >= 30)
    employees = session.exec(statement).all()
```

**תוצאה SQL:**
```sql
SELECT * FROM employee WHERE age >= 30
```

### 5. קטן מ- (`<`)

```python
# מציאת עובדים עם שכר מתחת ל-15,000
with Session(engine) as session:
    statement = select(Employee).where(Employee.salary < 15000)
    employees = session.exec(statement).all()
```

**תוצאה SQL:**
```sql
SELECT * FROM employee WHERE salary < 15000
```

### 6. קטן או שווה ל- (`<=`)

```python
# מציאת עובדים עד גיל 25
with Session(engine) as session:
    statement = select(Employee).where(Employee.age <= 25)
    employees = session.exec(statement).all()
```

**תוצאה SQL:**
```sql
SELECT * FROM employee WHERE age <= 25
```

---

## אופרטורים לוגיים

### 1. וגם - AND

#### שימוש עם `,` (פסיק)

```python
# עובדים בגיל 25-35 עם שכר מעל 12,000
with Session(engine) as session:
    statement = select(Employee).where(
        Employee.age >= 25,
        Employee.age <= 35,
        Employee.salary > 12000
    )
    employees = session.exec(statement).all()
```

#### שימוש עם `&` (אופרטור AND)

```python
from sqlmodel import and_

# אותה שאילתה עם אופרטור &
with Session(engine) as session:
    statement = select(Employee).where(
        (Employee.age >= 25) & (Employee.age <= 35) & (Employee.salary > 12000)
    )
    employees = session.exec(statement).all()
```

#### שימוש עם `and_()`

```python
# אותה שאילתה עם פונקציית and_
with Session(engine) as session:
    statement = select(Employee).where(
        and_(
            Employee.age >= 25,
            Employee.age <= 35,
            Employee.salary > 12000
        )
    )
    employees = session.exec(statement).all()
```

**תוצאה SQL:**
```sql
SELECT * FROM employee 
WHERE age >= 25 AND age <= 35 AND salary > 12000
```

### 2. או - OR

```python
from sqlmodel import or_

# עובדים במחלקת פיתוח או שירות לקוחות
with Session(engine) as session:
    statement = select(Employee).where(
        or_(
            Employee.department == "פיתוח",
            Employee.department == "שירות לקוחות"
        )
    )
    employees = session.exec(statement).all()
```

#### שימוש עם `|` (אופרטור OR)

```python
# אותה שאילתה עם אופרטור |
with Session(engine) as session:
    statement = select(Employee).where(
        (Employee.department == "פיתוח") | (Employee.department == "שירות לקוחות")
    )
    employees = session.exec(statement).all()
```

**תוצאה SQL:**
```sql
SELECT * FROM employee 
WHERE department = 'פיתוח' OR department = 'שירות לקוחות'
```

### 3. שילוב AND ו-OR

```python
# עובדים במחלקת פיתוח עם שכר מעל 15,000 
# או במחלקת מכירות עם שכר מעל 20,000
with Session(engine) as session:
    statement = select(Employee).where(
        or_(
            and_(Employee.department == "פיתוח", Employee.salary > 15000),
            and_(Employee.department == "מכירות", Employee.salary > 20000)
        )
    )
    employees = session.exec(statement).all()
```

**תוצאה SQL:**
```sql
SELECT * FROM employee 
WHERE (department = 'פיתוח' AND salary > 15000) 
   OR (department = 'מכירות' AND salary > 20000)
```

### 4. NOT - שלילה

```python
from sqlmodel import not_

# עובדים שלא פעילים
with Session(engine) as session:
    statement = select(Employee).where(not_(Employee.is_active == True))
    employees = session.exec(statement).all()
```

#### שימוש עם `~` (אופרטור NOT)

```python
# אותה שאילתה עם אופרטור ~
with Session(engine) as session:
    statement = select(Employee).where(~(Employee.is_active == True))
    employees = session.exec(statement).all()
```

**תוצאה SQL:**
```sql
SELECT * FROM employee WHERE NOT (is_active = 1)
```

---

## אופרטורי טקסט

### 1. LIKE - התאמה עם תבניות

```python
from sqlmodel import col

# מציאת עובדים שהשם שלהם מתחיל ב-"יו"
with Session(engine) as session:
    statement = select(Employee).where(Employee.name.like("יו%"))
    employees = session.exec(statement).all()
```

**תבניות נפוצות:**
- `%` - כל רצף תווים
- `_` - תו בודד

**דוגמאות:**

```python
# שם מסתיים ב-"סי"
statement = select(Employee).where(Employee.name.like("%סי"))

# שם מכיל "דן"
statement = select(Employee).where(Employee.name.like("%דן%"))

# שם עם 4 תווים בדיוק
statement = select(Employee).where(Employee.name.like("____"))

# שם מתחיל ב-"א" ומסתיים ב-"ה"
statement = select(Employee).where(Employee.name.like("א%ה"))
```

**תוצאה SQL:**
```sql
SELECT * FROM employee WHERE name LIKE 'יו%'
```

### 2. NOT LIKE - שלילה של LIKE

```python
# עובדים שהשם שלהם לא מתחיל ב-"א"
with Session(engine) as session:
    statement = select(Employee).where(Employee.name.notlike("א%"))
    employees = session.exec(statement).all()
```

**תוצאה SQL:**
```sql
SELECT * FROM employee WHERE name NOT LIKE 'א%'
```

### 3. ILIKE - LIKE ללא תלות ברישיות (אותיות גדולות/קטנות)

```python
# מציאת עובדים ללא תלות ברישיות
with Session(engine) as session:
    statement = select(Employee).where(Employee.name.ilike("YOSSI%"))
    employees = session.exec(statement).all()
```

**הערה:** ILIKE לא נתמך בכל מסדי הנתונים (נתמך ב-PostgreSQL)

### 4. STARTSWITH - מתחיל ב

```python
# שם מתחיל ב-"דוד"
with Session(engine) as session:
    statement = select(Employee).where(Employee.name.startswith("דוד"))
    employees = session.exec(statement).all()
```

**תוצאה SQL:**
```sql
SELECT * FROM employee WHERE name LIKE 'דוד%'
```

### 5. ENDSWITH - מסתיים ב

```python
# אימייל מסתיים ב-"@company.com"
with Session(engine) as session:
    statement = select(Employee).where(Employee.email.endswith("@company.com"))
    employees = session.exec(statement).all()
```

**תוצאה SQL:**
```sql
SELECT * FROM employee WHERE email LIKE '%@company.com'
```

### 6. CONTAINS - מכיל

```python
# שם מכיל "אב"
with Session(engine) as session:
    statement = select(Employee).where(Employee.name.contains("אב"))
    employees = session.exec(statement).all()
```

**תוצאה SQL:**
```sql
SELECT * FROM employee WHERE name LIKE '%אב%'
```

---

## אופרטורים מתקדמים

### 1. IN - בתוך רשימה

```python
# עובדים ממחלקות מסוימות
with Session(engine) as session:
    departments = ["פיתוח", "מכירות", "שיווק"]
    statement = select(Employee).where(Employee.department.in_(departments))
    employees = session.exec(statement).all()
```

**תוצאה SQL:**
```sql
SELECT * FROM employee 
WHERE department IN ('פיתוח', 'מכירות', 'שיווק')
```

### 2. NOT IN - לא בתוך רשימה

```python
# עובדים שלא ממחלקות מסוימות
with Session(engine) as session:
    departments = ["ניהול", "משאבי אנוש"]
    statement = select(Employee).where(Employee.department.notin_(departments))
    employees = session.exec(statement).all()
```

**תוצאה SQL:**
```sql
SELECT * FROM employee 
WHERE department NOT IN ('ניהול', 'משאבי אנוש')
```

### 3. BETWEEN - בין

```python
# עובדים עם שכר בין 10,000 ל-20,000
with Session(engine) as session:
    statement = select(Employee).where(Employee.salary.between(10000, 20000))
    employees = session.exec(statement).all()
```

**תוצאה SQL:**
```sql
SELECT * FROM employee WHERE salary BETWEEN 10000 AND 20000
```

### 4. IS NULL - ערך ריק

```python
# עובדים ללא אימייל
with Session(engine) as session:
    statement = select(Employee).where(Employee.email.is_(None))
    employees = session.exec(statement).all()
```

**תוצאה SQL:**
```sql
SELECT * FROM employee WHERE email IS NULL
```

### 5. IS NOT NULL - ערך לא ריק

```python
# עובדים עם אימייל
with Session(engine) as session:
    statement = select(Employee).where(Employee.email.isnot(None))
    employees = session.exec(statement).all()
```

**תוצאה SQL:**
```sql
SELECT * FROM employee WHERE email IS NOT NULL
```

### 6. DISTINCT - ערכים ייחודיים

```python
from sqlmodel import func

# כל המחלקות הייחודיות
with Session(engine) as session:
    statement = select(Employee.department).distinct()
    departments = session.exec(statement).all()
```

**תוצאה SQL:**
```sql
SELECT DISTINCT department FROM employee
```

---

## דוגמאות מעשיות

### דוגמה 1: מערכת חיפוש מתקדמת

```python
from typing import Optional
from datetime import date

def search_employees(
    session: Session,
    min_age: Optional[int] = None,
    max_age: Optional[int] = None,
    min_salary: Optional[float] = None,
    max_salary: Optional[float] = None,
    departments: Optional[list[str]] = None,
    name_search: Optional[str] = None,
    is_active: Optional[bool] = None,
    hired_after: Optional[date] = None,
    hired_before: Optional[date] = None
):
    """
    פונקציה לחיפוש עובדים עם פילטרים מרובים
    """
    statement = select(Employee)
    conditions = []
    
    # סינון לפי גיל
    if min_age is not None:
        conditions.append(Employee.age >= min_age)
    if max_age is not None:
        conditions.append(Employee.age <= max_age)
    
    # סינון לפי שכר
    if min_salary is not None:
        conditions.append(Employee.salary >= min_salary)
    if max_salary is not None:
        conditions.append(Employee.salary <= max_salary)
    
    # סינון לפי מחלקות
    if departments:
        conditions.append(Employee.department.in_(departments))
    
    # חיפוש בשם
    if name_search:
        conditions.append(Employee.name.contains(name_search))
    
    # סינון לפי סטטוס פעיל
    if is_active is not None:
        conditions.append(Employee.is_active == is_active)
    
    # סינון לפי תאריך קבלה לעבודה
    if hired_after:
        conditions.append(Employee.hire_date >= hired_after)
    if hired_before:
        conditions.append(Employee.hire_date <= hired_before)
    
    # הוספת כל התנאים לשאילתה
    if conditions:
        statement = statement.where(and_(*conditions))
    
    return session.exec(statement).all()

# שימוש בפונקציה
with Session(engine) as session:
    results = search_employees(
        session,
        min_age=25,
        max_age=40,
        min_salary=12000,
        departments=["פיתוח", "מכירות"],
        name_search="יוסי",
        is_active=True
    )
    
    for emp in results:
        print(f"{emp.name} - {emp.department} - ₪{emp.salary}")
```

### דוגמה 2: דוחות וסטטיסטיקות

```python
from sqlmodel import func

def generate_department_report(session: Session):
    """
    יצירת דוח לפי מחלקות
    """
    # ספירת עובדים לפי מחלקה
    statement = select(
        Employee.department,
        func.count(Employee.id).label("employee_count"),
        func.avg(Employee.salary).label("avg_salary"),
        func.min(Employee.salary).label("min_salary"),
        func.max(Employee.salary).label("max_salary")
    ).group_by(Employee.department)
    
    results = session.exec(statement).all()
    
    print("דוח מחלקות:")
    print("-" * 80)
    for dept, count, avg_sal, min_sal, max_sal in results:
        print(f"מחלקה: {dept}")
        print(f"  מספר עובדים: {count}")
        print(f"  שכר ממוצע: ₪{avg_sal:.2f}")
        print(f"  שכר מינימלי: ₪{min_sal:.2f}")
        print(f"  שכר מקסימלי: ₪{max_sal:.2f}")
        print("-" * 80)

with Session(engine) as session:
    generate_department_report(session)
```

### דוגמה 3: שאילתות מורכבות

```python
def find_high_performers(session: Session):
    """
    מציאת עובדים בעלי ביצועים גבוהים
    (שכר מעל הממוצע במחלקה שלהם)
    """
    # תת-שאילתה לחישוב שכר ממוצע לפי מחלקה
    avg_salary_subquery = (
        select(
            Employee.department,
            func.avg(Employee.salary).label("dept_avg_salary")
        )
        .group_by(Employee.department)
        .subquery()
    )
    
    # שאילתה ראשית
    statement = (
        select(Employee)
        .join(
            avg_salary_subquery,
            Employee.department == avg_salary_subquery.c.department
        )
        .where(Employee.salary > avg_salary_subquery.c.dept_avg_salary)
        .order_by(Employee.salary.desc())
    )
    
    return session.exec(statement).all()

with Session(engine) as session:
    high_performers = find_high_performers(session)
    print("עובדים עם שכר מעל הממוצע במחלקה:")
    for emp in high_performers:
        print(f"{emp.name} - {emp.department} - ₪{emp.salary}")
```

### דוגמה 4: סינון עם תאריכים

```python
from datetime import datetime, timedelta

def get_recent_hires(session: Session, days: int = 90):
    """
    מציאת עובדים שנקלטו בימים האחרונים
    """
    cutoff_date = date.today() - timedelta(days=days)
    
    statement = select(Employee).where(
        and_(
            Employee.hire_date >= cutoff_date,
            Employee.is_active == True
        )
    ).order_by(Employee.hire_date.desc())
    
    return session.exec(statement).all()

def get_employees_by_year(session: Session, year: int):
    """
    מציאת עובדים שנקלטו בשנה מסוימת
    """
    start_date = date(year, 1, 1)
    end_date = date(year, 12, 31)
    
    statement = select(Employee).where(
        Employee.hire_date.between(start_date, end_date)
    )
    
    return session.exec(statement).all()

with Session(engine) as session:
    # עובדים מ-90 הימים האחרונים
    recent = get_recent_hires(session, days=90)
    print(f"נקלטו {len(recent)} עובדים ב-90 הימים האחרונים")
    
    # עובדים משנת 2024
    year_2024 = get_employees_by_year(session, 2024)
    print(f"נקלטו {len(year_2024)} עובדים בשנת 2024")
```

### דוגמה 5: חיפוש מתקדם עם CASE

```python
from sqlmodel import case

def categorize_employees_by_salary(session: Session):
    """
    סיווג עובדים לפי רמת שכר
    """
    salary_category = case(
        (Employee.salary < 10000, "נמוך"),
        (Employee.salary.between(10000, 20000), "בינוני"),
        (Employee.salary > 20000, "גבוה"),
        else_="לא מוגדר"
    ).label("salary_category")
    
    statement = select(
        Employee.name,
        Employee.salary,
        salary_category
    ).order_by(Employee.salary.desc())
    
    results = session.exec(statement).all()
    
    for name, salary, category in results:
        print(f"{name}: ₪{salary} - רמה: {category}")

with Session(engine) as session:
    categorize_employees_by_salary(session)
```

### דוגמה 6: פילטר דינמי

```python
def dynamic_filter(session: Session, filters: dict):
    """
    פילטר דינמי על בסיס מילון
    """
    statement = select(Employee)
    
    for field, value in filters.items():
        if isinstance(value, dict):
            # תמיכה באופרטורים מורכבים
            for operator, op_value in value.items():
                column = getattr(Employee, field)
                
                if operator == "eq":
                    statement = statement.where(column == op_value)
                elif operator == "ne":
                    statement = statement.where(column != op_value)
                elif operator == "gt":
                    statement = statement.where(column > op_value)
                elif operator == "gte":
                    statement = statement.where(column >= op_value)
                elif operator == "lt":
                    statement = statement.where(column < op_value)
                elif operator == "lte":
                    statement = statement.where(column <= op_value)
                elif operator == "in":
                    statement = statement.where(column.in_(op_value))
                elif operator == "like":
                    statement = statement.where(column.like(op_value))
                elif operator == "contains":
                    statement = statement.where(column.contains(op_value))
        else:
            # פילטר פשוט (שוויון)
            column = getattr(Employee, field)
            statement = statement.where(column == value)
    
    return session.exec(statement).all()

# שימוש בפילטר דינמי
with Session(engine) as session:
    filters = {
        "age": {"gte": 25, "lte": 40},
        "salary": {"gt": 12000},
        "department": {"in": ["פיתוח", "מכירות"]},
        "name": {"contains": "יוסי"},
        "is_active": True
    }
    
    results = dynamic_filter(session, filters)
    for emp in results:
        print(f"{emp.name} - {emp.age} - ₪{emp.salary}")
```

---

## טבלת סיכום אופרטורים

| אופרטור | תיאור | דוגמה Python | SQL מקביל |
|---------|-------|--------------|-----------|
| `==` | שווה ל | `Employee.age == 30` | `age = 30` |
| `!=` | לא שווה ל | `Employee.age != 30` | `age != 30` |
| `>` | גדול מ | `Employee.salary > 10000` | `salary > 10000` |
| `>=` | גדול או שווה | `Employee.salary >= 10000` | `salary >= 10000` |
| `<` | קטן מ | `Employee.salary < 20000` | `salary < 20000` |
| `<=` | קטן או שווה | `Employee.salary <= 20000` | `salary <= 20000` |
| `&` / `and_()` | וגם (AND) | `(a > 5) & (b < 10)` | `a > 5 AND b < 10` |
| `\|` / `or_()` | או (OR) | `(a == 1) \| (b == 2)` | `a = 1 OR b = 2` |
| `~` / `not_()` | שלילה (NOT) | `~(age > 30)` | `NOT (age > 30)` |
| `.like()` | התאמת תבנית | `name.like("יו%")` | `name LIKE 'יו%'` |
| `.notlike()` | שלילת התאמה | `name.notlike("א%")` | `name NOT LIKE 'א%'` |
| `.ilike()` | LIKE ללא רישיות | `name.ilike("YOSSI")` | `name ILIKE 'YOSSI'` |
| `.startswith()` | מתחיל ב | `name.startswith("דוד")` | `name LIKE 'דוד%'` |
| `.endswith()` | מסתיים ב | `email.endswith(".com")` | `email LIKE '%.com'` |
| `.contains()` | מכיל | `name.contains("אב")` | `name LIKE '%אב%'` |
| `.in_()` | בתוך רשימה | `dept.in_(["IT", "HR"])` | `dept IN ('IT', 'HR')` |
| `.notin_()` | לא בתוך רשימה | `dept.notin_(["IT"])` | `dept NOT IN ('IT')` |
| `.between()` | בין | `salary.between(10k, 20k)` | `salary BETWEEN 10000 AND 20000` |
| `.is_()` | הוא (NULL) | `email.is_(None)` | `email IS NULL` |
| `.isnot()` | אינו (NOT NULL) | `email.isnot(None)` | `email IS NOT NULL` |

---

## טיפים ושיטות עבודה מומלצות

### 1. שימוש נכון בסוגריים

```python
# ✅ נכון - עם סוגריים
statement = select(Employee).where(
    (Employee.age > 25) & (Employee.salary > 10000)
)

# ❌ שגוי - ללא סוגריים (עלול לגרום לשגיאות)
statement = select(Employee).where(
    Employee.age > 25 & Employee.salary > 10000
)
```

### 2. בדיקת NULL בצורה נכונה

```python
# ✅ נכון
statement = select(Employee).where(Employee.email.is_(None))

# ❌ שגוי
statement = select(Employee).where(Employee.email == None)
```

### 3. שימוש ב-IN עבור רשימות

```python
# ✅ נכון - יעיל
departments = ["פיתוח", "מכירות", "שיווק"]
statement = select(Employee).where(Employee.department.in_(departments))

# ❌ לא יעיל
statement = select(Employee).where(
    (Employee.department == "פיתוח") |
    (Employee.department == "מכירות") |
    (Employee.department == "שיווק")
)
```

### 4. חיפוש טקסט יעיל

```python
# חיפוש בתחילת השדה - יעיל יותר
statement = select(Employee).where(Employee.name.startswith("א"))

# חיפוש בכל מקום - פחות יעיל
statement = select(Employee).where(Employee.name.contains("א"))
```

### 5. שימוש ב-BETWEEN

```python
# ✅ נכון - יעיל וקריא
statement = select(Employee).where(Employee.age.between(25, 35))

# ❌ פחות קריא
statement = select(Employee).where(
    (Employee.age >= 25) & (Employee.age <= 35)
)
```

---

## סיכום

במדריך זה למדנו:

1. ✅ **אופרטורי השוואה**: `==`, `!=`, `>`, `>=`, `<`, `<=`
2. ✅ **אופרטורים לוגיים**: `&` (AND), `|` (OR), `~` (NOT)
3. ✅ **אופרטורי טקסט**: `like`, `ilike`, `startswith`, `endswith`, `contains`
4. ✅ **אופרטורים מתקדמים**: `in_`, `notin_`, `between`, `is_`, `isnot`
5. ✅ **דוגמאות מעשיות**: חיפוש מתקדם, דוחות, שאילתות מורכבות
6. ✅ **שיטות עבודה מומלצות**: טיפים לקוד יעיל וקריא

SQLModel מספקת כלים חזקים ופשוטים לעבודה עם מסדי נתונים בצורה פיתונית. השימוש באופרטורים הללו יאפשר לך לבנות שאילתות מורכבות ויעילות בקלות!

---

## משאבים נוספים

- [תיעוד רשמי של SQLModel](https://sqlmodel.tiangolo.com/)
- [SQLAlchemy - ספריית הבסיס](https://docs.sqlalchemy.org/)
- [Pydantic - אימות נתונים](https://docs.pydantic.dev/)

**בהצלחה! 🚀**
