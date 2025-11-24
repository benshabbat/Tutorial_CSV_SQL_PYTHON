# מדריך פונקציות ב-SQLModel

## מה זה פונקציות SQL?
פונקציות SQL מאפשרות לבצע חישובים וטרנספורמציות על הנתונים במסד הנתונים.

---

## התקנה

```bash
pip install sqlmodel
```

---

## פונקציות אגרגציה (Aggregation Functions)

### הגדרת מודל לדוגמה

```python
from sqlmodel import SQLModel, Field, Session, create_engine, select, func
from typing import Optional

class Employee(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    department: str
    salary: int
    age: int

# יצירת מנוע ומסד נתונים
engine = create_engine("sqlite:///company.db")
SQLModel.metadata.create_all(engine)

# הוספת נתונים לדוגמה
def add_sample_data():
    with Session(engine) as session:
        employees = [
            Employee(name="דני", department="פיתוח", salary=15000, age=25),
            Employee(name="שרה", department="פיתוח", salary=18000, age=30),
            Employee(name="יוסי", department="שיווק", salary=12000, age=28),
            Employee(name="רחל", department="שיווק", salary=13000, age=26),
            Employee(name="משה", department="פיתוח", salary=20000, age=35),
        ]
        session.add_all(employees)
        session.commit()
```

---

## 1. COUNT - ספירה

```python
from sqlmodel import Session, select, func

# ספירת כל העובדים
with Session(engine) as session:
    statement = select(func.count(Employee.id))
    total = session.exec(statement).one()
    print(f"סך כל העובדים: {total}")

# ספירה לפי מחלקה
with Session(engine) as session:
    statement = select(
        Employee.department,
        func.count(Employee.id).label("count")
    ).group_by(Employee.department)
    
    results = session.exec(statement).all()
    for dept, count in results:
        print(f"{dept}: {count} עובדים")
```

**פלט:**
```
סך כל העובדים: 5
פיתוח: 3 עובדים
שיווק: 2 עובדים
```

---

## 2. SUM - סכום

```python
# סכום כל המשכורות
with Session(engine) as session:
    statement = select(func.sum(Employee.salary))
    total_salary = session.exec(statement).one()
    print(f"סך כל המשכורות: {total_salary} ש״ח")

# סכום משכורות לפי מחלקה
with Session(engine) as session:
    statement = select(
        Employee.department,
        func.sum(Employee.salary).label("total")
    ).group_by(Employee.department)
    
    results = session.exec(statement).all()
    for dept, total in results:
        print(f"{dept}: {total} ש״ח")
```

**פלט:**
```
סך כל המשכורות: 78000 ש״ח
פיתוח: 53000 ש״ח
שיווק: 25000 ש״ח
```

---

## 3. AVG - ממוצע

```python
# ממוצע משכורות
with Session(engine) as session:
    statement = select(func.avg(Employee.salary))
    avg_salary = session.exec(statement).one()
    print(f"ממוצע משכורות: {avg_salary:.2f} ש״ח")

# ממוצע משכורות לפי מחלקה
with Session(engine) as session:
    statement = select(
        Employee.department,
        func.avg(Employee.salary).label("average")
    ).group_by(Employee.department)
    
    results = session.exec(statement).all()
    for dept, avg in results:
        print(f"{dept}: {avg:.2f} ש״ח")
```

**פלט:**
```
ממוצע משכורות: 15600.00 ש״ח
פיתוח: 17666.67 ש״ח
שיווק: 12500.00 ש״ח
```

---

## 4. MIN / MAX - מינימום ומקסימום

```python
# משכורת מינימלית ומקסימלית
with Session(engine) as session:
    min_salary = session.exec(select(func.min(Employee.salary))).one()
    max_salary = session.exec(select(func.max(Employee.salary))).one()
    
    print(f"משכורת מינימלית: {min_salary} ש״ח")
    print(f"משכורת מקסימלית: {max_salary} ש״ח")

# מי מקבל את המשכורת הגבוהה ביותר?
with Session(engine) as session:
    max_sal = session.exec(select(func.max(Employee.salary))).one()
    statement = select(Employee).where(Employee.salary == max_sal)
    top_earner = session.exec(statement).first()
    print(f"השכר הגבוה ביותר: {top_earner.name} - {top_earner.salary} ש״ח")
```

