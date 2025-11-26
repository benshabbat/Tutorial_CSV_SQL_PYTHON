# מדריך מקיף: FastAPI עם קבצי CSV
## העלאה, ייצוא וניהול נתונים - שלב אחר שלב למתחילים

---

## תוכן עניינים
1. [הקדמה ומה נלמד](#הקדמה)
2. [הכנת הסביבה](#הכנת-הסביבה)
3. [פרויקט 1: העלאת קובץ CSV פשוט](#פרויקט-1-העלאת-קובץ-csv-פשוט)
4. [פרויקט 2: קריאה והצגת נתוני CSV](#פרויקט-2-קריאה-והצגת-נתוני-csv)
5. [פרויקט 3: ייצוא נתונים ל-CSV](#פרויקט-3-ייצוא-נתונים-ל-csv)
6. [פרויקט 4: CRUD מלא עם CSV](#פרויקט-4-crud-מלא-עם-csv)
7. [פרויקט 5: אימות נתונים עם Pydantic](#פרויקט-5-אימות-נתונים-עם-pydantic)
8. [פרויקט 6: מערכת ניהול משתמשים מלאה](#פרויקט-6-מערכת-ניהול-משתמשים-מלאה)
9. [טיפים ושגיאות נפוצות](#טיפים-ושגיאות-נפוצות)

---

## הקדמה

### מה נלמד במדריך?
- העלאת קבצי CSV לשרת FastAPI
- קריאה ועיבוד נתוני CSV
- ייצוא נתונים לקובץ CSV
- בניית API מלא עם פעולות CRUD
- אימות נתונים עם Pydantic
- ניהול קבצים ושגיאות

### למה FastAPI?
- מהיר ויעיל
- תיעוד אוטומטי (Swagger UI)
- קל ללמידה
- תמיכה מובנית ב-async

---

## הכנת הסביבה

### שלב 1: התקנת חבילות נדרשות

```bash
pip install fastapi uvicorn python-multipart pandas
```

**הסבר על כל חבילה:**
- `fastapi` - ה-framework לבניית ה-API
- `uvicorn` - שרת ASGI להרצת FastAPI
- `python-multipart` - נדרש להעלאת קבצים
- `pandas` - לעבודה עם CSV בצורה נוחה

### שלב 2: יצירת מבנה פרויקט

```
my_csv_api/
├── main.py              # הקובץ הראשי
├── uploads/             # תיקייה לקבצים שהועלו
└── data/                # תיקייה לקבצי CSV
```

צור את התיקיות:
```bash
mkdir uploads
mkdir data
```

---

## פרויקט 1: העלאת קובץ CSV פשוט

### מטרה: ללמוד להעלות קובץ CSV לשרת

**קובץ: `01_basic_upload.py`**

```python
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import os

app = FastAPI(title="CSV Upload - Basic")

# יצירת תיקיית uploads אם לא קיימת
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/")
def root():
    """נקודת קצה ראשית"""
    return {"message": "שלום! העלה קובץ CSV ב-/upload"}


@app.post("/upload")
async def upload_csv(file: UploadFile = File(...)):
    """
    העלאת קובץ CSV
    
    Parameters:
    - file: קובץ CSV להעלאה
    
    Returns:
    - מידע על הקובץ שהועלה
    """
    # בדיקה שהקובץ הוא CSV
    if not file.filename.endswith('.csv'):
        return JSONResponse(
            status_code=400,
            content={"error": "רק קבצי CSV מותרים"}
        )
    
    # שמירת הקובץ
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
    
    return {
        "message": "הקובץ הועלה בהצלחה!",
        "filename": file.filename,
        "size": len(content),
        "path": file_path
    }


# הרצה: uvicorn 01_basic_upload:app --reload
```

### איך להשתמש:

1. **הרץ את השרת:**
```bash
uvicorn 01_basic_upload:app --reload
```

2. **גש לתיעוד האינטראקטיבי:**
   - פתח דפדפן: `http://localhost:8000/docs`

3. **נסה להעלות קובץ:**
   - לחץ על `/upload`
   - לחץ "Try it out"
   - בחר קובץ CSV
   - לחץ "Execute"

### הסברים:

```python
@app.post("/upload")
async def upload_csv(file: UploadFile = File(...)):
```
- `@app.post` - מגדיר נקודת קצה ל-POST request
- `async` - פונקציה אסינכרונית (מהירה יותר)
- `UploadFile` - טיפוס מיוחד לקבצים
- `File(...)` - מסמן פרמטר חובה

```python
if not file.filename.endswith('.csv'):
```
- בדיקת תקינות - רק קבצי CSV

```python
content = await file.read()
```
- `await` - ממתין לקריאת הקובץ (async)

---

## פרויקט 2: קריאה והצגת נתוני CSV

### מטרה: לקרוא קובץ CSV ולהציג את התוכן

**קובץ: `02_read_csv.py`**

```python
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import pandas as pd
import os
from typing import List, Dict

app = FastAPI(title="CSV Reader")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.post("/upload-and-read")
async def upload_and_read_csv(file: UploadFile = File(...)):
    """
    העלאה וקריאת קובץ CSV
    
    מחזיר את כל השורות בקובץ
    """
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="רק קבצי CSV מותרים")
    
    # שמירת הקובץ
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    content = await file.read()
    
    with open(file_path, "wb") as f:
        f.write(content)
    
    try:
        # קריאת CSV עם pandas
        df = pd.read_csv(file_path)
        
        # המרה ל-JSON
        data = df.to_dict(orient='records')
        
        return {
            "message": "קובץ נקרא בהצלחה",
            "filename": file.filename,
            "rows": len(df),
            "columns": list(df.columns),
            "data": data
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"שגיאה בקריאת הקובץ: {str(e)}")


@app.get("/files")
def list_uploaded_files():
    """רשימת קבצים שהועלו"""
    files = os.listdir(UPLOAD_DIR)
    csv_files = [f for f in files if f.endswith('.csv')]
    
    return {
        "count": len(csv_files),
        "files": csv_files
    }


@app.get("/read/{filename}")
def read_csv_file(filename: str):
    """קריאת קובץ CSV קיים"""
    file_path = os.path.join(UPLOAD_DIR, filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="קובץ לא נמצא")
    
    try:
        df = pd.read_csv(file_path)
        
        return {
            "filename": filename,
            "rows": len(df),
            "columns": list(df.columns),
            "preview": df.head(10).to_dict(orient='records')  # 10 שורות ראשונות
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"שגיאה: {str(e)}")


# הרצה: uvicorn 02_read_csv:app --reload
```

### דוגמת שימוש:

**צור קובץ `students.csv` לבדיקה:**
```csv
id,name,age,grade
1,דני כהן,20,85
2,מיכל לוי,22,92
3,יוסי אברהם,21,78
```

**נסה את ה-API:**
1. העלה את הקובץ דרך `/upload-and-read`
2. קבל רשימת קבצים דרך `/files`
3. קרא קובץ ספציפי דרך `/read/students.csv`

### הסברים חשובים:

```python
df = pd.read_csv(file_path)
```
- `pandas` קורא את ה-CSV ל-DataFrame

```python
data = df.to_dict(orient='records')
```
- המרה ל-list של dictionaries
- כל שורה הופכת ל-dictionary

```python
df.head(10)
```
- מחזיר 10 שורות ראשונות (preview)

---

## פרויקט 3: ייצוא נתונים ל-CSV

### מטרה: ליצור ולייצא קובץ CSV מנתונים

**קובץ: `03_export_csv.py`**

```python
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List
import pandas as pd
import os
from datetime import datetime

app = FastAPI(title="CSV Exporter")

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)


# מודל נתונים
class Student(BaseModel):
    id: int
    name: str
    age: int
    grade: float


@app.post("/create-csv")
def create_csv_from_data(students: List[Student]):
    """
    יצירת קובץ CSV מנתונים
    
    Parameters:
    - students: רשימת סטודנטים
    
    Returns:
    - מידע על הקובץ שנוצר
    """
    if not students:
        raise HTTPException(status_code=400, detail="הרשימה ריקה")
    
    # המרה ל-DataFrame
    df = pd.DataFrame([student.dict() for student in students])
    
    # יצירת שם קובץ עם timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"students_{timestamp}.csv"
    filepath = os.path.join(DATA_DIR, filename)
    
    # שמירה ל-CSV
    df.to_csv(filepath, index=False, encoding='utf-8-sig')  # utf-8-sig לעברית
    
    return {
        "message": "קובץ נוצר בהצלחה",
        "filename": filename,
        "rows": len(df),
        "path": filepath
    }


@app.get("/download/{filename}")
def download_csv(filename: str):
    """
    הורדת קובץ CSV
    
    Parameters:
    - filename: שם הקובץ להורדה
    """
    filepath = os.path.join(DATA_DIR, filename)
    
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="קובץ לא נמצא")
    
    return FileResponse(
        path=filepath,
        filename=filename,
        media_type='text/csv'
    )


@app.get("/export-sample")
def export_sample_csv():
    """ייצוא נתוני דוגמה"""
    sample_data = [
        {"id": 1, "name": "אלון", "age": 20, "grade": 85.5},
        {"id": 2, "name": "רחל", "age": 22, "grade": 92.0},
        {"id": 3, "name": "דוד", "age": 21, "grade": 78.3}
    ]
    
    df = pd.DataFrame(sample_data)
    filename = "sample_students.csv"
    filepath = os.path.join(DATA_DIR, filename)
    
    df.to_csv(filepath, index=False, encoding='utf-8-sig')
    
    return {
        "message": "קובץ דוגמה נוצר",
        "download_url": f"/download/{filename}"
    }


@app.get("/list-exports")
def list_exported_files():
    """רשימת קבצים מיוצאים"""
    files = [f for f in os.listdir(DATA_DIR) if f.endswith('.csv')]
    
    file_info = []
    for f in files:
        filepath = os.path.join(DATA_DIR, f)
        size = os.path.getsize(filepath)
        file_info.append({
            "filename": f,
            "size_bytes": size,
            "download_url": f"/download/{f}"
        })
    
    return {
        "count": len(files),
        "files": file_info
    }


# הרצה: uvicorn 03_export_csv:app --reload
```

### דוגמת שימוש ב-curl או Python:

**Python client:**
```python
import requests

# יצירת CSV מנתונים
students = [
    {"id": 1, "name": "דני", "age": 20, "grade": 85.5},
    {"id": 2, "name": "מיכל", "age": 22, "grade": 92.0}
]

response = requests.post("http://localhost:8000/create-csv", json=students)
print(response.json())

# הורדת הקובץ
filename = response.json()["filename"]
download_response = requests.get(f"http://localhost:8000/download/{filename}")

with open(f"downloaded_{filename}", "wb") as f:
    f.write(download_response.content)
```

### הסברים:

```python
df.to_csv(filepath, index=False, encoding='utf-8-sig')
```
- `index=False` - ללא עמודת אינדקס
- `encoding='utf-8-sig'` - קידוד לעברית (Excel יכיר)

```python
return FileResponse(path=filepath, filename=filename, media_type='text/csv')
```
- `FileResponse` - מחזיר קובץ להורדה
- הדפדפן יתחיל הורדה אוטומטית

---

## פרויקט 4: CRUD מלא עם CSV

### מטרה: Create, Read, Update, Delete על קובץ CSV

**קובץ: `04_crud_csv.py`**

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import pandas as pd
import os

app = FastAPI(title="CSV CRUD Operations")

CSV_FILE = "data/students_db.csv"
os.makedirs("data", exist_ok=True)


class Student(BaseModel):
    id: int
    name: str
    age: int
    grade: float
    email: Optional[str] = None


def load_csv():
    """טעינת CSV לדף נתונים"""
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE)
    else:
        # יצירת DataFrame ריק אם הקובץ לא קיים
        return pd.DataFrame(columns=['id', 'name', 'age', 'grade', 'email'])


def save_csv(df: pd.DataFrame):
    """שמירת DataFrame ל-CSV"""
    df.to_csv(CSV_FILE, index=False, encoding='utf-8-sig')


# ========== CREATE ==========

@app.post("/students", response_model=Student)
def create_student(student: Student):
    """
    יצירת סטודנט חדש
    
    מוסיף סטודנט ל-CSV
    """
    df = load_csv()
    
    # בדיקה אם ID כבר קיים
    if student.id in df['id'].values:
        raise HTTPException(status_code=400, detail=f"סטודנט עם ID {student.id} כבר קיים")
    
    # הוספת שורה חדשה
    new_row = pd.DataFrame([student.dict()])
    df = pd.concat([df, new_row], ignore_index=True)
    
    save_csv(df)
    
    return student


@app.post("/students/bulk")
def create_students_bulk(students: List[Student]):
    """הוספת מספר סטודנטים בבת אחת"""
    df = load_csv()
    
    for student in students:
        if student.id in df['id'].values:
            raise HTTPException(
                status_code=400,
                detail=f"סטודנט עם ID {student.id} כבר קיים"
            )
    
    new_rows = pd.DataFrame([s.dict() for s in students])
    df = pd.concat([df, new_rows], ignore_index=True)
    
    save_csv(df)
    
    return {
        "message": f"{len(students)} סטודנטים נוספו",
        "count": len(students)
    }


# ========== READ ==========

@app.get("/students")
def get_all_students():
    """קבלת כל הסטודנטים"""
    df = load_csv()
    
    if df.empty:
        return {"students": [], "count": 0}
    
    return {
        "students": df.to_dict(orient='records'),
        "count": len(df)
    }


@app.get("/students/{student_id}")
def get_student(student_id: int):
    """קבלת סטודנט לפי ID"""
    df = load_csv()
    
    student = df[df['id'] == student_id]
    
    if student.empty:
        raise HTTPException(status_code=404, detail="סטודנט לא נמצא")
    
    return student.to_dict(orient='records')[0]


@app.get("/students/search/by-name")
def search_students_by_name(name: str):
    """חיפוש סטודנטים לפי שם"""
    df = load_csv()
    
    # חיפוש חלקי (contains)
    results = df[df['name'].str.contains(name, case=False, na=False)]
    
    return {
        "query": name,
        "results": results.to_dict(orient='records'),
        "count": len(results)
    }


# ========== UPDATE ==========

@app.put("/students/{student_id}")
def update_student(student_id: int, student: Student):
    """עדכון סטודנט"""
    df = load_csv()
    
    if student_id not in df['id'].values:
        raise HTTPException(status_code=404, detail="סטודנט לא נמצא")
    
    # עדכון השורה
    df.loc[df['id'] == student_id, ['name', 'age', 'grade', 'email']] = [
        student.name,
        student.age,
        student.grade,
        student.email
    ]
    
    save_csv(df)
    
    return {"message": "סטודנט עודכן", "student": student}


@app.patch("/students/{student_id}/grade")
def update_student_grade(student_id: int, grade: float):
    """עדכון ציון בלבד"""
    df = load_csv()
    
    if student_id not in df['id'].values:
        raise HTTPException(status_code=404, detail="סטודנט לא נמצא")
    
    df.loc[df['id'] == student_id, 'grade'] = grade
    
    save_csv(df)
    
    return {"message": f"ציון עודכן ל-{grade}"}


# ========== DELETE ==========

@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    """מחיקת סטודנט"""
    df = load_csv()
    
    if student_id not in df['id'].values:
        raise HTTPException(status_code=404, detail="סטודנט לא נמצא")
    
    # מחיקת השורה
    df = df[df['id'] != student_id]
    
    save_csv(df)
    
    return {"message": f"סטודנט {student_id} נמחק"}


@app.delete("/students")
def delete_all_students():
    """מחיקת כל הסטודנטים"""
    df = pd.DataFrame(columns=['id', 'name', 'age', 'grade', 'email'])
    save_csv(df)
    
    return {"message": "כל הסטודנטים נמחקו"}


# ========== STATISTICS ==========

@app.get("/statistics")
def get_statistics():
    """סטטיסטיקות"""
    df = load_csv()
    
    if df.empty:
        return {"message": "אין נתונים"}
    
    return {
        "total_students": len(df),
        "average_grade": float(df['grade'].mean()),
        "highest_grade": float(df['grade'].max()),
        "lowest_grade": float(df['grade'].min()),
        "average_age": float(df['age'].mean())
    }


# הרצה: uvicorn 04_crud_csv:app --reload
```

### תרחישי שימוש:

**1. יצירת סטודנט:**
```json
POST /students
{
  "id": 1,
  "name": "דני כהן",
  "age": 20,
  "grade": 85.5,
  "email": "danny@example.com"
}
```

**2. קבלת כל הסטודנטים:**
```
GET /students
```

**3. חיפוש:**
```
GET /students/search/by-name?name=דני
```

**4. עדכון:**
```json
PUT /students/1
{
  "id": 1,
  "name": "דני כהן",
  "age": 21,
  "grade": 90.0,
  "email": "danny.new@example.com"
}
```

**5. מחיקה:**
```
DELETE /students/1
```

---

## פרויקט 5: אימות נתונים עם Pydantic

### מטרה: אימות מתקדם של נתונים

**קובץ: `05_validation.py`**

```python
from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel, Field, validator, EmailStr
from typing import List, Optional
from enum import Enum
import pandas as pd
import os

app = FastAPI(title="CSV with Validation")

CSV_FILE = "data/validated_students.csv"
os.makedirs("data", exist_ok=True)


# Enum למגדר
class Gender(str, Enum):
    male = "male"
    female = "female"
    other = "other"


# מודל עם אימותים
class Student(BaseModel):
    id: int = Field(..., gt=0, description="ID חיובי")
    name: str = Field(..., min_length=2, max_length=50, description="שם בין 2-50 תווים")
    age: int = Field(..., ge=18, le=120, description="גיל בין 18-120")
    grade: float = Field(..., ge=0, le=100, description="ציון בין 0-100")
    email: EmailStr = Field(..., description="כתובת אימייל תקינה")
    gender: Optional[Gender] = None
    phone: Optional[str] = Field(None, regex=r'^05\d-?\d{7}$', description="מספר טלפון ישראלי")
    
    @validator('name')
    def name_must_contain_letters(cls, v):
        """בדיקה שהשם מכיל אותיות"""
        if not any(c.isalpha() for c in v):
            raise ValueError('השם חייב להכיל אותיות')
        return v.strip()
    
    @validator('grade')
    def round_grade(cls, v):
        """עיגול ציון לספרה אחת אחרי הנקודה"""
        return round(v, 1)
    
    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "name": "דני כהן",
                "age": 20,
                "grade": 85.5,
                "email": "danny@example.com",
                "gender": "male",
                "phone": "050-1234567"
            }
        }


def load_csv():
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE)
    return pd.DataFrame(columns=['id', 'name', 'age', 'grade', 'email', 'gender', 'phone'])


def save_csv(df: pd.DataFrame):
    df.to_csv(CSV_FILE, index=False, encoding='utf-8-sig')


@app.post("/students", response_model=Student)
def create_student(student: Student):
    """
    יצירת סטודנט עם אימות מלא
    
    הנתונים עוברים אימות אוטומטי לפי הכללים במודל
    """
    df = load_csv()
    
    if student.id in df['id'].values:
        raise HTTPException(status_code=400, detail=f"ID {student.id} כבר קיים")
    
    # אימות נוסף - בדיקת אימייל ייחודי
    if student.email in df['email'].values:
        raise HTTPException(status_code=400, detail="האימייל כבר קיים במערכת")
    
    new_row = pd.DataFrame([student.dict()])
    df = pd.concat([df, new_row], ignore_index=True)
    save_csv(df)
    
    return student


@app.post("/upload-csv-validated")
async def upload_csv_with_validation(file: UploadFile = File(...)):
    """
    העלאת CSV עם אימות כל שורה
    
    בודק שכל שורה עומדת בדרישות
    """
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="רק CSV")
    
    # קריאת הקובץ
    content = await file.read()
    temp_file = "temp_upload.csv"
    
    with open(temp_file, "wb") as f:
        f.write(content)
    
    try:
        df = pd.read_csv(temp_file)
        
        # אימות כל שורה
        errors = []
        valid_students = []
        
        for idx, row in df.iterrows():
            try:
                # ניסוח ל-Student model (יבצע אימות)
                student = Student(**row.to_dict())
                valid_students.append(student)
            except Exception as e:
                errors.append({
                    "row": idx + 1,
                    "error": str(e),
                    "data": row.to_dict()
                })
        
        # שמירת שורות תקינות בלבד
        if valid_students:
            existing_df = load_csv()
            new_df = pd.DataFrame([s.dict() for s in valid_students])
            combined_df = pd.concat([existing_df, new_df], ignore_index=True)
            
            # הסרת כפילויות לפי ID
            combined_df = combined_df.drop_duplicates(subset=['id'], keep='last')
            
            save_csv(combined_df)
        
        return {
            "message": "העלאה הושלמה",
            "valid_rows": len(valid_students),
            "invalid_rows": len(errors),
            "errors": errors[:10]  # עד 10 שגיאות ראשונות
        }
    
    finally:
        # מחיקת קובץ זמני
        if os.path.exists(temp_file):
            os.remove(temp_file)


@app.get("/students")
def get_all_students():
    """קבלת כל הסטודנטים"""
    df = load_csv()
    return {
        "students": df.to_dict(orient='records'),
        "count": len(df)
    }


# הרצה: uvicorn 05_validation:app --reload
```

### דוגמאות לאימות:

**תקין ✓**
```json
{
  "id": 1,
  "name": "דני כהן",
  "age": 20,
  "grade": 85.5,
  "email": "danny@example.com",
  "phone": "050-1234567"
}
```

**שגיאות שיתפסו:**

```json
{
  "id": -5,  // ❌ חייב להיות חיובי
  "name": "א",  // ❌ קצר מדי
  "age": 15,  // ❌ צעיר מדי
  "grade": 150,  // ❌ מעל 100
  "email": "not-email",  // ❌ לא כתובת אימייל
  "phone": "123"  // ❌ לא מספר ישראלי תקין
}
```

### הסברים על Pydantic:

```python
Field(..., gt=0, description="ID חיובי")
```
- `...` = שדה חובה
- `gt=0` = גדול מ-0 (greater than)
- `ge=18` = גדול או שווה ל-18
- `le=100` = קטן או שווה ל-100

```python
@validator('name')
def name_must_contain_letters(cls, v):
```
- Validator מותאם אישית
- רץ אוטומטית בזמן יצירת אובייקט

---

## פרויקט 6: מערכת ניהול משתמשים מלאה

### מטרה: פרויקט מלא עם כל מה שלמדנו

**קובץ: `06_complete_system.py`**

```python
from fastapi import FastAPI, HTTPException, UploadFile, File, Query
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel, Field, EmailStr, validator
from typing import List, Optional
from datetime import datetime
import pandas as pd
import os
import io

app = FastAPI(
    title="מערכת ניהול סטודנטים מלאה",
    description="API מלא לניהול סטודנטים עם CSV",
    version="1.0.0"
)

# קבועים
DATA_DIR = "data"
UPLOAD_DIR = "uploads"
CSV_FILE = os.path.join(DATA_DIR, "students_complete.csv")

# יצירת תיקיות
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(UPLOAD_DIR, exist_ok=True)


# ========== מודלים ==========

class StudentBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    age: int = Field(..., ge=16, le=120)
    grade: float = Field(..., ge=0, le=100)
    email: EmailStr
    
    @validator('grade')
    def round_grade(cls, v):
        return round(v, 1)


class StudentCreate(StudentBase):
    """מודל ליצירת סטודנט - ללא ID"""
    pass


class Student(StudentBase):
    """מודל סטודנט מלא - עם ID"""
    id: int
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())
    
    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "name": "שרה לוי",
                "age": 20,
                "grade": 88.5,
                "email": "sara@example.com",
                "created_at": "2025-11-26T10:00:00"
            }
        }


class StudentUpdate(BaseModel):
    """מודל לעדכון - כל השדות אופציונליים"""
    name: Optional[str] = Field(None, min_length=2)
    age: Optional[int] = Field(None, ge=16, le=120)
    grade: Optional[float] = Field(None, ge=0, le=100)
    email: Optional[EmailStr] = None


# ========== פונקציות עזר ==========

def load_csv() -> pd.DataFrame:
    """טעינת CSV"""
    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE)
        # ודא שיש עמודת created_at
        if 'created_at' not in df.columns:
            df['created_at'] = datetime.now().isoformat()
        return df
    return pd.DataFrame(columns=['id', 'name', 'age', 'grade', 'email', 'created_at'])


