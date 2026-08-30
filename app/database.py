from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String

DATABASE_URL = "postgresql://fastapi_user:fastapi_pass@localhost:5432/fastapi_db"

engine = create_engine(DATABASE_URL)
metadata = MetaData()

# جدول الدورات
courses_table = Table(
    "courses",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("title", String(100), nullable=False),
    Column("description", String(255), nullable=True),
    Column("instructor", String(100), nullable=False),
)

# جدول الطلاب
students_table = Table(
    "students",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(100), nullable=False),
    Column("email", String(100), nullable=False),
    Column("age", Integer, nullable=False),
)

def init_db():
    metadata.create_all(engine)