-- Hospital Management System - PostgreSQL Advanced Concepts

-- ==========================================
-- 1. TRIGGERS
-- ==========================================

-- Trigger: Automatically update bill status to "Paid" when payment equals total_amount
CREATE OR REPLACE FUNCTION update_bill_status()
RETURNS TRIGGER AS $$
DECLARE
    v_total_amount DECIMAL(10,2);
BEGIN
    -- Get the total amount of the bill
    SELECT total_amount INTO v_total_amount FROM bills WHERE bill_id = NEW.bill_id;
    
    -- Check if payment covers the bill
    IF NEW.amount_paid >= v_total_amount THEN
        UPDATE bills SET payment_status = 'Paid' WHERE bill_id = NEW.bill_id;
    ELSIF NEW.amount_paid > 0 THEN
        UPDATE bills SET payment_status = 'Partially Paid' WHERE bill_id = NEW.bill_id;
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER after_payment_insert
AFTER INSERT ON payments
FOR EACH ROW
EXECUTE FUNCTION update_bill_status();


-- Trigger: Prevent overlapping appointments for the same doctor
CREATE OR REPLACE FUNCTION check_doctor_availability()
RETURNS TRIGGER AS $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM appointments 
        WHERE doctor_id = NEW.doctor_id 
        AND appointment_date = NEW.appointment_date
        AND status != 'Cancelled'
    ) THEN
        RAISE EXCEPTION 'Doctor is already booked for this time slot.';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER before_appointment_insert
BEFORE INSERT ON appointments
FOR EACH ROW
EXECUTE FUNCTION check_doctor_availability();


-- ==========================================
-- 2. STORED PROCEDURES
-- ==========================================

-- Procedure: Calculate total hospital revenue for a given month and year
CREATE OR REPLACE PROCEDURE get_hospital_revenue(
    IN p_month INT, 
    IN p_year INT,
    INOUT p_total_revenue DECIMAL(10,2) DEFAULT 0
)
LANGUAGE plpgsql
AS $$
BEGIN
    SELECT COALESCE(SUM(amount_paid), 0)
    INTO p_total_revenue
    FROM payments
    WHERE EXTRACT(MONTH FROM payment_date) = p_month
    AND EXTRACT(YEAR FROM payment_date) = p_year;
END;
$$;
-- Call Example:
-- CALL get_hospital_revenue(11, 2023, null);


-- Procedure: Get the number of appointments for a doctor
CREATE OR REPLACE PROCEDURE get_doctor_stats(
    IN p_doctor_id INT,
    INOUT p_total_appointments INT DEFAULT 0
)
LANGUAGE plpgsql
AS $$
BEGIN
    SELECT COUNT(*)
    INTO p_total_appointments
    FROM appointments
    WHERE doctor_id = p_doctor_id;
END;
$$;
-- Call Example:
-- CALL get_doctor_stats(1, null);


-- ==========================================
-- 3. VIEWS
-- ==========================================

-- View: Unpaid Bills with Patient Details
CREATE OR REPLACE VIEW vw_unpaid_bills AS
SELECT 
    b.bill_id, 
    p.name AS patient_name, 
    p.phone AS patient_phone,
    b.total_amount, 
    b.bill_date
FROM bills b
JOIN patients p ON b.patient_id = p.patient_id
WHERE b.payment_status != 'Paid';

-- View: Today's Appointments Summary
CREATE OR REPLACE VIEW vw_today_appointments AS
SELECT 
    a.appointment_id,
    a.appointment_date,
    p.name AS patient_name,
    d.doctor_name,
    a.status
FROM appointments a
JOIN patients p ON a.patient_id = p.patient_id
JOIN doctors d ON a.doctor_id = d.doctor_id
WHERE DATE(a.appointment_date) = CURRENT_DATE;

-- View: Doctor Summary
CREATE OR REPLACE VIEW vw_doctor_summary AS
SELECT 
    d.doctor_id,
    d.doctor_name,
    d.specialization,
    COUNT(a.appointment_id) AS total_appointments
FROM doctors d
LEFT JOIN appointments a ON d.doctor_id = a.doctor_id
GROUP BY d.doctor_id, d.doctor_name, d.specialization;


-- ==========================================
-- 4. TRANSACTIONS (Example Script)
-- ==========================================
-- PostgreSQL handles transactions automatically in standard scripts via BEGIN/COMMIT.
-- In Python/Flask, we'll use `conn.commit()` and `conn.rollback()`.
--
-- Example SQL transaction demonstrating ACID:
-- BEGIN;
--   INSERT INTO bills (patient_id, total_amount, payment_status) VALUES (1, 500.00, 'Unpaid');
--   -- If something fails here, we rollback
--   -- ROLLBACK;
-- COMMIT;


-- ==========================================
-- 5. CASCADING DELETES
-- ==========================================
-- Demonstrated in schema.sql:
-- CONSTRAINT fk_patient FOREIGN KEY(patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE
-- If we delete a patient: DELETE FROM patients WHERE patient_id = 1;
-- Their appointments, bills, and lab reports are automatically deleted.


-- ==========================================
-- 6. JOINS
-- ==========================================
-- INNER JOIN: Fetching patients and their doctors (vw_today_appointments)
-- LEFT JOIN: Fetching ALL doctors and their appointment counts (even if 0) (vw_doctor_summary)
-- RIGHT JOIN Example:
-- SELECT p.name, a.appointment_date 
-- FROM appointments a
-- RIGHT JOIN patients p ON a.patient_id = p.patient_id;
