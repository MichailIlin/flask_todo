## Задачи
# 1. Разобраться с механизмом работы элементов flask
# 2. Написать приложение-заметчик, в котором можно добавлять, удалять заметки и 
# менять их статус (выполнено/невыполнено)
# 3. Запустить приложенеи на сервере

# документация flask https://flask.palletsprojects.com/en/3.0.x/

# импорт класса веб-приложения и базы данных
import flask
from flask_sqlalchemy import SQLAlchemy


# создание экземпляра приложения (класса) с базой данных
app=flask.Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db=SQLAlchemy(app)

#Хранение информации о заметках  в модели Todo
class Todo(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(100))
    complete=db.Column(db.Boolean, default=False)

@app.route("/")
# def hello_world(): #простейший вариант
#     return "<p>Hello world</p>"
def index(): 
    # Jinja2 позволяет передать код python на html-страницу
    todo_list=Todo.query.all()
    return flask.render_template('index.html', todo_list=todo_list)
#маршрутизатор - это декоратор, кльлорый формиркет url -адрес и по нему выполняет функцию
#метод add_url_rule() - формирует url-адрес, по которому нужно запустить функцию
# как формируется url
# https://www.ranepa.ru/about
# https://127.0.0.1:5000/about

#### Вариант записи 1
# def about():
#     return '<h2>About page</h2>'

# app.add_url_rule("/about",view_func=about)

#### Вариант записи 2
# Использование декоратора app.route
@app.route("/about")
def about():
    return '<h2>About page</h2>'


@app.route('/add', methods=['POST'])
def add():
    title = flask.request.form["content"]
    new_todo=Todo(title=title)
    db.session.add(new_todo)
    db.session.commit()
    return flask.redirect(flask.url_for('index'))

@app.route('/delete/<todo_id>', methods=['GET'])
def delete(todo_id):
    todo=Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return flask.redirect(flask.url_for('index'))

@app.route('/update/<todo_id>', methods=['GET'])
def update(todo_id):
    todo=Todo.query.filter_by(id=todo_id).first()
    todo.complete=not todo.complete
    db.session.commit()
    return flask.redirect(flask.url_for('index'))

# @app.route("/add", methods=["POST"])
# def add():
#     text=flask.request.form["content"]
#     return flask.redirect(flask.url_for("content, text=text"))

# @app.route("/<text>")
# def content(text):
#     return f'<h1>{text}</h1>'

# flask --app hello run # запуск приложения в терминале
# или
if __name__ =='__main__':
    
    # оператор with работает с контекстным менеджером
    # позволяет закрыть соединение с БД после выхода из оператора with
    with app.app_context():
        db.create_all()
      
    
    app.run(debug=True) # debug=True - включение режима отладчика