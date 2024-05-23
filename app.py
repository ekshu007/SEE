from flask import Flask, render_template, request, redirect, url_for, g
import sqlite3

app = Flask(__name__)

DATABASE = 'ecommerce.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()

        cursor.execute('DROP TABLE IF EXISTS cart;')
        cursor.execute('DROP TABLE IF EXISTS products;')

        cursor.execute('''
            CREATE TABLE products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                price REAL,
                image TEXT
            );
        ''')

        cursor.execute('''
            CREATE TABLE cart (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER,
                FOREIGN KEY (product_id) REFERENCES products (id)
            );
        ''')

        cursor.executemany('''
            INSERT INTO products (name, description, price, image) VALUES (?, ?, ?, ?);
        ''', [
            ('Product 1', 'Description of Product 1', 19.99, 'product1.jpg'),
            ('Product 2', 'Description of Product 2', 29.99, 'product2.jpg'),
            ('Product 3', 'Description of Product 3', 39.99, 'product3.jpg')
        ])

        db.commit()


@app.route('/')
def index():
    db = get_db()
    try:
        cur = db.execute('SELECT * FROM products')
        products = cur.fetchall()
        return render_template('index.html', products=products)
    except sqlite3.Error as e:
        print("An error occurred:", e.args[0])
        return "An error occurred while retrieving products."

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    try:
        product_id = request.form['product_id']
        db = get_db()
        db.execute('INSERT INTO cart (product_id) VALUES (?)', [product_id])
        db.commit()
        return redirect(url_for('index'))
    except sqlite3.Error as e:
        print("An error occurred:", e.args[0])
        return "An error occurred while adding to cart."

@app.route('/cart')
def cart():
    db = get_db()
    try:
        cur = db.execute('SELECT p.id, p.name, p.description, p.price, p.image FROM cart c JOIN products p ON c.product_id = p.id')
        products = cur.fetchall()
        return render_template('cart.html', products=products)
    except sqlite3.Error as e:
        print("An error occurred:", e.args[0])
        return "An error occurred while retrieving cart."

@app.route('/clear_cart')
def clear_cart():
    try:
        db = get_db()
        db.execute('DELETE FROM cart')
        db.commit()
        return redirect(url_for('cart'))
    except sqlite3.Error as e:
        print("An error occurred:", e.args[0])
        return "An error occurred while clearing cart."

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
