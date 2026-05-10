-- Hospital Management System - Dummy Data

-- Insert Admins
INSERT INTO admins (username, password_hash) VALUES 
('admin1', 'pbkdf2:sha256:600000$P2O7uH...'), -- password is 'password123'
('admin2', 'pbkdf2:sha256:600000$X9Q1vI...');

-- Insert Patients
INSERT INTO patients (name, age, gender, blood_group, phone, address, emergency_contact) VALUES
('John Doe', 34, 'Male', 'O+', '9876543210', '123 Elm St, Cityville', '9876543211'),
('Jane Smith', 28, 'Female', 'A-', '8765432109', '456 Oak St, Townsville', '8765432100'),
('Alice Brown', 45, 'Female', 'B+', '7654321098', '789 Pine St, Villageville', '7654321099');

-- Insert Doctors
INSERT INTO doctors (doctor_name, specialization, experience, availability, phone, consultation_fee) VALUES
('Dr. Robert Green', 'Cardiology', 15, 'Mon-Fri 09:00-13:00', '1234567890', 500.00),
('Dr. Emily White', 'Neurology', 10, 'Mon-Wed 14:00-18:00', '2345678901', 600.00),
('Dr. Richard Black', 'General Medicine', 5, 'Mon-Sat 10:00-17:00', '3456789012', 300.00);

-- Insert Appointments
INSERT INTO appointments (patient_id, doctor_id, appointment_date, status, symptoms) VALUES
(1, 1, '2023-11-01 10:00:00', 'Completed', 'Chest pain'),
(2, 2, '2023-11-02 15:00:00', 'Completed', 'Frequent headaches'),
(3, 3, '2023-11-03 11:30:00', 'Scheduled', 'Fever and cough');

-- Insert Prescriptions
INSERT INTO prescriptions (appointment_id, medicines, dosage, notes) VALUES
(1, 'Aspirin', '1 pill a day after meals', 'Rest for 3 days'),
(2, 'Paracetamol', '2 pills a day if pain persists', 'Drink plenty of water');

-- Insert Lab Reports
INSERT INTO lab_reports (patient_id, test_name, result, report_date) VALUES
(1, 'ECG', 'Normal sinus rhythm', '2023-11-01 12:00:00'),
(2, 'MRI Brain', 'No abnormalities detected', '2023-11-02 16:30:00');

-- Insert Bills
INSERT INTO bills (patient_id, total_amount, payment_status, bill_date) VALUES
(1, 1500.00, 'Paid', '2023-11-01 13:00:00'),
(2, 2600.00, 'Unpaid', '2023-11-02 17:00:00');

-- Insert Payments
INSERT INTO payments (bill_id, amount_paid, payment_method, payment_date) VALUES
(1, 1500.00, 'Credit Card', '2023-11-01 13:10:00');
