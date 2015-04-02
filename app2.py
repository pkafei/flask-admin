import os
import os.path as op
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from wtforms import validators

import flask_admin as admin
from flask_admin.contrib import sqla
from flask_admin.contrib.sqla import filters


# Create application
app = Flask(__name__)

# Create dummy secrey key so we can use sessions
app.config['SECRET_KEY'] = '123456790'

# Create in-memory database
app.config['DATABASE_FILE'] = 'donors.sqlite'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + app.config['DATABASE_FILE']
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

# Flask views
@app.route('/')
def index():
    return '<a href="/admin/">Click me to get to Admin!</a>'

class Donors(db.Model):
    __tablename__ = 'donors'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    profession = db.Column(db.String(50))
    email_address = db.Column(db.String(50))
    donation_amount = db.Column(db.Integer)

    def __unicode__(self):
        return self.first_name

class DonorsAdmin(sqla.ModelView):
    column_display_pk = True
    form_columns = ['id', 'first_name', 'last_name', 'profession', 'email_address', 'donation_amount']


# Create admin
admin = admin.Admin(app, name='Find that Donor')
admin.add_view(DonorsAdmin(Donors, db.session))

if __name__ == '__main__':

    # Create DB
    db.create_all()

    # Start app
    app.run(debug=True)


