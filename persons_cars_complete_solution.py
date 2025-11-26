"""
Complete Solution Example - Persons and Cars Management System
OOP + SQLite3 + CSV
"""

import sqlite3
import csv
from datetime import datetime


# ========================================
# Part 1: Classes Definition
# ========================================

class Person:
    """Represents a person with personal details and car ownership"""
    
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
    
    def __repr__(self):
        return self.__str__()
    
    def to_dict(self):
        """Convert person to dictionary"""
        return {
            'person_id': self.person_id,
            'name': self.name,
            'age': self.age,
            'email': self.email,
            'cars_count': self.get_cars_count()
        }


class Car:
    """Represents a car with details and ownership"""
    
    def __init__(self, car_id, brand, model, year, color, owner_id=None):
        self.car_id = car_id
        self.brand = brand
        self.model = model
        self.year = year
        self.color = color
        self.owner_id = owner_id
    
    def get_age(self):
        """Calculate car age"""
        current_year = datetime.now().year
        return current_year - self.year
    
    def __str__(self):
        """String representation of car"""
        return f"Car(ID: {self.car_id}, {self.brand} {self.model} {self.year}, Color: {self.color}, Owner: {self.owner_id})"
    
    def __repr__(self):
        return self.__str__()
    
    def to_dict(self):
        """Convert car to dictionary"""
        return {
            'car_id': self.car_id,
            'brand': self.brand,
            'model': self.model,
            'year': self.year,
            'color': self.color,
            'owner_id': self.owner_id,
            'age': self.get_age()
        }


# ========================================
# Part 2: Database Manager
# ========================================

