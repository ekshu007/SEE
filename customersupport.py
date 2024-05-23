from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def create_connection():
    conn = sqlite3.connect('inquiries.db')
    return conn

def create_table(conn):
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS inquiries
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      name TEXT NOT NULL,
                      email TEXT NOT NULL,
                      mobile TEXT NOT NULL,
                      query_type TEXT NOT NULL,
                      message TEXT NOT NULL)''')
    conn.commit()
    cursor.close()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/contact-us', methods=['GET', 'POST'])
def contact_us():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        mobile = request.form['mobile']
        query_type = request.form['query_type']
        message = request.form['message']
        
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO inquiries (name, email, mobile, query_type, message)
                          VALUES (?, ?, ?, ?, ?)''', (name, email, mobile, query_type, message))
        conn.commit()
        conn.close()

        return redirect(url_for('thank_you'))
    return render_template('contact_us.html')

@app.route('/thank-you')
def thank_you():
    return render_template('thank_you.html')

if __name__ == '__main__':
    create_table(create_connection())  # Create the database table if it doesn't exist
    app.run(debug=True)
