from flask import Flask, request, render_template, redirect, url_for
import pandas as pd

app = Flask(__name__)

# Load data
df_citations = pd.read_csv('citations.csv')
df_authors = pd.read_csv('unique_authors_filled.csv')

# Ensure 'country' and 'continent' columns exist
if 'country' not in df_authors.columns:
    df_authors['country'] = None
if 'continent' not in df_authors.columns:
    df_authors['continent'] = None

@app.route('/')
def index():
    return render_template('index.html', authors=df_authors)

@app.route('/details/<author>', methods=['GET', 'POST'])
def details(author):
    rows = df_citations[df_citations['Authors'].str.contains(author, na=False)]
    if request.method == 'POST':
        affiliation = request.form.get('affiliation')
        domain = request.form.get('domain')
        country = request.form.get('country')
        continent = request.form.get('continent')
        df_authors.loc[df_authors['Author'] == author, ['affiliation', 'domain', 'country', 'continent']] = [affiliation, domain, country, continent]
        # df_authors.to_csv('unique_authors_filled.csv', index=False)
        return redirect(url_for('index'))
    return render_template('details.html', author=author, rows=rows.to_dict('records'))

@app.route('/save', methods=['GET', 'POST'])
def save():
    df_authors.to_csv('unique_authors_filled.csv', index=False)
    # if request.method == 'POST':
    return render_template('save.html')


if __name__ == '__main__':
    app.run(debug=True)
