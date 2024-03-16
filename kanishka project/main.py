from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from datetime import datetime

app = Flask(__name__)

# MySQL configurations
mysql_config = {
    'user': 'root',
    'password': 'kani@123!',
    'host': 'localhost',
    'database': 'admission'
}

# Route for the home page
@app.route('/')
def home():
    return render_template("home.html")

# Route for the achievements page
@app.route('/achievements')
def achievements():
    return render_template("achievements.html")

# Route for the about us page
@app.route('/about_us')
def about_us():
    return render_template("about_us.html")

# Route for the login page
@app.route('/login')
def login():
    return render_template("login.html")

# Route for the admission page
@app.route('/admission', methods=['GET', 'POST'])
def admission():
    if request.method == 'POST':
        try:
            # Fetch form data
            full_name = request.form['fullName']
            email = request.form['email']
            phone = request.form['phone']
            dob = request.form['dob']
            address = request.form['address']
            marks_tamil = request.form['marksTamil']
            marks_english = request.form['marksEnglish']
            marks_mathematics = request.form['marksMathematics']
            marks_science = request.form['marksScience']
            marks_social_science = request.form['marksSocialScience']
            selected_group = request.form['selectedGroup']
            engineering_cutoff = request.form['engineeringCutoff']
            aadhar_number = request.form['aadharNumber']
            pan_number = request.form['panNumber']
            state = request.form['state']
            parent_name = request.form['parentName']
            parent_mobile1 = request.form['parentMobile1']
            parent_mobile2 = request.form.get('parentMobile2', '')
            parent_occupation = request.form['parentOccupation']
            parent_aadhar_number = request.form['parentAadharNumber']
            parent_pan_number = request.form['parentPanNumber']
            parent_annual_income = request.form['parentAnnualIncome']
            parent_email = request.form.get('parentEmail', '')

            # Save the form data into MySQL database
            connection = mysql.connector.connect(**mysql_config)
            cursor = connection.cursor()
            cursor.execute("INSERT INTO registered_users (full_name, email, phone, dob, address, marks_tamil, marks_english, marks_mathematics, marks_science, marks_social_science, selected_group, engineering_cutoff, aadhar_number, pan_number, state, parent_name, parent_mobile1, parent_mobile2, parent_occupation, parent_aadhar_number, parent_pan_number, parent_annual_income, parent_email, filled_time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                            (full_name, email, phone, dob, address, marks_tamil, marks_english, marks_mathematics, marks_science, marks_social_science, selected_group, engineering_cutoff, aadhar_number, pan_number, state, parent_name, parent_mobile1, parent_mobile2, parent_occupation, parent_aadhar_number, parent_pan_number, parent_annual_income, parent_email, datetime.now()))
            connection.commit()
            cursor.close()
            connection.close()

            return redirect(url_for('registered_users'))
        except Exception as e:
            return render_template("error.html", message=str(e))
    else:
        return render_template("admission.html")

# Route for the registered users page
@app.route('/registered_users')
def registered_users():
    try:
        connection = mysql.connector.connect(**mysql_config)
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM registered_users")
        users = cursor.fetchall()
        cursor.close()
        connection.close()
        return render_template("registered_users.html", users=users)
    except Exception as e:
        return render_template("error.html", message=str(e))


if __name__ == "__main__":
    app.run(debug=True)
