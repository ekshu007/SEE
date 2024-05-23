from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# Connect to database (create if it doesn't exist)
conn = sqlite3.connect('products.db')
c = conn.cursor()

# Create table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY, name TEXT, price REAL)''')

# Sample data (replace with your own)
products = [
    ("T-Shirt", 19.99),
    ("Mug", 9.99),
    ("Notebook", 14.99)
]

# Insert sample data
for name, price in products:
    c.execute("INSERT INTO products (name, price) VALUES (?, ?)", (name, price))

conn.commit()
conn.close()

@app.route('/')
def home():
    # Connect to database
    conn = sqlite3.connect('products.db')
    c = conn.cursor()

    # Get all products
    c.execute("SELECT * FROM products")
    data = c.fetchall()

    # Close connection
    conn.close()

    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
