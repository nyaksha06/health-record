import pymysql

def connect_to_db():
    try:
        conn = pymysql.connect(
            host="localhost",
            user="root",
            password="your_new_password",
            database="ehr"
        )
        return conn
    except pymysql.MySQLError as e:
        print(f"Error connecting to MySQL: {e}")
        return None
    

def test_connection():
    connection = connect_to_db()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT DATABASE();")
        db = cursor.fetchone()
        print(f"Connected to database: {db[0]}")
        cursor.close()
        connection.close()
    else:
        print("Failed to connect to the database.")


if __name__ == "__main__":
    test_connection()    