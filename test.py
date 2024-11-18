import streamlit as st
import pymysql

import bcrypt


def connect_to_db():
    try:
        conn = pymysql.connect(
            host="localhost",
            user="root",
            password="your_new_password",
            database="ehr01"
        )
        return conn
    except pymysql.MySQLError as e:
        print(f"Error connecting to MySQL: {e}")
        return None


# Hash Password
def hash_password(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)


# Verify Password
def verify_password(password, hashed):
    # Check if hashed password is valid
    if not hashed:
        print("No hashed password provided.")
        return False
    
    # Ensure the hash is in bytes format
    hashed = hashed.encode('utf-8') if isinstance(hashed, str) else hashed

    try:
        return bcrypt.checkpw(password.encode('utf-8'), hashed)
    except ValueError as e:
        print(f"Error verifying password: {e}")
        return False





def sign_up_patient(first_name, last_name, dob, address, phone, email, password):
    conn = connect_to_db()
    cursor = conn.cursor()
    hashed_pw = hash_password(password)  # Hash the password for security

    query = """
        INSERT INTO Patient (FirstName, LastName, DOB, Address, PhoneNumber, Email, Password)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    try:
        cursor.execute(query, (first_name, last_name, dob, address, phone, email, hashed_pw ))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False
    finally:
        conn.close()

def sign_up_doctor(first_name, last_name, specialization, email, password):
    conn = connect_to_db()
    cursor = conn.cursor()
    hashed_pw = hash_password(password)  # Hash the password for security

    query = """
        INSERT INTO Doctor (FirstName, LastName, Specialization, Email, Password)
        VALUES (%s, %s,  %s, %s, %s)
    """
    try:
        cursor.execute(query, (first_name, last_name, specialization, email, hashed_pw ))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False
    finally:
        conn.close()


def fetch_patient_id(email):
    conn = connect_to_db()
    cursor = conn.cursor()

    query = "SELECT PatientID FROM Patient WHERE Email = %s"
    try:
        cursor.execute(query, (email,))
        result = cursor.fetchone()
        if result:
            return result[0]  # Return the PatientID
        else:
            print("No patient found with this email.")
            return None
    except Exception as e:
        print(f"Error fetching PatientID: {e}")
        return None
    finally:
        conn.close()



def sign_up_patient_ui():
    st.subheader("Patient Sign-Up")
    first_name = st.text_input("First Name")
    last_name = st.text_input("Last Name")
    dob = st.date_input("Date of Birth")
    address = st.text_area("Address")
    phone = st.text_input("Phone Number")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Sign Up"):
        if password != confirm_password:
            st.error("Passwords do not match!")
        elif not all([first_name, last_name, dob, address, phone, email, password]):
            st.error("All fields are required!")
        else:
            success = sign_up_patient(first_name, last_name, dob, address, phone, email, password)
            if success:
                st.success("Patient account created successfully!")
                st.session_state["logged_in"] = True
                st.session_state["user_id"] = fetch_patient_id(email)  # Fetch the new patient ID
                st.session_state["role"] = "Patient"
                st.session_state["redirect_to_create"] = True  # Set redirection
            else:
                st.error("Failed to create account. Please try again.")



def sign_up_doctor_ui():
    st.subheader("Doctor Sign-Up")

    first_name = st.text_input("First Name")
    last_name = st.text_input("Last Name")
    specialization = st.text_input("Specialization")
    
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Sign Up"):
        if password != confirm_password:
            st.error("Passwords do not match!")
        elif not all([first_name, last_name, specialization,  email, password]):
            st.error("All fields are required!")
        else:
            success = sign_up_doctor(first_name, last_name, specialization, email, password)
            if success:
                st.success("Doctor account created successfully!")
            else:
                st.error("Failed to create account. Please try again.")

def login_user(email, password, role):
    conn = connect_to_db()
    cursor = conn.cursor()

    if role == "Patient":
        query = "SELECT PatientID, Password FROM Patient WHERE Email=%s"
    elif role == "Doctor":
        query = "SELECT DoctorID, Password FROM Doctor WHERE Email=%s"
    else:
        return None, False

    cursor.execute(query, (email,))
    result = cursor.fetchone()
    conn.close()

    if result and verify_password(password, result[1]):  # Compare hashed password
        return result[0], True  # Return user ID and login success
    return None, False

def login_ui():
    st.subheader("Login")
    role = st.radio("Role", ["Patient", "Doctor"])
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user_id, success = login_user(email, password, role)
        if success:
            st.success(f"Welcome back, {role}!")
            st.session_state["logged_in"] = True
            st.session_state["user_id"] = user_id
            st.session_state["role"] = role
            st.session_state["redirect_to_create"] = True  # Set redirection
        else:
            st.error("Invalid email or password.")


def logout_ui():
    if st.button("Logout"):
        st.session_state["logged_in"] = False
        st.session_state["user_id"] = None
        st.session_state["role"] = None
        st.success("You have been logged out.")


def fetch_doctors():
    conn = connect_to_db()
    cursor = conn.cursor()
    query = "SELECT DoctorID, FirstName, LastName, Specialization FROM Doctor"
    try:
        cursor.execute(query)
        doctors = cursor.fetchall()
        return doctors
    except Exception as e:
        print(f"Error fetching doctors: {e}")
        return []
    finally:
        conn.close()


def create_appointment(patient_id, doctor_id, date, time):
    conn = connect_to_db()
    cursor = conn.cursor()
    query = """
        INSERT INTO Appointment (PatientID, DoctorID, Date, Time)
        VALUES (%s, %s, %s, %s)
    """
    try:
        cursor.execute(query, (patient_id, doctor_id, date, time))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error creating appointment: {e}")
        return False
    finally:
        conn.close()




def create_appointment_ui():
    if not st.session_state.get("logged_in") or st.session_state["role"] != "Patient":
        st.warning("You must log in as a patient to create an appointment.")
        return

    st.subheader("Create an Appointment")

    # Fetch and display doctors
    doctors = fetch_doctors()
    if not doctors:
        st.warning("No doctors available.")
        return

    doctor_options = {f"{doc[1]} {doc[2]} ({doc[3]})": doc[0] for doc in doctors}  # Format: "FirstName LastName (Specialization)"
    selected_doctor = st.selectbox("Select a Doctor", options=list(doctor_options.keys()))
    doctor_id = doctor_options[selected_doctor]

    # Appointment Details
    date = st.date_input("Select Appointment Date")
    time = st.time_input("Select Appointment Time")

    if st.button("Create Appointment"):
        patient_id = st.session_state["user_id"]  # Use session state to get logged-in patient ID
        success = create_appointment(patient_id, doctor_id, date, time)
        if success:
            st.success("Appointment created successfully!")
        else:
            st.error("Failed to create appointment. Please try again.")


def fetch_patient_appointments(patient_id):
    conn = connect_to_db()
    cursor = conn.cursor()

    # SQL query to fetch appointments for the patient, ordered by date and time (latest first)
    query = """
        SELECT 
            a.AppointmentID, 
            a.Date, 
            a.Time, 
            d.FirstName AS DoctorFirstName, 
            d.LastName AS DoctorLastName, 
            d.Specialization
        FROM 
            Appointment a
        JOIN 
            Doctor d ON a.DoctorID = d.DoctorID
        WHERE 
            a.PatientID = %s
        ORDER BY 
            a.Date DESC, a.Time DESC
    """
    try:
        cursor.execute(query, (patient_id,))
        appointments = cursor.fetchall()
        return appointments
    except Exception as e:
        print(f"Error fetching appointments: {e}")
        return []
    finally:
        conn.close()


def view_patient_appointments_ui():
    if not st.session_state.get("logged_in") or st.session_state["role"] != "Patient":
        st.warning("You must log in as a patient to view your appointments.")
        return

    st.subheader("Your Past Appointments")

    # Fetch appointments for the logged-in patient
    patient_id = st.session_state["user_id"]
    appointments = fetch_patient_appointments(patient_id)

    if not appointments:
        st.info("You have no past appointments.")
        return

    # Display appointments in a table
    st.write("### Past Appointments (Latest at the Top)")
    appointment_data = [
        {
            "Appointment ID": appt[0],
            "Date": appt[1],
            "Time": appt[2],
            "Doctor": f"{appt[3]} {appt[4]}",
            "Specialization": appt[5]
        }
        for appt in appointments
    ]
    st.dataframe(appointment_data)




def main():
    st.title("Health Records Management System")

    # Check for redirection after login or sign-up
    if st.session_state.get("redirect_to_create"):
        st.session_state["redirect_to_create"] = False  # Reset the redirection state
        create_appointment_ui()
        return

    # Main menu
    menu = ["Home", "Login", "Sign Up", "Create Appointment", "View Appointments", "Logout"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        if st.session_state.get("logged_in"):
            st.subheader(f"Welcome back, {st.session_state['role']}!")
        else:
            st.subheader("Welcome to the Health Records System!")

    elif choice == "Login":
        login_ui()

    elif choice == "Sign Up":
        role = st.radio("Sign-Up As", ["Patient", "Doctor"])
        if role == "Patient":
            sign_up_patient_ui()
        elif role == "Doctor":
            sign_up_doctor_ui()

    elif choice == "Create Appointment":
        create_appointment_ui()

    elif choice == "View Appointments":
        if st.session_state.get("role") == "Patient":
            view_patient_appointments_ui()
        else:
            st.warning("Only patients can view their appointments.")

    elif choice == "Logout":
        logout_ui()







if __name__ == "__main__":

    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
        st.session_state["user_id"] = None
        st.session_state["role"] = None

    main()
