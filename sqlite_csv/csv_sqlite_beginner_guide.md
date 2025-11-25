# מדריך מקיף: CSV עם SQLite לרמת מתחילים

## תוכן עניינים
1. [מבוא](#מבוא)
2. [התקנה והכנה](#התקנה-והכנה)
3. [עבודה מתקדמת עם קבצי CSV](#עבודה-מתקדמת-עם-קבצי-csv)
   - 3.1 [יצירת קובץ CSV](#יצירת-קובץ-csv)
   - 3.2 [קריאת CSV - שיטות שונות](#קריאת-csv---שיטות-שונות)
   - 3.3 [כתיבה ועדכון CSV](#כתיבה-ועדכון-csv)
   - 3.4 [פעולות מתקדמות על CSV](#פעולות-מתקדמות-על-csv)
   - 3.5 [סינון וחיפוש בקבצי CSV](#סינון-וחיפוש-בקבצי-csv)
   - 3.6 [עבודה עם מספר קבצי CSV](#עבודה-עם-מספר-קבצי-csv)
4. [אינטגרציה עם SQLite](#אינטגרציה-עם-sqlite)
5. [תרגילים מעשיים](#תרגילים-מעשיים)

---

## מבוא

### מה זה CSV?
CSV (Comma-Separated Values) הוא פורמט קובץ פשוט לאחסון נתונים בטבלה. כל שורה מייצגת רשומה, והערכים מופרדים בפסיקים.

**דוגמה לקובץ CSV:**
```csv
name,age,city
Alice,25,Tel Aviv
Bob,30,Jerusalem
Charlie,35,Haifa
```

### מה זה SQLite?
SQLite הוא מסד נתונים רלציוני קל משקל שלא דורש שרת נפרד. הוא מושלם למתחילים ולפרויקטים קטנים-בינוניים.

### למה לשלב בין CSV ל-SQLite?
- **CSV**: קל לעריכה, קריא לבני אדם, תואם לאקסל
- **SQLite**: מאפשר שאילתות מורכבות, קשרים בין טבלאות, ביצועים טובים

---

## התקנה והכנה

### דרישות מקדימות
Python כבר מותקן במחשב שלך (גרסה 3.6 ומעלה).

### בדיקת גרסת Python
```bash
python --version
```

### ספריות נדרשות
Python מגיע עם הספריות הבאות מובנות:
- `csv` - לעבודה עם קבצי CSV
- `sqlite3` - לעבודה עם מסדי נתונים SQLite

**אין צורך בהתקנה נוספת!**

---

## עבודה מתקדמת עם קבצי CSV

### 3.1 יצירת קובץ CSV

#### שיטה 1: יצירה ידנית (טקסט רגיל)

צור קובץ בשם `students.csv` עם עורך טקסט:

```csv
id,name,age,grade,city
1,דני,20,85,תל אביב
2,שרה,22,92,ירושלים
3,יוסי,21,78,חיפה
4,רחל,23,88,באר שבע
5,משה,20,95,נתניה
```

#### שיטה 2: יצירה עם csv.writer

```python
import csv

# נתונים כרשימה של רשימות
students_data = [
    ['id', 'name', 'age', 'grade', 'city'],
    [1, 'דני', 20, 85, 'תל אביב'],
    [2, 'שרה', 22, 92, 'ירושלים'],
    [3, 'יוסי', 21, 78, 'חיפה'],
    [4, 'רחל', 23, 88, 'באר שבע'],
    [5, 'משה', 20, 95, 'נתניה']
]

# כתיבה לקובץ CSV
with open('students.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerows(students_data)

print("✓ קובץ CSV נוצר בהצלחה!")
```

**הסבר פרמטרים חשובים:**
- `'w'` - מצב כתיבה (יוצר קובץ חדש או מחליף קיים)
- `newline=''` - **חובה!** מונע שורות ריקות נוספות
- `encoding='utf-8'` - **חובה לעברית!** תמיכה בתווים מיוחדים
- `csv.writer()` - יוצר אובייקט לכתיבת CSV
- `writerows()` - כותב מספר שורות בבת אחת

#### שיטה 3: יצירה עם DictWriter (מומלץ!)

```python
import csv

# נתונים כרשימה של מילונים
students = [
    {'id': 1, 'name': 'דני', 'age': 20, 'grade': 85, 'city': 'תל אביב'},
    {'id': 2, 'name': 'שרה', 'age': 22, 'grade': 92, 'city': 'ירושלים'},
    {'id': 3, 'name': 'יוסי', 'age': 21, 'grade': 78, 'city': 'חיפה'}
]

# הגדרת שמות העמודות
fieldnames = ['id', 'name', 'age', 'grade', 'city']

# כתיבה עם DictWriter
with open('students_dict.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    
    # כתיבת כותרות
    writer.writeheader()
    
    # כתיבת הנתונים
    writer.writerows(students)

print("✓ קובץ נוצר עם DictWriter")
```

**יתרונות DictWriter:**
- קוד יותר קריא ומובן
- פחות סיכוי לטעויות בסדר העמודות
- קל לתחזוקה ועדכון

#### שיטה 4: יצירת CSV עם מפרידים שונים

```python
import csv

data = [
    ['שם', 'גיל', 'עיר'],
    ['דני', '20', 'תל אביב'],
    ['שרה', '22', 'ירושלים']
]

# CSV עם נקודה-פסיק (;) כמפריד
with open('students_semicolon.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file, delimiter=';')
    writer.writerows(data)

# CSV עם TAB כמפריד (TSV)
with open('students_tab.tsv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file, delimiter='\t')
    writer.writerows(data)

# CSV עם pipe (|) כמפריד
with open('students_pipe.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file, delimiter='|')
    writer.writerows(data)

print("✓ נוצרו קבצים עם מפרידים שונים")
```

---

### 3.2 קריאת CSV - שיטות שונות

#### שיטה 1: קריאה בסיסית עם csv.reader

```python
import csv

# קריאה פשוטה
with open('students.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    
    # קריאת כל השורות
    for row in reader:
        print(row)
```

**פלט:**
```
['id', 'name', 'age', 'grade', 'city']
['1', 'דני', '20', '85', 'תל אביב']
['2', 'שרה', '22', '92', 'ירושלים']
```

#### שיטה 2: קריאה עם DictReader (מומלץ!)

```python
import csv

with open('students.csv', 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    
    for row in reader:
        print(f"שם: {row['name']}, גיל: {row['age']}, ציון: {row['grade']}")
```

**פלט:**
```
שם: דני, גיל: 20, ציון: 85
שם: שרה, גיל: 22, ציון: 92
שם: יוסי, גיל: 21, ציון: 78
```

#### שיטה 3: קריאה לרשימה

```python
import csv

# קריאת כל הקובץ לזיכרון
with open('students.csv', 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    students = list(reader)

# עכשיו אפשר לעבוד עם הנתונים
print(f"יש {len(students)} תלמידים")
print(f"התלמיד הראשון: {students[0]['name']}")
print(f"התלמיד האחרון: {students[-1]['name']}")

# גישה לתלמיד ספציפי
for student in students:
    if student['name'] == 'שרה':
        print(f"מצאתי את שרה! ציון: {student['grade']}")
```

#### שיטה 4: קריאה עם דילוג על שורות

```python
import csv

with open('students.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    
    # דילוג על שורת הכותרות
    next(reader)
    
    # קריאת שאר השורות
    for row in reader:
        print(f"תלמיד: {row[1]}, ציון: {row[3]}")
```

#### שיטה 5: קריאה עם טיפול בשגיאות

```python
import csv
import os

def read_csv_safe(filename):
    """קריאת CSV בטוחה עם טיפול בשגיאות"""
    
    # בדיקה אם הקובץ קיים
    if not os.path.exists(filename):
        print(f"✗ שגיאה: הקובץ {filename} לא נמצא")
        return None
    
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            data = list(reader)
            print(f"✓ נקראו {len(data)} רשומות מ-{filename}")
            return data
    
    except UnicodeDecodeError:
        print(f"✗ שגיאת קידוד. נסה encoding='windows-1255' לעברית ישנה")
        return None
    
    except csv.Error as e:
        print(f"✗ שגיאת CSV: {e}")
        return None
    
    except Exception as e:
        print(f"✗ שגיאה כללית: {e}")
        return None

# שימוש
students = read_csv_safe('students.csv')
if students:
    for student in students:
        print(student['name'])
```

#### שיטה 6: קריאת CSV גדול (שורה-שורה)

```python
import csv

def process_large_csv(filename):
    """עיבוד קובץ גדול ללא טעינת כל הקובץ לזיכרון"""
    
    count = 0
    total_grade = 0
    
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            count += 1
            total_grade += int(row['grade'])
            
            # עיבוד שורה-שורה
            if int(row['grade']) > 90:
                print(f"תלמיד מצטיין: {row['name']}")
    
    # חישוב ממוצע
    if count > 0:
        avg = total_grade / count
        print(f"\nממוצע כללי: {avg:.2f}")
        print(f"סה\"כ תלמידים: {count}")

process_large_csv('students.csv')
```

---

### 3.3 כתיבה ועדכון CSV

#### הוספת שורה אחת לקובץ קיים

```python
import csv

def add_student(filename, student_data):
    """הוספת תלמיד חדש לקובץ CSV קיים"""
    
    with open(filename, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(student_data)
    
    print(f"✓ תלמיד נוסף: {student_data[1]}")

# דוגמה לשימוש
add_student('students.csv', [6, 'אביגיל', 21, 90, 'רמת גן'])
add_student('students.csv', [7, 'יעקב', 22, 87, 'פתח תקווה'])
```

**שימו לב:** מצב `'a'` (append) מוסיף לסוף הקובץ ללא מחיקת התוכן הקיים.

#### עדכון שורה קיימת

```python
import csv

def update_student_grade(filename, student_id, new_grade):
    """עדכון ציון של תלמיד לפי ID"""
    
    # קריאת כל הנתונים
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        students = list(reader)
        fieldnames = reader.fieldnames
    
    # עדכון הציון
    updated = False
    for student in students:
        if student['id'] == str(student_id):
            student['grade'] = str(new_grade)
            updated = True
            print(f"✓ ציון {student['name']} עודכן ל-{new_grade}")
            break
    
    if not updated:
        print(f"✗ תלמיד עם ID {student_id} לא נמצא")
        return
    
    # כתיבה חזרה לקובץ
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(students)

# שימוש
update_student_grade('students.csv', 1, 95)  # עדכון ציון דני ל-95
```

#### מחיקת שורה

```python
import csv

def delete_student(filename, student_id):
    """מחיקת תלמיד לפי ID"""
    
    # קריאת הנתונים
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        students = list(reader)
        fieldnames = reader.fieldnames
    
    # סינון (הסרת התלמיד)
    original_count = len(students)
    students = [s for s in students if s['id'] != str(student_id)]
    
    if len(students) == original_count:
        print(f"✗ תלמיד עם ID {student_id} לא נמצא")
        return
    
    # כתיבה חזרה
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(students)
    
    print(f"✓ תלמיד נמחק. נותרו {len(students)} תלמידים")

# שימוש
delete_student('students.csv', 3)  # מחיקת יוסי
```

---

### 3.4 פעולות מתקדמות על CSV

#### מיון קובץ CSV

```python
import csv

def sort_csv(filename, sort_by, reverse=False):
    """מיון קובץ CSV לפי עמודה"""
    
    # קריאה
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        students = list(reader)
        fieldnames = reader.fieldnames
    
    # מיון
    students.sort(key=lambda x: x[sort_by], reverse=reverse)
    
    # כתיבה
    output_file = f'sorted_by_{sort_by}.csv'
    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(students)
    
    print(f"✓ הקובץ מוין לפי {sort_by} ונשמר ב-{output_file}")

# דוגמאות שימוש
sort_csv('students.csv', 'name')           # מיון לפי שם (א-ב)
sort_csv('students.csv', 'grade', True)    # מיון לפי ציון (גבוה לנמוך)
sort_csv('students.csv', 'age')            # מיון לפי גיל
```

#### מיון מספרי (חשוב!)

```python
import csv

def sort_csv_numeric(filename, sort_by, reverse=False):
    """מיון מספרי נכון"""
    
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        students = list(reader)
        fieldnames = reader.fieldnames
    
    # המרה למספר לפני מיון
    students.sort(key=lambda x: int(x[sort_by]), reverse=reverse)
    
    output_file = f'sorted_numeric_{sort_by}.csv'
    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(students)
    
    print(f"✓ מיון מספרי לפי {sort_by}")

sort_csv_numeric('students.csv', 'grade', True)
```

#### סינון נתונים

```python
import csv

def filter_csv(filename, condition_func, output_file):
    """סינון CSV לפי תנאי"""
    
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        students = list(reader)
        fieldnames = reader.fieldnames
    
    # סינון
    filtered = [s for s in students if condition_func(s)]
    
    # כתיבה
    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(filtered)
    
    print(f"✓ נמצאו {len(filtered)} רשומות מתוך {len(students)}")

# דוגמאות סינון

# תלמידים עם ציון מעל 85
filter_csv('students.csv', 
           lambda s: int(s['grade']) > 85,
           'high_grades.csv')

# תלמידים מתל אביב
filter_csv('students.csv',
           lambda s: s['city'] == 'תל אביב',
           'tel_aviv_students.csv')

# תלמידים צעירים מ-21
filter_csv('students.csv',
           lambda s: int(s['age']) < 21,
           'young_students.csv')
```

---

### 3.5 סינון וחיפוש בקבצי CSV

#### חיפוש פשוט

```python
import csv

def search_student(filename, search_term):
    """חיפוש תלמיד לפי שם"""
    
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        found = False
        for row in reader:
            if search_term.lower() in row['name'].lower():
                print(f"נמצא: {row['name']} - גיל {row['age']}, ציון {row['grade']}")
                found = True
        
        if not found:
            print(f"לא נמצאו תוצאות עבור '{search_term}'")

# שימוש
search_student('students.csv', 'דני')
search_student('students.csv', 'שר')  # ימצא "שרה"
```

#### חיפוש מתקדם

```python
import csv

def advanced_search(filename, **criteria):
    """חיפוש לפי מספר קריטריונים"""
    
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        results = []
        for row in reader:
            match = True
            
            for key, value in criteria.items():
                if key not in row:
                    continue
                
                if isinstance(value, tuple):  # טווח (min, max)
                    if not (int(value[0]) <= int(row[key]) <= int(value[1])):
                        match = False
                        break
                elif str(row[key]) != str(value):
                    match = False
                    break
            
            if match:
                results.append(row)
        
        return results

# דוגמאות שימוש

# תלמידים בני 20-22 עם ציון מעל 85
results = advanced_search('students.csv', 
                         age=(20, 22),
                         grade=(85, 100))
print(f"נמצאו {len(results)} תלמידים")

# תלמידים מירושלים
results = advanced_search('students.csv', city='ירושלים')
for r in results:
    print(r['name'])
```

---

### 3.6 עבודה עם מספר קבצי CSV

#### איחוד שני קבצי CSV

```python
import csv

def merge_csv_files(file1, file2, output_file):
    """איחוד שני קבצי CSV לקובץ אחד"""
    
    all_data = []
    fieldnames = None
    
    # קריאת קובץ ראשון
    with open(file1, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        all_data.extend(list(reader))
    
    # קריאת קובץ שני
    with open(file2, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        all_data.extend(list(reader))
    
    # כתיבת הקובץ המאוחד
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_data)
    
    print(f"✓ אוחדו {len(all_data)} רשומות ל-{output_file}")

# שימוש
merge_csv_files('students.csv', 'new_students.csv', 'all_students.csv')
```

#### השוואה בין שני קבצי CSV

```python
import csv

def compare_csv_files(file1, file2, key_field='id'):
    """השוואה בין שני קבצי CSV"""
    
    # קריאת קבצים
    with open(file1, 'r', encoding='utf-8') as f:
        data1 = {row[key_field]: row for row in csv.DictReader(f)}
    
    with open(file2, 'r', encoding='utf-8') as f:
        data2 = {row[key_field]: row for row in csv.DictReader(f)}
    
    # מציאת הבדלים
    only_in_file1 = set(data1.keys()) - set(data2.keys())
    only_in_file2 = set(data2.keys()) - set(data1.keys())
    common = set(data1.keys()) & set(data2.keys())
    
    print(f"רק ב-{file1}: {len(only_in_file1)}")
    print(f"רק ב-{file2}: {len(only_in_file2)}")
    print(f"משותף: {len(common)}")
    
    # בדיקת שינויים ברשומות משותפות
    changed = []
    for key in common:
        if data1[key] != data2[key]:
            changed.append(key)
    
    print(f"רשומות ששונו: {len(changed)}")
    
    return {
        'only_in_file1': only_in_file1,
        'only_in_file2': only_in_file2,
        'changed': changed
    }

# שימוש
diff = compare_csv_files('students_old.csv', 'students_new.csv')
```

#### חיבור קבצי CSV (JOIN)

```python
import csv

def join_csv_files(file1, file2, key1, key2, output_file):
    """חיבור שני קבצי CSV כמו JOIN ב-SQL"""
    
    # קריאת הקובץ הראשון
    with open(file1, 'r', encoding='utf-8') as f:
        reader1 = csv.DictReader(f)
        data1 = {row[key1]: row for row in reader1}
    
    # קריאת הקובץ השני וחיבור
    results = []
    with open(file2, 'r', encoding='utf-8') as f:
        reader2 = csv.DictReader(f)
        
        for row2 in reader2:
            if row2[key2] in data1:
                # מיזוג שני השורות
                merged = {**data1[row2[key2]], **row2}
                results.append(merged)
    
    # כתיבת התוצאה
    if results:
        fieldnames = results[0].keys()
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)
        
        print(f"✓ חובר {len(results)} רשומות")

# דוגמה: חיבור תלמידים עם ציונים
join_csv_files('students.csv', 'grades.csv', 'id', 'student_id', 'full_data.csv')
```

---

## אינטגרציה עם SQLite

כעת נלמד איך להעביר את הנתונים מקבצי CSV למסד נתונים SQLite ולהיפך.

### יצירת מסד נתונים SQLite בסיסי

```python
import sqlite3

# יצירת/חיבור למסד נתונים
conn = sqlite3.connect('school.db')
cursor = conn.cursor()

# יצירת טבלה
cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        age INTEGER,
        grade INTEGER,
        city TEXT
    )
''')

conn.commit()
conn.close()
print("✓ מסד נתונים נוצר בהצלחה")
```

---

## העברת נתונים מ-CSV ל-SQLite

### שלב 1: קריאה מ-CSV והכנסה ל-SQLite

```python
import csv
import sqlite3

# חיבור למסד נתונים
conn = sqlite3.connect('school.db')
cursor = conn.cursor()

# יצירת טבלה
cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        age INTEGER,
        grade INTEGER,
        city TEXT
    )
''')

# קריאת הנתונים מ-CSV והכנסה ל-SQLite
with open('students.csv', 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    
    for row in reader:
        cursor.execute('''
            INSERT INTO students (id, name, age, grade, city)
            VALUES (?, ?, ?, ?, ?)
        ''', (row['id'], row['name'], row['age'], row['grade'], row['city']))

# שמירת השינויים
conn.commit()

# בדיקה - כמה רשומות הוכנסו
cursor.execute('SELECT COUNT(*) FROM students')
count = cursor.fetchone()[0]
print(f"הוכנסו {count} תלמידים למסד הנתונים")

conn.close()
```

**הסבר:**
- `?` - placeholders למניעת SQL Injection
- `commit()` - שומר את השינויים במסד הנתונים
- `fetchone()` - מחזיר רשומה אחת

### שלב 2: גרסה משופרת עם טיפול בשגיאות

```python
import csv
import sqlite3

def import_csv_to_sqlite(csv_file, db_file, table_name):
    """
    מייבא נתונים מ-CSV ל-SQLite
    """
    try:
        # חיבור למסד נתונים
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        
        # יצירת טבלה
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {table_name} (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                age INTEGER,
                grade INTEGER,
                city TEXT
            )
        ''')
        
        # ניקוי הטבלה (אופציונלי)
        cursor.execute(f'DELETE FROM {table_name}')
        
        # קריאה והכנסת נתונים
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                cursor.execute(f'''
                    INSERT INTO {table_name} (id, name, age, grade, city)
                    VALUES (?, ?, ?, ?, ?)
                ''', (row['id'], row['name'], row['age'], row['grade'], row['city']))
        
        conn.commit()
        
        # בדיקה
        cursor.execute(f'SELECT COUNT(*) FROM {table_name}')
        count = cursor.fetchone()[0]
        print(f"✓ הצלחה! {count} רשומות יובאו לטבלת {table_name}")
        
    except FileNotFoundError:
        print(f"✗ שגיאה: הקובץ {csv_file} לא נמצא")
    except sqlite3.Error as e:
        print(f"✗ שגיאת SQLite: {e}")
    except Exception as e:
        print(f"✗ שגיאה כללית: {e}")
    finally:
        if conn:
            conn.close()

# שימוש בפונקציה
import_csv_to_sqlite('students.csv', 'school.db', 'students')
```

---

## שאילתות בסיסיות

### 1. בחירת כל הנתונים (SELECT)

```python
import sqlite3

conn = sqlite3.connect('school.db')
cursor = conn.cursor()

# שאילתה בסיסית
cursor.execute('SELECT * FROM students')
results = cursor.fetchall()

print("כל התלמידים:")
for row in results:
    print(row)

conn.close()
```

### 2. בחירת עמודות ספציפיות

```python
import sqlite3

conn = sqlite3.connect('school.db')
cursor = conn.cursor()

# בחירת שם וציון בלבד
cursor.execute('SELECT name, grade FROM students')
results = cursor.fetchall()

print("שמות וציונים:")
for name, grade in results:
    print(f"{name}: {grade}")

conn.close()
```

### 3. סינון נתונים (WHERE)

```python
import sqlite3

conn = sqlite3.connect('school.db')
cursor = conn.cursor()

# תלמידים עם ציון מעל 85
cursor.execute('SELECT name, grade FROM students WHERE grade > 85')
results = cursor.fetchall()

print("תלמידים מצטיינים (ציון מעל 85):")
for name, grade in results:
    print(f"{name}: {grade}")

conn.close()
```

### 4. מיון תוצאות (ORDER BY)

```python
import sqlite3

conn = sqlite3.connect('school.db')
cursor = conn.cursor()

# מיון לפי ציון בסדר יורד
cursor.execute('SELECT name, grade FROM students ORDER BY grade DESC')
results = cursor.fetchall()

print("תלמידים לפי ציונים (מהגבוה לנמוך):")
for i, (name, grade) in enumerate(results, 1):
    print(f"{i}. {name}: {grade}")

conn.close()
```

### 5. חישובים סטטיסטיים

```python
import sqlite3

conn = sqlite3.connect('school.db')
cursor = conn.cursor()

# ממוצע ציונים
cursor.execute('SELECT AVG(grade) FROM students')
avg = cursor.fetchone()[0]
print(f"ממוצע הציונים: {avg:.2f}")

# ציון מקסימלי
cursor.execute('SELECT MAX(grade) FROM students')
max_grade = cursor.fetchone()[0]
print(f"הציון הגבוה ביותר: {max_grade}")

# ציון מינימלי
cursor.execute('SELECT MIN(grade) FROM students')
min_grade = cursor.fetchone()[0]
print(f"הציון הנמוך ביותר: {min_grade}")

# ספירת תלמידים
cursor.execute('SELECT COUNT(*) FROM students')
count = cursor.fetchone()[0]
print(f"מספר התלמידים: {count}")

conn.close()
```

### 6. קיבוץ נתונים (GROUP BY)

```python
import sqlite3

conn = sqlite3.connect('school.db')
cursor = conn.cursor()

# מספר תלמידים בכל עיר
cursor.execute('SELECT city, COUNT(*) as count FROM students GROUP BY city')
results = cursor.fetchall()

print("מספר תלמידים לפי עיר:")
for city, count in results:
    print(f"{city}: {count} תלמידים")

conn.close()
```

---

## ייצוא נתונים מ-SQLite ל-CSV

### שלב 1: ייצוא בסיסי

```python
import sqlite3
import csv

conn = sqlite3.connect('school.db')
cursor = conn.cursor()

# שאילתה
cursor.execute('SELECT * FROM students')
results = cursor.fetchall()

# קבלת שמות העמודות
column_names = [description[0] for description in cursor.description]

# כתיבה ל-CSV
with open('students_export.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    
    # כתיבת כותרות
    writer.writerow(column_names)
    
    # כתיבת הנתונים
    writer.writerows(results)

print("הנתונים יוצאו בהצלחה ל-students_export.csv")
conn.close()
```

### שלב 2: ייצוא עם סינון

```python
import sqlite3
import csv

def export_to_csv(db_file, query, output_file):
    """
    מייצא תוצאות שאילתה ל-CSV
    """
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    cursor.execute(query)
    results = cursor.fetchall()
    column_names = [description[0] for description in cursor.description]
    
    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(column_names)
        writer.writerows(results)
    
    print(f"✓ {len(results)} רשומות יוצאו ל-{output_file}")
    conn.close()

# דוגמאות שימוש:

# ייצוא תלמידים מצטיינים
export_to_csv('school.db', 
              'SELECT * FROM students WHERE grade >= 90',
              'excellent_students.csv')

# ייצוא תלמידים מעיר מסוימת
export_to_csv('school.db',
              "SELECT * FROM students WHERE city = 'תל אביב'",
              'tel_aviv_students.csv')

# ייצוא עם מיון
export_to_csv('school.db',
              'SELECT name, grade FROM students ORDER BY grade DESC',
              'students_by_grade.csv')
```

---

## תרגילים מעשיים - התמקדות ב-CSV

### תרגיל 1: מערכת ניהול מוצרים בחנות

```python
import csv
from datetime import datetime

class ProductManager:
    """מערכת ניהול מוצרים עם CSV"""
    
    def __init__(self, filename='products.csv'):
        self.filename = filename
        self.fieldnames = ['id', 'name', 'price', 'quantity', 'category', 'last_updated']
        self.create_file_if_not_exists()
    
    def create_file_if_not_exists(self):
        """יצירת קובץ אם לא קיים"""
        try:
            with open(self.filename, 'r', encoding='utf-8'):
                pass
        except FileNotFoundError:
            with open(self.filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=self.fieldnames)
                writer.writeheader()
            print(f"✓ נוצר קובץ {self.filename}")
    
    def add_product(self, name, price, quantity, category):
        """הוספת מוצר חדש"""
        # קבלת ID הבא
        products = self.get_all_products()
        next_id = max([int(p['id']) for p in products], default=0) + 1
        
        # יצירת מוצר חדש
        product = {
            'id': next_id,
            'name': name,
            'price': price,
            'quantity': quantity,
            'category': category,
            'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # הוספה לקובץ
        with open(self.filename, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=self.fieldnames)
            writer.writerow(product)
        
        print(f"✓ מוצר '{name}' נוסף בהצלחה (ID: {next_id})")
        return next_id
    
    def get_all_products(self):
        """קבלת כל המוצרים"""
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                return list(reader)
        except FileNotFoundError:
            return []
    
    def search_by_name(self, search_term):
        """חיפוש מוצר לפי שם"""
        products = self.get_all_products()
        results = [p for p in products if search_term.lower() in p['name'].lower()]
        
        print(f"\n=== נמצאו {len(results)} תוצאות עבור '{search_term}' ===")
        for p in results:
            print(f"ID: {p['id']}, {p['name']} - ₪{p['price']} ({p['quantity']} במלאי)")
        
        return results
    
    def search_by_category(self, category):
        """חיפוש לפי קטגוריה"""
        products = self.get_all_products()
        results = [p for p in products if p['category'].lower() == category.lower()]
        
        print(f"\n=== {len(results)} מוצרים בקטגוריה '{category}' ===")
        for p in results:
            print(f"{p['name']}: ₪{p['price']}")
        
        return results
    
    def update_quantity(self, product_id, new_quantity):
        """עדכון כמות במלאי"""
        products = self.get_all_products()
        
        for p in products:
            if p['id'] == str(product_id):
                p['quantity'] = str(new_quantity)
                p['last_updated'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                break
        
        # שמירה חזרה
        with open(self.filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=self.fieldnames)
            writer.writeheader()
            writer.writerows(products)
        
        print(f"✓ כמות עודכנה ל-{new_quantity}")
    
    def get_low_stock(self, threshold=5):
        """מציאת מוצרים עם מלאי נמוך"""
        products = self.get_all_products()
        low_stock = [p for p in products if int(p['quantity']) < threshold]
        
        print(f"\n=== מוצרים עם מלאי מתחת ל-{threshold} ===")
        for p in low_stock:
            print(f"⚠️  {p['name']}: רק {p['quantity']} במלאי")
        
        return low_stock
    
    def generate_report(self):
        """יצירת דוח מלאי"""
        products = self.get_all_products()
        
        if not products:
            print("אין מוצרים במערכת")
            return
        
        # חישובים
        total_products = len(products)
        total_value = sum(float(p['price']) * int(p['quantity']) for p in products)
        categories = {}
        
        for p in products:
            cat = p['category']
            if cat not in categories:
                categories[cat] = {'count': 0, 'value': 0}
            categories[cat]['count'] += 1
            categories[cat]['value'] += float(p['price']) * int(p['quantity'])
        
        # הדפסת דוח
        print("\n" + "="*50)
        print("           דוח מלאי מפורט")
        print("="*50)
        print(f"סה\"כ מוצרים: {total_products}")
        print(f"שווי כולל: ₪{total_value:,.2f}")
        print(f"\nפילוח לפי קטגוריות:")
        for cat, data in categories.items():
            print(f"  {cat}: {data['count']} מוצרים (שווי: ₪{data['value']:,.2f})")
        print("="*50)
    
    def export_category(self, category, output_file):
        """ייצוא קטגוריה ספציפית לקובץ נפרד"""
        products = self.search_by_category(category)
        
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=self.fieldnames)
            writer.writeheader()
            writer.writerows(products)
        
        print(f"✓ {len(products)} מוצרים יוצאו ל-{output_file}")

# דוגמת שימוש
if __name__ == "__main__":
    manager = ProductManager()
    
    # הוספת מוצרים
    manager.add_product('לפטופ Dell', 3500, 10, 'מחשבים')
    manager.add_product('עכבר Logitech', 80, 50, 'אביזרים')
    manager.add_product('מקלדת מכנית', 350, 25, 'אביזרים')
    manager.add_product('מסך 27 אינץ', 1200, 3, 'מסכים')
    manager.add_product('כבל HDMI', 45, 100, 'כבלים')
    
    # חיפושים
    manager.search_by_name('Dell')
    manager.search_by_category('אביזרים')
    
    # מציאת מלאי נמוך
    manager.get_low_stock(10)
    
    # עדכון מלאי
    manager.update_quantity(4, 15)
    
    # דוח
    manager.generate_report()
    
    # ייצוא
    manager.export_category('אביזרים', 'accessories.csv')
```

### תרגיל 2: מערכת רישום נוכחות

```python
import csv
from datetime import datetime, date

class AttendanceSystem:
    """מערכת רישום נוכחות"""
    
    def __init__(self, students_file='students.csv', attendance_file='attendance.csv'):
        self.students_file = students_file
        self.attendance_file = attendance_file
        self.init_attendance_file()
    
    def init_attendance_file(self):
        """יצירת קובץ נוכחות אם לא קיים"""
        try:
            with open(self.attendance_file, 'r', encoding='utf-8'):
                pass
        except FileNotFoundError:
            with open(self.attendance_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['date', 'student_id', 'student_name', 'status', 'time'])
            print(f"✓ נוצר קובץ נוכחות: {self.attendance_file}")
    
    def mark_attendance(self, student_id, student_name, status='נוכח'):
        """רישום נוכחות"""
        today = date.today().strftime('%Y-%m-%d')
        time_now = datetime.now().strftime('%H:%M:%S')
        
        # בדיקה אם כבר נרשם היום
        if self.check_if_marked(student_id, today):
            print(f"⚠️  {student_name} כבר נרשם/ה היום")
            return False
        
        # רישום
        with open(self.attendance_file, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([today, student_id, student_name, status, time_now])
        
        print(f"✓ {student_name} נרשם/ה כ{status} בשעה {time_now}")
        return True
    
    def check_if_marked(self, student_id, date_str):
        """בדיקה אם תלמיד כבר נרשם בתאריך מסוים"""
        try:
            with open(self.attendance_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row['student_id'] == str(student_id) and row['date'] == date_str:
                        return True
        except FileNotFoundError:
            pass
        return False
    
    def get_daily_report(self, date_str=None):
        """דוח נוכחות יומי"""
        if date_str is None:
            date_str = date.today().strftime('%Y-%m-%d')
        
        with open(self.attendance_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            daily = [r for r in reader if r['date'] == date_str]
        
        print(f"\n=== דוח נוכחות ליום {date_str} ===")
        present = [r for r in daily if r['status'] == 'נוכח']
        absent = [r for r in daily if r['status'] == 'חסר']
        
        print(f"נוכחים: {len(present)}")
        print(f"חסרים: {len(absent)}")
        
        if present:
            print("\nרשימת נוכחים:")
            for r in present:
                print(f"  - {r['student_name']} (הגיע/ה בשעה {r['time']})")
        
        if absent:
            print("\nרשימת חסרים:")
            for r in absent:
                print(f"  - {r['student_name']}")
        
        return daily
    
    def get_student_attendance(self, student_id):
        """דוח נוכחות לתלמיד ספציפי"""
        with open(self.attendance_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            records = [r for r in reader if r['student_id'] == str(student_id)]
        
        if not records:
            print(f"לא נמצאו רשומות עבור תלמיד {student_id}")
            return []
        
        student_name = records[0]['student_name']
        present = len([r for r in records if r['status'] == 'נוכח'])
        total = len(records)
        percentage = (present / total * 100) if total > 0 else 0
        
        print(f"\n=== דוח נוכחות: {student_name} ===")
        print(f"ימי נוכחות: {present}/{total} ({percentage:.1f}%)")
        
        return records
    
    def export_monthly_report(self, year, month):
        """ייצוא דוח חודשי"""
        with open(self.attendance_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            monthly = [r for r in reader 
                      if r['date'].startswith(f"{year}-{month:02d}")]
        
        output_file = f'attendance_{year}_{month:02d}.csv'
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            if monthly:
                writer = csv.DictWriter(f, fieldnames=monthly[0].keys())
                writer.writeheader()
                writer.writerows(monthly)
        
        print(f"✓ דוח חודשי יוצא ל-{output_file} ({len(monthly)} רשומות)")

# דוגמת שימוש
if __name__ == "__main__":
    system = AttendanceSystem()
    
    # רישום נוכחות
    system.mark_attendance(1, 'דני כהן', 'נוכח')
    system.mark_attendance(2, 'שרה לוי', 'נוכח')
    system.mark_attendance(3, 'יוסי ישראלי', 'חסר')
    system.mark_attendance(4, 'רחל אברהם', 'נוכח')
    
    # דוח יומי
    system.get_daily_report()
    
    # דוח לתלמיד
    system.get_student_attendance(1)
```

### תרגיל 3: ניתוח ועיבוד קובץ CSV גדול

```python
import csv
from collections import defaultdict, Counter

class CSVAnalyzer:
    """כלי לניתוח קבצי CSV גדולים"""
    
    def __init__(self, filename):
        self.filename = filename
    
    def analyze_structure(self):
        """ניתוח מבנה הקובץ"""
        with open(self.filename, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            # קריאת שורה ראשונה
            first_row = next(reader, None)
            if not first_row:
                print("הקובץ ריק")
                return
            
            # ספירת שורות
            row_count = 1
            for row in reader:
                row_count += 1
            
            print(f"\n=== ניתוח מבנה: {self.filename} ===")
            print(f"מספר עמודות: {len(first_row)}")
            print(f"מספר שורות: {row_count}")
            print(f"שמות עמודות: {', '.join(first_row.keys())}")
    
    def column_statistics(self, column_name):
        """סטטיסטיקות עבור עמודה"""
        values = []
        
        with open(self.filename, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                if column_name in row and row[column_name]:
                    values.append(row[column_name])
        
        if not values:
            print(f"לא נמצאו ערכים בעמודה '{column_name}'")
            return
        
        print(f"\n=== סטטיסטיקות עבור '{column_name}' ===")
        print(f"סה\"כ ערכים: {len(values)}")
        
        # ניסיון לזהות אם זה מספר
        try:
            numeric_values = [float(v) for v in values]
            print(f"סוג: מספרי")
            print(f"ממוצע: {sum(numeric_values) / len(numeric_values):.2f}")
            print(f"מינימום: {min(numeric_values)}")
            print(f"מקסימום: {max(numeric_values)}")
        except ValueError:
            # זה טקסט
            print(f"סוג: טקסט")
            print(f"ערכים ייחודיים: {len(set(values))}")
            
            # הצגת הערכים הנפוצים ביותר
            counter = Counter(values)
            print(f"הערכים הנפוצים ביותר:")
            for value, count in counter.most_common(5):
                print(f"  {value}: {count} פעמים")
    
    def group_by(self, group_column, aggregate_column, operation='count'):
        """קיבוץ נתונים לפי עמודה"""
        groups = defaultdict(list)
        
        with open(self.filename, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                key = row[group_column]
                if aggregate_column:
                    groups[key].append(row[aggregate_column])
                else:
                    groups[key].append(1)
        
        print(f"\n=== קיבוץ לפי '{group_column}' ===")
        
        for key, values in sorted(groups.items()):
            if operation == 'count':
                print(f"{key}: {len(values)}")
            elif operation == 'sum' and aggregate_column:
                try:
                    total = sum(float(v) for v in values if v)
                    print(f"{key}: {total:.2f}")
                except ValueError:
                    print(f"{key}: לא ניתן לחשב סכום")
            elif operation == 'avg' and aggregate_column:
                try:
                    avg = sum(float(v) for v in values if v) / len(values)
                    print(f"{key}: {avg:.2f}")
                except ValueError:
                    print(f"{key}: לא ניתן לחשב ממוצע")
    
    def find_duplicates(self, column_name):
        """מציאת ערכים כפולים"""
        values = defaultdict(list)
        
        with open(self.filename, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for i, row in enumerate(reader, 1):
                value = row[column_name]
                values[value].append(i)
        
        # סינון רק ערכים שחוזרים
        duplicates = {k: v for k, v in values.items() if len(v) > 1}
        
        if duplicates:
            print(f"\n=== נמצאו {len(duplicates)} ערכים כפולים ב-'{column_name}' ===")
            for value, rows in list(duplicates.items())[:10]:
                print(f"{value}: מופיע {len(rows)} פעמים (שורות: {', '.join(map(str, rows))})")
        else:
            print(f"✓ לא נמצאו ערכים כפולים ב-'{column_name}'")
    
    def clean_and_export(self, output_file, remove_duplicates=False, sort_by=None):
        """ניקוי וייצוא הקובץ"""
        with open(self.filename, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            data = list(reader)
            fieldnames = reader.fieldnames
        
        # הסרת שורות ריקות
        data = [row for row in data if any(row.values())]
        
        # הסרת כפילויות
        if remove_duplicates:
            seen = set()
            unique_data = []
            for row in data:
                row_tuple = tuple(row.items())
                if row_tuple not in seen:
                    seen.add(row_tuple)
                    unique_data.append(row)
            data = unique_data
        
        # מיון
        if sort_by and sort_by in fieldnames:
            try:
                data.sort(key=lambda x: float(x[sort_by]))
            except ValueError:
                data.sort(key=lambda x: x[sort_by])
        
        # כתיבה
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        
        print(f"✓ קובץ מנוקה נשמר ב-{output_file} ({len(data)} רשומות)")

# דוגמת שימוש
if __name__ == "__main__":
    analyzer = CSVAnalyzer('students.csv')
    
    # ניתוח מבנה
    analyzer.analyze_structure()
    
    # סטטיסטיקות
    analyzer.column_statistics('grade')
    analyzer.column_statistics('city')
    
    # קיבוץ
    analyzer.group_by('city', 'grade', 'avg')
    
    # מציאת כפילויות
    analyzer.find_duplicates('name')
    
    # ניקוי וייצוא
    analyzer.clean_and_export('students_clean.csv', remove_duplicates=True, sort_by='grade')
```

---

## טיפים וטריקים מתקדמים

### 1. שימוש ב-Context Manager

```python
import sqlite3

class DatabaseConnection:
    """Context manager לחיבור מסד נתונים"""
    
    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = None
    
    def __enter__(self):
        self.conn = sqlite3.connect(self.db_file)
        return self.conn.cursor()
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            if exc_type is None:
                self.conn.commit()
            else:
                self.conn.rollback()
            self.conn.close()

# שימוש
with DatabaseConnection('school.db') as cursor:
    cursor.execute('SELECT * FROM students')
    results = cursor.fetchall()
    for row in results:
        print(row)
```

### 2. Bulk Insert מהיר יותר

```python
import csv
import sqlite3

conn = sqlite3.connect('school.db')
cursor = conn.cursor()

# קריאת כל הנתונים מ-CSV
with open('students.csv', 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    data = [(row['id'], row['name'], row['age'], row['grade'], row['city']) 
            for row in reader]

# הכנסה מהירה של כל הנתונים בבת אחת
cursor.executemany('''
    INSERT INTO students (id, name, age, grade, city)
    VALUES (?, ?, ?, ?, ?)
''', data)

conn.commit()
conn.close()
```

### 3. שאילתות פרמטריות בטוחות

```python
import sqlite3

def safe_search(name_pattern):
    """חיפוש בטוח עם פרמטרים"""
    conn = sqlite3.connect('school.db')
    cursor = conn.cursor()
    
    # שימוש נכון ב-parameters
    cursor.execute('SELECT * FROM students WHERE name LIKE ?', (f'%{name_pattern}%',))
    results = cursor.fetchall()
    
    conn.close()
    return results

# שימוש
results = safe_search('דני')
for row in results:
    print(row)
```

---

## שגיאות נפוצות ופתרונות

### שגיאה 1: UnicodeDecodeError
**בעיה:** טקסט בעברית לא מוצג כראוי

**פתרון:**
```python
# תמיד להוסיף encoding='utf-8'
with open('file.csv', 'r', encoding='utf-8') as file:
    # קוד...
```

### שגיאה 2: sqlite3.OperationalError: table already exists
**בעיה:** ניסיון ליצור טבלה קיימת

**פתרון:**
```python
# שימוש ב-IF NOT EXISTS
cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (...)
''')
```

### שגיאה 3: נתונים לא נשמרים
**בעיה:** שכחתם לקרוא ל-commit()

**פתרון:**
```python
conn = sqlite3.connect('school.db')
cursor = conn.cursor()
cursor.execute('INSERT INTO ...')
conn.commit()  # חובה!
conn.close()
```

---

## סיכום ומה הלאה

### מה למדנו:
✓ עבודה עם קבצי CSV (קריאה וכתיבה)  
✓ יצירת מסד נתונים SQLite  
✓ העברת נתונים בין CSV ל-SQLite  
✓ שאילתות SQL בסיסיות  
✓ ייצוא נתונים  
✓ טיפול בשגיאות  

### צעדים הבאים:
1. למד על יחסים בין טבלאות (Foreign Keys)
2. התנסה עם Pandas לניתוח נתונים מתקדם
3. למד על SQLAlchemy או SQLModel לעבודה מתקדמת
4. בנה פרויקט אמיתי משלך

### משאבים נוספים:
- [תיעוד Python CSV](https://docs.python.org/3/library/csv.html)
- [תיעוד Python SQLite3](https://docs.python.org/3/library/sqlite3.html)
- [SQLite Tutorial](https://www.sqlitetutorial.net/)

---

**בהצלחה! 🚀**
