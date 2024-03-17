from flask import Flask, render_template, request, redirect, url_for
import pandas as pd

app = Flask(__name__)

CSV_FILE = 'properties.csv'

@app.route('/home', methods=['GET', 'POST'])
def search():
    results = []
    if request.method == 'POST':
        search_price = request.form('search')
        if search_price is not None:
            df = pd.read_csv(CSV_FILE)
            filtered_df = df[df['Listing Price'] <= search_price]
            results = filtered_df.to_dict(orient='records')
            return redirect(url_for('search'))
    return render_template('search.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
