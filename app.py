from flask import Flask, render_template, request, redirect
import psycopg2
import os

app = Flask(__name__)

# Connect to the Database
def get_db_connection():
    conn = psycopg2.connect(os.environ['DATABASE_URL'], sslmode='require')
    return conn

# Setup database tables
def setup_db():
    conn = get_db_connection()
    c = conn.cursor()

    # Create categories table
    c.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id SERIAL PRIMARY KEY,
            name TEXT UNIQUE NOT NULL,
            image TEXT
        );
    ''')

    # Create locations table
    c.execute('''
        CREATE TABLE IF NOT EXISTS locations (
            id SERIAL PRIMARY KEY,
            name TEXT UNIQUE NOT NULL,
            image TEXT
        );
    ''')

    # Create Storage Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS storage (
            id SERIAL PRIMARY KEY,
            item TEXT NOT NULL,
            location_id INTEGER REFERENCES locations(id),
            spot TEXT,
            notes TEXT,
            category_id INTEGER REFERENCES categories(id),
            image TEXT
        );
    ''')

    # Insert initial categories
    c.execute("INSERT INTO categories (name) VALUES ('Altro') ON CONFLICT (name) DO NOTHING;")
    c.execute("INSERT INTO categories (name) VALUES ('Viaggio') ON CONFLICT (name) DO NOTHING;")
    c.execute("INSERT INTO categories (name) VALUES ('Vestiti') ON CONFLICT (name) DO NOTHING;")

    # Insert initial locations
    c.execute("INSERT INTO locations (name) VALUES ('Solaio Nonno') ON CONFLICT (name) DO NOTHING;")
    c.execute("INSERT INTO locations (name) VALUES ('Garage Tatona') ON CONFLICT (name) DO NOTHING;")
    c.execute("INSERT INTO locations (name) VALUES ('Garage Tatina') ON CONFLICT (name) DO NOTHING;")
    c.execute("INSERT INTO locations (name) VALUES ('Solaio Nostro') ON CONFLICT (name) DO NOTHING;")

    conn.commit()
    c.close()
    conn.close()

# Run the setup when app starts
setup_db()

# Home page
@app.route('/', methods=['GET', 'POST'])
def index():
    conn = get_db_connection()
    cur = conn.cursor()

    # Fetch categories and locations
    cur.execute('SELECT id, name FROM categories ORDER BY name')
    categories = cur.fetchall()

    cur.execute('SELECT id, name FROM locations ORDER BY name')
    locations = cur.fetchall()

    if request.method == 'POST':
        item = request.form['item']
        location_id = request.form['location']
        spot = request.form['spot']
        notes = request.form['notes']
        category_id = request.form['category']
        image = request.form['image'] or None

        cur.execute('''
            INSERT INTO storage (item, location_id, spot, notes, category_id)
            VALUES (%s, %s, %s, %s, %s)
        ''', (item, location_id, spot, notes, category_id))

        conn.commit()
        cur.close()
        conn.close()
        return redirect('/list')

    cur.close()
    conn.close()
    return render_template('index.html', categories=categories, locations=locations)

# List page
@app.route('/list')
def list_items():
    q = request.args.get('q', '')
    location_filter = request.args.get('location', '')
    reset = request.args.get('reset', '')

    if reset:
        q = ''
        location_filter = ''

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute('SELECT id, name FROM locations ORDER BY name')
    locations = cur.fetchall()

    query = '''
        SELECT storage.id, storage.item, storage.spot, storage.notes,
               categories.name AS category_name,
               locations.name AS location_name
        FROM storage
        LEFT JOIN categories ON storage.category_id = categories.id
        LEFT JOIN locations ON storage.location_id = locations.id
    '''
    params = []
    where_clauses = []

    if q:
        where_clauses.append("(storage.item ILIKE %s OR storage.notes ILIKE %s OR locations.name ILIKE %s)")
        params += [f'%{q}%', f'%{q}%', f'%{q}%']

    if location_filter:
        where_clauses.append("storage.location_id = %s")
        params.append(location_filter)

    if where_clauses:
        query += ' WHERE ' + ' AND '.join(where_clauses)

    query += ' ORDER BY storage.item ASC'

    cur.execute(query, params)
    items = cur.fetchall()

    cur.close()
    conn.close()

    return render_template('list.html', items=items, locations=locations, 
                           location_filter=location_filter, search_query=q)

@app.route('/edit/<int:item_id>', methods=['GET', 'POST'])
def edit_item(item_id):
    conn = get_db_connection()
    c = conn.cursor()

    c.execute('SELECT * FROM categories ORDER BY name')
    categories = c.fetchall()

    c.execute('SELECT * FROM locations ORDER BY name')
    locations = c.fetchall()
    
    if request.method == 'POST':
        item = request.form['item']
        location_id = request.form['location']
        spot = request.form['spot']
        notes = request.form['notes']
        category_id = request.form['category']
        image = request.form['image'] or None

        c.execute('''
            UPDATE storage
            SET item = %s, location_id = %s, spot = %s, notes = %s, category_id = %s
            WHERE id = %s
        ''', (item, location_id, spot, notes, category_id, item_id))

        conn.commit()
        conn.close()
        return redirect('/list')
    
    c.execute('SELECT * FROM storage WHERE id = %s', (item_id,))
    item = c.fetchone()
    conn.close

    return render_template('edit.html', item=item, categories=categories, locations=locations)

@app.route('/delete/<int:item_id>')
def delete_item(item_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('DELETE FROM storage WHERE id = %s', (item_id,))
    conn.commit()
    conn.close()
    return redirect('/list')

# Route to display categories and manage them
@app.route('/manage_categories')
def manage_categories():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM categories ORDER BY name')
    categories = c.fetchall()
    conn.close()
    return render_template('manage_categories.html', categories=categories)

# Route to manage adding categories
@app.route('/add_category', methods=['POST'])
def add_category():
    name = request.form['category']
    image = request.form['image'] or None
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO categories (name, image) VALUES (%s) ON CONFLICT (name) DO NOTHING;', (name, image))
    conn.commit()
    conn.close()
    return redirect('/manage_categories')

# Route to delete a category
@app.route('/delete_category/<int:category_id>')
def delete_category(category_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('DELETE FROM categories WHERE id = %s', (category_id,))
    conn.commit()
    conn.close()
    return redirect('/manage_categories')


# Route to display locations and manage them
@app.route('/manage_locations')
def manage_locations():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM locations ORDER BY name')
    locations = c.fetchall()
    conn.close()
    return render_template('manage_locations.html', locations=locations)

# Route to manage adding locations
@app.route('/add_location', methods=['POST'])
def add_location():
    name = request.form['location']
    image = request.form['image'] or None
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO locations (name, image) VALUES (%s) ON CONFLICT (name) DO NOTHING;', (name, image))
    conn.commit()
    conn.close()
    return redirect('/manage_locations')

# Route to delete a location
@app.route('/delete_location/<int:location_id>')
def delete_location(location_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('DELETE FROM locations WHERE id = %s', (location_id,))
    conn.commit()
    conn.close()
    return redirect('/manage_locations')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)