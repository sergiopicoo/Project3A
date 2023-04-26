import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect, abort
import pygal
import csv
#from stock_data import StockData
#from generate_chart import ChartGenerator

# make a Flask application object called app
app = Flask(__name__)
app.config["DEBUG"] = True

#flash  the secret key to secure sessions
app.config['SECRET_KEY'] = 'your secret key'

def query_api():
    pass

# in classs
def get_chart():
    line_chart = pygal.Line()
    line_chart.title = 'Browser usage evolution (in %)'
    line_chart.x_labels = map(str, range(2002, 2013))
    line_chart.add('Firefox', [None, None,    0, 16.6,   25,   31, 36.4, 45.5, 46.3, 42.8, 37.1])
    line_chart.add('Chrome',  [None, None, None, None, None, None,    0,  3.9, 10.8, 23.8, 35.3])
    line_chart.add('IE',      [85.8, 84.6, 84.7, 74.5,   66, 58.6, 54.7, 44.8, 36.2, 26.6, 20.1])
    line_chart.add('Others',  [14.2, 15.4, 15.3,  8.9,    9, 10.4,  8.9,  5.8,  6.7,  6.8,  7.5])
    line_chart.render_data_uri()

    return line_chart.render_data_uri()

# Function to open a connection to the database.db file
def get_db_connection():
    # create connection to the database
    conn = sqlite3.connect('database.db')
    
    # allows us to have name-based access to columns
    # the database connection will return rows we can access like regular Python dictionaries
    conn.row_factory = sqlite3.Row

    #return the connection object
    return conn

## function to get a post
def get_post(post_id):
    #get a database connection
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
    conn.close()

    if post is None:
        abort(404)
    
    return post


# use the app.route() decorator to create a Flask view function called index()
@app.route('/')
def index():
    #get a database connection
    conn = get_db_connection()

    #execute an sql query to select all entries from the posts table
    #use fetchall() to get all of the rows of the query result
    posts = conn.execute('SELECT * FROM posts').fetchall()

    #close the connection  
    conn.close()
    
    return render_template('index.html', posts=posts)

@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        #get title and content
        title = request.form['title']
        content = request.form['content']

        #display error if title of content not submitted
        #otherwise make database connection and insert the content
        if not title:
            flash('Title is required!')
        elif not content:
            flash('Content is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)', (title, content))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('create.html')

#route to edit post
@app.route('/<int:id>/edit/', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        #get title and content
        title = request.form['title']
        content = request.form['content']

        #display error if title of content not submitted
        #otherwise make database connection and insert the content
        if not title:
            flash('Title is required!')
        elif not content:
            flash('Content is required!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE posts SET title = ?, content = ? WHERE id = ?', (title, content, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))


    return render_template('edit.html', post=post)

# route to delete a post
@app.route('/<int:id>/delete/', methods=('POST',))
def delete(id):
    #get post
    post = get_post(id)

    #connect to database
    conn = get_db_connection()

    #run the delete query
    conn.execute('DELETE FROM POSTS WHERE id = ?', (id,))

    #commit the changes and close the connection
    conn.commit()
    conn.close()

    #show deletes successful message
    flash('"{}" was successfully deleted!'.format(post['title']))
    
    #go to index page after delete
    return redirect(url_for('index'))

def get_symbols():
    return['GOOG', 'GOOGL', 'IBM']

#route for the stock user input form
@app.route("/stocks", methods=['GET', 'POST'])
def stocks():
    symbol_list = ()
    if request.method == "POST":
        #print(request.form)
        symbol = request.form['symbol_list']
        chart_type = request.form["chart_type"]

        if symbol == "":
            flash("Symbol is required")
        #else: 
           # sd = StockData()
           # gc = ChartGenerator()
        elif chart_type == "":
            flash("Chart type required")

        else:
            chart = get_chart()
            return render_template("stock.html", chart = chart)
        
    return render_template("stock.html", symbol_list = symbol_list)

def drop():
    with open('stocks.csv', 'r') as file:
        reader = csv.reader(file)
        column = list(zip(*reader))[1][1:]

    item = request.form[drop]
    return render_template('stock.html', column=column)

  #  with open('stocks.csv', 'r') as file:
   #     reader = csv.DictReader(file)
    #    column_values = [row[1] for row in reader]
    
    # Pass the column values to the template
    return render_template('index.html', column_values=column_values)

  #  return render_template('stock.html', column_values=column_values)

if __name__ == '__main__':
    app.run(debug=True)

#host="0.0.0.0"
app.run()