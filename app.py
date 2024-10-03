from flask import Flask, request, jsonify, render_template_string
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.exc import SQLAlchemyError, OperationalError
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

def get_db_config():
    db_user = os.environ.get('DB_USER')
    db_password = os.environ.get('DB_PASSWORD')
    db_host = os.environ.get('DB_HOST')
    db_name = os.environ.get('DB_NAME')
    
    if not all([db_user, db_password, db_host, db_name]):
        logger.error("Database configuration is incomplete. Please check environment variables.")
        return None
    
    return f'postgresql://{db_user}:{db_password}@{db_host}/{db_name}'

def create_db_if_not_exists(db_uri):
    engine = SQLAlchemy().create_engine(db_uri)
    if not database_exists(engine.url):
        create_database(engine.url)
        logger.info(f"Created database: {engine.url.database}")
    else:
        logger.info(f"Database already exists: {engine.url.database}")

db_uri = get_db_config()
if db_uri:
    try:
        create_db_if_not_exists(db_uri)
        app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db = SQLAlchemy(app)

        # Test database connection
        with app.app_context():
            db.engine.connect()
            logger.info("Successfully connected to the database!")
    except OperationalError as e:
        logger.error(f"Failed to create or connect to the database. Error: {str(e)}")
else:
    logger.error("Failed to configure database URI. Application will not function correctly.")


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
            .message { color: #0000ff; }
        </style>
    </head>
    <body>
        <h1>User Management</h1>
        {% if message %}
            <p class="message">{{ message }}</p>
        {% endif %}
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
    message = None
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        new_user = User(username=username, email=email)
        try:
            db.session.add(new_user)
            db.session.commit()
            message = f"User {username} added successfully!"
        except IntegrityError:
            db.session.rollback()
            message = f"Username {username} already exists. Please choose a different username."
    
    users = User.query.all()
    return render_template_string(HTML, users=users, message=message)

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{"id": user.id, "username": user.username, "email": user.email} for user in users])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
