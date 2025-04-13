
-- Users table to store common user information
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    role ENUM('caregiver', 'doctor', 'hospital', 'patient', 'super_user') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Caregivers table
CREATE TABLE caregivers (
    caregiver_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(15),
    address TEXT,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Doctors table
CREATE TABLE doctors (
    doctor_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    specialty VARCHAR(100),
    phone VARCHAR(15),
    address TEXT,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Hospitals table
CREATE TABLE hospitals (
    hospital_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    location TEXT,
    phone VARCHAR(15),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Patients table
CREATE TABLE patients (
    patient_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    date_of_birth DATE,
    gender ENUM('male', 'female', 'other'),
    phone VARCHAR(15),
    address TEXT,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Super Users table
CREATE TABLE super_users (
    super_user_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(15),
    address TEXT,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Insert sample users
INSERT INTO users (username, password, email, role) VALUES
('caregiver1', 'password_hash', 'caregiver1@example.com', 'caregiver'),
('doctor1', 'password_hash', 'doctor1@example.com', 'doctor'),
('hospital1', 'password_hash', 'hospital1@example.com', 'hospital'),
('patient1', 'password_hash', 'patient1@example.com', 'patient'),
('superuser1', 'password_hash', 'superuser1@example.com', 'super_user');

-- Insert sample caregivers
INSERT INTO caregivers (user_id, name, phone, address) VALUES
(1, 'Caregiver One', '1234567890', '123 Caregiver St');

-- Insert sample doctors
INSERT INTO doctors (user_id, name, specialty, phone, address) VALUES
(2, 'Doctor One', 'Cardiology', '0987654321', '456 Doctor Ave');

-- Insert sample hospitals
INSERT INTO hospitals (user_id, name, location, phone) VALUES
(3, 'Hospital One', '789 Hospital Rd', '1122334455');

-- Insert sample patients
INSERT INTO patients (user_id, name, date_of_birth, gender, phone, address) VALUES
(4, 'Patient One', '1990-01-01', 'male', '2233445566', '101 Patient Blvd');

-- Insert sample super users
INSERT INTO super_users (user_id, name, phone, address) VALUES
(5, 'Super User One', '3344556677', '202 Superuser Ln');
