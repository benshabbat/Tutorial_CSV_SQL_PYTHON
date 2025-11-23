# מדריך למתחילים: FastAPI, CSV, MySQL, SQLModel ו-Python

## תוכן עניינים
1. [מבוא](#מבוא)
2. [התקנה והכנה](#התקנה-והכנה)
3. [חלק 1: FastAPI - היסודות](#חלק-1-fastapi---היסודות)
4. [חלק 2: SQLModel עם MySQL](#חלק-2-sqlmodel-עם-mysql)
5. [חלק 3: בניית REST API מלא](#חלק-3-בניית-rest-api-מלא)
6. [חלק 4: עבודה עם CSV](#חלק-4-עבודה-עם-csv)
7. [חלק 5: פרויקט מלא - מערכת ניהול עובדים](#חלק-5-פרויקט-מלא---מערכת-ניהול-עובדים)
8. [חלק 6: פריסה ובדיקות](#חלק-6-פריסה-ובדיקות)
9. [תרגילים מעשיים](#תרגילים-מעשיים)

---

## מבוא

### מה נלמד?
במדריך זה נלמד כיצד:
- לבנות REST API מודרני עם FastAPI
- לעבוד עם SQLModel למסד נתונים
- לחבר MySQL למערכת
- לייבא/לייצא נתונים מ/ל-CSV
- לבנות אפליקציה מלאה עם כל הפיצ'רים

### מה זה FastAPI?
FastAPI היא ספרייה מודרנית לבניית APIs ש:
- **מהירה** - ביצועים גבוהים מאוד
- **קלה ללמידה** - תחביר פשוט ואינטואיטיבי
- **אוטומטית** - תיעוד אוטומטי (Swagger UI)
- **בטיחותית** - Type hints ווולידציה
- **אסינכרונית** - תמיכה ב-async/await

### למי המדריך מיועד?
- מתחילים בפיתוח Backend
- מפתחים שרוצים ללמוד FastAPI
- מי שמעוניין בבניית APIs מודרניים

---

## התקנה והכנה

### שלב 1: ודא ש-Python מותקן

```bash
python --version
```

נדרש Python 3.7 ומעלה (מומלץ 3.10+).

### שלב 2: יצירת סביבת עבודה

```bash
# יצירת תיקייה לפרויקט
mkdir employee_api
cd employee_api

# יצירת סביבה וירטואלית
python -m venv venv

# הפעלת הסביבה הוירטואלית
# ב-Windows:
venv\Scripts\activate
# ב-Mac/Linux:
source venv/bin/activate
```

### שלב 3: התקנת הספריות

```bash
pip install fastapi uvicorn sqlmodel pymysql pandas python-multipart
```

**הסבר:**
- `fastapi` - הספרייה העיקרית
- `uvicorn` - שרת ASGI להרצת FastAPI
- `sqlmodel` - ORM מודרני
- `pymysql` - דרייבר MySQL
- `pandas` - עבודה עם CSV
- `python-multipart` - להעלאת קבצים

### שלב 4: התקנת MySQL

1. הורד והתקן MySQL Server
2. הגדר סיסמת root
3. צור מסד נתונים:

```sql
CREATE DATABASE company_db;
```

---

## חלק 1: FastAPI - היסודות

### 1.1: ה-API הראשון שלך

צור קובץ `main.py`:

```python
from fastapi import FastAPI

# יצירת אפליקציית FastAPI
app = FastAPI(
    title="Employee Management API",
    description="API לניהול עובדים",
    version="1.0.0"
)

# נתיב פשוט
@app.get("/")
def read_root():
    """עמוד הבית"""
    return {"message": "ברוכים הבאים ל-Employee API!"}

# נתיב עם פרמטר
@app.get("/hello/{name}")
def say_hello(name: str):
    """ברכה אישית"""
    return {"message": f"שלום, {name}!"}

# נתיב עם Query Parameters
@app.get("/items/")
def read_items(skip: int = 0, limit: int = 10):
    """קבלת פריטים עם פגינציה"""
    return {
        "skip": skip,
        "limit": limit,
        "items": [f"item_{i}" for i in range(skip, skip + limit)]
    }
```

### הרצת השרת:

```bash
uvicorn main:app --reload
```

**גש לדפדפן:**
- `http://127.0.0.1:8000` - ה-API שלך
- `http://127.0.0.1:8000/docs` - תיעוד אינטראקטיבי (Swagger UI)
- `http://127.0.0.1:8000/redoc` - תיעוד חלופי

### 1.2: Request Body עם Pydantic

```python
from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()

# מודל Pydantic
class Employee(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    age: int = Field(..., gt=18, lt=120)
    city: str
    salary: float = Field(..., gt=0)
    department: Optional[str] = None

# POST - יצירת עובד
@app.post("/employees/")
def create_employee(employee: Employee):
    """יצירת עובד חדש"""
    return {
        "message": "עובד נוצר בהצלחה!",
        "employee": employee
    }

# PUT - עדכון עובד
@app.put("/employees/{employee_id}")
def update_employee(employee_id: int, employee: Employee):
    """עדכון עובד קיים"""
    return {
        "employee_id": employee_id,
        "updated_data": employee
    }
```

### 1.3: Response Models

```python
from typing import List

class EmployeeResponse(BaseModel):
    id: int
    name: str
    age: int
    city: str
    salary: float
    department: Optional[str] = None
    
    class Config:
        from_attributes = True  # לתמיכה ב-ORM

# GET עם Response Model
@app.get("/employees/", response_model=List[EmployeeResponse])
def get_employees():
    """קבלת כל העובדים"""
    # בינתיים נתונים מזויפים
    fake_employees = [
        {"id": 1, "name": "Alice", "age": 25, "city": "Tel Aviv", "salary": 10000},
        {"id": 2, "name": "Bob", "age": 30, "city": "Jerusalem", "salary": 12000}
    ]
    return fake_employees
```

### 1.4: Status Codes ו-Exceptions

```python
from fastapi import HTTPException, status

# מסד נתונים מזויף
fake_db = {
    1: {"id": 1, "name": "Alice", "age": 25, "city": "Tel Aviv", "salary": 10000}
}

@app.get("/employees/{employee_id}", response_model=EmployeeResponse)
def get_employee(employee_id: int):
    """קבלת עובד לפי ID"""
    if employee_id not in fake_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"עובד עם ID {employee_id} לא נמצא"
        )
    return fake_db[employee_id]

@app.delete("/employees/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(employee_id: int):
    """מחיקת עובד"""
    if employee_id not in fake_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"עובד עם ID {employee_id} לא נמצא"
        )
    del fake_db[employee_id]
    return None
```

---

## חלק 2: SQLModel עם MySQL

### 2.1: הגדרת מודל וחיבור

צור קובץ `database.py`:

```python
from sqlmodel import SQLModel, create_engine
from typing import Optional

# כתובת מסד הנתונים
DATABASE_URL = "mysql+pymysql://root:your_password@localhost:3306/company_db"

# יצירת מנוע
engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    """יצירת כל הטבלאות"""
    SQLModel.metadata.create_all(engine)
```

צור קובץ `models.py`:

```python
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Employee(SQLModel, table=True):
    """מודל עובד"""
    __tablename__ = "employees"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100, index=True)
    age: int = Field(ge=18, le=120)
    city: str = Field(max_length=100)
    salary: float = Field(gt=0)
    department: Optional[str] = Field(default=None, max_length=100)
    hire_date: Optional[str] = Field(default=None)
    is_active: bool = Field(default=True)
    created_at: Optional[str] = Field(default=None)
    
    class Config:
        arbitrary_types_allowed = True

# מודל לקבלת נתונים (ללא ID)
class EmployeeCreate(SQLModel):
    name: str = Field(min_length=2, max_length=100)
    age: int = Field(ge=18, le=120)
    city: str
    salary: float = Field(gt=0)
    department: Optional[str] = None
    hire_date: Optional[str] = None

# מודל לעדכון (כל השדות אופציונליים)
class EmployeeUpdate(SQLModel):
    name: Optional[str] = None
    age: Optional[int] = None
    city: Optional[str] = None
    salary: Optional[float] = None
    department: Optional[str] = None
    is_active: Optional[bool] = None

# מודל לתשובה
class EmployeeResponse(SQLModel):
    id: int
    name: str
    age: int
    city: str
    salary: float
    department: Optional[str] = None
    hire_date: Optional[str] = None
    is_active: bool
    created_at: Optional[str] = None
    
    class Config:
        from_attributes = True
```

### 2.2: Dependency Injection - Session

צור קובץ `dependencies.py`:

```python
from sqlmodel import Session
from database import engine
from typing import Generator

def get_session() -> Generator[Session, None, None]:
    """מחזיר session למסד נתונים"""
    with Session(engine) as session:
        yield session
```

---

## חלק 3: בניית REST API מלא

### 3.1: CRUD Operations

צור קובץ `crud.py`:

```python
from sqlmodel import Session, select
from models import Employee, EmployeeCreate, EmployeeUpdate
from typing import List, Optional
from datetime import datetime

class EmployeeCRUD:
    """פעולות CRUD על עובדים"""
    
    @staticmethod
    def create(session: Session, employee: EmployeeCreate) -> Employee:
        """יצירת עובד חדש"""
        db_employee = Employee(
            **employee.model_dump(),
            created_at=datetime.now().isoformat()
        )
        session.add(db_employee)
        session.commit()
        session.refresh(db_employee)
        return db_employee
    
    @staticmethod
    def get_by_id(session: Session, employee_id: int) -> Optional[Employee]:
        """קבלת עובד לפי ID"""
        return session.get(Employee, employee_id)
    
    @staticmethod
    def get_all(
        session: Session,
        skip: int = 0,
        limit: int = 100
    ) -> List[Employee]:
        """קבלת כל העובדים עם פגינציה"""
        statement = select(Employee).offset(skip).limit(limit)
        return session.exec(statement).all()
    
    @staticmethod
    def get_by_city(session: Session, city: str) -> List[Employee]:
        """קבלת עובדים לפי עיר"""
        statement = select(Employee).where(Employee.city == city)
        return session.exec(statement).all()
    
    @staticmethod
    def get_by_department(session: Session, department: str) -> List[Employee]:
        """קבלת עובדים לפי מחלקה"""
        statement = select(Employee).where(Employee.department == department)
        return session.exec(statement).all()
    
    @staticmethod
    def search(
        session: Session,
        city: Optional[str] = None,
        department: Optional[str] = None,
        min_salary: Optional[float] = None,
        max_salary: Optional[float] = None,
        is_active: Optional[bool] = None
    ) -> List[Employee]:
        """חיפוש עובדים עם פילטרים"""
        statement = select(Employee)
        
        if city:
            statement = statement.where(Employee.city == city)
        if department:
            statement = statement.where(Employee.department == department)
        if min_salary is not None:
            statement = statement.where(Employee.salary >= min_salary)
        if max_salary is not None:
            statement = statement.where(Employee.salary <= max_salary)
        if is_active is not None:
            statement = statement.where(Employee.is_active == is_active)
        
        return session.exec(statement).all()
    
    @staticmethod
    def update(
        session: Session,
        employee_id: int,
        employee_update: EmployeeUpdate
    ) -> Optional[Employee]:
        """עדכון עובד"""
        db_employee = session.get(Employee, employee_id)
        
        if not db_employee:
            return None
        
        # עדכון רק השדות שסופקו
        update_data = employee_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_employee, key, value)
        
        session.add(db_employee)
        session.commit()
        session.refresh(db_employee)
        return db_employee
    
    @staticmethod
    def delete(session: Session, employee_id: int) -> bool:
        """מחיקת עובד"""
        db_employee = session.get(Employee, employee_id)
        
        if not db_employee:
            return False
        
        session.delete(db_employee)
        session.commit()
        return True
    
    @staticmethod
    def count(session: Session) -> int:
        """ספירת עובדים"""
        statement = select(Employee)
        return len(session.exec(statement).all())
```

### 3.2: Routes - נתיבי API

צור קובץ `routes.py`:

```python
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session
from typing import List, Optional

from models import Employee, EmployeeCreate, EmployeeUpdate, EmployeeResponse
from crud import EmployeeCRUD
from dependencies import get_session

router = APIRouter(
    prefix="/api/v1/employees",
    tags=["employees"]
)

# CREATE - יצירת עובד
@router.post("/", response_model=EmployeeResponse, status_code=status.HTTP_201_CREATED)
def create_employee(
    employee: EmployeeCreate,
    session: Session = Depends(get_session)
):
    """
    יצירת עובד חדש
    
    - **name**: שם העובד (2-100 תווים)
    - **age**: גיל (18-120)
    - **city**: עיר מגורים
    - **salary**: משכורת (מעל 0)
    - **department**: מחלקה (אופציונלי)
    - **hire_date**: תאריך קבלה (אופציונלי)
    """
    return EmployeeCRUD.create(session, employee)

# READ - קבלת כל העובדים
@router.get("/", response_model=List[EmployeeResponse])
def get_employees(
    skip: int = Query(0, ge=0, description="מספר עובדים לדלג"),
    limit: int = Query(100, ge=1, le=1000, description="מספר מקסימלי לתוצאות"),
    session: Session = Depends(get_session)
):
    """קבלת רשימת עובדים עם פגינציה"""
    return EmployeeCRUD.get_all(session, skip, limit)

# READ - קבלת עובד לפי ID
@router.get("/{employee_id}", response_model=EmployeeResponse)
def get_employee(
    employee_id: int,
    session: Session = Depends(get_session)
):
    """קבלת עובד לפי ID"""
    employee = EmployeeCRUD.get_by_id(session, employee_id)
    
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"עובד עם ID {employee_id} לא נמצא"
        )
    
    return employee

# READ - חיפוש עובדים
@router.get("/search/advanced", response_model=List[EmployeeResponse])
def search_employees(
    city: Optional[str] = Query(None, description="סינון לפי עיר"),
    department: Optional[str] = Query(None, description="סינון לפי מחלקה"),
    min_salary: Optional[float] = Query(None, ge=0, description="משכורת מינימלית"),
    max_salary: Optional[float] = Query(None, ge=0, description="משכורת מקסימלית"),
    is_active: Optional[bool] = Query(None, description="סינון לפי סטטוס"),
    session: Session = Depends(get_session)
):
    """חיפוש מתקדם של עובדים"""
    return EmployeeCRUD.search(
        session,
        city=city,
        department=department,
        min_salary=min_salary,
        max_salary=max_salary,
        is_active=is_active
    )

# UPDATE - עדכון עובד
@router.put("/{employee_id}", response_model=EmployeeResponse)
def update_employee(
    employee_id: int,
    employee: EmployeeUpdate,
    session: Session = Depends(get_session)
):
    """עדכון פרטי עובד"""
    updated_employee = EmployeeCRUD.update(session, employee_id, employee)
    
    if not updated_employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"עובד עם ID {employee_id} לא נמצא"
        )
    
    return updated_employee

# PATCH - עדכון חלקי
@router.patch("/{employee_id}", response_model=EmployeeResponse)
def partial_update_employee(
    employee_id: int,
    employee: EmployeeUpdate,
    session: Session = Depends(get_session)
):
    """עדכון חלקי של עובד"""
    return update_employee(employee_id, employee, session)

# DELETE - מחיקת עובד
@router.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(
    employee_id: int,
    session: Session = Depends(get_session)
):
    """מחיקת עובד"""
    success = EmployeeCRUD.delete(session, employee_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"עובד עם ID {employee_id} לא נמצא"
        )
    
    return None

# סטטיסטיקות
@router.get("/stats/count")
def get_employee_count(session: Session = Depends(get_session)):
    """ספירת עובדים"""
    return {"total_employees": EmployeeCRUD.count(session)}
```

---

## חלק 4: עבודה עם CSV

### 4.1: ייבוא וייצוא CSV

צור קובץ `csv_operations.py`:

```python
import csv
import pandas as pd
from sqlmodel import Session
from typing import List
from models import Employee, EmployeeCreate
from crud import EmployeeCRUD
from io import StringIO

class CSVOperations:
    """פעולות CSV"""
    
    @staticmethod
    def import_from_csv(session: Session, file_content: str) -> dict:
        """ייבוא עובדים מקובץ CSV"""
        csv_file = StringIO(file_content)
        csv_reader = csv.DictReader(csv_file)
        
        imported = 0
        errors = []
        
        for row_num, row in enumerate(csv_reader, start=2):
            try:
                employee = EmployeeCreate(
                    name=row['name'],
                    age=int(row['age']),
                    city=row['city'],
                    salary=float(row['salary']),
                    department=row.get('department'),
                    hire_date=row.get('hire_date')
                )
                
                EmployeeCRUD.create(session, employee)
                imported += 1
                
            except Exception as e:
                errors.append({
                    "row": row_num,
                    "error": str(e),
                    "data": row
                })
        
        return {
            "imported": imported,
            "errors": errors,
            "total_rows": imported + len(errors)
        }
    
    @staticmethod
    def export_to_csv(employees: List[Employee]) -> str:
        """ייצוא עובדים ל-CSV"""
        output = StringIO()
        
        if not employees:
            return ""
        
        fieldnames = ['id', 'name', 'age', 'city', 'salary', 'department', 'hire_date', 'is_active']
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        
        writer.writeheader()
        
        for emp in employees:
            writer.writerow({
                'id': emp.id,
                'name': emp.name,
                'age': emp.age,
                'city': emp.city,
                'salary': emp.salary,
                'department': emp.department,
                'hire_date': emp.hire_date,
                'is_active': emp.is_active
            })
        
        return output.getvalue()
    
    @staticmethod
    def export_to_excel(employees: List[Employee]) -> bytes:
        """ייצוא עובדים ל-Excel"""
        data = []
        
        for emp in employees:
            data.append({
                'ID': emp.id,
                'שם': emp.name,
                'גיל': emp.age,
                'עיר': emp.city,
                'משכורת': emp.salary,
                'מחלקה': emp.department,
                'תאריך קבלה': emp.hire_date,
                'פעיל': 'כן' if emp.is_active else 'לא'
            })
        
        df = pd.DataFrame(data)
        
        # שמירה ל-BytesIO
        from io import BytesIO
        output = BytesIO()
        df.to_excel(output, index=False, engine='openpyxl')
        output.seek(0)
        
        return output.getvalue()
```

### 4.2: נתיבי CSV

צור קובץ `csv_routes.py`:

```python
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from fastapi.responses import StreamingResponse, Response
from sqlmodel import Session
from io import BytesIO, StringIO

from dependencies import get_session
from crud import EmployeeCRUD
from csv_operations import CSVOperations

router = APIRouter(
    prefix="/api/v1/csv",
    tags=["CSV Operations"]
)

@router.post("/import")
async def import_csv(
    file: UploadFile = File(...),
    session: Session = Depends(get_session)
):
    """
    ייבוא עובדים מקובץ CSV
    
    הקובץ צריך להכיל עמודות: name, age, city, salary, department (אופציונלי), hire_date (אופציונלי)
    """
    if not file.filename.endswith('.csv'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="הקובץ חייב להיות מסוג CSV"
        )
    
    content = await file.read()
    file_content = content.decode('utf-8')
    
    result = CSVOperations.import_from_csv(session, file_content)
    
    return {
        "message": f"ייבוא הסתיים: {result['imported']} עובדים יובאו",
        "details": result
    }

@router.get("/export")
def export_csv(
    city: str = None,
    department: str = None,
    session: Session = Depends(get_session)
):
    """ייצוא עובדים ל-CSV"""
    
    if city or department:
        employees = EmployeeCRUD.search(session, city=city, department=department)
    else:
        employees = EmployeeCRUD.get_all(session)
    
    csv_content = CSVOperations.export_to_csv(employees)
    
    return StreamingResponse(
        iter([csv_content]),
        media_type="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename=employees.csv"
        }
    )

@router.get("/export/excel")
def export_excel(
    city: str = None,
    department: str = None,
    session: Session = Depends(get_session)
):
    """ייצוא עובדים ל-Excel"""
    
    if city or department:
        employees = EmployeeCRUD.search(session, city=city, department=department)
    else:
        employees = EmployeeCRUD.get_all(session)
    
    excel_content = CSVOperations.export_to_excel(employees)
    
    return Response(
        content=excel_content,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": "attachment; filename=employees.xlsx"
        }
    )

@router.get("/template")
def download_template():
    """הורדת תבנית CSV"""
    template = "name,age,city,salary,department,hire_date\n"
    template += "John Doe,30,Tel Aviv,10000,IT,2024-01-15\n"
    template += "Jane Smith,25,Jerusalem,12000,Sales,2024-02-20\n"
    
    return StreamingResponse(
        iter([template]),
        media_type="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=employee_template.csv"
        }
    )
```

---

## חלק 5: פרויקט מלא - מערכת ניהול עובדים

### 5.1: מבנה הפרויקט

```
employee_api/
│
├── main.py                 # נקודת כניסה ראשית
├── database.py             # הגדרת מסד נתונים
├── models.py               # מודלים
├── crud.py                 # פעולות CRUD
├── routes.py               # נתיבי API עובדים
├── csv_routes.py           # נתיבי CSV
├── csv_operations.py       # פעולות CSV
├── dependencies.py         # Dependency Injection
├── config.py               # הגדרות
├── requirements.txt        # תלויות
└── README.md              # תיעוד
```

### 5.2: קובץ הגדרות

צור קובץ `config.py`:

```python
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    """הגדרות אפליקציה"""
    
    # מסד נתונים
    DATABASE_URL: str = "mysql+pymysql://root:your_password@localhost:3306/company_db"
    
    # API
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "Employee Management API"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "API מלא לניהול עובדים עם תמיכה ב-CSV"
    
    # CORS
    BACKEND_CORS_ORIGINS: list = ["http://localhost:3000", "http://localhost:8080"]
    
    # Pagination
    DEFAULT_PAGE_SIZE: int = 100
    MAX_PAGE_SIZE: int = 1000
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    """קבלת הגדרות (cached)"""
    return Settings()
```

### 5.3: Main - קובץ ראשי מלא

עדכן את `main.py`:

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from database import create_db_and_tables
from routes import router as employee_router
from csv_routes import router as csv_router
from config import get_settings

settings = get_settings()

# Lifespan - פעולות בהפעלה וסגירה
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🚀 מפעיל את האפליקציה...")
    create_db_and_tables()
    print("✓ מסד נתונים מוכן!")
    
    yield
    
    # Shutdown
    print("👋 סוגר את האפליקציה...")

# יצירת אפליקציה
app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.DESCRIPTION,
    version=settings.VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# רישום Routers
app.include_router(employee_router)
app.include_router(csv_router)

# נתיב בית
@app.get("/", tags=["Root"])
def read_root():
    """עמוד הבית"""
    return {
        "message": "ברוכים הבאים ל-Employee Management API!",
        "version": settings.VERSION,
        "docs": "/docs",
        "health": "/health"
    }

# Health Check
@app.get("/health", tags=["Health"])
def health_check():
    """בדיקת תקינות"""
    return {
        "status": "healthy",
        "version": settings.VERSION
    }

# הרצה ישירה
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
```

### 5.4: Requirements

צור קובץ `requirements.txt`:

```txt
fastapi==0.109.0
uvicorn[standard]==0.27.0
sqlmodel==0.0.14
pymysql==1.1.0
pandas==2.1.4
python-multipart==0.0.6
openpyxl==3.1.2
pydantic-settings==2.1.0
python-dotenv==1.0.0
```

התקנה:
```bash
pip install -r requirements.txt
```

### 5.5: קובץ .env

צור קובץ `.env`:

```env
DATABASE_URL=mysql+pymysql://root:your_password@localhost:3306/company_db
PROJECT_NAME="Employee Management API"
VERSION=1.0.0
```

---

## חלק 6: פריסה ובדיקות

### 6.1: הרצת האפליקציה

```bash
# הרצה רגילה
uvicorn main:app --reload

# הרצה עם host ו-port מותאמים
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# הרצה עם workers (production)
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 6.2: בדיקות עם curl

```bash
# בדיקת תקינות
curl http://localhost:8000/health

# יצירת עובד
curl -X POST "http://localhost:8000/api/v1/employees/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Alice",
    "age": 25,
    "city": "Tel Aviv",
    "salary": 10000,
    "department": "IT"
  }'

# קבלת כל העובדים
curl http://localhost:8000/api/v1/employees/

# קבלת עובד לפי ID
curl http://localhost:8000/api/v1/employees/1

# חיפוש עובדים
curl "http://localhost:8000/api/v1/employees/search/advanced?city=Tel%20Aviv&min_salary=9000"

# עדכון עובד
curl -X PUT "http://localhost:8000/api/v1/employees/1" \
  -H "Content-Type: application/json" \
  -d '{
    "salary": 11000
  }'

# מחיקת עובד
curl -X DELETE "http://localhost:8000/api/v1/employees/1"

# ייצוא CSV
curl "http://localhost:8000/api/v1/csv/export" -o employees.csv

# ייצוא Excel
curl "http://localhost:8000/api/v1/csv/export/excel" -o employees.xlsx
```

### 6.3: בדיקות עם Python

צור קובץ `test_api.py`:

```python
import requests

BASE_URL = "http://localhost:8000"

def test_create_employee():
    """בדיקת יצירת עובד"""
    url = f"{BASE_URL}/api/v1/employees/"
    data = {
        "name": "Test Employee",
        "age": 30,
        "city": "Tel Aviv",
        "salary": 10000,
        "department": "IT"
    }
    
    response = requests.post(url, json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    return response.json()["id"]

def test_get_employees():
    """בדיקת קבלת עובדים"""
    url = f"{BASE_URL}/api/v1/employees/"
    response = requests.get(url)
    
    print(f"Status: {response.status_code}")
    print(f"Total employees: {len(response.json())}")
    
    return response.json()

def test_search_employees():
    """בדיקת חיפוש"""
    url = f"{BASE_URL}/api/v1/employees/search/advanced"
    params = {
        "city": "Tel Aviv",
        "min_salary": 9000
    }
    
    response = requests.get(url, params=params)
    print(f"Status: {response.status_code}")
    print(f"Found: {len(response.json())} employees")

def test_update_employee(employee_id):
    """בדיקת עדכון"""
    url = f"{BASE_URL}/api/v1/employees/{employee_id}"
    data = {
        "salary": 12000
    }
    
    response = requests.put(url, json=data)
    print(f"Status: {response.status_code}")
    print(f"Updated: {response.json()}")

def test_delete_employee(employee_id):
    """בדיקת מחיקה"""
    url = f"{BASE_URL}/api/v1/employees/{employee_id}"
    response = requests.delete(url)
    
    print(f"Status: {response.status_code}")

if __name__ == "__main__":
    print("=== Testing API ===\n")
    
    # יצירה
    print("1. Creating employee...")
    emp_id = test_create_employee()
    print()
    
    # קריאה
    print("2. Getting all employees...")
    test_get_employees()
    print()
    
    # חיפוש
    print("3. Searching employees...")
    test_search_employees()
    print()
    
    # עדכון
    print("4. Updating employee...")
    test_update_employee(emp_id)
    print()
    
    # מחיקה
    print("5. Deleting employee...")
    test_delete_employee(emp_id)
    print()
    
    print("=== All tests completed! ===")
```

הרצה:
```bash
python test_api.py
```

### 6.4: Client פשוט ב-HTML/JavaScript

צור קובץ `client.html`:

```html
<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ניהול עובדים - Employee API</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: Arial, sans-serif;
            background: #f5f5f5;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        h1 {
            color: #333;
            margin-bottom: 30px;
            text-align: center;
        }
        
        .form-group {
            margin-bottom: 15px;
        }
        
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
            color: #555;
        }
        
        input, select {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 14px;
        }
        
        button {
            background: #007bff;
            color: white;
            padding: 12px 25px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            margin: 5px;
        }
        
        button:hover {
            background: #0056b3;
        }
        
        .btn-success {
            background: #28a745;
        }
        
        .btn-success:hover {
            background: #218838;
        }
        
        .btn-danger {
            background: #dc3545;
        }
        
        .btn-danger:hover {
            background: #c82333;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        
        th, td {
            padding: 12px;
            text-align: right;
            border-bottom: 1px solid #ddd;
        }
        
        th {
            background: #f8f9fa;
            font-weight: bold;
        }
        
        tr:hover {
            background: #f8f9fa;
        }
        
        .actions {
            display: flex;
            gap: 5px;
            justify-content: center;
        }
        
        .message {
            padding: 15px;
            margin: 15px 0;
            border-radius: 5px;
        }
        
        .message.success {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        
        .message.error {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🏢 ניהול עובדים - Employee Management</h1>
        
        <div id="message"></div>
        
        <!-- טופס הוספת עובד -->
        <div class="form-section">
            <h2>הוספת עובד חדש</h2>
            <form id="employeeForm">
                <div class="form-group">
                    <label>שם:</label>
                    <input type="text" id="name" required>
                </div>
                
                <div class="form-group">
                    <label>גיל:</label>
                    <input type="number" id="age" min="18" max="120" required>
                </div>
                
                <div class="form-group">
                    <label>עיר:</label>
                    <input type="text" id="city" required>
                </div>
                
                <div class="form-group">
                    <label>משכורת:</label>
                    <input type="number" id="salary" min="0" step="0.01" required>
                </div>
                
                <div class="form-group">
                    <label>מחלקה:</label>
                    <input type="text" id="department">
                </div>
                
                <button type="submit" class="btn-success">➕ הוסף עובד</button>
                <button type="button" onclick="loadEmployees()">🔄 רענן רשימה</button>
                <button type="button" onclick="exportCSV()" class="btn-success">📥 ייצוא CSV</button>
            </form>
        </div>
        
        <!-- טבלת עובדים -->
        <div class="table-section">
            <h2>רשימת עובדים</h2>
            <table id="employeesTable">
                <thead>
                    <tr>
                        <th>פעולות</th>
                        <th>מחלקה</th>
                        <th>משכורת</th>
                        <th>עיר</th>
                        <th>גיל</th>
                        <th>שם</th>
                        <th>ID</th>
                    </tr>
                </thead>
                <tbody id="employeesBody">
                    <!-- רשימת עובדים תוצג כאן -->
                </tbody>
            </table>
        </div>
    </div>
    
    <script>
        const API_URL = 'http://localhost:8000/api/v1';
        
        // הצגת הודעה
        function showMessage(text, type = 'success') {
            const messageDiv = document.getElementById('message');
            messageDiv.className = `message ${type}`;
            messageDiv.textContent = text;
            
            setTimeout(() => {
                messageDiv.className = '';
                messageDiv.textContent = '';
            }, 5000);
        }
        
        // טעינת עובדים
        async function loadEmployees() {
            try {
                const response = await fetch(`${API_URL}/employees/`);
                const employees = await response.json();
                
                const tbody = document.getElementById('employeesBody');
                tbody.innerHTML = '';
                
                employees.forEach(emp => {
                    const row = tbody.insertRow();
                    row.innerHTML = `
                        <td class="actions">
                            <button onclick="deleteEmployee(${emp.id})" class="btn-danger">🗑️</button>
                        </td>
                        <td>${emp.department || '-'}</td>
                        <td>₪${emp.salary.toLocaleString()}</td>
                        <td>${emp.city}</td>
                        <td>${emp.age}</td>
                        <td>${emp.name}</td>
                        <td>${emp.id}</td>
                    `;
                });
                
                showMessage(`נטענו ${employees.length} עובדים`, 'success');
            } catch (error) {
                showMessage('שגיאה בטעינת עובדים', 'error');
                console.error(error);
            }
        }
        
        // הוספת עובד
        document.getElementById('employeeForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const data = {
                name: document.getElementById('name').value,
                age: parseInt(document.getElementById('age').value),
                city: document.getElementById('city').value,
                salary: parseFloat(document.getElementById('salary').value),
                department: document.getElementById('department').value || null
            };
            
            try {
                const response = await fetch(`${API_URL}/employees/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(data)
                });
                
                if (response.ok) {
                    showMessage('עובד נוסף בהצלחה!', 'success');
                    document.getElementById('employeeForm').reset();
                    loadEmployees();
                } else {
                    showMessage('שגיאה בהוספת עובד', 'error');
                }
            } catch (error) {
                showMessage('שגיאה בהוספת עובד', 'error');
                console.error(error);
            }
        });
        
        // מחיקת עובד
        async function deleteEmployee(id) {
            if (!confirm('האם אתה בטוח שברצונך למחוק עובד זה?')) {
                return;
            }
            
            try {
                const response = await fetch(`${API_URL}/employees/${id}`, {
                    method: 'DELETE'
                });
                
                if (response.ok || response.status === 204) {
                    showMessage('עובד נמחק בהצלחה!', 'success');
                    loadEmployees();
                } else {
                    showMessage('שגיאה במחיקת עובד', 'error');
                }
            } catch (error) {
                showMessage('שגיאה במחיקת עובד', 'error');
                console.error(error);
            }
        }
        
        // ייצוא CSV
        function exportCSV() {
            window.location.href = `${API_URL}/csv/export`;
            showMessage('מוריד קובץ CSV...', 'success');
        }
        
        // טעינה ראשונית
        loadEmployees();
    </script>
</body>
</html>
```

פתח את הקובץ בדפדפן לאחר שה-API רץ.

---

## תרגילים מעשיים

### תרגיל 1: הוספת אימות (Authentication)

**משימה:** הוסף אימות פשוט עם API Key

```python
from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader

API_KEY = "my-secret-api-key"
api_key_header = APIKeyHeader(name="X-API-Key")

def get_api_key(api_key: str = Security(api_key_header)):
    """בדיקת API Key"""
    if api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="API Key לא תקין"
        )
    return api_key

# שימוש ב-route
@router.get("/employees/", dependencies=[Depends(get_api_key)])
def get_employees():
    # הקוד שלך
    pass
```

### תרגיל 2: הוספת לוג (Logging)

```python
import logging
from datetime import datetime

# הגדרת logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

@router.post("/employees/")
def create_employee(employee: EmployeeCreate, session: Session = Depends(get_session)):
    logger.info(f"Creating new employee: {employee.name}")
    
    try:
        result = EmployeeCRUD.create(session, employee)
        logger.info(f"Employee created successfully with ID: {result.id}")
        return result
    except Exception as e:
        logger.error(f"Error creating employee: {str(e)}")
        raise
```

### תרגיל 3: הוספת Cache

```python
from functools import lru_cache
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi_cache.decorator import cache

# אתחול cache
@app.on_event("startup")
async def startup():
    FastAPICache.init(InMemoryBackend())

# שימוש ב-cache
@router.get("/employees/")
@cache(expire=60)  # cache למשך 60 שניות
async def get_employees(session: Session = Depends(get_session)):
    return EmployeeCRUD.get_all(session)
```

---

## סיכום

במדריך זה למדת:

✅ **FastAPI:**
- בניית REST API מלא
- Routing, Request/Response Models
- Validation, Error Handling
- Documentation אוטומטי

✅ **SQLModel:**
- ORM מודרני עם Type Hints
- CRUD Operations
- Dependency Injection
- חיבור ל-MySQL

✅ **CSV:**
- ייבוא/ייצוא CSV
- העלאת קבצים
- ייצוא ל-Excel

✅ **פרויקט מלא:**
- ארכיטקטורה נכונה
- Separation of Concerns
- Configuration Management
- Error Handling

### צעדים הבאים

1. **למד על Authentication:** JWT, OAuth2
2. **הוסף Tests:** pytest, TestClient
3. **Deploy:** Docker, AWS, Heroku
4. **הוסף Frontend:** React, Vue
5. **למד Async:** SQLAlchemy 2.0 async

### משאבים נוספים

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Uvicorn Documentation](https://www.uvicorn.org/)

**בהצלחה בבניית ה-API שלך! 🚀**
