from flask import Flask, jsonify, send_file, request
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

# DB connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="soluser",
        password="1234",  # <-- PUT YOUR PASSWORD
        database="campus_resource_db"
    )

# Home route
@app.route('/')
def home():
    return "Campus Resource Analyzer Running 🚀"

# =========================
# GET SESSIONS
# =========================
@app.route('/sessions')
def sessions():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
    SELECT 
        s.session_id,
        d.dept_name,
        r.resource_name,
        s.start_time,
        s.end_time
    FROM Usage_Session s
    JOIN Department d ON s.dept_id = d.dept_id
    JOIN Resource r ON s.resource_id = r.resource_id
    """)

    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

# =========================
# GET CONFLICTS
# =========================
@app.route('/conflicts')
def conflicts():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
    SELECT 
        c.conflict_id,
        d1.dept_name AS dept1,
        d2.dept_name AS dept2,
        s1.start_time AS start1,
        s1.end_time AS end1,
        s2.start_time AS start2,
        s2.end_time AS end2,
        r.resource_name
    FROM Conflict c
    JOIN Usage_Session s1 ON c.session1_id = s1.session_id
    JOIN Usage_Session s2 ON c.session2_id = s2.session_id
    JOIN Department d1 ON s1.dept_id = d1.dept_id
    JOIN Department d2 ON s2.dept_id = d2.dept_id
    JOIN Resource r ON c.resource_id = r.resource_id
    """)

    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

# =========================
# ADD SESSION (NEW FEATURE)
# =========================
@app.route('/add_session', methods=['POST'])
def add_session():
    data = request.json

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO Usage_Session (dept_id, resource_id, start_time, end_time)
    VALUES (%s, %s, %s, %s)
    """, (
        data['dept_id'],
        data['resource_id'],
        data['start_time'],
        data['end_time']
    ))

    conn.commit()
    cursor.close()
    conn.close()

    return {"message": "Session added successfully"}

# =========================
# UI ROUTE
# =========================
@app.route('/ui')
def ui():
    return send_file('index.html')

# =========================
# RUN SERVER
# =========================
if __name__ == '__main__':
    app.run(debug=True)
