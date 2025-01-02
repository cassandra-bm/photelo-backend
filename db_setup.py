import psycopg2

def setup_database():
    conn = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="photelo",
        password="photelo"
    )
    cursor = conn.cursor()

    with open('schema.sql', 'r') as file:
        cursor.execute(file.read())

    conn.commit()
    cursor.close()
    conn.close()

if __name__ == '__main__':
    setup_database()