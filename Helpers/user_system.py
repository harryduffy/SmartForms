from app import app
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from flask_session import Session
from flask import flash
from celery import Celery
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError

app.config['SECRET_KEY'] = '19ec65279d5b111753edafec5790680c'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SESSION_PERMANENT"] = False
app.config['SESSION_TYPE'] = 'filesystem'

db = SQLAlchemy(app)
csrf = CSRFProtect(app)
bcrypt = Bcrypt(app)
sess = Session(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'arterial.login'

# use this when resetting the tables or database to reset the database
@app.before_first_request
def create_tables():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):

    return User.query.get(int(user_id))

class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)

class RegisterForm(FlaskForm):

    username = StringField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={'placeholder': 'Username'})

    password = PasswordField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={'placeholder': 'Password'})

    submit = SubmitField('Register')

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(username=username.data).first()

        if existing_user_username:
            flash('That username already exists. Please choose a different one.')
            raise ValidationError('That username already exists. Please choose a different one.')

class LoginForm(FlaskForm):

    username = StringField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={'placeholder': 'Username'})

    password = PasswordField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={'placeholder': 'Password'})

    submit = SubmitField('Login')