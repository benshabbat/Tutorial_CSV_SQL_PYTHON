# מדריך Decorators ב-SQLModel

## תוכן עניינים
1. [מבוא ל-Decorators](#מבוא-ל-decorators)
2. [Validators](#validators)
3. [Computed Fields](#computed-fields)
4. [Property Decorators](#property-decorators)
5. [Event Listeners](#event-listeners)
6. [Custom Decorators](#custom-decorators)
7. [דוגמאות מתקדמות](#דוגמאות-מתקדמות)

---

## מבוא ל-Decorators

Decorators הם דרך לשנות או להוסיף פונקציונליות למחלקות ופונקציות. ב-SQLModel משתמשים ב-decorators מ-Pydantic.

### התקנה

```bash
pip install sqlmodel
pip install pydantic
```

---

## Validators

### 1. Field Validator - בדיקת שדה בודד

```python
from sqlmodel import SQLModel, Field
from pydantic import field_validator, ValidationError
from typing import Optional

class Employee(SQLModel, table=True):
    """עובד עם validations"""
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str
    age: int
    salary: float
    
    @field_validator('name')
    @classmethod
    def validate_name(cls, value: str) -> str:
        """בדיקת שם - לפחות 2 מילים"""
        if len(value.strip().split()) < 2:
            raise ValueError('שם חייב להכיל לפחות שם פרטי ושם משפחה')
        return value.strip().title()
    
    @field_validator('email')
    @classmethod
    def validate_email(cls, value: str) -> str:
        """בדיקת אימייל"""
        if '@' not in value or '.' not in value:
            raise ValueError('אימייל לא תקין')
        return value.lower()
    
    @field_validator('age')
    @classmethod
    def validate_age(cls, value: int) -> int:
        """בדיקת גיל"""
        if value < 18:
            raise ValueError('גיל חייב להיות לפחות 18')
        if value > 120:
            raise ValueError('גיל לא יכול להיות מעל 120')
        return value
    
    @field_validator('salary')
    @classmethod
    def validate_salary(cls, value: float) -> float:
        """בדיקת משכורת"""
        if value < 0:
            raise ValueError('משכורת לא יכולה להיות שלילית')
        return round(value, 2)

# שימוש
try:
    emp1 = Employee(name="ישראל ישראלי", email="israel@example.com", 
                    age=30, salary=15000.50)
    print(f"✓ עובד נוצר: {emp1.name}")
except ValidationError as e:
    print(f"✗ שגיאה: {e}")

try:
    emp2 = Employee(name="ישראל", email="bad-email", age=15, salary=-1000)
except ValidationError as e:
    print(f"✗ שגיאות: {e.error_count()} שגיאות")
    for error in e.errors():
        print(f"  - {error['loc'][0]}: {error['msg']}")
```

### 2. Multiple Field Validator - בדיקת מספר שדות

```python
from pydantic import field_validator

class Product(SQLModel, table=True):
    """מוצר עם validations"""
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: str
    price: float
    discount_price: Optional[float] = None
    stock: int
    
    @field_validator('name', 'description')
    @classmethod
    def clean_text(cls, value: str) -> str:
        """ניקוי טקסט - הסרת רווחים מיותרים"""
        return ' '.join(value.split())
    
    @field_validator('price', 'discount_price')
    @classmethod
    def validate_prices(cls, value: Optional[float]) -> Optional[float]:
        """בדיקת מחירים"""
        if value is not None:
            if value < 0:
                raise ValueError('מחיר לא יכול להיות שלילי')
            return round(value, 2)
        return value
    
    @field_validator('stock')
    @classmethod
    def validate_stock(cls, value: int) -> int:
        """בדיקת מלאי"""
        if value < 0:
            raise ValueError('מלאי לא יכול להיות שלילי')
        return value

# שימוש
product = Product(
    name="  מחשב נייד  ",
    description="מחשב   נייד   חזק",
    price=3999.999,
    discount_price=3499.99,
    stock=10
)
print(f"מוצר: {product.name}")
print(f"מחיר: {product.price}")
```

### 3. Model Validator - בדיקת המודל כולו

```python
from pydantic import model_validator

class Order(SQLModel, table=True):
    """הזמנה עם בדיקות כלליות"""
    id: Optional[int] = Field(default=None, primary_key=True)
    product_name: str
    quantity: int
    price: float
    discount: float = 0
    total: Optional[float] = None
    
    @model_validator(mode='after')
    def calculate_total(self):
        """חישוב סכום כולל אחרי יצירת המודל"""
        subtotal = self.price * self.quantity
        discount_amount = subtotal * (self.discount / 100)
        self.total = round(subtotal - discount_amount, 2)
        return self
    
    @model_validator(mode='after')
    def validate_discount(self):
        """בדיקת הנחה"""
        if self.discount < 0 or self.discount > 100:
            raise ValueError('הנחה חייבת להיות בין 0 ל-100')
        return self

# שימוש
order = Order(
    product_name="מקלדת",
    quantity=3,
    price=150.00,
    discount=10
)
print(f"הזמנה: {order.product_name}")
print(f"כמות: {order.quantity} x {order.price} ₪")
print(f"הנחה: {order.discount}%")
print(f"סה\"כ: {order.total} ₪")
```

---

## Computed Fields

### 1. Computed Field - שדה מחושב

```python
from pydantic import computed_field

class Student(SQLModel, table=True):
    """תלמיד עם שדות מחושבים"""
    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str
    last_name: str
    grade_math: float = Field(ge=0, le=100)
    grade_english: float = Field(ge=0, le=100)
    grade_science: float = Field(ge=0, le=100)
    
    @computed_field
    @property
    def full_name(self) -> str:
        """שם מלא"""
        return f"{self.first_name} {self.last_name}"
    
    @computed_field
    @property
    def average_grade(self) -> float:
        """ממוצע ציונים"""
        return round((self.grade_math + self.grade_english + self.grade_science) / 3, 2)
    
    @computed_field
    @property
    def passed(self) -> bool:
        """האם עבר"""
        return self.average_grade >= 60

# שימוש
student = Student(
    first_name="דני",
    last_name="כהן",
    grade_math=85,
    grade_english=90,
    grade_science=78
)

print(f"שם: {student.full_name}")
print(f"ממוצע: {student.average_grade}")
print(f"סטטוס: {'עבר ✓' if student.passed else 'נכשל ✗'}")
```

### 2. Computed Field עם Logic מורכב

```python
from datetime import datetime
from pydantic import computed_field

class BankAccount(SQLModel, table=True):
    """חשבון בנק עם שדות מחושבים"""
    id: Optional[int] = Field(default=None, primary_key=True)
    account_number: str
    balance: float
    credit_limit: float = 0
    interest_rate: float = 0.02  # 2%
    
    @computed_field
    @property
    def available_balance(self) -> float:
        """יתרה זמינה (כולל אשראי)"""
        return self.balance + self.credit_limit
    
    @computed_field
    @property
    def is_overdrawn(self) -> bool:
        """האם בחריגה"""
        return self.balance < 0
    
    @computed_field
    @property
    def monthly_interest(self) -> float:
        """ריבית חודשית"""
        if self.balance > 0:
            return round(self.balance * (self.interest_rate / 12), 2)
        return 0
    
    @computed_field
    @property
    def status(self) -> str:
        """סטטוס חשבון"""
        if self.balance < 0:
            return "חריגה"
        elif self.balance < 1000:
            return "יתרה נמוכה"
        elif self.balance < 10000:
            return "רגיל"
        else:
            return "יתרה גבוהה"

# שימוש
account = BankAccount(
    account_number="123-456-789",
    balance=5000,
    credit_limit=2000,
    interest_rate=0.03
)

print(f"חשבון: {account.account_number}")
print(f"יתרה: {account.balance} ₪")
print(f"יתרה זמינה: {account.available_balance} ₪")
print(f"סטטוס: {account.status}")
print(f"ריבית חודשית: {account.monthly_interest} ₪")
```

---

## Property Decorators

### 1. Property - קריאה וכתיבה

```python
class Temperature(SQLModel, table=True):
    """טמפרטורה עם המרה אוטומטית"""
    id: Optional[int] = Field(default=None, primary_key=True)
    location: str
    _celsius: float = Field(default=0, alias="celsius")
    
    @property
    def celsius(self) -> float:
        """טמפרטורה בצלזיוס"""
        return self._celsius
    
    @celsius.setter
    def celsius(self, value: float):
        """הגדרת טמפרטורה בצלזיוס"""
        self._celsius = round(value, 1)
    
    @property
    def fahrenheit(self) -> float:
        """טמפרטורה בפרנהייט"""
        return round((self._celsius * 9/5) + 32, 1)
    
    @fahrenheit.setter
    def fahrenheit(self, value: float):
        """הגדרת טמפרטורה בפרנהייט"""
        self._celsius = round((value - 32) * 5/9, 1)
    
    @property
    def kelvin(self) -> float:
        """טמפרטורה בקלווין"""
        return round(self._celsius + 273.15, 1)

# שימוש
temp = Temperature(location="תל אביב", celsius=25)
print(f"מיקום: {temp.location}")
print(f"צלזיוס: {temp.celsius}°C")
print(f"פרנהייט: {temp.fahrenheit}°F")
print(f"קלווין: {temp.kelvin}K")

# שינוי דרך פרנהייט
temp.fahrenheit = 86
print(f"\nאחרי שינוי ל-86°F:")
print(f"צלזיוס: {temp.celsius}°C")
```

---

## Event Listeners

### 1. Before/After Validators

```python
from datetime import datetime
from pydantic import field_validator, model_validator

class Post(SQLModel, table=True):
    """פוסט בבלוג עם event handlers"""
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content: str
    author: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    view_count: int = 0
    
    @field_validator('title', mode='before')
    @classmethod
    def title_before(cls, value):
        """טיפול בכותרת לפני validation"""
        if isinstance(value, str):
            return value.strip()
        return value
    
    @field_validator('content', mode='after')
    @classmethod
    def content_after(cls, value):
        """טיפול בתוכן אחרי validation"""
        # הוספת נקודה בסוף אם חסרה
        if value and not value.endswith('.'):
            return value + '.'
        return value
    
    @model_validator(mode='before')
    @classmethod
    def set_timestamps(cls, values):
        """הגדרת זמנים לפני יצירת המודל"""
        now = str(datetime.now())
        if not values.get('created_at'):
            values['created_at'] = now
        values['updated_at'] = now
        return values

# שימוש
post = Post(
    title="  המדריך הטוב ביותר לPython  ",
    content="זהו מדריך מצוין ללימוד Python",
    author="דני כהן"
)

print(f"כותרת: {post.title}")
print(f"תוכן: {post.content}")
print(f"נוצר: {post.created_at}")
```

### 2. Custom Event System

```python
from typing import Callable, Dict, List

class EventManager:
    """מנהל אירועים"""
    _listeners: Dict[str, List[Callable]] = {}
    
    @classmethod
    def on(cls, event: str):
        """Decorator לרישום listener"""
        def decorator(func: Callable):
            if event not in cls._listeners:
                cls._listeners[event] = []
            cls._listeners[event].append(func)
            return func
        return decorator
    
    @classmethod
    def emit(cls, event: str, *args, **kwargs):
        """הפעלת כל ה-listeners של אירוע"""
        if event in cls._listeners:
            for listener in cls._listeners[event]:
                listener(*args, **kwargs)

class User(SQLModel, table=True):
    """משתמש עם מערכת אירועים"""
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    email: str
    is_active: bool = True
    login_count: int = 0
    
    def login(self):
        """התחברות משתמש"""
        self.login_count += 1
        EventManager.emit('user:login', self)
    
    def logout(self):
        """התנתקות משתמש"""
        EventManager.emit('user:logout', self)
    
    @model_validator(mode='after')
    def user_created(self):
        """אחרי יצירת משתמש"""
        EventManager.emit('user:created', self)
        return self

# רישום listeners
@EventManager.on('user:created')
def on_user_created(user: User):
    print(f"✓ משתמש חדש נוצר: {user.username}")

@EventManager.on('user:login')
def on_user_login(user: User):
    print(f"✓ התחברות: {user.username} (פעם #{user.login_count})")

@EventManager.on('user:logout')
def on_user_logout(user: User):
    print(f"✓ התנתקות: {user.username}")

# שימוש
user = User(username="israeli", email="israeli@example.com")
user.login()
user.login()
user.logout()
```

---

## Custom Decorators

### 1. Logging Decorator

```python
from functools import wraps
from datetime import datetime

def log_action(action_name: str):
    """Decorator לתיעוד פעולות"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(f"[{datetime.now().strftime('%H:%M:%S')}] {action_name} - התחיל")
            try:
                result = func(*args, **kwargs)
                print(f"[{datetime.now().strftime('%H:%M:%S')}] {action_name} - הצליח ✓")
                return result
            except Exception as e:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] {action_name} - נכשל ✗: {e}")
                raise
        return wrapper
    return decorator

class Invoice(SQLModel, table=True):
    """חשבונית עם logging"""
    id: Optional[int] = Field(default=None, primary_key=True)
    customer_name: str
    amount: float
    is_paid: bool = False
    
    @log_action("תשלום חשבונית")
    def pay(self):
        """תשלום חשבונית"""
        if self.is_paid:
            raise ValueError("החשבונית כבר שולמה")
        self.is_paid = True
        return True
    
    @log_action("ביטול תשלום")
    def cancel_payment(self):
        """ביטול תשלום"""
        if not self.is_paid:
            raise ValueError("החשבונית לא שולמה")
        self.is_paid = False
        return True

# שימוש
invoice = Invoice(customer_name="ישראל ישראלי", amount=1500)
invoice.pay()
try:
    invoice.pay()  # ינסה לשלם שוב
except ValueError as e:
    print(f"שגיאה: {e}")
```

### 2. Validation Decorator

```python
def validate_positive(field_name: str):
    """Decorator לבדיקת ערך חיובי"""
    def decorator(func):
        @wraps(func)
        def wrapper(self, value):
            if value <= 0:
                raise ValueError(f"{field_name} חייב להיות חיובי")
            return func(self, value)
        return wrapper
    return decorator

def validate_range(min_val: float, max_val: float):
    """Decorator לבדיקת טווח"""
    def decorator(func):
        @wraps(func)
        def wrapper(self, value):
            if not min_val <= value <= max_val:
                raise ValueError(f"ערך חייב להיות בין {min_val} ל-{max_val}")
            return func(self, value)
        return wrapper
    return decorator

class Score(SQLModel, table=True):
    """ציון עם decorators מותאמים"""
    id: Optional[int] = Field(default=None, primary_key=True)
    student_name: str
    _score: float = Field(default=0, alias="score")
    
    @property
    def score(self) -> float:
        return self._score
    
    @score.setter
    @validate_range(0, 100)
    @validate_positive("ציון")
    def score(self, value: float):
        self._score = value

# שימוש
score = Score(student_name="דני")
score.score = 85
print(f"ציון: {score.score}")

try:
    score.score = 150  # מעל הטווח
except ValueError as e:
    print(f"שגיאה: {e}")
```

---

## דוגמאות מתקדמות

### 1. מערכת שלמה עם כל סוגי ה-Decorators

```python
from datetime import datetime
from pydantic import field_validator, model_validator, computed_field
from typing import Optional

class Transaction(SQLModel, table=True):
    """טרנזקציה בנקאית מלאה"""
    id: Optional[int] = Field(default=None, primary_key=True)
    account_number: str
    amount: float
    transaction_type: str  # "deposit" או "withdrawal"
    description: Optional[str] = None
    created_at: Optional[str] = None
    processed: bool = False
    
    # Field Validators
    @field_validator('account_number')
    @classmethod
    def validate_account(cls, value: str) -> str:
        """בדיקת מספר חשבון"""
        value = value.strip().replace('-', '')
        if not value.isdigit() or len(value) != 9:
            raise ValueError('מספר חשבון לא תקין')
        return f"{value[:3]}-{value[3:6]}-{value[6:]}"
    
    @field_validator('amount')
    @classmethod
    def validate_amount(cls, value: float) -> float:
        """בדיקת סכום"""
        if value <= 0:
            raise ValueError('סכום חייב להיות חיובי')
        return round(value, 2)
    
    @field_validator('transaction_type')
    @classmethod
    def validate_type(cls, value: str) -> str:
        """בדיקת סוג טרנזקציה"""
        allowed = ['deposit', 'withdrawal']
        if value not in allowed:
            raise ValueError(f'סוג טרנזקציה חייב להיות: {", ".join(allowed)}')
        return value
    
    # Model Validator
    @model_validator(mode='before')
    @classmethod
    def set_created_at(cls, values):
        """הגדרת זמן יצירה"""
        if not values.get('created_at'):
            values['created_at'] = str(datetime.now())
        return values
    
    # Computed Fields
    @computed_field
    @property
    def formatted_amount(self) -> str:
        """סכום מעוצב"""
        return f"{self.amount:,.2f} ₪"
    
    @computed_field
    @property
    def type_hebrew(self) -> str:
        """סוג בעברית"""
        types = {
            'deposit': 'הפקדה',
            'withdrawal': 'משיכה'
        }
        return types.get(self.transaction_type, 'לא ידוע')
    
    @computed_field
    @property
    def status(self) -> str:
        """סטטוס"""
        return "✓ בוצע" if self.processed else "⏳ ממתין"
    
    # Methods
    @log_action("עיבוד טרנזקציה")
    def process(self):
        """עיבוד טרנזקציה"""
        if self.processed:
            raise ValueError("הטרנזקציה כבר עובדה")
        self.processed = True
        EventManager.emit('transaction:processed', self)

# Event Listeners
@EventManager.on('transaction:processed')
def on_transaction_processed(transaction: Transaction):
    print(f"✓ טרנזקציה עובדה: {transaction.formatted_amount} - {transaction.type_hebrew}")

# שימוש
try:
    trans = Transaction(
        account_number="123456789",
        amount=1500.50,
        transaction_type="deposit",
        description="הפקדה ראשונית"
    )
    
    print(f"חשבון: {trans.account_number}")
    print(f"סכום: {trans.formatted_amount}")
    print(f"סוג: {trans.type_hebrew}")
    print(f"סטטוס: {trans.status}")
    print(f"תיאור: {trans.description}")
    
    trans.process()
    
except ValidationError as e:
    for error in e.errors():
        print(f"✗ {error['loc'][0]}: {error['msg']}")
```

### 2. מערכת Caching עם Decorator

```python
from functools import lru_cache
from typing import Dict, Any

class CachedModel(SQLModel):
    """Base model עם caching"""
    
    @staticmethod
    def cache_method(maxsize=128):
        """Decorator לcaching של methods"""
        def decorator(func):
            cached_func = lru_cache(maxsize=maxsize)(func)
            @wraps(func)
            def wrapper(*args, **kwargs):
                return cached_func(*args, **kwargs)
            wrapper.cache_clear = cached_func.cache_clear
            wrapper.cache_info = cached_func.cache_info
            return wrapper
        return decorator

class Product(CachedModel, table=True):
    """מוצר עם caching"""
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    price: float
    category: str
    
    @CachedModel.cache_method(maxsize=100)
    def calculate_discount(self, percentage: float) -> float:
        """חישוב הנחה - cached"""
        print(f"מחשב הנחה עבור {self.name}...")
        return round(self.price * (1 - percentage / 100), 2)
    
    @computed_field
    @property
    def final_price(self) -> float:
        """מחיר סופי עם הנחה"""
        return self.calculate_discount(10)  # 10% הנחה

# שימוש
product = Product(
    name="מקלדת",
    price=200,
    category="אלקטרוניקה"
)

print(f"מחיר: {product.price}")
print(f"מחיר עם הנחה: {product.calculate_discount(10)}")  # יחשב
print(f"מחיר עם הנחה: {product.calculate_discount(10)}")  # מcache
print(f"Cache info: {product.calculate_discount.cache_info()}")
```

### 3. Decorator למניעת SQL Injection

```python
import re

def sanitize_input(func):
    """Decorator למניעת SQL injection"""
    @wraps(func)
    def wrapper(self, value):
        if isinstance(value, str):
            # הסרת תווים מסוכנים
            dangerous_patterns = [
                r"(\bOR\b|\bAND\b).*=",  # OR/AND injection
                r"[;']",  # semicolon או quote
                r"--",  # SQL comments
                r"/\*.*\*/",  # Multi-line comments
            ]
            
            for pattern in dangerous_patterns:
                if re.search(pattern, value, re.IGNORECASE):
                    raise ValueError("קלט לא חוקי - נמצאו תווים מסוכנים")
        
        return func(self, value)
    return wrapper

class SafeUser(SQLModel, table=True):
    """משתמש מאובטח"""
    id: Optional[int] = Field(default=None, primary_key=True)
    _username: str = Field(alias="username")
    _email: str = Field(alias="email")
    
    @property
    def username(self) -> str:
        return self._username
    
    @username.setter
    @sanitize_input
    def username(self, value: str):
        self._username = value
    
    @property
    def email(self) -> str:
        return self._email
    
    @email.setter
    @sanitize_input
    def email(self, value: str):
        self._email = value

# שימוש
try:
    user = SafeUser(username="israeli", email="test@example.com")
    print(f"✓ משתמש: {user.username}")
    
    # ניסיון SQL injection
    user.username = "admin' OR '1'='1"
except ValueError as e:
    print(f"✗ {e}")
```

---

## סיכום

### Decorators עיקריים ב-SQLModel:

1. **`@field_validator`** - בדיקת שדה בודד
2. **`@model_validator`** - בדיקת המודל כולו
3. **`@computed_field`** - שדה מחושב
4. **`@property`** - property מותאם
5. **Custom decorators** - decorators מותאמים אישית

### Best Practices:

✅ השתמש ב-`field_validator` לvalidation פשוטה של שדה בודד  
✅ השתמש ב-`model_validator` לvalidation שדורשת מספר שדות  
✅ השתמש ב-`computed_field` לערכים שמחושבים משדות אחרים  
✅ צור custom decorators לפונקציונליות שחוזרת על עצמה  
✅ הוסף logging לפעולות חשובות  
✅ תמיד נקה ו-sanitize קלט מהמשתמש  

### מקורות נוספים:

- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)
- [Pydantic Validators](https://docs.pydantic.dev/latest/concepts/validators/)
- [Python Decorators Guide](https://realpython.com/primer-on-python-decorators/)

---

**נוצר ב-2025 | מדריך מקיף ל-Decorators ב-SQLModel** 🐍