def save_csv(df: pd.DataFrame):
    """שמירת CSV"""
    df.to_csv(CSV_FILE, index=False, encoding='utf-8-sig')


def get_next_id() -> int:
    """קבלת ID הבא"""
    df = load_csv()
    if df.empty:
        return 1
    return int(df['id'].max()) + 1


# ========== נקודות קצה - CREATE ==========

@app.post("/api/students", response_model=Student, status_code=201)
def create_student(student: StudentCreate):
    """
    יצירת סטודנט חדש
    
    - **name**: שם מלא (2-100 תווים)
    - **age**: גיל (16-120)
    - **grade**: ציון (0-100)
    - **email**: כתובת אימייל תקינה
    """
    df = load_csv()
    
    # בדיקת אימייל ייחודי
    if not df.empty and student.email in df['email'].values:
        raise HTTPException(status_code=400, detail="אימייל כבר קיים")
    
    # יצירת סטודנט עם ID
    new_id = get_next_id()
    new_student = Student(
        id=new_id,
        **student.dict()
    )
    
    # הוספה ל-DataFrame
    new_row = pd.DataFrame([new_student.dict()])
    df = pd.concat([df, new_row], ignore_index=True)
    save_csv(df)
    
    return new_student


@app.post("/api/students/bulk", status_code=201)
def create_students_bulk(students: List[StudentCreate]):
    """יצירת מספר סטודנטים בבת אחת"""
    df = load_csv()
    created_students = []
    
    for student in students:
        # בדיקת ייחודיות אימייל
        if student.email in df['email'].values:
            continue  # דלג על כפילויות
        
        new_id = get_next_id() if df.empty else int(df['id'].max()) + 1
        new_student = Student(id=new_id, **student.dict())
        
        new_row = pd.DataFrame([new_student.dict()])
        df = pd.concat([df, new_row], ignore_index=True)
        created_students.append(new_student)
    
    save_csv(df)
    
    return {
        "message": f"{len(created_students)} סטודנטים נוצרו",
        "students": created_students
    }


