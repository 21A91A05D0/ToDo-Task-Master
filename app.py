import os
from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
from sqlalchemy import func
from flask_wtf.csrf import CSRFProtect, generate_csrf
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Load configuration from environment variables
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI', 'sqlite:///test.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.getenv('SECRET_KEY')
app.config['WTF_CSRF_ENABLED'] = True
app.config['WTF_CSRF_SECRET_KEY'] = os.getenv('WTF_CSRF_SECRET_KEY')

db = SQLAlchemy(app)
csrf = CSRFProtect(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.Date, nullable=True)
    priority = db.Column(db.String(20), default='medium')
    category = db.Column(db.String(50), default='General')

    def __repr__(self):
        return f'<Task {self.id}: {self.content}>'

@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}

@app.context_processor
def inject_csrf_token():
    return {'csrf_token_value': generate_csrf()}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        task_content = request.form.get('content', '').strip()
        if not task_content:
            flash('Task content cannot be empty!', 'error')
            return redirect(url_for('index'))
            
        new_task = Todo(
            content=task_content,
            priority=request.form.get('priority', 'medium'),
            category=request.form.get('category', 'General')
        )
        
        due_date_str = request.form.get('due_date')
        if due_date_str:
            try:
                new_task.due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
            except ValueError:
                flash('Invalid date format. Please use YYYY-MM-DD', 'error')
                return redirect(url_for('index'))

        try:
            db.session.add(new_task)
            db.session.commit()
            flash('Task added successfully!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash('There was an issue adding your task.', 'error')
            return redirect(url_for('index'))
    
    category_filter = request.args.get('category', 'all')
    priority_filter = request.args.get('priority', 'all')
    
    query = Todo.query
    
    if category_filter != 'all':
        query = query.filter_by(category=category_filter)
    if priority_filter != 'all':
        query = query.filter_by(priority=priority_filter)
    
    tasks = query.order_by(Todo.completed, Todo.date_created.desc()).all()
    categories = [cat[0] for cat in db.session.query(Todo.category).distinct().all() if cat[0]]
    
    return render_template(
        "index.html",
        tasks=tasks,
        categories=categories,
        current_category=category_filter,
        current_priority=priority_filter
    )

@app.route('/toggle/<int:id>', methods=['POST'])
def toggle(id):
    task = Todo.query.get_or_404(id)
    task.completed = not task.completed
    try:
        db.session.commit()
        return jsonify({'success': True, 'completed': task.completed})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        flash('Task deleted successfully!', 'success')
    except:
        db.session.rollback()
        flash('There was a problem deleting the task.', 'error')
    return redirect(url_for('index'))

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    
    if request.method == 'POST':
        task.content = request.form.get('content', '').strip()
        task.priority = request.form.get('priority', 'medium')
        task.category = request.form.get('category', 'General')
        
        due_date_str = request.form.get('due_date')
        if due_date_str:
            try:
                task.due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
            except ValueError:
                task.due_date = None
        else:
            task.due_date = None
            
        try:
            db.session.commit()
            flash('Task updated successfully!', 'success')
            return redirect(url_for('index'))
        except:
            db.session.rollback()
            flash('There was an issue updating your task.', 'error')
    
    categories = [cat[0] for cat in db.session.query(Todo.category).distinct().all() if cat[0]]
    return render_template("update.html", task=task, categories=categories)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)