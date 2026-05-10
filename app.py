from flask import Flask, render_template, request, redirect, url_for, session, flash, Response
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config, get_db_connection
import functools
import os
import csv
from io import StringIO

app = Flask(__name__)
app.config.from_object(Config)

# ==========================================
# AUTHENTICATION DECORATOR
# ==========================================
def login_required(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
            flash('Please log in to access this page.', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# ==========================================
# ROUTES: AUTHENTICATION
# ==========================================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM admins WHERE username = %s", (username,))
        admin = cur.fetchone()
        cur.close()
        conn.close()
        
        if admin and check_password_hash(admin['password_hash'], password):
            session['admin_id'] = admin['admin_id']
            session['username'] = admin['username']
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.', 'danger')
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

# ==========================================
# ROUTES: DASHBOARD
# ==========================================
@app.route('/')
@app.route('/dashboard')
@login_required
def dashboard():
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Example queries for dashboard stats
    cur.execute("SELECT COUNT(*) as count FROM patients")
    total_patients = cur.fetchone()['count']
    
    cur.execute("SELECT COUNT(*) as count FROM doctors")
    total_doctors = cur.fetchone()['count']
    
    cur.execute("SELECT COUNT(*) as count FROM appointments WHERE DATE(appointment_date) = CURRENT_DATE")
    today_appointments = cur.fetchone()['count']
    
    # We can also call our stored procedure here or use sum
    cur.execute("SELECT COALESCE(SUM(amount_paid), 0) as total FROM payments")
    total_revenue = cur.fetchone()['total']
    
    cur.close()
    conn.close()
    
    return render_template('dashboard.html', 
                           total_patients=total_patients, 
                           total_doctors=total_doctors,
                           today_appointments=today_appointments,
                           total_revenue=total_revenue)

@app.route('/generate_report')
@login_required
def generate_report():
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT COUNT(*) as count FROM patients")
    total_patients = cur.fetchone()['count']
    
    cur.execute("SELECT COUNT(*) as count FROM doctors")
    total_doctors = cur.fetchone()['count']
    
    cur.execute("SELECT COUNT(*) as count FROM appointments WHERE DATE(appointment_date) = CURRENT_DATE")
    today_appointments = cur.fetchone()['count']
    
    cur.execute("SELECT COALESCE(SUM(amount_paid), 0) as total FROM payments")
    total_revenue = cur.fetchone()['total']
    
    cur.close()
    conn.close()

    si = StringIO()
    cw = csv.writer(si)
    cw.writerow(['Metric', 'Value'])
    cw.writerow(['Total Patients', total_patients])
    cw.writerow(['Total Doctors', total_doctors])
    cw.writerow(["Today's Appointments", today_appointments])
    cw.writerow(['Total Revenue ($)', total_revenue])
    
    output = si.getvalue()
    
    return Response(
        output,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=hospital_summary_report.csv"}
    )

# ==========================================
# ROUTES: PATIENTS
# ==========================================
@app.route('/patients')
@login_required
def patients():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM patients ORDER BY created_at DESC")
    all_patients = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('patients.html', patients=all_patients)

@app.route('/patients/add', methods=['POST'])
@login_required
def add_patient():
    name = request.form['name']
    age = request.form['age']
    gender = request.form['gender']
    phone = request.form['phone']
    blood_group = request.form.get('blood_group', '')
    address = request.form.get('address', '')
    emergency_contact = request.form.get('emergency_contact', '')
    
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO patients (name, age, gender, blood_group, phone, address, emergency_contact) VALUES (%s, %s, %s, %s, %s, %s, %s)", 
                    (name, age, gender, blood_group, phone, address, emergency_contact))
        conn.commit()
        flash('Patient added successfully!', 'success')
    except Exception as e:
        conn.rollback()
        flash(f'Error adding patient: {str(e)}', 'danger')
    finally:
        cur.close()
        conn.close()
    return redirect(url_for('patients'))

@app.route('/patients/edit/<int:id>', methods=['POST'])
@login_required
def edit_patient(id):
    name = request.form['name']
    age = request.form['age']
    gender = request.form['gender']
    phone = request.form['phone']
    blood_group = request.form.get('blood_group', '')
    address = request.form.get('address', '')
    emergency_contact = request.form.get('emergency_contact', '')
    
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            UPDATE patients 
            SET name=%s, age=%s, gender=%s, blood_group=%s, phone=%s, address=%s, emergency_contact=%s
            WHERE patient_id=%s
        """, (name, age, gender, blood_group, phone, address, emergency_contact, id))
        conn.commit()
        flash('Patient updated successfully!', 'success')
    except Exception as e:
        conn.rollback()
        flash(f'Error updating patient: {str(e)}', 'danger')
    finally:
        cur.close()
        conn.close()
    return redirect(url_for('patients'))

@app.route('/patients/delete/<int:id>', methods=['POST'])
@login_required
def delete_patient(id):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM patients WHERE patient_id = %s", (id,))
        conn.commit()
        flash('Patient deleted successfully!', 'success')
    except Exception as e:
        conn.rollback()
        flash(f'Error deleting patient: {str(e)}', 'danger')
    finally:
        cur.close()
        conn.close()
    return redirect(url_for('patients'))

# ==========================================
# ROUTES: DOCTORS
# ==========================================
@app.route('/doctors')
@login_required
def doctors():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM doctors ORDER BY doctor_name ASC")
    all_doctors = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('doctors.html', doctors=all_doctors)

@app.route('/doctors/add', methods=['POST'])
@login_required
def add_doctor():
    doctor_name = request.form['doctor_name']
    specialization = request.form['specialization']
    consultation_fee = request.form['consultation_fee']
    phone = request.form['phone']
    
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO doctors (doctor_name, specialization, consultation_fee, phone) VALUES (%s, %s, %s, %s)", 
                    (doctor_name, specialization, consultation_fee, phone))
        conn.commit()
        flash('Doctor added successfully!', 'success')
    except Exception as e:
        conn.rollback()
        flash(f'Error adding doctor: {str(e)}', 'danger')
    finally:
        cur.close()
        conn.close()
    return redirect(url_for('doctors'))

@app.route('/doctors/delete/<int:id>', methods=['POST'])
@login_required
def delete_doctor(id):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM doctors WHERE doctor_id = %s", (id,))
        conn.commit()
        flash('Doctor deleted successfully!', 'success')
    except Exception as e:
        conn.rollback()
        flash(f'Error deleting doctor: {str(e)}', 'danger')
    finally:
        cur.close()
        conn.close()
    return redirect(url_for('doctors'))

# ==========================================
# ROUTES: APPOINTMENTS
# ==========================================
@app.route('/appointments')
@login_required
def appointments():
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Using JOIN to get patient and doctor names
    cur.execute("""
        SELECT a.*, p.name as patient_name, d.doctor_name 
        FROM appointments a
        JOIN patients p ON a.patient_id = p.patient_id
        JOIN doctors d ON a.doctor_id = d.doctor_id
        ORDER BY a.appointment_date DESC
    """)
    all_appointments = cur.fetchall()
    
    # Fetch lists for the Add Appointment modal
    cur.execute("SELECT patient_id, name, phone FROM patients ORDER BY name")
    patients_list = cur.fetchall()
    
    cur.execute("SELECT doctor_id, doctor_name, specialization FROM doctors ORDER BY doctor_name")
    doctors_list = cur.fetchall()
    
    cur.close()
    conn.close()
    
    return render_template('appointments.html', 
                           appointments=all_appointments,
                           patients_list=patients_list,
                           doctors_list=doctors_list)

@app.route('/appointments/add', methods=['POST'])
@login_required
def add_appointment():
    patient_id = request.form['patient_id']
    doctor_id = request.form['doctor_id']
    appointment_date = request.form['appointment_date']
    symptoms = request.form['symptoms']
    
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO appointments (patient_id, doctor_id, appointment_date, symptoms) 
            VALUES (%s, %s, %s, %s)
        """, (patient_id, doctor_id, appointment_date, symptoms))
        conn.commit()
        flash('Appointment booked successfully!', 'success')
    except Exception as e:
        conn.rollback()
        # This will catch our PostgreSQL trigger exception for overlapping appointments
        flash(f'Error booking appointment: {str(e)}', 'danger')
    finally:
        cur.close()
        conn.close()
    return redirect(url_for('appointments'))

