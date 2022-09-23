
from flask import Flask, request, g, render_template, flash
import os
import sqlite3 
import string
def connect_db():
    conn = sqlite3.connect(app.config["DATABASE"])
    conn.row_factory = sqlite3.Row
    return conn
def create_db():
    db = connect_db()
    with app.open_resource("sq_db.sql",mode="r") as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()
def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return

DATABASE = "//flsite.db"
DEBUG = True


app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, "flsite.db")))
app.config['SECRET_KEY'] = 'dfdgbgfdbsgjdbt45fuedfhvd45'

allowed_symbols = string.digits + "абвгдеёжзийклмнопрстуфхцчшщъыьэюя" + "-"
def is_allowed(title):
    return all(map(lambda x: x in allowed_symbols,title.strip().lower()))


@app.route("/", methods=["POST","GET"])
def index():
    if request.method == "POST":
        
        data = (request.form['name'], request.form['gender'],
                request.form['age'], request.form['experience'], request.form['city'])
        sql = '''
        INSERT INTO users (name, gender, age, experience, city)
        VALUES(?,?,?,?,?)
        '''
        print(*data)
        #
        #
        if  all(map(lambda x: len(x.strip()) > 0, data)) and is_allowed(request.form['city']) and is_allowed(request.form['name']) and request.form['age'].isdigit() and request.form['experience'].isdigit():
            flash('Сообщение отправлено, спасибо за обращение')
        else:
            flash('Произошла ошибка, отправьте данные повторно')


        conn = connect_db()
        cur = conn.cursor()
        cur.execute(sql, data)
        conn.commit()


    return render_template('index.html')

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()


if __name__ == "__main__":
    app.run(debug=True)
