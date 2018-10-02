from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

class News(db.Model):
    __tablename__ = 'news'
    id = db.Column(db.Integer, primary_key = True)
    article = db.Column(db.String)
    title = db.Column(db.String)
    date = db.Column(db.DateTime())
    link = db.Column(db.String)
    website = db.Column(db.String)

