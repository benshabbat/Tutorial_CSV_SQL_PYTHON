# תרגיל OOP - מערכת ניהול אנשים ומכוניות
## שילוב Python OOP, SQLite3 ו-CSV

---

## חלק 1: הגדרת המחלקות (Classes)

### תיאור:
צור שתי מחלקות בסיסיות: `Person` ו-`Car` שמייצגות אנשים ומכוניות.

### דרישות למחלקה Person:

**Attributes (תכונות):**
- `person_id` - מזהה ייחודי (int)
- `name` - שם מלא (str)
- `age` - גיל (int)
- `email` - כתובת אימייל (str)
- `cars` - רשימה של מכוניות שבבעלות האדם (list)

**Methods (מתודות):**
- `__init__()` - constructor
- `add_car(car)` - הוספת מכונית לאדם
- `get_cars_count()` - החזרת מספר המכוניות
- `__str__()` - ייצוג טקסטואלי
- `to_dict()` - המרה ל-dictionary

### דרישות למחלקה Car:

**Attributes (תכונות):**
- `car_id` - מזהה ייחודי (int)
- `brand` - יצרן (str)
- `model` - דגם (str)
- `year` - שנת ייצור (int)
- `color` - צבע (str)
- `owner_id` - מזהה הבעלים (int)

**Methods (מתודות):**
- `__init__()` - constructor
- `__str__()` - ייצוג טקסטואלי
- `to_dict()` - המרה ל-dictionary
- `get_age()` - חישוב גיל המכונית

### קוד לדוגמה להתחלה:

```python
from datetime import datetime

class Person:
    def __init__(self, person_id, name, age, email):
        self.person_id = person_id
        self.name = name
        self.age = age
        self.email = email
        self.cars = []
    
    def add_car(self, car):
        """Add a car to person's cars list"""
        # TODO: implement
        pass
    
    def get_cars_count(self):
        """Return the number of cars owned"""
        # TODO: implement
        pass
    
    def __str__(self):
        """String representation of person"""
        # TODO: implement
        pass
    
    def to_dict(self):
        """Convert person to dictionary"""
        # TODO: implement
        pass


class Car:
    def __init__(self, car_id, brand, model, year, color, owner_id=None):
        self.car_id = car_id
        self.brand = brand
        self.model = model
        self.year = year
        self.color = color
        self.owner_id = owner_id
    
    def get_age(self):
        """Calculate car age"""
        # TODO: implement
        pass
    
    def __str__(self):
        """String representation of car"""
        # TODO: implement
        pass
    
    def to_dict(self):
        """Convert car to dictionary"""
        # TODO: implement
        pass
```

---

## חלק 2: מחלקת ניהול מסד נתונים (DatabaseManager)

### תיאור:
צור מחלקה `DatabaseManager` שמנהלת את כל הפעולות עם SQLite3.

### דרישות:

**Structure של מסד הנתונים:**

**טבלה: persons**
```sql
CREATE TABLE persons (
    person_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    age INTEGER NOT NULL,
    email TEXT UNIQUE NOT NULL
)
```

**טבלה: cars**
```sql
CREATE TABLE cars (
    car_id INTEGER PRIMARY KEY,
    brand TEXT NOT NULL,
    model TEXT NOT NULL,
    year INTEGER NOT NULL,
    color TEXT NOT NULL,
    owner_id INTEGER,
    FOREIGN KEY (owner_id) REFERENCES persons(person_id)
)
```

**Methods נדרשות:**
1. `__init__(db_name)` - חיבור למסד נתונים
2. `create_tables()` - יצירת הטבלאות
3. `insert_person(person)` - הוספת אדם למסד
4. `insert_car(car)` - הוספת מכונית למסד
5. `get_all_persons()` - שליפת כל האנשים
6. `get_all_cars()` - שליפת כל המכוניות
7. `get_person_by_id(person_id)` - שליפת אדם לפי ID
8. `get_cars_by_owner(owner_id)` - שליפת מכוניות לפי בעלים
9. `update_person(person)` - עדכון פרטי אדם
10. `delete_person(person_id)` - מחיקת אדם
11. `close()` - סגירת החיבור למסד

### קוד שלד:

