from flask import Flask, render_template, redirect, url_for, request, session, flash
from models import db, User, Product, CartItem
from forms import LoginForm, RegisterForm
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = 'mysecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize Database
db.init_app(app)

# Create Tables
with app.app_context():
    db.create_all()

# Home Page
@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

# Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        existing_user = User.query.filter_by(
            username=form.username.data
        ).first()

        if existing_user:
            flash("Username already exists")
            return redirect(url_for('register'))

        user = User(
            username=form.username.data,
            password=generate_password_hash(form.password.data)
        )

        db.session.add(user)
        db.session.commit()

        flash("Registration Successful")
        return redirect(url_for('login'))

    return render_template('register.html', form=form)

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(
            username=form.username.data
        ).first()

        if user and check_password_hash(
            user.password,
            form.password.data
        ):
            session['user_id'] = user.id
            flash("Login Successful")
            return redirect(url_for('index'))

        flash("Invalid Username or Password")

    return render_template('login.html', form=form)

# Logout
@app.route('/logout')
def logout():
    session.clear()
    flash("Logged Out Successfully")
    return redirect(url_for('login'))

# Add To Cart
@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):

    if 'user_id' not in session:
        return redirect(url_for('login'))

    item = CartItem.query.filter_by(
        user_id=session['user_id'],
        product_id=product_id
    ).first()

    if item:
        item.quantity += 1
    else:
        item = CartItem(
            user_id=session['user_id'],
            product_id=product_id,
            quantity=1
        )
        db.session.add(item)

    db.session.commit()

    return redirect(url_for('cart'))

# Cart
@app.route('/cart')
def cart():

    if 'user_id' not in session:
        return redirect(url_for('login'))

    items = CartItem.query.filter_by(
        user_id=session['user_id']
    ).all()

    return render_template('cart.html', items=items)

# Checkout
@app.route('/checkout')
def checkout():

    if 'user_id' not in session:
        return redirect(url_for('login'))

    CartItem.query.filter_by(
        user_id=session['user_id']
    ).delete()

    db.session.commit()

    return render_template('checkout.html')

# Run App
if __name__ == '__main__':
    app.run(debug=True)