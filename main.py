from flask import Flask, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap5
from sqlalchemy import String, Text, Integer, Float
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user
from forms import RegisterForm, LoginForm, MechanicForm


app = Flask(__name__)
app.config["SECRET_KEY"] = "Austin200*556"
bootstrap5 = Bootstrap5(app)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)


class Base(DeclarativeBase):
    pass
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///isede.db"

db = SQLAlchemy(model_class=Base)
db.init_app(app)


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String, nullable=False)


class Mechanic(db.Model):
    __tablename__ = "mechanics"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    phone_number: Mapped[int] = mapped_column(Integer, nullable=False)
    address: Mapped[str] = mapped_column(String, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    years_of_experience: Mapped[str] = mapped_column(String, nullable=False)

with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html", current_user=current_user)


@app.route("/register", methods=["POST", "GET"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data
        hashed_password = generate_password_hash(password=password,method="scrypt", salt_length=8)
        user = db.session.execute(db.select(User).where(User.email==email)).scalar()
        if user:
            flash("This user already exist. Kindly proceed to login")
            return redirect(url_for("login"))
        new_user = User(name=name, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash(f"Welcome {new_user.name}!")
        return redirect(url_for("mechanic"))
    return render_template("register.html", form=form)

@app.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = db.session.execute(db.select(User).where(User.email == email)).scalar()
        if not user:
            flash("We do not have an account for this email")
            return redirect(url_for("login"))
        elif not check_password_hash(user.password, password):
            flash("Incorrect password! Check your password and retry login again")
            return redirect(url_for("login"))
        else:
            flash(f"Welcome {user.name}")
            login_user(user)
            return redirect(url_for("mechanic"))
    return render_template("login.html", current_user=current_user, form=form)


@app.route("/add-mekanic", methods=["POST", "GET"])
def add_mekanic():
    form = MechanicForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        phone = form.phone.data
        address = form.address.data
        password = form.password.data
        years_of_experience = form.years_of_experience.data
        hashed_password = generate_password_hash(password, method="scrypt", salt_length=8)
        user = db.session.execute(db.select(User).where(User.email == email)).scalar()
        if user:
            flash("This account already exists on our mechanic database")
        new_mechanic = Mechanic(name=name, email=email, phone_number=phone, address=address,
                                password=hashed_password, years_of_experience=years_of_experience)
        db.session.add(new_mechanic)
        db.session.commit()
        return redirect(url_for("mechanic"))
    return render_template("mechanic.html", form=form)


@app.route("/mechanic_data")
def mechanic():
    mechanic = db.session.execute(db.select(Mechanic)).scalars().all()
    return render_template("mekanic-users.html", users=mechanic, current_user=current_user)




if __name__ == "__main__":
    app.run(debug=True)