```python
import sqlite3

class DatabaseManager:
    def __init__(self, db_name='persons_cars.db'):
        """Initialize database connection"""
        self.db_name = db_name
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
    
    def create_tables(self):
        """Create persons and cars tables"""
        # TODO: Create persons table
        # TODO: Create cars table
        pass
    
    def insert_person(self, person):
        """Insert a person into database"""
        # TODO: implement
        pass
    
    def insert_car(self, car):
        """Insert a car into database"""
        # TODO: implement
        pass
    
    def get_all_persons(self):
        """Get all persons from database"""
        # TODO: implement and return list of Person objects
        pass
    
    def get_all_cars(self):
        """Get all cars from database"""
        # TODO: implement and return list of Car objects
        pass
    
    def get_person_by_id(self, person_id):
        """Get person by ID"""
        # TODO: implement
        pass
    
    def get_cars_by_owner(self, owner_id):
        """Get all cars owned by a person"""
        # TODO: implement
        pass
    
    def update_person(self, person):
        """Update person details"""
        # TODO: implement
        pass
    
    def delete_person(self, person_id):
        """Delete person from database"""
        # TODO: implement
        pass
    
    def close(self):
        """Close database connection"""
        self.connection.close()
```

---

## חלק 3: מחלקת ניהול CSV (CSVManager)

### תיאור:
צור מחלקה `CSVManager` שמטפלת בקריאה וכתיבה של קבצי CSV.

### דרישות:

**Methods נדרשות:**
1. `export_persons_to_csv(persons, filename)` - ייצוא אנשים ל-CSV
2. `export_cars_to_csv(cars, filename)` - ייצוא מכוניות ל-CSV
3. `import_persons_from_csv(filename)` - ייבוא אנשים מ-CSV
4. `import_cars_from_csv(filename)` - ייבוא מכוניות מ-CSV
5. `export_full_report(db_manager, filename)` - דוח מלא של אנשים + מכוניות

### פורמט CSV לדוגמה:

**persons.csv:**
```
person_id,name,age,email
1,David Cohen,35,david@example.com
2,Sarah Levi,28,sarah@example.com
```

**cars.csv:**
```
car_id,brand,model,year,color,owner_id
1,Toyota,Corolla,2020,White,1
2,Honda,Civic,2019,Blue,1
3,Mazda,3,2021,Red,2
```

### קוד שלד:

```python
import csv

class CSVManager:
    @staticmethod
    def export_persons_to_csv(persons, filename):
        """Export persons list to CSV file"""
        # TODO: implement
        pass
    
    @staticmethod
    def export_cars_to_csv(cars, filename):
        """Export cars list to CSV file"""
        # TODO: implement
        pass
    
    @staticmethod
    def import_persons_from_csv(filename):
        """Import persons from CSV file"""
        # TODO: implement and return list of Person objects
        pass
    
    @staticmethod
    def import_cars_from_csv(filename):
        """Import cars from CSV file"""
        # TODO: implement and return list of Car objects
        pass
    
    @staticmethod
    def export_full_report(db_manager, filename):
        """Export full report with persons and their cars"""
        # TODO: Create a CSV with columns: person_name, age, email, cars_count, car_brands
        pass
```

---

## חלק 4: תרגילים מעשיים

### תרגיל 4.1: יצירת מערכת בסיסית

צור תוכנית שמבצעת את השלבים הבאים:

1. צור 3 אנשים עם הפרטים הבאים:
   - דוד כהן, גיל 35, david@example.com
   - שרה לוי, גיל 28, sarah@example.com
   - יוסי אברהם, גיל 42, yossi@example.com

2. צור 5 מכוניות:
   - Toyota Corolla 2020 לבן - לדוד
   - Honda Civic 2019 כחול - לדוד
   - Mazda 3 2021 אדום - לשרה
   - Hyundai i30 2022 שחור - ליוסי
   - Kia Sportage 2023 אפור - ליוסי

3. שמור הכל במסד נתונים SQLite3

4. הצג את כל האנשים והמכוניות שלהם

```python
def main():
    # TODO: Create DatabaseManager instance
    # TODO: Create tables
    # TODO: Create persons
    # TODO: Create cars
    # TODO: Insert to database
    # TODO: Print all data
    pass

if __name__ == "__main__":
    main()
```

### תרגיל 4.2: שאילתות מתקדמות

כתוב פונקציות ששואלות את מסד הנתונים:

