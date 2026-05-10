# Viva Questions & Answers

**Q1: What is Normalization? Why did you use it?**
**Answer:** Normalization is the process of organizing data in a database to reduce redundancy and improve data integrity. I used it to prevent insert, update, and delete anomalies. Our database is in 3NF, ensuring no transitive dependencies exist.

**Q2: How does your database handle a situation where a patient is deleted?**
**Answer:** I implemented `ON DELETE CASCADE` foreign key constraints. When a patient is deleted, the database automatically cascades this deletion to the `appointments`, `bills`, and `lab_reports` tables associated with that `patient_id` to maintain referential integrity.

**Q3: Explain the triggers used in your project.**
**Answer:** I created two main triggers in PostgreSQL:
1. `after_payment_insert`: Automatically checks if the payment amount matches the bill total. If it does, it updates the bill's `payment_status` to 'Paid'.
2. `before_appointment_insert`: Checks for overlapping appointment slots for the same doctor to prevent double-booking.

**Q4: What is a Stored Procedure, and where is it used here?**
**Answer:** A stored procedure is a prepared SQL code that you can save and reuse. In this project, I wrote procedures like `get_hospital_revenue` which calculates total hospital earnings for a specific month and year, handling complex aggregation logic entirely on the database side rather than the application server.

**Q5: What are Views? Give an example from your project.**
**Answer:** A view is a virtual table based on the result-set of an SQL statement. It simplifies complex queries. I created `vw_unpaid_bills` which JOINs the `bills` and `patients` tables to show exactly who owes money and how much, without needing to write the JOIN query repeatedly in the application.

**Q6: What is the difference between DELETE and TRUNCATE?**
**Answer:** DELETE is a DML command used to remove specific rows based on a WHERE clause and logs each row deletion (so it can be rolled back). TRUNCATE is a DDL command that removes all rows from a table quickly by deallocating the data pages, and it cannot be easily rolled back in some DBs (though PostgreSQL handles it in transactions). TRUNCATE does not fire ON DELETE triggers.

**Q7: Why use indexing? Where did you use it?**
**Answer:** Indexing improves data retrieval speed. I added indexes on frequently searched columns like `phone` in the `patients` table, `specialization` in the `doctors` table, and `appointment_date` in the `appointments` table.
