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

def calculate_completion_percentage(df):
    # df['completed'] = df[['affiliation', 'domain', 'country', 'continent']].notnull().all(axis=1)
    df['completed'] = df[['country']].notnull().all(axis=1)
    num_completed = df['completed'].sum()
    total_authors = len(df)
    ans =  round((num_completed / total_authors) * 100, 3)
    ans = f'{ans}%, {num_completed}/{total_authors}'
    return ans

# Initial calculation of completion percentage
completion_percentage = calculate_completion_percentage(df_authors)

@app.route('/')
def index():
    return render_template('index.html', authors=df_authors, completion_percentage=completion_percentage)

@app.route('/details/<author>', methods=['GET', 'POST'])
def details(author):
    if request.method == 'POST':
        affiliation = request.form.get('affiliation')
        domain = request.form.get('domain')
        country = request.form.get('country')
        continent = request.form.get('continent')
        df_authors.loc[df_authors['Author'] == author, ['affiliation', 'domain', 'country', 'continent']] = [affiliation, domain, country, continent]
        df_authors.to_csv('unique_authors_filled.csv', index=False)
        
        return redirect(url_for('details', author=author))
    else:
        rows = df_citations[df_citations['Authors'].str.contains(author, na=False)]
        author_details = df_authors[df_authors['Author'] == author].iloc[0]
        return render_template('details.html', author=author, rows=rows.to_dict('records'))

@app.route('/save', methods=['POST'])
def save():
    global completion_percentage
    completion_percentage = calculate_completion_percentage(df_authors)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
