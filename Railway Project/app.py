from flask import Flask, render_template, request, redirect, url_for,session,flash,jsonify
from flask_session import Session
import pymysql

app = Flask(__name__)

app.secret_key = 'your_secret_key'

# MySQL configuration (Replace with your MySQL details)
DB_HOST = 'sql6.freesqldatabase.com'
DB_USER = 'sql6634252'
DB_PASSWORD = 'vwwjYCVGq5'
DB_NAME = 'sql6634252'

@app.route('/')
def start():
    return render_template('index.html')

@app.route('/entry_login')
def entry_login():
    return render_template('entry_login.html')

@app.route('/rem_login')
def rem_login():
    return render_template('remove_login.html')

@app.route('/login', methods=['POST'])
def login():
    try:
        # Get username and password from the form
        username = request.form['username']
        password = request.form['password']

        # Establish a connection to the database
        connection = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
        
        # Create a cursor object to execute queries
        cursor = connection.cursor()
        
        # Query to check the provided username and password against the table
        query = "SELECT * FROM Entry_Login_Details WHERE username=%s AND password=%s;"
        
        # Execute the query with the provided username and password
        cursor.execute(query, (username, password))
        
        # Fetch the result
        result = cursor.fetchone()
        
        # Close the cursor and connection
        cursor.close()
        connection.close()
        
        if result:
            # Authentication successful, store the username in the session
            session['username'] = username
            # Redirect to the dashboard
            return redirect(url_for('entry'))
        else:
            flash("Invalid credentials. Please try again.", "error")
            return redirect(url_for('entry_login'))
        
            
    
    except pymysql.Error as e:
        # Handle any potential errors
        return "Error: {}".format(e)
    
@app.route('/remove_login', methods=['POST'])
def remove_login():
    try:
        # Get username and password from the form
        username1 = request.form['username1']
        password1 = request.form['password1']

        # Establish a connection to the database
        connection = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
        
        # Create a cursor object to execute queries
        cursor = connection.cursor()
        
        # Query to check the provided username and password against the table
        query = "SELECT * FROM Entry_Login_Details WHERE username=%s AND password=%s;"
        
        # Execute the query with the provided username and password
        cursor.execute(query, (username1, password1))
        
        # Fetch the result
        result = cursor.fetchone()
        
        # Close the cursor and connection
        cursor.close()
        connection.close()
        
        if result:
            # Authentication successful, store the username in the session
            session['username1'] = username1
            # Redirect to the dashboard
            return redirect(url_for('remove'))
        else:
            flash("Invalid credentials. Please try again.", "error")
            return redirect(url_for('remove_login'))
        
            
    
    except pymysql.Error as e:
        # Handle any potential errors
        return "Error: {}".format(e)

@app.route('/entry')
def entry():
    # Check if the user is logged in
    if 'username' in session:
       return render_template('entry.html')
    else:
        # If the user is not logged in, redirect to the login page
        return redirect(url_for('entry_login'))
    
@app.route('/remove')
def remove():
    # Check if the user is logged in
    if 'username1' in session:
       return render_template('remove.html')
    else:
        # If the user is not logged in, redirect to the login page
        return redirect(url_for('remove_login'))
    
def aadhar_exists(aadhar_number):
    try:
        # Establish a connection to the database
        connection = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
        
        # Create a cursor object to execute queries
        cursor = connection.cursor()
        
        # Query to check if Aadhar number exists in the table
        query = "SELECT * FROM Employee WHERE AadharNo=%s;"
        
        # Execute the query with the provided Aadhar number
        cursor.execute(query, (aadhar_number,))
        
        # Fetch the result
        result = cursor.fetchone()
        
        # Close the cursor and connection
        cursor.close()
        connection.close()
        
        return result is not None  # Returns True if Aadhar number exists in the database, False otherwise
    
    except pymysql.Error as e:
        # Handle any potential errors
        print("Error: {}".format(e))
        return False

@app.route('/check_aadhar', methods=['POST'])
def check_aadhar():
    aadhar_number = request.form['aadhar_number']
    exists = aadhar_exists(aadhar_number)
    return jsonify({'exists': exists})


@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    return redirect(url_for('entry_login'))

@app.route('/logout_remove', methods=['POST'])
def logout_remove():
    session.pop('username1', None)
    return redirect(url_for('rem_login'))

@app.route('/submit_entry', methods=['POST'])
def submit_entry():
    # Check if the user is logged in
    if 'username' in session:
        try:
            # Get form data
            name = request.form['name']
            father_name = request.form['father_name']
            aadhar_no = request.form['aadhar_no']
            p_address= request.form['p_address']
            c_address=request.form['c_address']
            r_id=request.form['r_id']
            contractor=request.form['contractor']
            designation=request.form['designation']
            zone=request.form['zone']
            division=request.form['division']
            depot=request.form['depot']
            contract=request.form['contract']
            working_from=request.form['working_from']
            username = session['username']

            # Establish a connection to the database
            connection = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)

            # Create a cursor object to execute queries
            cursor = connection.cursor()

            # Query to insert data into the Employee table
            query = "INSERT INTO Employee (Name, FatherName, AadharNo, PermanentAddress, CorrespondenceAddress, RailwayIDNo, Contractor, Designation, Zone, Division, Depot, Contract, WorkingFrom, Entered_by) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"

            # Execute the query with the form data
            cursor.execute(query, (name, father_name, aadhar_no, p_address, c_address, r_id, contractor, designation, zone, division, depot, contract, working_from, username))

            # Commit the changes to the database
            connection.commit()

            # Close the cursor and connection
            cursor.close()
            connection.close()

            flash("Data successfully submitted!", "success")

            # Redirect to the entry page
            return redirect(url_for('entry'))

        except pymysql.Error as e:
            # Handle any potential errors
            return "Error: {}".format(e)

    else:
        # If the user is not logged in, redirect to the login page
        return redirect(url_for('entry_login'))



if __name__ == '__main__':
    app.run(debug=False, port='0.0.0.0')