# ========== נקודות קצה - READ ==========

@app.get("/api/students", response_model=List[Student])
def get_students(
    skip: int = Query(0, ge=0, description="דלג על X רשומות"),
    limit: int = Query(100, ge=1, le=1000, description="מקסימום רשומות"),
    sort_by: Optional[str] = Query(None, description="מיון לפי שדה"),
    min_grade: Optional[float] = Query(None, ge=0, le=100),
    max_grade: Optional[float] = Query(None, ge=0, le=100)
):
    """
    קבלת רשימת סטודנטים עם סינון ומיון
    
    - **skip**: pagination - דלג על רשומות
    - **limit**: מקסימום רשומות להחזיר
    - **sort_by**: שדה למיון (id, name, grade, age)
    - **min_grade/max_grade**: סינון לפי טווח ציונים
    """
    df = load_csv()
    
    if df.empty:
        return []
    
    # סינון לפי ציונים
    if min_grade is not None:
        df = df[df['grade'] >= min_grade]
    if max_grade is not None:
        df = df[df['grade'] <= max_grade]
    
    # מיון
    if sort_by and sort_by in df.columns:
        df = df.sort_values(by=sort_by)
    
    # Pagination
    df = df[skip:skip+limit]
    
    return df.to_dict(orient='records')


@app.get("/api/students/{student_id}", response_model=Student)
def get_student(student_id: int):
    """קבלת סטודנט לפי ID"""
    df = load_csv()
    student = df[df['id'] == student_id]
    
    if student.empty:
        raise HTTPException(status_code=404, detail="סטודנט לא נמצא")
    
    return student.to_dict(orient='records')[0]


