from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Database setup and population
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS diseases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            symptoms TEXT NOT NULL,
            treatment TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS medications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            usage TEXT NOT NULL,
            before TEXT,
            after TEXT
        )
    ''')

    # Insert sample data
    cursor.execute('''
        INSERT INTO diseases (name, description, symptoms, treatment)
        VALUES 
        ('Diabetes', 'A chronic condition that affects the way the body processes blood sugar.', 
        'Increased thirst, frequent urination, extreme hunger', 
        'Insulin therapy, dietary changes, exercise'),

        ('Hypertension', 'A condition in which the force of the blood against the artery walls is too high.', 
        'Headaches, shortness of breath, nosebleeds', 
        'Lifestyle changes, medications'),

        ('Asthma', 'A condition in which your airways narrow and swell and may produce extra mucus.', 
        'Shortness of breath, chest tightness, wheezing', 
        'Inhalers, avoiding triggers, long-term medications')
    ''')

    cursor.execute('''
        INSERT INTO medications (name, usage, before, after)
        VALUES 
        ('Metformin', 'Used to control blood sugar levels in patients with type 2 diabetes.', 
        'Take with a meal to reduce stomach upset.', 
        'Avoid drinking large amounts of alcohol.'),

        ('Lisinopril', 'Used to treat high blood pressure (hypertension).', 
        'Check your blood pressure regularly.', 
        'Stay hydrated and avoid potassium supplements.'),

        ('Albuterol', 'Used to treat wheezing and shortness of breath caused by breathing problems.', 
        'Use only as prescribed by your doctor.', 
        'Rinse your mouth after using the inhaler.')
    ''')

    conn.commit()
    conn.close()

# Initialize the database at startup
init_db()

# Flask Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/diseases')
def diseases():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM diseases')
    diseases = cursor.fetchall()

    conn.close()

    return render_template('diseases.html', diseases=diseases)

@app.route('/disease/<int:disease_id>')
def disease(disease_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM diseases WHERE id = ?', (disease_id,))
    disease = cursor.fetchone()

    conn.close()

    return render_template('disease.html', disease=disease)

@app.route('/medications')
def medications():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM medications')
    medications = cursor.fetchall()

    conn.close()

    return render_template('medications.html', medications=medications)

@app.route('/medication/<int:medication_id>')
def medication(medication_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM medications WHERE id = ?', (medication_id,))
    medication = cursor.fetchone()

    conn.close()

    return render_template('medication.html', medication=medication)

@app.route('/quiz/<int:disease_id>', methods=['GET', 'POST'])
def quiz(disease_id):
    if request.method == 'POST':
        score = int(request.form['score'])
        user = "Anonymous"  # In real scenarios, use authenticated user data

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute('INSERT INTO user_progress (user, topic, score) VALUES (?, ?, ?)', (user, f'Disease {disease_id}', score))
        conn.commit()
        conn.close()

        return redirect(url_for('result'))

    return render_template('quiz.html')

@app.route('/result')
def result():
    return render_template('result.html')

if __name__ == '__main__':
    app.run(debug=True)
