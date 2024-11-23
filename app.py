# app.py (Updated with Registration Interface)

import streamlit as st # type: ignore
from utils.authentication import authenticate_user, register_patient, register_doctor
from db import connect_to_db as get_db_connection

# Initialize session state variables
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'user' not in st.session_state:
    st.session_state['user'] = None

def login():
    st.title("Electronic Health System (EHS) - Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username and password:
            user = authenticate_user(username, password)
            if user:
                st.session_state['logged_in'] = True
                st.session_state['user'] = user
                st.success(f"Logged in as {user[3]}")
            else:
                st.error("Invalid username or password.")
        else:
            st.warning("Please enter both username and password.")

def register():
    st.title("Electronic Health System (EHS) - Register")

    role = st.selectbox("Register as", ["Patient", "Doctor"])

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if role == "Patient":
        full_name = st.text_input("Full Name")
        dob = st.date_input("Date of Birth")
        contact_number = st.text_input("Contact Number")
        email = st.text_input("Email")
        address = st.text_area("Address")
    elif role == "Doctor":
        full_name = st.text_input("Full Name")
        specialty = st.text_input("Specialty")
        contact_number = st.text_input("Contact Number")
        email = st.text_input("Email")
        consultation_fee = st.number_input("Consultation Fee", min_value=0.0, format="%.2f")

    if st.button("Register"):
        if not all([username, password, confirm_password]):
            st.warning("Please fill out all required fields.")
        elif password != confirm_password:
            st.error("Passwords do not match.")
        else:
            if role == "Patient":
                success = register_patient(
                    username=username,
                    plain_password=password,
                    full_name=full_name,
                    dob=dob.strftime("%Y-%m-%d"),
                    contact_number=contact_number,
                    email=email,
                    address=address
                )
            elif role == "Doctor":
                success = register_doctor(
                    username=username,
                    plain_password=password,
                    full_name=full_name,
                    specialty=specialty,
                    contact_number=contact_number,
                    email=email,
                    consultation_fee=consultation_fee
                )

            if success:
                st.success(f"{role} registered successfully! Please log in.")
            else:
                st.error(f"Failed to register {role}. Username might already be taken.")

def patient_dashboard(user):
    st.header("Patient Dashboard")
    st.write(f"Welcome, {user[1]}!")
    # Implement Patient-specific functionalities here

def doctor_dashboard(user):
    st.header("Doctor Dashboard")
    st.write(f"Welcome, Dr. {user[1]}!")
    # Implement Doctor-specific functionalities here

def admin_dashboard(user):
    st.header("Admin Dashboard")
    st.write(f"Welcome, Admin {user[1]}!")
    # Implement Admin-specific functionalities here

def main():
    menu = ["Login", "Register"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Login":
        if st.session_state['logged_in']:
            user = st.session_state['user']
            role = user['Role']

            st.sidebar.title(f"{role} Dashboard")
            st.sidebar.markdown("---")
            if role == "Patient":
                patient_dashboard(user)
            elif role == "Doctor":
                doctor_dashboard(user)
            elif role == "Admin":
                admin_dashboard(user)

            if st.sidebar.button("Logout"):
                st.session_state['logged_in'] = False
                st.session_state['user'] = None
                st.experimental_rerun()
        else:
            login()
    elif choice == "Register":
        register()

if __name__ == "__main__":
    main()