1. `find_persons_with_multiple_cars()` - מצא אנשים עם יותר ממכונית אחת
2. `find_cars_older_than(year)` - מצא מכוניות ישנות מ-X שנים
3. `get_average_cars_per_person()` - חשב ממוצע מכוניות לאדם
4. `find_most_popular_brand()` - מצא את היצרן הפופולרי ביותר
5. `get_persons_by_age_range(min_age, max_age)` - מצא אנשים בטווח גיל

```python
def find_persons_with_multiple_cars(db_manager):
    """Find persons who own more than one car"""
    # TODO: Write SQL query
    pass

def find_cars_older_than(db_manager, year):
    """Find cars older than specified year"""
    # TODO: Write SQL query
    pass
```

### תרגיל 4.3: עבודה עם CSV

1. ייצא את כל האנשים לקובץ `persons.csv`
2. ייצא את כל המכוניות לקובץ `cars.csv`
3. צור דוח מלא בקובץ `full_report.csv` עם העמודות:
   - שם אדם, גיל, אימייל, מספר מכוניות, רשימת יצרנים

```python
def export_all_data():
    # TODO: Export persons to CSV
    # TODO: Export cars to CSV
    # TODO: Create full report
    pass
```

### תרגיל 4.4: ייבוא מ-CSV ועדכון מסד נתונים

1. קרא נתונים מקבצי CSV
2. הוסף אותם למסד נתונים
3. בדוק שאין כפילויות

```python
def import_and_update():
    # TODO: Import from CSV
    # TODO: Check for duplicates
    # TODO: Update database
    pass
```

---

## חלק 5: תרגילים מתקדמים

### תרגיל 5.1: מחלקה מורחבת - CarOwnershipHistory

צור מחלקה `CarOwnershipHistory` שעוקבת אחרי היסטוריית בעלות על מכוניות:

```python
class CarOwnershipHistory:
    def __init__(self, car_id, previous_owner_id, new_owner_id, transfer_date):
        self.car_id = car_id
        self.previous_owner_id = previous_owner_id
        self.new_owner_id = new_owner_id
        self.transfer_date = transfer_date
    
    # TODO: Add methods
```

הוסף טבלה חדשה למסד הנתונים ומתודות מתאימות.

### תרגיל 5.2: Transaction Manager

צור מחלקה שמטפלת ב-transactions למכירת מכוניות:

```python
class TransactionManager:
    def __init__(self, db_manager):
        self.db_manager = db_manager
    
    def transfer_car_ownership(self, car_id, new_owner_id):
        """Transfer car from one owner to another"""
        # TODO: Update car owner
        # TODO: Add to history
        # TODO: Commit or rollback
        pass
```

### תרגיל 5.3: סטטיסטיקות ודוחות

צור מחלקה `StatisticsManager` שמחשבת סטטיסטיקות:

1. התפלגות גילאים של אנשים
2. התפלגות יצרנים של מכוניות
3. ממוצע גיל מכוניות לפי יצרן
4. אדם עם הכי הרבה מכוניות
5. הצבע הפופולרי ביותר

```python
class StatisticsManager:
    def __init__(self, db_manager):
        self.db_manager = db_manager
    
    def get_age_distribution(self):
        """Get age distribution of persons"""
        # TODO: implement
        pass
    
    def get_brand_distribution(self):
        """Get distribution of car brands"""
        # TODO: implement
        pass
```

---

## חלק 6: מטלה סופית - מערכת שלמה

### המטרה:
בנה מערכת ניהול מלאה עם תפריט אינטראקטיבי.

### דרישות:

1. **תפריט ראשי:**
```
=== מערכת ניהול אנשים ומכוניות ===
1. הוסף אדם חדש
2. הוסף מכונית חדשה
3. הצג כל האנשים
4. הצג כל המכוניות
5. חפש אדם לפי ID
6. הצג מכוניות של אדם
7. עדכן פרטי אדם
8. מחק אדם
9. ייצא לCSV
10. ייבא מCSV
11. סטטיסטיקות
0. יציאה
```

2. **Input Validation:**
   - וודא שכל הקלט תקין
   - טפל בשגיאות בצורה נאה
   - הצג הודעות ברורות למשתמש

3. **Error Handling:**
   - Try/Except לכל פעולות מסד נתונים
   - Try/Except לכל פעולות קבצים
   - הודעות שגיאה מפורטות

