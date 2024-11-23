-- Create Database
CREATE DATABASE electronic_health_system;
USE electronic_health_system;

-- Users Table
CREATE TABLE Users (
    UserID INT AUTO_INCREMENT PRIMARY KEY,
    Username VARCHAR(50) UNIQUE NOT NULL,
    Password VARCHAR(255) NOT NULL,
    Role ENUM('Patient', 'Doctor', 'Admin') NOT NULL,
    CreatedAt DATETIME DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Patients Table
CREATE TABLE Patients (
    PatientID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT UNIQUE,
    FullName VARCHAR(100) NOT NULL,
    DOB DATE,
    ContactNumber VARCHAR(20),
    Email VARCHAR(100),
    Address VARCHAR(255),
    FOREIGN KEY (UserID) REFERENCES Users(UserID) ON DELETE CASCADE
);

-- Doctors Table
CREATE TABLE Doctors (
    DoctorID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT UNIQUE,
    FullName VARCHAR(100) NOT NULL,
    Specialty VARCHAR(100),
    ContactNumber VARCHAR(20),
    Email VARCHAR(100),
    ConsultationFee DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (UserID) REFERENCES Users(UserID) ON DELETE CASCADE
);

-- LabTests Table
CREATE TABLE LabTests (
    LabTestID INT AUTO_INCREMENT PRIMARY KEY,
    TestName VARCHAR(100) UNIQUE NOT NULL,
    Description VARCHAR(255),
    Cost DECIMAL(10,2) NOT NULL,
    CreatedAt DATETIME DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Appointments Table
CREATE TABLE Appointments (
    AppointmentID INT AUTO_INCREMENT PRIMARY KEY,
    PatientID INT NOT NULL,
    DoctorID INT NOT NULL,
    AppointmentDateTime DATETIME NOT NULL,
    Status ENUM('Scheduled', 'Completed', 'Cancelled') DEFAULT 'Scheduled',
    
    CreatedAt DATETIME DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (PatientID) REFERENCES Patients(PatientID) ON DELETE CASCADE,
    FOREIGN KEY (DoctorID) REFERENCES Doctors(DoctorID) ON DELETE CASCADE,
   
);

-- Billing Table (Revised)
CREATE TABLE Billing (
    BillID INT AUTO_INCREMENT PRIMARY KEY,
    PatientID INT NOT NULL,
    AppointmentID INT NOT NULL,
    DoctorFee DECIMAL(10,2) NOT NULL,
    LabTestFees DECIMAL(10,2) DEFAULT 0.00,
    DueDate DATE NOT NULL,
    Status ENUM('Unpaid', 'Partially Paid', 'Paid') DEFAULT 'Unpaid',
    CreatedAt DATETIME DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (PatientID) REFERENCES Patients(PatientID) ON DELETE CASCADE,
    FOREIGN KEY (AppointmentID) REFERENCES Appointments(AppointmentID) ON DELETE CASCADE
);

-- MedicalRecords Table
CREATE TABLE MedicalRecords (
    RecordID INT AUTO_INCREMENT PRIMARY KEY,
    AppointmentID INT UNIQUE NOT NULL,
    Diagnosis TEXT,
    Treatment TEXT,
    Prescription TEXT,
    CreatedAt DATETIME DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (AppointmentID) REFERENCES Appointments(AppointmentID) ON DELETE CASCADE
);

-- MedicalRecord_LabTests Table (Associative Table)
CREATE TABLE MedicalRecord_LabTests (
    MR_LabTestID INT AUTO_INCREMENT PRIMARY KEY,
    RecordID INT NOT NULL,
    LabTestID INT NOT NULL,
    Result TEXT,
    FOREIGN KEY (RecordID) REFERENCES MedicalRecords(RecordID) ON DELETE CASCADE,
    FOREIGN KEY (LabTestID) REFERENCES LabTests(LabTestID) ON DELETE CASCADE
);

-- Wallets Table
CREATE TABLE Wallets (
    WalletID INT AUTO_INCREMENT PRIMARY KEY,
    PatientID INT UNIQUE NOT NULL,
    Balance DECIMAL(10,2) DEFAULT 0.00,
    FOREIGN KEY (PatientID) REFERENCES Patients(PatientID) ON DELETE CASCADE
);

-- WalletTransactions Table
CREATE TABLE WalletTransactions (
    TransactionID INT AUTO_INCREMENT PRIMARY KEY,
    WalletID INT NOT NULL,
    TransactionType ENUM('Credit', 'Debit') NOT NULL,
    Amount DECIMAL(10,2) NOT NULL,
    Description VARCHAR(255),
    TransactionDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (WalletID) REFERENCES Wallets(WalletID) ON DELETE CASCADE
);
