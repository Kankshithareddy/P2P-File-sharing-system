from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask import send_file
import sqlite3
import os
import mimetypes  # For detecting file type
import logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management

DATABASE = 'peer_network.db'

def create_database():
    """Create SQLite database and tables if they don't exist."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    ''')

    # Shared files table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS shared_files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            filepath TEXT,
            filesize INTEGER,
            filetype TEXT,
            FOREIGN KEY(username) REFERENCES users(username)
        )
    ''')

    conn.commit()
    conn.close()

create_database()  # Ensure database is created on server start


def query_db(query, args=(), one=False):
    """Helper function to query the database."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(query, args)
    rows = cursor.fetchall()
    conn.commit()
    conn.close()
    return (rows[0] if rows else None) if one else rows


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    
    existing_user = query_db('SELECT * FROM users WHERE username = ?', [username], one=True)
    if existing_user:
        flash('Username already exists! Try a different one.')
        return redirect(url_for('index'))
    
    query_db('INSERT INTO users (username, password) VALUES (?, ?)', [username, password])
    flash('Registration successful! Please log in.')
    return redirect(url_for('index'))


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    user = query_db('SELECT * FROM users WHERE username = ? AND password = ?', [username, password], one=True)
    if user:
        session['username'] = username
        flash('Login successful!')
        return redirect(url_for('dashboard'))
    else:
        flash('Invalid username or password.')
        return redirect(url_for('index'))


@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        flash('Please log in first!')
        return redirect(url_for('index'))
    return render_template('dashboard.html', username=session['username'])


@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.')
    return redirect(url_for('index'))

@app.route('/share', methods=['POST'])
def share_file():
    if 'username' not in session:
        flash('Please log in first!')
        return redirect(url_for('index'))
    
    username = session['username']
    filepath = request.form['filepath'].strip()

    # Remove any extra quotation marks
    filepath = filepath.strip('"\'')
    
    filepath = os.path.normpath(filepath)

    # Comprehensive file validation
    if not os.path.exists(filepath):
        flash(f'File not found: {filepath}')
        return redirect(url_for('dashboard'))
    
    if not os.path.isfile(filepath):
        flash(f'Not a valid file: {filepath}')
        return redirect(url_for('dashboard'))

    try:
        with open(filepath, 'rb') as file:
            filesize = os.path.getsize(filepath)
            filetype = mimetypes.guess_type(filepath)[0] or 'Unknown'

        query_db('''
            INSERT INTO shared_files (username, filepath, filesize, filetype) 
            VALUES (?, ?, ?, ?)
        ''', [username, filepath, filesize, filetype])
        
        flash('File shared successfully!')
        return redirect(url_for('dashboard'))
    
    except PermissionError:
        flash(f'Permission denied for file: {filepath}')
    except IOError as e:
        flash(f'Error accessing file: {str(e)}')
    
    return redirect(url_for('dashboard'))


@app.route('/search', methods=['GET'])
def search_files():
    if 'username' not in session:
        flash('Please log in first!')
        return redirect(url_for('index'))
    
    query = request.args.get('query', '')
    results = query_db('''
        SELECT id, username, filepath, filesize, filetype 
        FROM shared_files 
        WHERE filepath LIKE ? OR filetype LIKE ?
    ''', [f'%{query}%', f'%{query}%'])

    return render_template('search.html', results=results, query=query)

@app.route('/download/<int:file_id>')
def download_file(file_id):
    if 'username' not in session:
        flash('Please log in first!')
        return redirect(url_for('index'))
    
    # Retrieve file details from database
    file_details = query_db('SELECT filepath FROM shared_files WHERE id = ?', [file_id], one=True)
    
    if not file_details:
        flash('File not found!')
        return redirect(url_for('search_files'))
    
    filepath = file_details[0]
    
    # Security check: Ensure the file exists and is readable
    if not os.path.isfile(filepath):
        flash('File does not exist or is not accessible.')
        return redirect(url_for('search_files'))
    
    try:
        return send_file(filepath, as_attachment=True)
    except Exception as e:
        flash(f'Error downloading file: {str(e)}')
        return redirect(url_for('search_files'))
if __name__ == '__main__':
    app.run(debug=True)
