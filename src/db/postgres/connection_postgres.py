import psycopg2

conn = psycopg2.connect(
    dbname="ExamDB",
    user="postgres",
    password="postgres",
    host="localhost",
    port="5432"
)

def get_db():
    return conn
