import sqlite3
from abc import ABC, abstractmethod
from contextlib import closing

class BaseCRUD(ABC):
    def __init__(self, database_path, table_name):
        self.database_path = database_path
        self.table_name = table_name

class EmployeeCRUD(BaseCRUD):
    def __init__(self, database_path):
        super().__init__(database_path, "employees")
  
    def get_connection(self):
        return closing(sqlite3.connect(self.database_path))

    def insert(self, **kwargs):
        with self.get_connection() as connection:
            cursor = connection.cursor()
            columns = ', '.join(kwargs.keys())
            placeholders = ', '.join('?' for _ in kwargs)
            query = f"INSERT INTO {self.table_name} ({columns}) VALUES ({placeholders})"
            cursor.execute(query, tuple(kwargs.values()))
            connection.commit()
            return cursor.lastrowid

    def get(self, employee_id, id_column="employee_id"):
        with self.get_connection() as connection:
            cursor = connection.cursor()
            query = f"SELECT * FROM {self.table_name} WHERE {id_column}=?"
            cursor.execute(query, (employee_id,))
            return cursor.fetchone()

    def update(self, employee_id, id_column="employee_id", **kwargs):
        with self.get_connection() as connection:
            cursor = connection.cursor()
            columns = ', '.join(f"{key}=?" for key in kwargs)
            query = f"UPDATE {self.table_name} SET {columns} WHERE {id_column}=?"
            cursor.execute(query, (*kwargs.values(), employee_id))
            connection.commit()

    def delete(self, id, id_column="id"):
        with self.get_connection() as connection:
            cursor = connection.cursor()
            query = f"DELETE FROM {self.table_name} WHERE {id_column}=?"
            cursor.execute(query, (id,))
            connection.commit()

# Ma'lumot qo'shish
db_path = "sample-database.db"
emp_manager = EmployeeCRUD(db_path)

new_emp_id = emp_manager.insert(
    first_name="Mirzohid", 
    last_name="Xusainov", 
    email="mirzohid.dev@example.com", 
    phone_number="123456789",    
    hire_date="2024-05-22", 
    job_id=1,                    
    salary=5000, 
    manager_id=None,            
    department_id=1
)

print(f"Yangi xodim ID: {new_emp_id}")

employee = emp_manager.get(new_emp_id, id_column="employee_id")
print(f"Xodim ma'lumotlari: {employee}")

emp_manager.update(new_emp_id, id_column="employee_id", salary=5500)

#Update qilish
emp_manager.update(
    112,
    id_column="employee_id", 
    last_name="Aliyev",     
    salary=6000
)
print("Xodim ma'lumotlari yangilandi!")

# Delete qilish
emp_manager.delete(112, id_column="employee_id")
print("Xodim bazadan o'chirildi!")