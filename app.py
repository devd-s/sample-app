from flask import Flask, request, jsonify, render_template_string
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Database configuration
def get_db_config():
    db_user = os.environ['DB_USER']
    db_password = os.environ['DB_PASSWORD']
    db_host = os.environ['DB_HOST']
    db_name = os.environ['DB_NAME']
    return f'postgresql://{db_user}:{db_password}@{db_host}/{db_name}'

app.config['SQLALCHEMY_DATABASE_URI'] = get_db_config()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Add this block to test the database connection
with app.app_context():
    try:
        db.engine.connect()
        print("Successfully connected to the database!")
    except SQLAlchemyError as e:
        print("Failed to connect to the database. Error:", str(e))


# Define a simple model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

# Create tables
with app.app_context():
    db.create_all()

# HTML template
HTML = '''
<!doctype html>
<html>
    <head>
        <title>User Management</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 0; padding: 20px; }
            h1 { color: #333; }
            form { margin-bottom: 20px; }
            ul { list-style-type: none; padding: 0; }
            li { margin-bottom: 10px; }
        </style>
    </head>
    <body>
        <h1>User Management</h1>
        <form method="POST">
            <input type="text" name="username" placeholder="Username" required>
            <input type="email" name="email" placeholder="Email" required>
            <input type="submit" value="Add User">
        </form>
        <h2>Users:</h2>
        <ul>
            {% for user in users %}
                <li>{{ user.username }} ({{ user.email }})</li>
            {% endfor %}
        </ul>
    </body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        new_user = User(username=username, email=email)
        db.session.add(new_user)
        db.session.commit()
    users = User.query.all()
    return render_template_string(HTML, users=users)

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{"id": user.id, "username": user.username, "email": user.email} for user in users])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)