@app.route('/appointments/status/<int:id>', methods=['POST'])
@login_required
def update_appointment_status(id):
    status = request.form['status']
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("UPDATE appointments SET status = %s WHERE appointment_id = %s", (status, id))
        conn.commit()
        flash('Status updated!', 'success')
    except Exception as e:
        conn.rollback()
        flash(f'Error: {str(e)}', 'danger')
    finally:
        cur.close()
        conn.close()
    return redirect(url_for('appointments'))

@app.route('/appointments/delete/<int:id>', methods=['POST'])
@login_required
def delete_appointment(id):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM appointments WHERE appointment_id = %s", (id,))
        conn.commit()
        flash('Appointment deleted!', 'success')
    except Exception as e:
        conn.rollback()
        flash(f'Error: {str(e)}', 'danger')
    finally:
        cur.close()
        conn.close()
    return redirect(url_for('appointments'))

# ==========================================
# ROUTES: BILLING & PAYMENTS
# ==========================================
@app.route('/billing')
@login_required
def billing():
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("""
        SELECT b.*, p.name as patient_name
        FROM bills b
        JOIN patients p ON b.patient_id = p.patient_id
        ORDER BY b.bill_date DESC
    """)
    all_bills = cur.fetchall()
    
    cur.execute("SELECT patient_id, name FROM patients ORDER BY name")
    patients_list = cur.fetchall()
    
    cur.close()
    conn.close()
    return render_template('billing.html', bills=all_bills, patients_list=patients_list)

