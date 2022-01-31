from flask import Blueprint, redirect, url_for, render_template,request
from app import app
from flask_login import login_required, login_user, logout_user
from Helpers.user_system import LoginForm, RegisterForm, User, db, bcrypt

app.config['SECRET_KEY'] = '19ec65279d5b111753edafec5790680c'


arterial_blueprint = Blueprint("arterial", __name__, static_folder="static", template_folder="templates")

@app.before_first_request
def create_tables():
    db.create_all()

@arterial_blueprint.route("/", methods=["POST", "GET"])
def index():

    return render_template("index.html")

@arterial_blueprint.route("/login", methods=["POST", "GET"])
def login():

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                
                return redirect(url_for('generator.initial_form'))

    return render_template("login.html", form=form)

@arterial_blueprint.route("/register", methods=["POST", "GET"])
def register():

    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('arterial.login'))

    return render_template("register.html", form=form)

@arterial_blueprint.route("/logout", methods=["POST", "GET"])
def logout():

    logout_user()

    return redirect(url_for("arterial.index"))