@app.get("/api/students/search/")
def search_students(
    q: str = Query(..., min_length=1, description="טקסט לחיפוש"),
    field: str = Query("name", description="שדה לחיפוש (name/email)")
):
    """חיפוש סטודנטים"""
    df = load_csv()
    
    if field not in ['name', 'email']:
        raise HTTPException(status_code=400, detail="שדה לא חוקי")
    
    results = df[df[field].str.contains(q, case=False, na=False)]
    
    return {
        "query": q,
        "field": field,
        "count": len(results),
        "results": results.to_dict(orient='records')
    }


# ========== נקודות קצה - UPDATE ==========

@app.put("/api/students/{student_id}", response_model=Student)
def update_student(student_id: int, student_update: StudentUpdate):
    """עדכון מלא של סטודנט"""
    df = load_csv()
    
    if student_id not in df['id'].values:
        raise HTTPException(status_code=404, detail="סטודנט לא נמצא")
    
    # עדכון רק שדות שסופקו
    update_dict = student_update.dict(exclude_unset=True)
    
    for key, value in update_dict.items():
        df.loc[df['id'] == student_id, key] = value
    
    save_csv(df)
    
    # החזרת הסטודנט המעודכן
    updated = df[df['id'] == student_id].to_dict(orient='records')[0]
    return updated