class DatabaseManager:
    """Manages all database operations for persons and cars"""
    
    def __init__(self, db_name='persons_cars.db'):
        """Initialize database connection"""
        self.db_name = db_name
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
    
    def create_tables(self):
        """Create persons and cars tables"""
        # Create persons table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS persons (
                person_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                email TEXT UNIQUE NOT NULL
            )
        ''')
        
        # Create cars table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS cars (
                car_id INTEGER PRIMARY KEY,
                brand TEXT NOT NULL,
                model TEXT NOT NULL,
                year INTEGER NOT NULL,
                color TEXT NOT NULL,
                owner_id INTEGER,
                FOREIGN KEY (owner_id) REFERENCES persons(person_id) ON DELETE CASCADE
            )
        ''')
        
        self.connection.commit()
        print("✅ Tables created successfully")
    
    def insert_person(self, person):
        """Insert a person into database"""
        try:
            self.cursor.execute('''
                INSERT INTO persons (person_id, name, age, email)
                VALUES (?, ?, ?, ?)
            ''', (person.person_id, person.name, person.age, person.email))
            self.connection.commit()
            print(f"✅ Person {person.name} added successfully")
            return True
        except sqlite3.IntegrityError as e:
            print(f"❌ Error: {e}")
            return False
    
    def insert_car(self, car):
        """Insert a car into database"""
        try:
            self.cursor.execute('''
                INSERT INTO cars (car_id, brand, model, year, color, owner_id)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (car.car_id, car.brand, car.model, car.year, car.color, car.owner_id))
            self.connection.commit()
            print(f"✅ Car {car.brand} {car.model} added successfully")
            return True
        except sqlite3.IntegrityError as e:
            print(f"❌ Error: {e}")
            return False
    
    def get_all_persons(self):
        """Get all persons from database"""
        self.cursor.execute('SELECT * FROM persons')
        rows = self.cursor.fetchall()
        persons = []
        for row in rows:
            person = Person(row[0], row[1], row[2], row[3])
            # Load cars for this person
            person.cars = self.get_cars_by_owner(person.person_id)
            persons.append(person)
        return persons
    
    def get_all_cars(self):
        """Get all cars from database"""
        self.cursor.execute('SELECT * FROM cars')
        rows = self.cursor.fetchall()
        cars = []
        for row in rows:
            car = Car(row[0], row[1], row[2], row[3], row[4], row[5])
            cars.append(car)
        return cars
    
    def get_person_by_id(self, person_id):
        """Get person by ID"""
        self.cursor.execute('SELECT * FROM persons WHERE person_id = ?', (person_id,))
        row = self.cursor.fetchone()
        if row:
            person = Person(row[0], row[1], row[2], row[3])
            person.cars = self.get_cars_by_owner(person.person_id)
            return person
        return None
    
    def get_cars_by_owner(self, owner_id):
        """Get all cars owned by a person"""
        self.cursor.execute('SELECT * FROM cars WHERE owner_id = ?', (owner_id,))
        rows = self.cursor.fetchall()
        cars = []
        for row in rows:
            car = Car(row[0], row[1], row[2], row[3], row[4], row[5])
            cars.append(car)
        return cars
    
    def update_person(self, person):
        """Update person details"""
        try:
            self.cursor.execute('''
                UPDATE persons 
                SET name = ?, age = ?, email = ?
                WHERE person_id = ?
            ''', (person.name, person.age, person.email, person.person_id))
            self.connection.commit()
            print(f"✅ Person {person.name} updated successfully")
            return True
        except sqlite3.IntegrityError as e:
            print(f"❌ Error: {e}")
            return False
    
    def delete_person(self, person_id):
        """Delete person from database"""
        # First delete all cars owned by this person
        self.cursor.execute('DELETE FROM cars WHERE owner_id = ?', (person_id,))
        # Then delete the person
        self.cursor.execute('DELETE FROM persons WHERE person_id = ?', (person_id,))
        self.connection.commit()
        print(f"✅ Person ID {person_id} deleted successfully")
    
    def find_persons_with_multiple_cars(self):
        """Find persons who own more than one car"""
        self.cursor.execute('''
            SELECT p.*, COUNT(c.car_id) as car_count
            FROM persons p
            JOIN cars c ON p.person_id = c.owner_id
            GROUP BY p.person_id
            HAVING car_count > 1
        ''')
        rows = self.cursor.fetchall()
        return rows
    
    def find_cars_older_than(self, year):
        """Find cars older than specified year"""
        self.cursor.execute('''
            SELECT * FROM cars WHERE year < ?
        ''', (year,))
        rows = self.cursor.fetchall()
        cars = []
        for row in rows:
            car = Car(row[0], row[1], row[2], row[3], row[4], row[5])
            cars.append(car)
        return cars
    
    def get_average_cars_per_person(self):
        """Calculate average cars per person"""
        self.cursor.execute('''
            SELECT AVG(car_count) FROM (
                SELECT COUNT(car_id) as car_count
                FROM cars
                GROUP BY owner_id
            )
        ''')
        result = self.cursor.fetchone()
        return result[0] if result[0] else 0
    
    def find_most_popular_brand(self):
        """Find the most popular car brand"""
        self.cursor.execute('''
            SELECT brand, COUNT(*) as count
            FROM cars
            GROUP BY brand
            ORDER BY count DESC
            LIMIT 1
        ''')
        result = self.cursor.fetchone()
        return result if result else None
    
    def get_persons_by_age_range(self, min_age, max_age):
        """Find persons in age range"""
        self.cursor.execute('''
            SELECT * FROM persons 
            WHERE age BETWEEN ? AND ?
        ''', (min_age, max_age))
        rows = self.cursor.fetchall()
        persons = []
        for row in rows:
            person = Person(row[0], row[1], row[2], row[3])
            persons.append(person)
        return persons
    
    def close(self):
        """Close database connection"""
        self.connection.close()
        print("✅ Database connection closed")


# ========================================
# Part 3: CSV Manager
# ========================================

class CSVManager:
    """Manages CSV import/export operations"""
    
    @staticmethod
    def export_persons_to_csv(persons, filename='persons.csv'):
        """Export persons list to CSV file"""
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as file:
                fieldnames = ['person_id', 'name', 'age', 'email']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                
                writer.writeheader()
                for person in persons:
                    writer.writerow({
                        'person_id': person.person_id,
                        'name': person.name,
                        'age': person.age,
                        'email': person.email
                    })
            print(f"✅ Persons exported to {filename}")
            return True
        except Exception as e:
            print(f"❌ Error exporting persons: {e}")
            return False
    
    @staticmethod
    def export_cars_to_csv(cars, filename='cars.csv'):
        """Export cars list to CSV file"""
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as file:
                fieldnames = ['car_id', 'brand', 'model', 'year', 'color', 'owner_id']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                
                writer.writeheader()
                for car in cars:
                    writer.writerow({
                        'car_id': car.car_id,
                        'brand': car.brand,
                        'model': car.model,
                        'year': car.year,
                        'color': car.color,
                        'owner_id': car.owner_id
                    })
            print(f"✅ Cars exported to {filename}")
            return True
        except Exception as e:
            print(f"❌ Error exporting cars: {e}")
            return False
    
    @staticmethod
    def import_persons_from_csv(filename='persons.csv'):
        """Import persons from CSV file"""
        persons = []
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    person = Person(
                        int(row['person_id']),
                        row['name'],
                        int(row['age']),
                        row['email']
                    )
                    persons.append(person)
            print(f"✅ {len(persons)} persons imported from {filename}")
            return persons
        except Exception as e:
            print(f"❌ Error importing persons: {e}")
            return []
    
    @staticmethod
    def import_cars_from_csv(filename='cars.csv'):
        """Import cars from CSV file"""
        cars = []
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    owner_id = int(row['owner_id']) if row['owner_id'] else None
                    car = Car(
                        int(row['car_id']),
                        row['brand'],
                        row['model'],
                        int(row['year']),
                        row['color'],
                        owner_id
                    )
                    cars.append(car)
            print(f"✅ {len(cars)} cars imported from {filename}")
            return cars
        except Exception as e:
            print(f"❌ Error importing cars: {e}")
            return []
    
    @staticmethod
    def export_full_report(db_manager, filename='full_report.csv'):
        """Export full report with persons and their cars"""
        try:
            persons = db_manager.get_all_persons()
            with open(filename, 'w', newline='', encoding='utf-8') as file:
                fieldnames = ['person_name', 'age', 'email', 'cars_count', 'car_brands']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                
                writer.writeheader()
                for person in persons:
                    brands = ', '.join([f"{car.brand} {car.model}" for car in person.cars])
                    writer.writerow({
                        'person_name': person.name,
                        'age': person.age,
                        'email': person.email,
                        'cars_count': person.get_cars_count(),
                        'car_brands': brands if brands else 'No cars'
                    })
            print(f"✅ Full report exported to {filename}")
            return True
        except Exception as e:
            print(f"❌ Error exporting report: {e}")
            return False


# ========================================
# Part 4: Statistics Manager
# ========================================

class StatisticsManager:
    """Manages statistical calculations and reports"""
    
    def __init__(self, db_manager):
        self.db_manager = db_manager
    
    def get_age_distribution(self):
        """Get age distribution of persons"""
        persons = self.db_manager.get_all_persons()
        ages = [p.age for p in persons]
        if ages:
            return {
                'min_age': min(ages),
                'max_age': max(ages),
                'avg_age': sum(ages) / len(ages),
                'total_persons': len(ages)
            }
        return None
    
    def get_brand_distribution(self):
        """Get distribution of car brands"""
        cars = self.db_manager.get_all_cars()
        brands = {}
        for car in cars:
            brands[car.brand] = brands.get(car.brand, 0) + 1
        return brands
    
    def get_color_distribution(self):
        """Get distribution of car colors"""
        cars = self.db_manager.get_all_cars()
        colors = {}
        for car in cars:
            colors[car.color] = colors.get(car.color, 0) + 1
        return colors
    
    def print_statistics(self):
        """Print comprehensive statistics"""
        print("\n" + "="*60)
        print("📊 STATISTICS REPORT")
        print("="*60)
        
        # Age distribution
        age_dist = self.get_age_distribution()
        if age_dist:
            print("\n👥 Persons Age Distribution:")
            print(f"   Total persons: {age_dist['total_persons']}")
            print(f"   Age range: {age_dist['min_age']} - {age_dist['max_age']}")
            print(f"   Average age: {age_dist['avg_age']:.1f}")
        
        # Brand distribution
        brand_dist = self.get_brand_distribution()
        if brand_dist:
            print("\n🚗 Car Brand Distribution:")
            for brand, count in sorted(brand_dist.items(), key=lambda x: x[1], reverse=True):
                print(f"   {brand}: {count} cars")
        
        # Color distribution
        color_dist = self.get_color_distribution()
        if color_dist:
            print("\n🎨 Car Color Distribution:")
            for color, count in sorted(color_dist.items(), key=lambda x: x[1], reverse=True):
                print(f"   {color}: {count} cars")
        
        # Average cars per person
        avg_cars = self.db_manager.get_average_cars_per_person()
        print(f"\n📈 Average cars per person: {avg_cars:.2f}")
        
        # Most popular brand
        popular_brand = self.db_manager.find_most_popular_brand()
        if popular_brand:
            print(f"\n⭐ Most popular brand: {popular_brand[0]} ({popular_brand[1]} cars)")
        
        print("="*60 + "\n")


# ========================================
# Part 5: Main Management System
# ========================================

class PersonCarManagementSystem:
    """Main system with interactive menu"""
    
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.db_manager.create_tables()
        self.stats_manager = StatisticsManager(self.db_manager)
    
    def display_menu(self):
        """Display main menu"""
        print("\n" + "="*60)
        print("🚗 מערכת ניהול אנשים ומכוניות")
        print("="*60)
        print("1.  הוסף אדם חדש")
        print("2.  הוסף מכונית חדשה")
        print("3.  הצג כל האנשים")
        print("4.  הצג כל המכוניות")
        print("5.  חפש אדם לפי ID")
        print("6.  הצג מכוניות של אדם")
        print("7.  עדכן פרטי אדם")
        print("8.  מחק אדם")
        print("9.  ייצא לCSV")
        print("10. ייבא מCSV")
        print("11. סטטיסטיקות")
        print("12. מצא אנשים עם מספר מכוניות")
        print("0.  יציאה")
        print("="*60)
    
    def add_person(self):
        """Add new person"""
        print("\n--- הוספת אדם חדש ---")
        try:
            person_id = int(input("מזהה: "))
            name = input("שם: ")
            age = int(input("גיל: "))
            email = input("אימייל: ")
            
            person = Person(person_id, name, age, email)
            self.db_manager.insert_person(person)
        except ValueError:
            print("❌ קלט לא תקין")
    
    def add_car(self):
        """Add new car"""
        print("\n--- הוספת מכונית חדשה ---")
        try:
            car_id = int(input("מזהה מכונית: "))
            brand = input("יצרן: ")
            model = input("דגם: ")
            year = int(input("שנה: "))
            color = input("צבע: ")
            owner_id = input("מזהה בעלים (או Enter לריק): ")
            owner_id = int(owner_id) if owner_id else None
            
            car = Car(car_id, brand, model, year, color, owner_id)
            self.db_manager.insert_car(car)
        except ValueError:
            print("❌ קלט לא תקין")
    
    def show_all_persons(self):
        """Show all persons"""
        print("\n--- כל האנשים ---")
        persons = self.db_manager.get_all_persons()
        if not persons:
            print("אין אנשים במערכת")
            return
        
        for person in persons:
            print(f"\n{person}")
            if person.cars:
                print("  מכוניות:")
                for car in person.cars:
                    print(f"    - {car.brand} {car.model} ({car.year})")
    
    def show_all_cars(self):
        """Show all cars"""
        print("\n--- כל המכוניות ---")
        cars = self.db_manager.get_all_cars()
        if not cars:
            print("אין מכוניות במערכת")
            return
        
        for car in cars:
            print(car)
    
    def search_person(self):
        """Search person by ID"""
        print("\n--- חיפוש אדם ---")
        try:
            person_id = int(input("מזהה אדם: "))
            person = self.db_manager.get_person_by_id(person_id)
            if person:
                print(f"\nנמצא: {person}")
                if person.cars:
                    print("מכוניות:")
                    for car in person.cars:
                        print(f"  - {car}")
            else:
                print("❌ אדם לא נמצא")
        except ValueError:
            print("❌ קלט לא תקין")
    
    def show_person_cars(self):
        """Show cars of a person"""
        print("\n--- מכוניות של אדם ---")
        try:
            owner_id = int(input("מזהה אדם: "))
            cars = self.db_manager.get_cars_by_owner(owner_id)
            if cars:
                print(f"\nמכוניות של אדם {owner_id}:")
                for car in cars:
                    print(f"  {car}")
            else:
                print("אין מכוניות לאדם זה")
        except ValueError:
            print("❌ קלט לא תקין")
    
    def update_person(self):
        """Update person details"""
        print("\n--- עדכון פרטי אדם ---")
        try:
            person_id = int(input("מזהה אדם: "))
            person = self.db_manager.get_person_by_id(person_id)
            if person:
                print(f"פרטים נוכחיים: {person}")
                name = input(f"שם חדש ({person.name}): ") or person.name
                age = input(f"גיל חדש ({person.age}): ")
                age = int(age) if age else person.age
                email = input(f"אימייל חדש ({person.email}): ") or person.email
                
                person.name = name
                person.age = age
                person.email = email
                self.db_manager.update_person(person)
            else:
                print("❌ אדם לא נמצא")
        except ValueError:
            print("❌ קלט לא תקין")
    
    def delete_person(self):
        """Delete person"""
        print("\n--- מחיקת אדם ---")
        try:
            person_id = int(input("מזהה אדם: "))
            confirm = input(f"האם למחוק אדם {person_id}? (yes/no): ")
            if confirm.lower() == 'yes':
                self.db_manager.delete_person(person_id)
        except ValueError:
            print("❌ קלט לא תקין")
    
    def export_to_csv(self):
        """Export data to CSV"""
        print("\n--- ייצוא לCSV ---")
        persons = self.db_manager.get_all_persons()
        cars = self.db_manager.get_all_cars()
        
        CSVManager.export_persons_to_csv(persons)
        CSVManager.export_cars_to_csv(cars)
        CSVManager.export_full_report(self.db_manager)
    
    def import_from_csv(self):
        """Import data from CSV"""
        print("\n--- ייבוא מCSV ---")
        print("1. ייבא אנשים")
        print("2. ייבא מכוניות")
        choice = input("בחר: ")
        
        if choice == '1':
            persons = CSVManager.import_persons_from_csv()
            for person in persons:
                self.db_manager.insert_person(person)
        elif choice == '2':
            cars = CSVManager.import_cars_from_csv()
            for car in cars:
                self.db_manager.insert_car(car)
    
    def show_statistics(self):
        """Show statistics"""
        self.stats_manager.print_statistics()
    
    def find_persons_with_multiple_cars(self):
        """Find persons with multiple cars"""
        print("\n--- אנשים עם מספר מכוניות ---")
        results = self.db_manager.find_persons_with_multiple_cars()
        if results:
            for row in results:
                print(f"{row[1]} (ID: {row[0]}) - {row[4]} מכוניות")
        else:
            print("לא נמצאו אנשים עם יותר ממכונית אחת")
    
    def run(self):
        """Main loop"""
        print("🎉 ברוכים הבאים למערכת ניהול אנשים ומכוניות!")
        
        while True:
            self.display_menu()
            choice = input("\nבחר אפשרות: ").strip()
            
            if choice == '1':
                self.add_person()
            elif choice == '2':
                self.add_car()
            elif choice == '3':
                self.show_all_persons()
            elif choice == '4':
                self.show_all_cars()
            elif choice == '5':
                self.search_person()
            elif choice == '6':
                self.show_person_cars()
            elif choice == '7':
                self.update_person()
            elif choice == '8':
                self.delete_person()
            elif choice == '9':
                self.export_to_csv()
            elif choice == '10':
                self.import_from_csv()
            elif choice == '11':
                self.show_statistics()
            elif choice == '12':
                self.find_persons_with_multiple_cars()
            elif choice == '0':
                print("\n👋 להתראות!")
                self.db_manager.close()
                break
            else:
                print("❌ אפשרות לא קיימת")


# ========================================
# Demo Function
# ========================================

def demo():
    """Demo function with sample data"""
    print("\n🎬 Running Demo with Sample Data...\n")
    
    # Create database manager
    db = DatabaseManager('demo_persons_cars.db')
    db.create_tables()
    
    # Create persons
    persons = [
        Person(1, "David Cohen", 35, "david@example.com"),
        Person(2, "Sarah Levi", 28, "sarah@example.com"),
        Person(3, "Yossi Abraham", 42, "yossi@example.com")
    ]
    
    # Create cars
    cars = [
        Car(1, "Toyota", "Corolla", 2020, "White", 1),
        Car(2, "Honda", "Civic", 2019, "Blue", 1),
        Car(3, "Mazda", "3", 2021, "Red", 2),
        Car(4, "Hyundai", "i30", 2022, "Black", 3),
        Car(5, "Kia", "Sportage", 2023, "Gray", 3)
    ]
    
    # Insert to database
    print("📝 Inserting data...")
    for person in persons:
        db.insert_person(person)
    
    for car in cars:
        db.insert_car(car)
    
    # Display all
    print("\n" + "="*60)
    all_persons = db.get_all_persons()
    print("👥 All Persons:")
    for person in all_persons:
        print(f"\n{person}")
        for car in person.cars:
            print(f"   └─ {car}")
    
    # Statistics
    stats = StatisticsManager(db)
    stats.print_statistics()
    
    # Export to CSV
    print("\n📤 Exporting to CSV...")
    CSVManager.export_persons_to_csv(all_persons, 'demo_persons.csv')
    CSVManager.export_cars_to_csv(db.get_all_cars(), 'demo_cars.csv')
    CSVManager.export_full_report(db, 'demo_full_report.csv')
    
    # Close database
    db.close()
    print("\n✅ Demo completed!\n")


# ========================================
# Main Entry Point
# ========================================

if __name__ == "__main__":
    print("Choose an option:")
    print("1. Run Demo")
    print("2. Run Management System")
    choice = input("Enter choice (1/2): ").strip()
    
    if choice == '1':
        demo()
    else:
        system = PersonCarManagementSystem()
        system.run()
