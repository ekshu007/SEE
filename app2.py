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

        while True:
            name = input("Enter product name (or leave blank to stop adding products): ")
            if not name:
                break
            description = input("Enter product description: ")
            price = float(input("Enter product price: "))
            image = input("Enter product image filename: ")

            cursor.execute('''
                INSERT INTO products (name, description, price, image) VALUES (?, ?, ?, ?);
            ''', (name, description, price, image))

            db.commit()

        print("Products added successfully.")
