from datetime import datetime, UTC
import database
import psycopg2
from psycopg2.extras import RealDictCursor


class ModelBase:
    def __init__(self, id=None, created_at=datetime.now(UTC), modified_at=datetime.now(UTC), active=True):
        self.id = id
        self.created_at = created_at
        self.modified_at = modified_at
        self.active = active


class Department(ModelBase):

    def __init__(self, id=None, created_at=datetime.now(UTC), modified_at=datetime.now(UTC), active=True, name=None):
        super().__init__(id=id, created_at=created_at, modified_at=modified_at, active=active)
        self.name = name

    @staticmethod
    def get_all():
        departments = []
        cursor = None
        try:
            with database.open_connection() as connection:  # abre a conexão com o banco de dados
                with connection.cursor(
                        cursor_factory=RealDictCursor) as cursor:  # abre o cursor que é um objeto da biblioteca
                    # para trabalhar com os registros do
                    # banco de dados. Vale ressaltar que o
                    # cursor_factory=RealDictCursor é para
                    # que os resultados venham como dicionário
                    cursor.execute(f'select * from department')  # executa o comando de consulta no banco de dados
                    rows = cursor.fetchall()  # fetchall permite que tragamos todos os registros da tabela

                    for row in rows:
                        d = Department(**row)  # aqui usamos o ** para pegar o dicionário e passar os parâmetros para
                        # o construtor da classe de departamento, para transformar o dicionário em
                        # nosso objeto
                        departments.append(d)  # adiciona na lista de retorno

        except psycopg2.DatabaseError as e:
            print(f'Erro ao realizar consulta {e}')

        return departments

    def save(self):
        try:
            with database.open_connection() as connection:
                with connection.cursor() as cursor:
                    command = f"insert into department (name) values ('{self.name}')"
                    cursor.execute(command)
        except psycopg2.DatabaseError as e:
            print(f'Erro ao inserir os dados {e}')

class Employee(ModelBase):

    def __init__(self, id=None, created_at=datetime.now(UTC), modified_at=datetime.now(UTC), active=True,
                 name=None, salary=None, admission_date=None, birth_date=None, gender=None,
                 id_department=None, id_marital_status=None, id_district=None):
        super().__init__(id=id, created_at=created_at, modified_at=modified_at, active=active)
        self.name = name
        self.salary = float(salary) if salary is not None else 0.0
        self.admission_date = admission_date
        self.birth_date = birth_date
        self.gender = gender
        self.id_department = id_department
        self.id_marital_status = id_marital_status
        self.id_district = id_district

    @staticmethod
    def get_all():
        employees = []
        cursor = None
        try:
            with database.open_connection() as connection:
                with connection.cursor(cursor_factory=RealDictCursor) as cursor:
                    cursor.execute(f'select * from employee')
                    rows = cursor.fetchall()

                    for row in rows:
                        e = Employee(**row)
                        employees.append(e)

        except psycopg2.DatabaseError as e:
            print(f'Erro ao realizar consulta {e}')

        return employees

    def save(self):
        try:
            with database.open_connection() as connection:
                with connection.cursor() as cursor:
                    command = f"""
                    insert into employee (name, salary, admission_date, birth_date, gender, id_department, id_marital_status, id_district)
                    values ('{self.name}', {self.salary}, '{self.admission_date}', '{self.birth_date}', '{self.gender}', {self.id_department}, {self.id_marital_status}, {self.id_district})
                    """
                    cursor.execute(command)
        except psycopg2.DatabaseError as e:
            print(f'Erro ao inserir os dados {e}')


class Supplier(ModelBase):

    def __init__(self, id=None, created_at=datetime.now(UTC), modified_at=datetime.now(UTC), active=True, name=None, legal_document=None):
        super().__init__(id=id, created_at=created_at, modified_at=modified_at, active=active)
        self.name = name
        self.legal_document = legal_document

    @staticmethod
    def get_all():
        suppliers = []
        cursor = None
        try:
            with database.open_connection() as connection:
                with connection.cursor(
                        cursor_factory=RealDictCursor) as cursor:
                    cursor.execute(f'select * from supplier')
                    rows = cursor.fetchall()

                    for row in rows:
                        s = Supplier(**row)
                        suppliers.append(s)

        except psycopg2.DatabaseError as e:
            print(f'Erro ao realizar consulta {e}')

        return suppliers

    def save(self):
        try:
            with database.open_connection() as connection:
                with connection.cursor() as cursor:
                    command = f"insert into supplier (name, legal_document) values ('{self.name}', '{self.legal_document}')"
                    cursor.execute(command)
        except psycopg2.DatabaseError as e:
            print(f'Erro ao inserir os dados {e}')