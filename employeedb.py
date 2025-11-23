import mysql.connector 
from mysql.connector import Error 

class EmployeeDB:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        
    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host = self.host,
                username = self.user,
                password = self.password,
                database = self.database
            )
            
            if self.connection.is_connected():
                print("✓ Connected to MySQL")
       
        except Error as e:
            print(f"Error: {e}")    
        
        
        
emp = EmployeeDB("localhost","root","","employeeDB")

emp.connect()