**פלט:**
```
משכורת מינימלית: 12000 ש״ח
משכורת מקסימלית: 20000 ש״ח
השכר הגבוה ביותר: משה - 20000 ש״ח
```

---

## 5. GROUP BY - קיבוץ נתונים

```python
# סטטיסטיקות מלאות לפי מחלקה
with Session(engine) as session:
    statement = select(
        Employee.department,
        func.count(Employee.id).label("employees"),
        func.avg(Employee.salary).label("avg_salary"),
        func.min(Employee.salary).label("min_salary"),
        func.max(Employee.salary).label("max_salary"),
        func.sum(Employee.salary).label("total_salary")
    ).group_by(Employee.department)
    
    results = session.exec(statement).all()
    
    print("סטטיסטיקות לפי מחלקה:")
    for dept, count, avg, min_sal, max_sal, total in results:
        print(f"\n{dept}:")
        print(f"  עובדים: {count}")
        print(f"  ממוצע: {avg:.2f} ש״ח")
        print(f"  מינימום: {min_sal} ש״ח")
        print(f"  מקסימום: {max_sal} ש״ח")
        print(f"  סך הכל: {total} ש״ח")
```

**פלט:**
```
סטטיסטיקות לפי מחלקה:

פיתוח:
  עובדים: 3
  ממוצע: 17666.67 ש״ח
  מינימום: 15000 ש״ח
  מקסימום: 20000 ש״ח
  סך הכל: 53000 ש״ח

שיווק:
  עובדים: 2
  ממוצע: 12500.00 ש״ח
  מינימום: 12000 ש״ח
  מקסימום: 13000 ש״ח
  סך הכל: 25000 ש״ח
```

---

## 6. HAVING - סינון אחרי קיבוץ

```python
# מחלקות עם יותר מעובד אחד
with Session(engine) as session:
    statement = select(
        Employee.department,
        func.count(Employee.id).label("count")
    ).group_by(Employee.department).having(func.count(Employee.id) > 1)
    
    results = session.exec(statement).all()
    print("מחלקות עם יותר מעובד אחד:")
    for dept, count in results:
        print(f"{dept}: {count} עובדים")

# מחלקות עם ממוצע משכורת מעל 15000
with Session(engine) as session:
    statement = select(
        Employee.department,
        func.avg(Employee.salary).label("avg_salary")
    ).group_by(Employee.department).having(func.avg(Employee.salary) > 15000)
    
    results = session.exec(statement).all()
    print("\nמחלקות עם ממוצע משכורת מעל 15000:")
    for dept, avg in results:
        print(f"{dept}: {avg:.2f} ש״ח")
```

---

## 7. פונקציות טקסט

```python
# UPPER - אותיות גדולות
with Session(engine) as session:
    statement = select(func.upper(Employee.name), Employee.department)
    results = session.exec(statement).all()
    for name, dept in results:
        print(f"{name} - {dept}")

# LENGTH - אורך מחרוזת
with Session(engine) as session:
    statement = select(
        Employee.name,
        func.length(Employee.name).label("name_length")
    )
    results = session.exec(statement).all()
    for name, length in results:
        print(f"{name}: {length} תווים")

# CONCAT - חיבור מחרוזות
with Session(engine) as session:
    statement = select(
        func.concat(Employee.name, " - ", Employee.department).label("full_info")
    )
    results = session.exec(statement).all()
    for info in results:
        print(info[0])
```

---

## 8. פונקציות תאריך (Date Functions)

```python
from datetime import date

class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    created_at: date
    completed: bool = False

# יצירת טבלה
SQLModel.metadata.create_all(engine)

# הוספת משימות
with Session(engine) as session:
    tasks = [
        Task(title="משימה 1", created_at=date(2025, 1, 15)),
        Task(title="משימה 2", created_at=date(2025, 2, 20)),
        Task(title="משימה 3", created_at=date(2025, 3, 10)),
    ]
    session.add_all(tasks)
    session.commit()

# חילוץ שנה, חודש, יום
with Session(engine) as session:
    statement = select(
        Task.title,
        func.strftime('%Y', Task.created_at).label("year"),
        func.strftime('%m', Task.created_at).label("month"),
        func.strftime('%d', Task.created_at).label("day")
    )
    results = session.exec(statement).all()
    for title, year, month, day in results:
        print(f"{title}: {day}/{month}/{year}")
```

---

