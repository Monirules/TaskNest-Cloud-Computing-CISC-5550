from flask import Flask, render_template, redirect, url_for, request, flash, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from datetime import datetime
import requests
import os
import jwt

from config import Config
from models import db, User, Task

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

API_QUOTE_URL = 'https://api.quotable.io/random'
JWT_SECRET = app.config['SECRET_KEY']


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.before_request
def create_tables_once():
    if not hasattr(app, 'tables_created'):
        with app.app_context():
            db.create_all()
            app.tables_created = True


# ----- Public Pages -----
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'danger')
        else:
            user = User(username=username, password=password)  # no hashing
            db.session.add(user)
            db.session.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and user.password == request.form['password']:  # direct compare
            login_user(user)
            flash('Logged in successfully.', 'success')
            return redirect(url_for('dashboard'))
        flash('Invalid credentials', 'danger')
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

# ----- Dashboard -----
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

@app.route('/dashboard')
@login_required
def dashboard():
    # Fetch inspirational quote, ignoring SSL cert errors (temporary)
    quote = requests.get(API_QUOTE_URL, verify=False).json()
    tasks = Task.query.filter_by(owner=current_user).order_by(Task.due_date).all()
    return render_template('dashboard.html', tasks=tasks, quote=quote)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/profile')
@login_required
def profile():
    user_tasks = Task.query.filter_by(user_id=current_user.id).all()
    return render_template('profile.html', user=current_user, tasks=user_tasks)



from flask import jsonify
from datetime import date, timedelta
import json

@app.route('/stats')
@login_required
def stats():
    # Example data calculations - adapt to your Task model/dates

    today = date.today()
    week_ago = today - timedelta(days=7)

    # Count completed tasks this week
    completed_this_week = Task.query.filter(
        Task.user_id == current_user.id,
        Task.status == 'done',
        Task.due_date >= week_ago,
        Task.due_date <= today
    ).count()

    # Count overdue tasks
    overdue_tasks = Task.query.filter(
        Task.user_id == current_user.id,
        Task.status != 'done',
        Task.due_date < today
    ).count()

    # Count total tasks
    total_tasks = Task.query.filter_by(user_id=current_user.id).count()

    stats_data = {
        'completed_this_week': completed_this_week,
        'overdue_tasks': overdue_tasks,
        'total_tasks': total_tasks,
        'pending_tasks': total_tasks - completed_this_week - overdue_tasks
    }

    return render_template('stats.html', stats=stats_data)




# ----- Task Management API (JSON) -----
@app.route('/api/tasks', methods=['GET'])
@login_required
def api_get_tasks():
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    return jsonify([
        { 'id': t.id, 'what_to_do': t.what_to_do,
          'due_date': t.due_date.isoformat(), 'status': t.status }
        for t in tasks
    ])

@app.route('/api/tasks', methods=['POST'])
@login_required
def api_add_task():
    data = request.get_json()
    t = Task(
        what_to_do=data['what_to_do'],
        due_date=datetime.fromisoformat(data['due_date']).date(),
        owner=current_user
    )
    db.session.add(t)
    db.session.commit()
    return jsonify({'message':'Task created','id':t.id}), 201

@app.route('/api/tasks/<int:id>', methods=['PUT','DELETE'])
@login_required
def api_modify_task(id):
    t = Task.query.get_or_404(id)
    if t.owner != current_user:
        return jsonify({'error':'Unauthorized'}), 403
    if request.method == 'PUT':
        data = request.get_json()
        t.what_to_do = data.get('what_to_do', t.what_to_do)
        if data.get('due_date'):
            t.due_date = datetime.fromisoformat(data['due_date']).date()
        t.status = data.get('status', t.status)
        db.session.commit()
        return jsonify({'message':'Task updated'})
    else:
        db.session.delete(t)
        db.session.commit()
        return jsonify({'message':'Task deleted'})

# ----- JWT Token for API -----
@app.route('/token')
@login_required
def get_token():
    token = jwt.encode({'user_id': current_user.id}, JWT_SECRET, algorithm='HS256')
    return jsonify({'token': token})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)




