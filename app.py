from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Business, Appointment
import os
from datetime import datetime

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'instance', 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    if current_user.is_authenticated:
        if current_user.role == 'owner':
            return redirect(url_for('owner_dashboard'))
        else:
            return redirect(url_for('customer_dashboard'))
    return render_template('auth.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    user = User.query.filter_by(username=username).first()
    
    if user and check_password_hash(user.password_hash, password):
        login_user(user)
        if user.role == 'owner':
            return redirect(url_for('owner_dashboard'))
        else:
            return redirect(url_for('customer_dashboard'))
    else:
        flash('Lütfen bilgilerinizi kontrol edin.', 'error')
        return redirect(url_for('index'))

@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    role = request.form.get('role') # owner or customer
    
    if User.query.filter_by(username=username).first():
        flash('Bu kullanıcı adı zaten alınmış.', 'error')
        return redirect(url_for('index'))

    new_user = User(username=username, password_hash=generate_password_hash(password), role=role)
    db.session.add(new_user)
    db.session.commit()
    
    login_user(new_user)
    if role == 'owner':
        return redirect(url_for('owner_dashboard'))
    else:
        return redirect(url_for('customer_dashboard'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard/owner')
@login_required
def owner_dashboard():
    if current_user.role != 'owner':
        return redirect(url_for('index'))
    return render_template('owner_dashboard.html', user=current_user)

@app.route('/dashboard/customer')
@login_required
def customer_dashboard():
    if current_user.role != 'customer':
        return redirect(url_for('index'))
    businesses = Business.query.all()
    return render_template('customer_dashboard.html', user=current_user, businesses=businesses)

@app.route('/business/create', methods=['POST'])
@login_required
def create_business():
    if current_user.role != 'owner':
        return redirect(url_for('index'))
    name = request.form.get('name')
    description = request.form.get('description')
    hours = request.form.get('hours')
    
    new_business = Business(owner_id=current_user.id, name=name, description=description, working_hours=hours)
    db.session.add(new_business)
    db.session.commit()
    return redirect(url_for('owner_dashboard'))

@app.route('/book/<int:business_id>', methods=['POST'])
@login_required
def book_appointment(business_id):
    if current_user.role != 'customer':
        return redirect(url_for('index'))
    date_str = request.form.get('date_time')
    date_time = datetime.strptime(date_str, '%Y-%m-%dT%H:%M')
    
    new_appointment = Appointment(business_id=business_id, customer_id=current_user.id, date_time=date_time)
    db.session.add(new_appointment)
    db.session.commit()
    flash('Randevu oluşturuldu!', 'success')
    return redirect(url_for('customer_dashboard'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