### קוד שלד למערכת המלאה:

```python
import sqlite3
import csv
from datetime import datetime

# TODO: Add all classes here (Person, Car, DatabaseManager, CSVManager, etc.)

class PersonCarManagementSystem:
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.db_manager.create_tables()
    
    def display_menu(self):
        """Display main menu"""
        print("\n" + "="*50)
        print("מערכת ניהול אנשים ומכוניות")
        print("="*50)
        print("1. הוסף אדם חדש")
        print("2. הוסף מכונית חדשה")
        print("3. הצג כל האנשים")
        print("4. הצג כל המכוניות")
        print("5. חפש אדם לפי ID")
        print("6. הצג מכוניות של אדם")
        print("7. עדכן פרטי אדם")
        print("8. מחק אדם")
        print("9. ייצא לCSV")
        print("10. ייבא מCSV")
        print("11. סטטיסטיקות")
        print("0. יציאה")
        print("="*50)
    
    def add_person(self):
        """Add new person"""
        # TODO: implement
        pass
    
    def add_car(self):
        """Add new car"""
        # TODO: implement
        pass
    
    def run(self):
        """Main loop"""
        while True:
            self.display_menu()
            choice = input("\nבחר אפשרות: ")
            # TODO: Handle all menu options
            if choice == "0":
                break

if __name__ == "__main__":
    system = PersonCarManagementSystem()
    system.run()
```

---

## דוגמת פתרון חלקי

הנה דוגמה לפתרון חלקי למחלקת `Person`:

```python
class Person:
    def __init__(self, person_id, name, age, email):
        self.person_id = person_id
        self.name = name
        self.age = age
        self.email = email
        self.cars = []
    
    def add_car(self, car):
        """Add a car to person's cars list"""
        self.cars.append(car)
        car.owner_id = self.person_id
    
    def get_cars_count(self):
        """Return the number of cars owned"""
        return len(self.cars)
    
    def __str__(self):
        """String representation of person"""
        return f"Person(ID: {self.person_id}, Name: {self.name}, Age: {self.age}, Email: {self.email}, Cars: {self.get_cars_count()})"
    
    def to_dict(self):
        """Convert person to dictionary"""
        return {
            'person_id': self.person_id,
            'name': self.name,
            'age': self.age,
            'email': self.email,
            'cars_count': self.get_cars_count()
        }
```

---

## טיפים והמלצות

### טיפים לעבודה עם SQLite3:
1. השתמש ב-`cursor.fetchone()` לשליפת רשומה בודדת
2. השתמש ב-`cursor.fetchall()` לשליפת כל הרשומות
3. תמיד בצע `commit()` אחרי פעולות INSERT/UPDATE/DELETE
4. השתמש ב-parameterized queries למניעת SQL Injection:
   ```python
   cursor.execute("SELECT * FROM persons WHERE person_id = ?", (person_id,))
   ```

### טיפים לעבודה עם CSV:
1. השתמש ב-`DictReader` ו-`DictWriter` לקריאה/כתיבה נוחה
2. תמיד השתמש ב-`with open()` לניהול נכון של קבצים
3. טפל ב-encoding: `open(file, 'r', encoding='utf-8')`

### טיפים ל-OOP:
1. שמור על encapsulation - השתמש ב-private attributes כשצריך
2. השתמש ב-`@property` decorators למתודות getter/setter
3. הוסף docstrings לכל המתודות
4. השתמש ב-inheritance כשיש קשר "is-a"
5. השתמש ב-composition כשיש קשר "has-a"

---

## שאלות לחשיבה

1. מה הקשר בין `Person` ל-`Car`? (one-to-many, many-to-many?)
2. איך תטפל במצב שבו רוצים למחוק אדם שיש לו מכוניות?
3. איך תוודא שלא ניתן להוסיף מכונית לאדם שלא קיים במסד?
4. איך תממש חיפוש מתקדם (לפי שם חלקי, טווח גילאים, וכו')?
5. איך תטפל בגיבוי ושחזור של מסד הנתונים?

---

## הערות סיום

תרגיל זה משלב מספר מושגים חשובים:
- ✅ Object-Oriented Programming
- ✅ Database Management (SQLite3)
- ✅ File Operations (CSV)
- ✅ Error Handling
- ✅ Data Validation
- ✅ CRUD Operations

בהצלחה! 🎯
