# utils/authentication.py

import bcrypt
from db import connect_to_db as get_db_connection

# def hash_password(plain_password):
#     """
#     Hashes a plain-text password using bcrypt.
#     """
#     # Generate a salt
#     salt = bcrypt.gensalt()
#     # Hash the password
#     hashed = bcrypt.hashpw(plain_password.encode('utf-8'), salt)
#     return hashed

def verify_password(plain_password, hashed_password):
    """
    Verifies a plain-text password against the hashed password.
    """
    return plain_password == hashed_password

def authenticate_user(username, password):
    """
    Authenticates a user by username and password.
    Returns user information if authenticated, else None.
    """
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        query = "SELECT * FROM Users WHERE Username = %s"
        cursor.execute(query, (username,))
        user = cursor.fetchone()
        cursor.close()
        connection.close()
        if user and verify_password(password, user[2]):
            # Fetch additional details based on role
            role = user[3]
            if role == 'Patient':
                connection = get_db_connection()
                cursor = connection.cursor()
                query = "SELECT * FROM Patients WHERE UserID = %s"
                cursor.execute(query, (user[1],))
                patient = cursor.fetchone()
                cursor.close()
                connection.close()
                if patient:
                    user.update(patient)
            elif role == 'Doctor':
                connection = get_db_connection()
                cursor = connection.cursor()
                query = "SELECT * FROM Doctors WHERE UserID = %s"
                cursor.execute(query, (user[1],))
                doctor = cursor.fetchone()
                cursor.close()
                connection.close()
                if doctor:
                    user.update(doctor)
            return user
    return None



# def register_user(username, plain_password, role):
#     """
#     Registers a new user with the given username, password, and role.
#     Returns True if successful, False otherwise.
#     """
#     connection = get_db_connection()
#     if connection:
#         cursor = connection.cursor()
#         try:
#             query = "INSERT INTO Users (Username, Password, Role) VALUES (%s, %s, %s)"
#             cursor.execute(query, (username, plain_password, role))
#             connection.commit()
#             return True
#         except Exception as e:
#             print(f"Error during user registration: {e}")
#             connection.rollback()
#             return False
#         finally:
#             cursor.close()
#             connection.close()
#     return False



# utils/authentication.py (Updated)

def register_patient(username, plain_password, full_name, dob, contact_number, email, address):
    """
    Registers a new patient.
    Returns True if successful, False otherwise.
    """
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        try:
            # Insert into Users table
            
            user_query = "INSERT INTO Users (Username, Password, Role) VALUES (%s, %s, %s)"
            cursor.execute(user_query, (username, plain_password, 'Patient'))
            user_id = cursor.lastrowid

            # Insert into Patients table
            patient_query = """
                INSERT INTO Patients (UserID, FullName, DOB, ContactNumber, Email, Address)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(patient_query, (user_id, full_name, dob, contact_number, email, address))
            connection.commit()
            return True
        except Exception as e:
            print(f"Error during patient registration: {e}")
            connection.rollback()
            return False
        finally:
            cursor.close()
            connection.close()
    return False

def register_doctor(username, plain_password, full_name, specialty, contact_number, email, consultation_fee):
    """
    Registers a new doctor.
    Returns True if successful, False otherwise.
    """
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        try:
            # Insert into Users table
            
            user_query = "INSERT INTO Users (Username, Password, Role) VALUES (%s, %s, %s)"
            cursor.execute(user_query, (username, plain_password, 'Doctor'))
            user_id = cursor.lastrowid

            # Insert into Doctors table
            doctor_query = """
                INSERT INTO Doctors (UserID, FullName, Specialty, ContactNumber, Email, ConsultationFee)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(doctor_query, (user_id, full_name, specialty, contact_number, email, consultation_fee))
            connection.commit()
            return True
        except Exception as e:
            print(f"Error during doctor registration: {e}")
            connection.rollback()
            return False
        finally:
            cursor.close()
            connection.close()
    return False