## 9. DISTINCT - ערכים ייחודיים

```python
# כל המחלקות (ללא כפילויות)
with Session(engine) as session:
    statement = select(func.distinct(Employee.department))
    departments = session.exec(statement).all()
    print("מחלקות:")
    for dept in departments:
        print(f"- {dept}")

# ספירת מחלקות ייחודיות
with Session(engine) as session:
    statement = select(func.count(func.distinct(Employee.department)))
    count = session.exec(statement).one()
    print(f"מספר מחלקות: {count}")
```

---

## 10. CASE - תנאים

```python
from sqlalchemy import case

# סיווג עובדים לפי גיל
with Session(engine) as session:
    age_category = case(
        (Employee.age < 27, "צעיר"),
        (Employee.age < 32, "בוגר"),
        else_="ותיק"
    )
    
    statement = select(
        Employee.name,
        Employee.age,
        age_category.label("category")
    )
    
    results = session.exec(statement).all()
    for name, age, category in results:
        print(f"{name} ({age}): {category}")

# ספירה לפי קטגוריה
with Session(engine) as session:
    age_category = case(
        (Employee.age < 27, "צעיר"),
        (Employee.age < 32, "בוגר"),
        else_="ותיק"
    )
    
    statement = select(
        age_category.label("category"),
        func.count(Employee.id).label("count")
    ).group_by(age_category)
    
    results = session.exec(statement).all()
    for category, count in results:
        print(f"{category}: {count} עובדים")
```

---

## דוגמה מקיפה - דוח מלא

```python
def generate_department_report():
    """יצירת דוח מפורט לפי מחלקות"""
    with Session(engine) as session:
        statement = select(
            Employee.department,
            func.count(Employee.id).label("total_employees"),
            func.avg(Employee.age).label("avg_age"),
            func.avg(Employee.salary).label("avg_salary"),
            func.min(Employee.salary).label("min_salary"),
            func.max(Employee.salary).label("max_salary"),
            func.sum(Employee.salary).label("total_cost")
        ).group_by(Employee.department).order_by(
            func.sum(Employee.salary).desc()
        )
        
        results = session.exec(statement).all()
        
        print("=" * 60)
        print("דוח מחלקות - סיכום")
        print("=" * 60)
        
        for dept, emp_count, avg_age, avg_sal, min_sal, max_sal, total in results:
            print(f"\nמחלקה: {dept}")
            print(f"  מספר עובדים: {emp_count}")
            print(f"  גיל ממוצע: {avg_age:.1f}")
            print(f"  משכורת ממוצעת: {avg_sal:,.0f} ש״ח")
            print(f"  טווח משכורות: {min_sal:,} - {max_sal:,} ש״ח")
            print(f"  עלות כוללת: {total:,} ש״ח")
        
        print("=" * 60)

# הרץ דוח
generate_department_report()
```

---

## טבלת סיכום פונקציות

| פונקציה | תיאור | דוגמה |
|---------|-------|--------|
| `count()` | ספירה | `func.count(Employee.id)` |
| `sum()` | סכום | `func.sum(Employee.salary)` |
| `avg()` | ממוצע | `func.avg(Employee.age)` |
| `min()` | מינימום | `func.min(Employee.salary)` |
| `max()` | מקסימום | `func.max(Employee.salary)` |
| `upper()` | אותיות גדולות | `func.upper(Employee.name)` |
| `lower()` | אותיות קטנות | `func.lower(Employee.name)` |
| `length()` | אורך | `func.length(Employee.name)` |
| `concat()` | חיבור מחרוזות | `func.concat(a, b)` |
| `distinct()` | ערכים ייחודיים | `func.distinct(Employee.dept)` |

---

## טיפים חשובים

1. **תמיד השתמש ב-`label()`** לשמות ברורים:
   ```python
   func.count(Employee.id).label("total")
   ```

2. **`group_by` לפני `having`**:
   ```python
   .group_by(Employee.department).having(func.count(Employee.id) > 2)
   ```

3. **שלב פונקציות עם `where`**:
   ```python
   select(func.avg(Employee.salary)).where(Employee.department == "פיתוח")
   ```

4. **השתמש ב-`.one()` לערך בודד** ו-`.all()` למספר תוצאות.

---

זהו! עכשיו אתה יכול להשתמש בפונקציות SQL ב-SQLModel לניתוח נתונים מתקדם.