@app.route('/billing/add', methods=['POST'])
@login_required
def add_bill():
    patient_id = request.form['patient_id']
    total_amount = request.form['total_amount']
    
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO bills (patient_id, total_amount) VALUES (%s, %s)", 
                    (patient_id, total_amount))
        conn.commit()
        flash('Bill generated successfully!', 'success')
    except Exception as e:
        conn.rollback()
        flash(f'Error: {str(e)}', 'danger')
    finally:
        cur.close()
        conn.close()
    return redirect(url_for('billing'))

@app.route('/billing/delete/<int:id>', methods=['POST'])
@login_required
def delete_bill(id):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM bills WHERE bill_id = %s", (id,))
        conn.commit()
        flash('Bill deleted!', 'success')
    except Exception as e:
        conn.rollback()
        flash(f'Error: {str(e)}', 'danger')
    finally:
        cur.close()
        conn.close()
    return redirect(url_for('billing'))

@app.route('/payments/add', methods=['POST'])
@login_required
def add_payment():
    bill_id = request.form['bill_id']
    amount_paid = request.form['amount_paid']
    payment_method = request.form['payment_method']
    
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        # The PostgreSQL Trigger (after_payment_insert) will automatically update the bill status!
        cur.execute("""
            INSERT INTO payments (bill_id, amount_paid, payment_method) 
            VALUES (%s, %s, %s)
        """, (bill_id, amount_paid, payment_method))
        conn.commit()
        flash('Payment processed successfully. Bill status automatically updated via Trigger!', 'success')
    except Exception as e:
        conn.rollback()
        flash(f'Error: {str(e)}', 'danger')
    finally:
        cur.close()
        conn.close()
    return redirect(url_for('billing'))

def init_db():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT to_regclass('public.admins');")
        result = cur.fetchone()
        if result['to_regclass'] is None:
            print("Initializing database from SQL files...")
            with open('database/schema.sql', 'r') as f:
                cur.execute(f.read())
            with open('database/advanced.sql', 'r') as f:
                cur.execute(f.read())
            with open('database/dummy_data.sql', 'r') as f:
                cur.execute(f.read())
            conn.commit()
            print("Database initialized successfully.")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Could not connect to or initialize database: {e}")
        print("Please ensure PostgreSQL is running and the 'hospital_db' database is created.")

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
