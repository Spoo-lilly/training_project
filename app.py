from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('participants.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS participants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            city TEXT,
            country TEXT,
            phone TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def main():
    return render_template('main.html')

@app.route('/add', methods=['GET', 'POST'])
def add_participant():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        city = request.form.get('city', '')
        country = request.form.get('country', '')
        phone = request.form.get('phone', '')

        conn = sqlite3.connect('participants.db')
        c = conn.cursor()
        try:
            c.execute('INSERT INTO participants (name, email, city, country, phone) VALUES (?, ?, ?, ?, ?)', 
                      (name, email, city, country, phone))
            conn.commit()
        except sqlite3.IntegrityError:
            pass  # Handle duplicate email error
        conn.close()
        return redirect(url_for('main'))
    return render_template('add_participant.html')

@app.route('/view')
def view_participants():
    conn = sqlite3.connect('participants.db')
    c = conn.cursor()
    c.execute('SELECT * FROM participants')
    participants = c.fetchall()
    conn.close()
    return render_template('view_participants.html', participants=participants)

@app.route('/delete', methods=['GET', 'POST'])
def delete_participant():
    if request.method == 'POST':
        email_to_delete = request.form['email_to_delete']
        conn = sqlite3.connect('participants.db')
        c = conn.cursor()
        c.execute('DELETE FROM participants WHERE email = ?', (email_to_delete,))
        conn.commit()
        conn.close()
        return redirect(url_for('main'))
    return render_template('delete_participant.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