@app.patch("/api/students/{student_id}/grade")
def update_grade(student_id: int, grade: float = Query(..., ge=0, le=100)):
    """עדכון ציון בלבד"""
    df = load_csv()
    
    if student_id not in df['id'].values:
        raise HTTPException(status_code=404, detail="סטודנט לא נמצא")
    
    df.loc[df['id'] == student_id, 'grade'] = round(grade, 1)
    save_csv(df)
    
    return {"message": "ציון עודכן", "new_grade": round(grade, 1)}


# ========== נקודות קצה - DELETE ==========

@app.delete("/api/students/{student_id}")
def delete_student(student_id: int):
    """מחיקת סטודנט"""
    df = load_csv()
    
    if student_id not in df['id'].values:
        raise HTTPException(status_code=404, detail="סטודנט לא נמצא")
    
    df = df[df['id'] != student_id]
    save_csv(df)
    
    return {"message": f"סטודנט {student_id} נמחק"}


# ========== העלאה וייצוא ==========

@app.post("/api/upload")
async def upload_csv(file: UploadFile = File(...)):
    """
    העלאת קובץ CSV
    
    הקובץ חייב להכיל: name, age, grade, email
    """
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="רק קבצי CSV")
    
    content = await file.read()
    temp_file = os.path.join(UPLOAD_DIR, f"temp_{file.filename}")
    
    with open(temp_file, "wb") as f:
        f.write(content)
    
    try:
        uploaded_df = pd.read_csv(temp_file)
        
        # בדיקת עמודות נדרשות
        required = ['name', 'age', 'grade', 'email']
        if not all(col in uploaded_df.columns for col in required):
            raise HTTPException(
                status_code=400,
                detail=f"חסרות עמודות: {required}"
            )
        
        # אימות וטעינה
        df = load_csv()
        valid_count = 0
        errors = []
        
        for idx, row in uploaded_df.iterrows():
            try:
                student = StudentCreate(**row[required].to_dict())
                
                # בדיקת ייחודיות אימייל
                if student.email not in df['email'].values:
                    new_id = get_next_id() if df.empty else int(df['id'].max()) + 1
                    new_student = Student(id=new_id, **student.dict())
                    new_row = pd.DataFrame([new_student.dict()])
                    df = pd.concat([df, new_row], ignore_index=True)
                    valid_count += 1
            except Exception as e:
                errors.append({"row": idx + 1, "error": str(e)})
        
        save_csv(df)
        
        return {
            "message": "העלאה הושלמה",
            "uploaded": valid_count,
            "errors": len(errors),
            "error_details": errors[:5]
        }
    
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)


