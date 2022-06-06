from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import json
from os import environ

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = str(environ['dbdir'])
db = SQLAlchemy(app)
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])

class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    descr = db.Column(db.String(), nullable=False)
    is_ticked = db.Column(db.BOOLEAN, default=False)

    def __repr__(self):
         return f"""{{'id':{self.id}, 'Description':'{self.descr}', 'Ticked':{self.is_ticked}}}"""


db.create_all()


@app.route('/')
def index():
    todos = Todo.query.all()
    return render_template('index.html', todos=todos)


@app.route('/listener')
def listener():
    Session = sessionmaker(bind=engine)
    session = Session()
    get_args_t = request.args.get('t')
    get_args_ch = request.args.get('ch')
    get_args_del = request.args.get('del')
    if get_args_t is not None:
        todos = Todo(descr=get_args_t)
        session.add(todos)
        session.commit()
        return '200 OK!'
    elif get_args_ch is not None:
        isticked = Todo.query.filter_by(id=int(get_args_ch)).first()
        if isticked.is_ticked == False:
            isticked.is_ticked = True
        else:
            isticked.is_ticked = False
        db.session.commit()
        return '200 OK!'
    elif get_args_del is not None:
        Todo.query.filter_by(id=int(get_args_del)).delete()
        db.session.commit()
        return '200 OK!'
    else:
        return '500 error!'


if __name__ == '__main__':
    app.run()
