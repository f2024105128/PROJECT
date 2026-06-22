import sqlite3
import random

def seed_database():
    connection = sqlite3.connect('instance/ecommerce.db')
    cursor = connection.cursor()

    # Table create karne ki query
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS product (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            image TEXT NOT NULL
        )
    """)

    cursor.execute("DELETE FROM product")

    product_names = [
        "Coffee Mug", "Laptop Stand", "Wireless Mouse", "Gaming Keyboard",
        "Bluetooth Speaker", "Smart Watch", "Phone Case", "Desk Lamp",
        "Water Bottle", "Headphones", "Backpack", "USB Hub",
        "Monitor", "Power Bank", "Notebook", "Office Chair",
        "Webcam", "Microphone", "Tablet", "Printer"
    ]

    products = []

    for i in range(1, 21):
        name = random.choice(product_names) + f" {i}"
        price = round(random.uniform(10, 500), 2)
        image = f"https://picsum.photos/300/200?random={i}"
        
        products.append((name, price, image))

    cursor.executemany("""
        INSERT INTO product (name, price, image)
        VALUES (?, ?, ?)
    """, products)

    connection.commit()
    connection.close()

    print("20 random products added successfully!")

if __name__ == "__main__":
    seed_database()