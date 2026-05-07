from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# Initialize Database
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute('''
    CREATE TABLE IF NOT EXISTS plants (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        color TEXT,
        plant_type TEXT,
        medicinal_use TEXT,
        days_to_grow TEXT
    )
    ''')

    vegetables = [
        ("Tomato", "Red", "Vegetable", "Rich in antioxidants and good for heart health", "60-80 days"),
        ("Carrot", "Orange", "Root Vegetable", "Improves eyesight and skin health", "70-80 days"),
        ("Potato", "Brown", "Tuber Vegetable", "Provides energy and supports digestion", "90-120 days"),
        ("Onion", "Purple/White", "Bulb Vegetable", "Boosts immunity and controls blood sugar", "90-120 days"),
        ("Spinach", "Green", "Leafy Vegetable", "Rich in iron and improves blood health", "40-50 days"),
        ("Cabbage", "Green/Purple", "Leafy Vegetable", "Improves digestion and immunity", "70-100 days"),
        ("Cauliflower", "White", "Flower Vegetable", "Good for brain and heart health", "80-120 days"),
        ("Brinjal", "Purple", "Vegetable", "Helps control cholesterol", "80-100 days"),
        ("Lady Finger", "Green", "Vegetable", "Improves digestion and controls diabetes", "50-65 days"),
        ("Beetroot", "Dark Red", "Root Vegetable", "Improves blood circulation", "55-70 days"),
        ("Radish", "White/Red", "Root Vegetable", "Good for liver and digestion", "30-50 days"),
        ("Pumpkin", "Orange", "Vegetable", "Boosts eye health and immunity", "90-120 days"),
        ("Bottle Gourd", "Light Green", "Vegetable", "Good for weight loss and hydration", "60-80 days"),
        ("Bitter Gourd", "Green", "Vegetable", "Helps control diabetes", "55-70 days"),
        ("Green Peas", "Green", "Legume Vegetable", "Rich in protein and fiber", "60-70 days"),
        ("Capsicum", "Green/Red/Yellow", "Vegetable", "Boosts immunity with vitamin C", "60-90 days"),
        ("Cucumber", "Green", "Vegetable", "Keeps body hydrated", "50-70 days"),
        ("Drumstick", "Green", "Tree Vegetable", "Rich in calcium and iron", "180-240 days"),
        ("Corn", "Yellow", "Grain Vegetable", "Provides energy and fiber", "60-100 days"),
        ("Garlic", "White", "Bulb Vegetable", "Improves immunity and heart health", "120-150 days")
    ]

    fruits = [
        ("Apple", "Red/Green", "Fruit", "Good for heart and digestion", "4-5 years"),
        ("Banana", "Yellow", "Fruit", "Improves digestion and energy", "240-300 days"),
        ("Mango", "Green/Yellow", "Fruit", "Boosts immunity and skin health", "3-5 years"),
        ("Orange", "Orange", "Citrus Fruit", "Rich in vitamin C", "3-4 years"),
        ("Grapes", "Green/Purple", "Fruit", "Improves heart health", "2-3 years"),
        ("Pineapple", "Yellow", "Tropical Fruit", "Improves digestion", "18-24 months"),
        ("Papaya", "Yellow/Orange", "Tropical Fruit", "Good for digestion and skin", "6-12 months"),
        ("Watermelon", "Green/Red", "Fruit", "Keeps body hydrated", "80-100 days"),
        ("Guava", "Green", "Fruit", "Boosts immunity and digestion", "2-4 years"),
        ("Pomegranate", "Red", "Fruit", "Improves blood circulation", "2-3 years"),
        ("Strawberry", "Red", "Berry Fruit", "Rich in antioxidants", "90-120 days"),
        ("Blueberry", "Blue", "Berry Fruit", "Improves brain health", "2-3 years"),
        ("Cherry", "Red", "Fruit", "Reduces inflammation", "3-5 years"),
        ("Kiwi", "Brown/Green", "Fruit", "Rich in vitamin C and fiber", "3-5 years"),
        ("Lemon", "Yellow", "Citrus Fruit", "Improves immunity and digestion", "2-3 years"),
        ("Custard Apple", "Green", "Fruit", "Good for weight gain and energy", "3-4 years"),
        ("Sapota", "Brown", "Fruit", "Provides energy and improves digestion", "5-8 years"),
        ("Jackfruit", "Green", "Tropical Fruit", "Rich in fiber and energy", "3-5 years"),
        ("Pear", "Green/Yellow", "Fruit", "Good for digestion and heart", "4-6 years"),
        ("Lychee", "Red", "Tropical Fruit", "Boosts immunity", "3-5 years")
    ]

    plants = vegetables + fruits

    c.execute("SELECT COUNT(*) FROM plants")
    count = c.fetchone()[0]

    if count == 0:
        c.executemany('''
        INSERT INTO plants(name, color, plant_type, medicinal_use, days_to_grow)
        VALUES (?, ?, ?, ?, ?)
        ''', plants)

    conn.commit()
    conn.close()


@app.route('/', methods=['GET', 'POST'])
def index():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT name FROM plants")
    all_plants = [row[0] for row in c.fetchall()]
    conn.close()
    
    plants = []
    search_query = ''
    if request.method == 'POST':
        search_query = request.form.get('search', '').strip()
        if search_query:
            conn = sqlite3.connect('database.db')
            c = conn.cursor()
            c.execute("SELECT id, name, plant_type FROM plants WHERE name LIKE ?", ('%' + search_query + '%',))
            plants = c.fetchall()
            conn.close()
    
    return render_template('index.html', all_plants=all_plants, plants=plants, search_query=search_query)

@app.route('/plant/<int:plant_id>')
def plant_detail(plant_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM plants WHERE id=?", (plant_id,))
    plant = c.fetchone()
    conn.close()
    if plant:
        return render_template('detail.html', plant=plant)
    else:
        return "Plant not found", 404


if __name__ == '__main__':
    init_db()
    app.run(debug=True)