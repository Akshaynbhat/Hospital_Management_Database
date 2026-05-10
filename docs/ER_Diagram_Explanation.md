# ER Diagram Explanation

## Entities and Relationships

1. **Patient (1) - (N) Appointment**
   - **Relationship:** A patient can book multiple appointments, but an appointment is for exactly one patient.
   - **Foreign Key:** `patient_id` in `appointments` table.
   - **Constraint:** ON DELETE CASCADE (If a patient is removed, their appointments are deleted).

2. **Doctor (1) - (N) Appointment**
   - **Relationship:** A doctor handles multiple appointments, but an appointment belongs to exactly one doctor.
   - **Foreign Key:** `doctor_id` in `appointments` table.

3. **Appointment (1) - (1) Prescription**
   - **Relationship:** Each appointment results in exactly one prescription (or zero).
   - **Foreign Key:** `appointment_id` in `prescriptions` table.
   - **Constraint:** ON DELETE CASCADE.

4. **Patient (1) - (N) Lab Report**
   - **Relationship:** A patient can have multiple lab reports.
   - **Foreign Key:** `patient_id` in `lab_reports` table.

5. **Patient (1) - (N) Bill**
   - **Relationship:** A patient can receive multiple bills.
   - **Foreign Key:** `patient_id` in `bills` table.

6. **Bill (1) - (N) Payment**
   - **Relationship:** A single bill can be paid in multiple installments (partial payments) leading to a one-to-many relationship.
   - **Foreign Key:** `bill_id` in `payments` table.
