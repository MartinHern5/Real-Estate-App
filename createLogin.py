from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

db = SQLAlchemy()
app = Flask(__name__)

db_name = 'real_estate_app.db'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Define the Login model
class Login(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

with app.app_context():
    db.create_all()
    if not Login.query.filter_by(username='admin').first():
        admin_user = Login(username='admin', password='1234')
        db.session.add(admin_user)
        db.session.commit()

@app.route('/')
def testdb():
    try:
        db.session.query(text('1')).from_statement(text('SELECT 1')).all()
        return '<h1>It works.</h1>'
    except Exception as e:
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text

@app.route('/show_logins')
def show_logins():
    try:
        users = Login.query.all()
        users_list = '<ul>'
        for user in users:
            users_list += f'<li>ID: {user.id}, Username: {user.username}, Password: {user.password}</li>'
        users_list += '</ul>'
        return f'<h2>Login Users</h2>{users_list}'
    except Exception as e:
        error_text = f"<p>An error occurred:<br>{e}</p>"
        return f'<h1>Failed to fetch users.</h1>{error_text}'

if __name__ == '__main__':
    app.run(debug=True)
