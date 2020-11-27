from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///avokadio.db'
db = SQLAlchemy(app)


class users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userno = db.Column(db.String(10), unique=True, nullable=False)
    name = db.Column(db.String(40), nullable=False)
    phone = db.Column(db.Integer, unique=True, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    height = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    leftpnif = db.Column(db.Integer, nullable=False)
    rightpnif = db.Column(db.Integer, nullable=False)
    birthyear= db.Column(db.Integer, nullable=False)
    note = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, default=datetime.now)



@app.route('/<phone>')
def get_channel(phone):
    user = users.query.filter_by(phone=phone).first()

    return f'This phone belongs to {user.name}'

@app.route('/')
def main():
    return("DB TEST")