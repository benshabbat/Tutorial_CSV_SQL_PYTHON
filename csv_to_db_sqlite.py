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
    rows = csv.DictReader(file)
    
    for row in rows:
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