@app.get("/api/export/csv")
def export_csv():
    """ייצוא כל הנתונים ל-CSV"""
    df = load_csv()
    
    if df.empty:
        raise HTTPException(status_code=404, detail="אין נתונים לייצא")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"students_export_{timestamp}.csv"
    filepath = os.path.join(DATA_DIR, filename)
    
    df.to_csv(filepath, index=False, encoding='utf-8-sig')
    
    return FileResponse(
        path=filepath,
        filename=filename,
        media_type='text/csv'
    )


@app.get("/api/export/excel")
def export_excel():
    """ייצוא ל-Excel"""
    df = load_csv()
    
    if df.empty:
        raise HTTPException(status_code=404, detail="אין נתונים")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"students_export_{timestamp}.xlsx"
    filepath = os.path.join(DATA_DIR, filename)
    
    df.to_excel(filepath, index=False, engine='openpyxl')
    
    return FileResponse(
        path=filepath,
        filename=filename,
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )


# ========== סטטיסטיקות ==========

@app.get("/api/statistics")
def get_statistics():
    """סטטיסטיקות כלליות"""
    df = load_csv()
    
    if df.empty:
        return {"message": "אין נתונים"}
    
    return {
        "total_students": len(df),
        "average_grade": round(float(df['grade'].mean()), 2),
        "highest_grade": float(df['grade'].max()),
        "lowest_grade": float(df['grade'].min()),
        "average_age": round(float(df['age'].mean()), 2),
        "grade_distribution": {
            "excellent (90-100)": len(df[df['grade'] >= 90]),
            "good (80-89)": len(df[(df['grade'] >= 80) & (df['grade'] < 90)]),
            "average (70-79)": len(df[(df['grade'] >= 70) & (df['grade'] < 80)]),
            "below_average (<70)": len(df[df['grade'] < 70])
        }
    }


