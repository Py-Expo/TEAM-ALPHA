from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

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
            marks_10 = request.form['marks10']
            marks_11 = request.form['marks11']
            marks_12 = request.form['marks12']
            percentage = request.form['percentage']
            selected_course = request.form['selectedCourse']
            engineering_cutoff = request.form['engineeringCutoff']

            # Save the form data into MySQL database
            connection = mysql.connector.connect(**mysql_config)
            cursor = connection.cursor()
            cursor.execute("INSERT INTO registered_users (full_name, email, phone, dob, address, selected_course) VALUES (%s, %s, %s, %s, %s, %s)",
                        (full_name, email, phone, dob, address, selected_course))
            connection.commit()
            cursor.close()
            connection.close()
            return redirect(url_for('registered_users'))
        except Exception as e:
            return render_template("error.html", message=str(e))
    else:
        return render_template("admission.html")

# Route for the login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Process login form data here
        return redirect(url_for('home'))
    return render_template("login.html")

# Route for the logout page
@app.route('/logout')
def logout():
    # Process logout here
    return redirect(url_for('home'))

# Route for the registered users page
@app.route('/registered_users')
def registered_users():
    try:
        connection = mysql.connector.connect(**mysql_config)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM registered_users")
        users = cursor.fetchall()
        cursor.close()
        connection.close()
        return render_template("registered_users.html", users=users)
    except Exception as e:
        return render_template("error.html", message=str(e))


if __name__ == "__main__":
    app.run(debug=True)
