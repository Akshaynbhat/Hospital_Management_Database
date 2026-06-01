# HMS Pro - Hospital Management System

## Overview

HMS Pro is a web-based Hospital Management System designed to streamline and automate various hospital operations including patient management, doctor management, appointment scheduling, prescription generation, billing, payment tracking, and medical record management.

The system is developed using a three-tier architecture consisting of a frontend interface, a Flask-based backend, and a PostgreSQL database. HMS Pro provides role-based access control for administrators, doctors, and patients, ensuring secure and organized management of hospital data.

---

## Features

### Patient Management

* Add, edit, view, and delete patient records
* Store patient demographic and contact information
* Maintain medical history records
* Upload and manage medical documents

### Doctor Management

* Add and manage doctor profiles
* Store specialization and consultation fee details
* Manage doctor availability schedules
* Track appointment history

### Appointment Management

* Schedule appointments with doctors
* Prevent duplicate booking using database triggers
* Accept, reject, or complete appointments
* Track appointment status

### Prescription Management

* Generate prescriptions after consultation
* Store diagnosis information
* Manage prescribed medicines
* View patient prescription history

### Billing and Payments

* Automatic bill generation
* Consultation fee management
* Payment tracking
* Paid and pending bill management

### Role-Based Access Control

* Administrator Module
* Doctor Module
* Patient Module

### Database Automation

* Stored Procedures
* Triggers
* Views
* Foreign Key Constraints
* Audit Logging

---

## Technologies Used

### Frontend

* HTML5
* CSS3
* JavaScript

### Backend

* Python 3.x
* Flask Framework

### Database

* PostgreSQL

### Development Tools

* Visual Studio Code
* pgAdmin
* Git
* GitHub

---

## System Architecture

The project follows a Three-Tier Architecture:

### Presentation Layer

Developed using HTML, CSS, and JavaScript. Provides user interfaces for administrators, doctors, and patients.

### Application Layer

Implemented using Flask. Handles business logic, authentication, appointment scheduling, billing operations, and database communication.

### Database Layer

Implemented using PostgreSQL. Stores patient records, doctor details, appointments, prescriptions, billing information, and audit logs.

---

## Database Features

### Normalization

The database schema is designed up to Third Normal Form (3NF) to eliminate redundancy and improve consistency.

### Triggers

* Prevent duplicate appointment booking
* Automatic bill generation
* Audit logging

### Stored Procedures

* Appointment booking
* Billing operations
* Transaction management

### Views

* Appointment Overview
* Patient History
* Billing Summary

### Constraints

* Primary Keys
* Foreign Keys
* Unique Constraints
* Check Constraints

---

## Database Tables

### Core Tables

* Users
* Departments
* Rooms
* Medicines

### Entity Tables

* Patients
* Doctors

### Operational Tables

* Appointments
* Doctor_Availability
* Admissions

### Clinical Tables

* Prescriptions
* Prescribed_Medicines
* Patient_Documents

### Financial Tables

* Bills
* Bill_Items
* Payments

### Audit Tables

* Login_History
* Appointment_Audit
* Deleted_Records_Log

---

## Installation Guide

### Prerequisites

Install the following software:

* Python 3.9 or later
* PostgreSQL 13 or later
* Git
* pgAdmin (optional)

---

## Clone Repository

```bash
git clone https://github.com/your-username/hms-pro.git

cd hms-pro
```

---

## Create Virtual Environment

```bash
python -m venv venv
```

Activate Virtual Environment:

Windows

```bash
venv\Scripts\activate
```

Linux/Mac

```bash
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Database

Create PostgreSQL database:

```sql
CREATE DATABASE hms_pro;
```

Update database configuration in:

```python
config.py
```

Example:

```python
SQLALCHEMY_DATABASE_URI =
'postgresql://username:password@localhost/hms_pro'
```

---

## Run Application

```bash
python app.py
```

Open browser:

```text
http://127.0.0.1:5000
```

---

## Demo Credentials

### Administrator

Email:

```text
admin@hms.com
```

Password:

```text
Admin@123
```

### Doctor

Email:

```text
smruti@hms.com
```

Password:

```text
Doctor@123
```

### Patient

Email:

```text
amogh@hms.com
```

Password:

```text
Patient@123
```

---

## Testing

The system has been tested for:

* Login Authentication
* Patient Management
* Appointment Scheduling
* Prescription Management
* Billing Operations
* Payment Processing
* Role-Based Access Control
* Database Validation
* Audit Logging

All test cases executed successfully.

---

## Security Features

* Password hashing using PBKDF2-SHA256
* Session management
* Role-based authorization
* Input validation
* Foreign key integrity constraints

---

## Future Enhancements

* Online payment gateway integration
* SMS and Email notifications
* Telemedicine support
* Mobile application
* AI-assisted appointment recommendations
* Electronic Health Record (EHR) integration
* Advanced analytics dashboard

---

## Advantages

* Reduces manual paperwork
* Improves operational efficiency
* Maintains data consistency
* Enhances security
* Automates hospital workflows
* Provides centralized information management

---

## Conclusion

HMS Pro is a comprehensive Hospital Management System that digitizes and automates core hospital operations. By integrating patient management, doctor scheduling, prescriptions, billing, and database automation into a single platform, the system improves efficiency, accuracy, and reliability while ensuring secure management of healthcare information.
