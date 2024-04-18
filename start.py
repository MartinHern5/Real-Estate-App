from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
import pandas as pd

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yoursecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///real_estate_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CSV_FILE = 'instance/properties.csv'

class Login(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    favorites = db.Column(db.String, nullable=True)
    
@app.route('/')
def start():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = Login.query.filter_by(username=username, password=password).first()
        if user:
            session['username'] = username
            return redirect(url_for('home', username=username))
        else:
            flash('Invalid username or password. Please try again.')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/home')
def home():
    username = request.args.get('username')
    return render_template('home.html', username=username)

@app.route('/search', methods=['GET', 'POST'])
def search():
    results = []
    if request.method == 'POST':
        df = pd.read_csv(CSV_FILE)
        
        # Retrieve form data
        min_price = request.form.get('min_price')
        max_price = request.form.get('max_price')
        beds = request.form.get('beds')
        baths = request.form.get('baths')
        min_year_built = request.form.get('min_year_built')
        max_year_built = request.form.get('max_year_built')
        square_ft = request.form.get('square_ft')
        days_on_site = request.form.get('days_on_site')
        status = request.form.get('status')
        advanceSearch = request.form.get('advanceSearch')
        
        if min_price:
            df = df[df['Listing Price'] >= float(min_price)]
        if max_price:
            df = df[df['Listing Price'] <= float(max_price)]
            
        if beds.isdigit():
            df = df[df['Beds'] >= float(beds)]
                
        if baths.isdigit():
            df = df[df['Baths'] >= float(baths)]
                
        if min_year_built:
            df = df[df['Year Built'] >= int(min_year_built)]
        if max_year_built:
            df = df[df['Year Built'] <= int(max_year_built)]
            
        if square_ft.isdigit():
            df = df[df['Square Ft'] >= int(square_ft)]
        
        if days_on_site.isdigit():
            if (int(days_on_site) == 12):
                df = df[df['Days on Site'] <= int(365)]
            else:
                df = df[df['Days on Site'] <= int(days_on_site * 30)]
                
        if status != 'Any':
            df = df[df['Status'] == status]
            
        if advanceSearch:
            df = df[df['Address'] == advanceSearch]

        results = df.to_dict(orient='records')
        results_count = len(results)
        return render_template('search.html', results=results, results_count=results_count)
    return redirect(url_for('home'))

@app.route('/addToFav', methods=['POST'])
def addToFav():
    if request.method == 'POST':
        # Retrieve the ID of the property from the form data
        property_id = request.form.get('property_id')
        
        # Retrieves username
        username = session.get('username')
        
        # Find the user in the database
        user = Login.query.filter_by(username=username).first()
        
        if user:
            # Retrieve the existing favorites string or initialize it if it's None
            favorites = user.favorites or ''
            
            #if property_id not in favorites:
            favorites += property_id + ','
            
            # Update the favorites column in the database
            user.favorites = favorites
            db.session.commit()
            return '',204
        else:
            return '',400

@app.route('/favorites')
def favorites():
    # Get the username from the session
    username = session.get('username')
    
    user = Login.query.filter_by(username=username).first()
        
    if user:
        # Split the favorites string into a list of property IDs
        favorite_ids = user.favorites.split(',') if user.favorites else []
        
        # Query the database to get the details of the favorite properties
        favorite_properties = []
        property_data = pd.read_csv(CSV_FILE)
        for property_id in favorite_ids:
            if property_id:
                property_data = property_data[property_data['ID'] == int(property_id)]
                if not property_data.empty:
                    favorite_properties.append(property_data.to_dict(orient='records'))
        
        return render_template('favorites.html', favorite_properties=favorite_properties)
if __name__ == '__main__':
    app.run(debug=True)
