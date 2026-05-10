-- Hospital Management System - PostgreSQL Schema

-- 1. Admins Table
CREATE TABLE admins (
    admin_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL
);

-- 2. Patients Table
CREATE TABLE patients (
    patient_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    age INT CHECK (age >= 0),
    gender VARCHAR(10),
    blood_group VARCHAR(5),
    phone VARCHAR(15) UNIQUE NOT NULL,
    address TEXT,
    emergency_contact VARCHAR(15),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_patient_phone ON patients(phone);

-- 3. Doctors Table
CREATE TABLE doctors (
    doctor_id SERIAL PRIMARY KEY,
    doctor_name VARCHAR(100) NOT NULL,
    specialization VARCHAR(100) NOT NULL,
    experience INT CHECK (experience >= 0),
    availability VARCHAR(255),
    phone VARCHAR(15) UNIQUE NOT NULL,
    consultation_fee DECIMAL(10, 2) NOT NULL
);
CREATE INDEX idx_doctor_specialization ON doctors(specialization);

-- 4. Appointments Table
CREATE TABLE appointments (
    appointment_id SERIAL PRIMARY KEY,
    patient_id INT NOT NULL,
    doctor_id INT NOT NULL,
    appointment_date TIMESTAMP NOT NULL,
    status VARCHAR(20) DEFAULT 'Scheduled',
    symptoms TEXT,
    CONSTRAINT fk_patient
        FOREIGN KEY(patient_id) 
        REFERENCES patients(patient_id) 
        ON DELETE CASCADE,
    CONSTRAINT fk_doctor
        FOREIGN KEY(doctor_id) 
        REFERENCES doctors(doctor_id)
);
CREATE INDEX idx_appointment_date ON appointments(appointment_date);

-- 5. Prescriptions Table
CREATE TABLE prescriptions (
    prescription_id SERIAL PRIMARY KEY,
    appointment_id INT NOT NULL,
    medicines TEXT NOT NULL,
    dosage TEXT NOT NULL,
    notes TEXT,
    CONSTRAINT fk_appointment
        FOREIGN KEY(appointment_id) 
        REFERENCES appointments(appointment_id) 
        ON DELETE CASCADE
);

-- 6. Lab Reports Table
CREATE TABLE lab_reports (
    report_id SERIAL PRIMARY KEY,
    patient_id INT NOT NULL,
    test_name VARCHAR(100) NOT NULL,
    result TEXT NOT NULL,
    report_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    file_path VARCHAR(255),
    CONSTRAINT fk_lab_patient
        FOREIGN KEY(patient_id) 
        REFERENCES patients(patient_id) 
        ON DELETE CASCADE
);

-- 7. Bills Table
CREATE TABLE bills (
    bill_id SERIAL PRIMARY KEY,
    patient_id INT NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    payment_status VARCHAR(20) DEFAULT 'Unpaid',
    bill_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_bill_patient
        FOREIGN KEY(patient_id) 
        REFERENCES patients(patient_id) 
        ON DELETE CASCADE
);

-- 8. Payments Table
CREATE TABLE payments (
    payment_id SERIAL PRIMARY KEY,
    bill_id INT NOT NULL,
    amount_paid DECIMAL(10, 2) NOT NULL,
    payment_method VARCHAR(50) NOT NULL,
    payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_payment_bill
        FOREIGN KEY(bill_id) 
        REFERENCES bills(bill_id) 
        ON DELETE CASCADE
);
