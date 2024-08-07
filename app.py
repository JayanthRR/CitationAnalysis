from flask import Flask, request, render_template, redirect, url_for
import pandas as pd

app = Flask(__name__)

df_b = pd.read_csv('unique_authors_filled.csv')
df_b['country'] = None
df_b['continent'] = None
df_a = pd.read_csv('citations.csv')
df_a['Num Authors'] = df_a['Authors'].apply(lambda x: len(x.split(';')))

@app.route('/')
def index():
    authors = df_b['Author'].tolist()
    return render_template('index.html', authors=authors)

@app.route('/details/<author>', methods=['GET', 'POST'])
def details(author):
    rows = df_a[df_a['Authors'].str.contains(author)]
    rows_c = df_b[df_b['Author']==author]
    if request.method == 'POST':
        affiliation = request.form.get('affiliation')
        domain = request.form.get('domain')
        country = request.form.get('country')
        continent = request.form.get('continent')
        df_b.loc[df_b['Author'] == author, 'affiliation'] = affiliation
        df_b.loc[df_b['Author'] == author, 'domain'] = domain
        df_b.loc[df_b['Author'] == author, 'country'] = country
        df_b.loc[df_b['Author'] == author, 'continent'] = continent
        return redirect(url_for('index'))
    return render_template('details.html', author=author, rows_b=rows.to_dict('records'), rows_c=rows_c.to_dict('records'))

# @app.route('/add_author', methods=['GET', 'POST'])
# def add_author():
#     if request.method == 'POST':
#         new_author = request.form.get('new_author')
#         if new_author not in df_a['Author'].values:
#             df_a.loc[len(df_a)] = [new_author, 0, 0]
#             df_b.loc[len(df_b)] = [new_author, f'Detail for {new_author}']
#         return redirect(url_for('index'))
#     return render_template('add_author.html')

@app.route('/save', methods=['GET', 'POST'])
def save():
    df_b.to_csv('unique_authors_filled.csv', index=False)
    # if request.method == 'POST':
    return render_template('save.html')

@app.route('/close')
def close():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return "Server shutting down..."

if __name__ == '__main__':
    app.run(debug=True)
