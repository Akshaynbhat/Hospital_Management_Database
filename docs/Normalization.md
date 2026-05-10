# Normalization in Hospital Management System

This database is designed following normalization rules up to the **Third Normal Form (3NF)**.

## First Normal Form (1NF)
**Rule:** No repeating groups or arrays. Every column must hold atomic (indivisible) values, and each record must be unique.
**Implementation:**
- In the `prescriptions` table, instead of having an array of medicines, we store them as a comma-separated text OR (ideally) we could create a separate `prescription_medicines` mapping table. For this project scope, we kept `medicines` and `dosage` as text, but every row is uniquely identified by a primary key (`prescription_id`).
- All tables have a unique Primary Key.

## Second Normal Form (2NF)
**Rule:** Must be in 1NF. All non-key attributes must be fully functionally dependent on the entire primary key (No partial dependency).
**Implementation:**
- We do not use composite primary keys. Every table uses a single-column surrogate key (e.g., `appointment_id`, `patient_id` using `SERIAL` in PostgreSQL).
- Because there are no composite keys, partial dependencies are inherently avoided. For instance, in the `appointments` table, the `status` depends entirely on `appointment_id`, not just on `patient_id` or `doctor_id`.

## Third Normal Form (3NF)
**Rule:** Must be in 2NF. There should be no transitive dependency (Non-key attributes should not depend on other non-key attributes).
**Implementation:**
- In the `bills` table, we store `patient_id` rather than storing the patient's name, age, and address directly in the bill. If we need the patient's address for the bill, we JOIN the `patients` table.
- This avoids data duplication and update anomalies. If a patient changes their phone number, we only update it in the `patients` table, and all views/bills automatically reflect the change.