@app.get("/api/statistics/top-students")
def get_top_students(limit: int = Query(10, ge=1, le=100)):
    """הסטודנטים עם הציונים הגבוהים ביותר"""
    df = load_csv()
    
    if df.empty:
        return []
    
    top = df.nlargest(limit, 'grade')
    return top.to_dict(orient='records')


# ========== בריאות המערכת ==========

@app.get("/")
def root():
    """נקודת כניסה"""
    return {
        "message": "ברוכים הבאים למערכת ניהול הסטודנטים",
        "version": "1.0.0",
        "docs": "/docs",
        "total_students": len(load_csv())
    }


@app.get("/health")
def health_check():
    """בדיקת בריאות"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "database": "connected" if os.path.exists(CSV_FILE) else "not_found"
    }


# הרצה: uvicorn 06_complete_system:app --reload
```

### איך להשתמש במערכת המלאה:

**1. הרץ את השרת:**
```bash
uvicorn 06_complete_system:app --reload
```

**2. גש לתיעוד:**
```
http://localhost:8000/docs
```

**3. תרחישי שימוש מלאים:**

```python
import requests

BASE_URL = "http://localhost:8000/api"

# יצירת סטודנט
student_data = {
    "name": "מיכל כהן",
    "age": 22,
    "grade": 95.5,
    "email": "michal@example.com"
}
response = requests.post(f"{BASE_URL}/students", json=student_data)
print(response.json())

# קבלת כל הסטודנטים
response = requests.get(f"{BASE_URL}/students")
students = response.json()
print(f"סה״כ: {len(students)}")

# חיפוש
response = requests.get(f"{BASE_URL}/students/search/?q=מיכל&field=name")
print(response.json())

# עדכון ציון
student_id = 1
response = requests.patch(f"{BASE_URL}/students/{student_id}/grade?grade=98.5")
print(response.json())

# סטטיסטיקות
response = requests.get(f"{BASE_URL}/statistics")
print(response.json())

# ייצוא
response = requests.get(f"{BASE_URL}/export/csv")
with open("export.csv", "wb") as f:
    f.write(response.content)
```

---

## טיפים ושגיאות נפוצות

### 1. בעיות קידוד עברית

**בעיה:** תווים מקולקלים בעברית

**פתרון:**
```python
# בזמן שמירה
df.to_csv(filepath, index=False, encoding='utf-8-sig')

# בזמן קריאה
df = pd.read_csv(filepath, encoding='utf-8-sig')
```

### 2. העלאת קבצים גדולים

**בעיה:** קובץ גדול מדי

**פתרון:**
```python
from fastapi import FastAPI
app = FastAPI()

# הגדלת גודל מקסימלי
app.add_middleware(
    MaxSizeMiddleware,
    max_size=50_000_000  # 50MB
)
```

### 3. טיפול בשגיאות נכון

```python
from fastapi import HTTPException

try:
    df = pd.read_csv(file)
except pd.errors.EmptyDataError:
    raise HTTPException(status_code=400, detail="קובץ ריק")
except pd.errors.ParserError:
    raise HTTPException(status_code=400, detail="פורמט CSV לא תקין")
except Exception as e:
    raise HTTPException(status_code=500, detail=f"שגיאה: {str(e)}")
```

### 4. ביצועים טובים יותר

```python
# במקום לטעון כל פעם
df = pd.read_csv(file)

# השתמש ב-chunks לקבצים גדולים
for chunk in pd.read_csv(file, chunksize=1000):
    process(chunk)
```

### 5. אבטחה

```python
import os

# בדוק סוג קובץ
ALLOWED_EXTENSIONS = {'.csv', '.xlsx'}

def validate_file(filename: str):
    ext = os.path.splitext(filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="סוג קובץ לא מורשה")

# הגבל גודל
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

async def check_file_size(file: UploadFile):
    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="קובץ גדול מדי")
    return content
```

### 6. שגיאות נפוצות ופתרונות

| שגיאה | סיבה | פתרון |
|-------|------|-------|
| `ModuleNotFoundError: No module named 'multipart'` | חסרה חבילה | `pip install python-multipart` |
| `UnicodeDecodeError` | בעיית קידוד | `encoding='utf-8-sig'` |
| `FileNotFoundError` | תיקייה לא קיימת | `os.makedirs(dir, exist_ok=True)` |
| `422 Unprocessable Entity` | נתונים לא תקינים | בדוק את המודל Pydantic |

---

## סיכום וצעדים הבאים

### מה למדנו:
✅ העלאת קבצי CSV  
✅ קריאה ועיבוד נתונים  
✅ ייצוא ל-CSV/Excel  
✅ פעולות CRUD מלאות  
✅ אימות נתונים עם Pydantic  
✅ סטטיסטיקות ודוחות  
✅ טיפול בשגיאות  

### תרגילים מומלצים:

1. **תרגיל 1:** הוסף אפשרות למחיקת מספר סטודנטים בבת אחת
2. **תרגיל 2:** צור endpoint לעדכון ציונים מקובץ CSV
3. **תרגיל 3:** הוסף filtering מתקדם (לפי טווח גילאים, מספר רשומות וכו')
4. **תרגיל 4:** צור מערכת גיבוי אוטומטית לקבצים
5. **תרגיל 5:** הוסף authentication (הרשאות משתמשים)

### משאבים נוספים:
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Pydantic Documentation](https://docs.pydantic.dev/)

---

**בהצלחה! 🚀**

נוצר ב-2025 | מדריך למתחילים בעברית
