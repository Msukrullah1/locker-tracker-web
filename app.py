"""
Locker Tracker - Flask Web Application with MySQL
AWS RDS MySQL Database Configuration
Production-Grade Setup
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, timedelta
import os
from functools import wraps
import logging

app = Flask(__name__)

# ============================================================
# Configuration - MySQL के लिए
# ============================================================

# AWS RDS MySQL या Local MySQL
if os.getenv('ENVIRONMENT') == 'production':
    # AWS RDS MySQL
    DB_USER = os.getenv('DB_USER', 'admin')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '3306')
    DB_NAME = os.getenv('DB_NAME', 'locker_tracker')
    
    # MySQL connection string
    DATABASE_URL = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
else:
    # Local development
    DATABASE_URL = os.getenv(
        'DATABASE_URL',
        'mysql+pymysql://root:password@localhost:3306/locker_tracker'
    )

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production-12345')
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_size': 10,
    'pool_recycle': 3600,
    'pool_pre_ping': True,
    'pool_timeout': 30,
}
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

db = SQLAlchemy(app)

# ============================================================
# Database Models (MySQL Optimized)
# ============================================================

class User(db.Model):
    __tablename__ = 'tbl_users'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(20), unique=True, nullable=False, index=True)
    user_name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    user_role = db.Column(db.String(20), nullable=False)
    is_active = db.Column(db.Boolean, default=True, index=True)
    last_login = db.Column(db.DateTime)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<User {self.user_id}>'


class Employee(db.Model):
    __tablename__ = 'tbl_employees'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    emp_id = db.Column(db.String(20), unique=True, nullable=False, index=True)
    emp_name = db.Column(db.String(100), nullable=False, index=True)
    designation = db.Column(db.String(50))
    dept_code = db.Column(db.String(10), index=True)
    dept_name = db.Column(db.String(50))
    email = db.Column(db.String(100), index=True)
    phone = db.Column(db.String(20))
    emp_status = db.Column(db.String(20), default='Active', index=True)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)


class Locker(db.Model):
    __tablename__ = 'tbl_lockers'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    locker_no = db.Column(db.String(20), unique=True, nullable=False, index=True)
    type_code = db.Column(db.String(10), index=True)
    type_name = db.Column(db.String(50))
    floor_code = db.Column(db.String(10), index=True)
    floor_name = db.Column(db.String(50))
    bay_no = db.Column(db.String(10))
    status = db.Column(db.String(20), default='Available', index=True)
    assigned_emp_id = db.Column(db.String(20), index=True)
    assigned_emp_name = db.Column(db.String(100))
    assigned_date = db.Column(db.DateTime)
    assigned_by = db.Column(db.String(20))
    keys_issued = db.Column(db.Integer, default=0)
    keys_available = db.Column(db.Integer, default=0)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)


class LockerHistory(db.Model):
    __tablename__ = 'tbl_locker_history'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    locker_no = db.Column(db.String(20), nullable=False, index=True)
    emp_id = db.Column(db.String(20), index=True)
    emp_name = db.Column(db.String(100))
    action = db.Column(db.String(20), index=True)
    keys_issued = db.Column(db.Integer, default=0)
    action_date = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    action_by = db.Column(db.String(20))
    remarks = db.Column(db.Text)


class AuditLog(db.Model):
    __tablename__ = 'tbl_audit_logs'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    log_datetime = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    user_id = db.Column(db.String(20), index=True)
    user_name = db.Column(db.String(100))
    action = db.Column(db.String(30), index=True)
    entity_type = db.Column(db.String(20))
    entity_id = db.Column(db.String(50))
    old_value = db.Column(db.Text)
    new_value = db.Column(db.Text)
    remarks = db.Column(db.Text)
    ip_address = db.Column(db.String(50))


class Floor(db.Model):
    __tablename__ = 'tbl_floors'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    floor_code = db.Column(db.String(10), unique=True, nullable=False, index=True)
    floor_name = db.Column(db.String(50), nullable=False)
    building = db.Column(db.String(50))
    is_active = db.Column(db.Boolean, default=True)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)


class Department(db.Model):
    __tablename__ = 'tbl_departments'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dept_code = db.Column(db.String(10), unique=True, nullable=False, index=True)
    dept_name = db.Column(db.String(50), nullable=False, index=True)
    is_active = db.Column(db.Boolean, default=True)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)


# ============================================================
# Decorators
# ============================================================
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def role_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                return redirect(url_for('login'))
            user = User.query.filter_by(user_id=session['user_id']).first()
            if not user or user.user_role not in roles:
                return jsonify({'error': 'Access Denied'}), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator


# ============================================================
# Helper Functions
# ============================================================
def log_audit(action, entity_type, entity_id, old_value='', new_value='', remarks=''):
    try:
        audit = AuditLog(
            user_id=session.get('user_id', ''),
            user_name=session.get('user_name', ''),
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            old_value=old_value,
            new_value=new_value,
            remarks=remarks,
            ip_address=request.remote_addr
        )
        db.session.add(audit)
        db.session.commit()
        logger.info(f"Audit logged: {action} by {session.get('user_id')}")
    except Exception as e:
        logger.error(f"Audit logging failed: {str(e)}")
        db.session.rollback()


def get_dashboard_stats():
    try:
        total_lockers = db.session.query(db.func.count(Locker.id)).scalar() or 0
        assigned = db.session.query(db.func.count(Locker.id)).filter_by(status='Assigned').scalar() or 0
        available = db.session.query(db.func.count(Locker.id)).filter_by(status='Available').scalar() or 0
        damaged = db.session.query(db.func.count(Locker.id)).filter_by(status='Damaged').scalar() or 0
        
        return {
            'total': total_lockers,
            'assigned': assigned,
            'available': available,
            'damaged': damaged,
            'utilization': round((assigned / total_lockers * 100) if total_lockers > 0 else 0, 1)
        }
    except Exception as e:
        logger.error(f"Dashboard stats error: {str(e)}")
        return {'total': 0, 'assigned': 0, 'available': 0, 'damaged': 0, 'utilization': 0}


# ============================================================
# Routes - Authentication
# ============================================================
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        user_id = data.get('user_id', '').strip()
        password = data.get('password', '')
        
        if not user_id or not password:
            return jsonify({'error': 'Please enter credentials'}), 400
        
        try:
            user = User.query.filter_by(user_id=user_id, is_active=True).first()
            
            if user and check_password_hash(user.password, password):
                session['user_id'] = user.user_id
                session['user_name'] = user.user_name
                session['user_role'] = user.user_role
                session.permanent = True
                
                user.last_login = datetime.utcnow()
                db.session.commit()
                
                log_audit('LOGIN', 'User', user_id, remarks='Successful login')
                
                if request.is_json:
                    return jsonify({'success': True, 'message': 'Login successful'}), 200
                return redirect(url_for('dashboard'))
            else:
                log_audit('LOGIN_FAILED', 'User', user_id, remarks='Failed login attempt')
                error_msg = 'Invalid credentials'
                if request.is_json:
                    return jsonify({'error': error_msg}), 401
                return render_template('login.html', error=error_msg), 401
        
        except Exception as e:
            logger.error(f"Login error: {str(e)}")
            return jsonify({'error': f'Login error: {str(e)}'}), 500
    
    return render_template('login.html')


@app.route('/logout')
def logout():
    log_audit('LOGOUT', 'User', session.get('user_id', ''), remarks='User logged out')
    session.clear()
    return redirect(url_for('login'))


# ============================================================
# Routes - Dashboard
# ============================================================
@app.route('/dashboard')
@login_required
def dashboard():
    try:
        stats = get_dashboard_stats()
        recent_history = LockerHistory.query.order_by(LockerHistory.action_date.desc()).limit(10).all()
        
        return render_template('dashboard.html', 
                             stats=stats, 
                             recent=recent_history,
                             user_name=session.get('user_name', ''),
                             user_role=session.get('user_role', ''))
    except Exception as e:
        logger.error(f"Dashboard error: {str(e)}")
        return jsonify({'error': 'Dashboard error'}), 500


# ============================================================
# API Routes - Locker Operations
# ============================================================
@app.route('/api/lockers/available')
@login_required
def get_available_lockers():
    try:
        lockers = Locker.query.filter_by(status='Available').all()
        return jsonify([{
            'locker_no': l.locker_no,
            'type_name': l.type_name,
            'floor_name': l.floor_name,
            'bay_no': l.bay_no
        } for l in lockers])
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return jsonify({'error': 'Failed to fetch lockers'}), 500


@app.route('/api/lockers/assigned')
@login_required
def get_assigned_lockers():
    try:
        lockers = Locker.query.filter_by(status='Assigned').all()
        return jsonify([{
            'locker_no': l.locker_no,
            'emp_name': l.assigned_emp_name,
            'emp_id': l.assigned_emp_id,
            'assigned_date': l.assigned_date.strftime('%d-%b-%y') if l.assigned_date else ''
        } for l in lockers])
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return jsonify({'error': 'Failed to fetch lockers'}), 500


@app.route('/api/locker/<locker_no>')
@login_required
def get_locker(locker_no):
    try:
        locker = Locker.query.filter_by(locker_no=locker_no).first()
        if not locker:
            return jsonify({'error': 'Locker not found'}), 404
        
        return jsonify({
            'locker_no': locker.locker_no,
            'type_name': locker.type_name,
            'floor_name': locker.floor_name,
            'bay_no': locker.bay_no,
            'status': locker.status,
            'assigned_emp_id': locker.assigned_emp_id or '',
            'assigned_emp_name': locker.assigned_emp_name or '',
            'assigned_date': locker.assigned_date.strftime('%d-%b-%y') if locker.assigned_date else '',
            'keys_issued': locker.keys_issued,
            'keys_available': locker.keys_available
        })
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return jsonify({'error': 'Failed to fetch locker'}), 500


@app.route('/api/locker/assign', methods=['POST'])
@login_required
@role_required('SuperAdmin', 'Admin', 'Operator')
def assign_locker():
    try:
        data = request.get_json()
        locker_no = data.get('locker_no')
        emp_id = data.get('emp_id')
        keys_to_issue = int(data.get('keys_to_issue', 1))
        remarks = data.get('remarks', '')
        
        locker = Locker.query.filter_by(locker_no=locker_no).first()
        if not locker:
            return jsonify({'error': 'Locker not found'}), 404
        
        if locker.status != 'Available':
            return jsonify({'error': 'Locker is not available'}), 400
        
        employee = Employee.query.filter_by(emp_id=emp_id).first()
        if not employee:
            return jsonify({'error': 'Employee not found'}), 404
        
        locker.status = 'Assigned'
        locker.assigned_emp_id = emp_id
        locker.assigned_emp_name = employee.emp_name
        locker.assigned_date = datetime.utcnow()
        locker.assigned_by = session['user_id']
        locker.keys_issued = keys_to_issue
        locker.keys_available = keys_to_issue
        
        history = LockerHistory(
            locker_no=locker_no,
            emp_id=emp_id,
            emp_name=employee.emp_name,
            action='ASSIGN',
            keys_issued=keys_to_issue,
            action_by=session['user_id'],
            remarks=remarks
        )
        
        db.session.add(history)
        db.session.commit()
        
        log_audit('ASSIGN_LOCKER', 'Locker', locker_no, 
                 new_value=f"Assigned to {employee.emp_name} ({emp_id})",
                 remarks=remarks)
        
        logger.info(f"Locker {locker_no} assigned to {emp_id}")
        return jsonify({'success': True, 'message': f'Locker {locker_no} assigned successfully'})
    
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        db.session.rollback()
        return jsonify({'error': f'Failed to assign locker: {str(e)}'}), 500


@app.route('/api/locker/release', methods=['POST'])
@login_required
@role_required('SuperAdmin', 'Admin', 'Operator')
def release_locker():
    try:
        data = request.get_json()
        locker_no = data.get('locker_no')
        keys_returned = int(data.get('keys_returned', 0))
        reason = data.get('reason', '')
        remarks = data.get('remarks', '')
        
        locker = Locker.query.filter_by(locker_no=locker_no).first()
        if not locker:
            return jsonify({'error': 'Locker not found'}), 404
        
        if locker.status != 'Assigned':
            return jsonify({'error': 'Locker is not assigned'}), 400
        
        old_emp = f"{locker.assigned_emp_name} ({locker.assigned_emp_id})"
        assigned_emp_id = locker.assigned_emp_id
        assigned_emp_name = locker.assigned_emp_name
        
        locker.status = 'Available'
        locker.assigned_emp_id = None
        locker.assigned_emp_name = None
        locker.assigned_date = None
        locker.keys_issued = 0
        locker.keys_available = 0
        
        history = LockerHistory(
            locker_no=locker_no,
            emp_id=assigned_emp_id,
            emp_name=assigned_emp_name,
            action='RELEASE',
            keys_issued=keys_returned,
            action_by=session['user_id'],
            remarks=f"Reason: {reason}. {remarks}"
        )
        
        db.session.add(history)
        db.session.commit()
        
        log_audit('RELEASE_LOCKER', 'Locker', locker_no,
                 old_value=f"Was assigned to {old_emp}",
                 new_value="Available",
                 remarks=f"Reason: {reason}")
        
        logger.info(f"Locker {locker_no} released")
        return jsonify({'success': True, 'message': f'Locker {locker_no} released successfully'})
    
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        db.session.rollback()
        return jsonify({'error': f'Failed to release locker: {str(e)}'}), 500


# ============================================================
# Routes - Employee Search
# ============================================================
@app.route('/employees')
@login_required
def employees():
    return render_template('employees.html', 
                         user_name=session.get('user_name', ''),
                         user_role=session.get('user_role', ''))


@app.route('/api/employees/search')
@login_required
def search_employees():
    try:
        search_term = request.args.get('q', '').strip()
        
        if search_term:
            # MySQL में LIKE use करते हैं (case-insensitive)
            employees = Employee.query.filter(
                (Employee.emp_id.like(f'%{search_term}%')) |
                (Employee.emp_name.like(f'%{search_term}%')) |
                (Employee.email.like(f'%{search_term}%'))
            ).limit(50).all()
        else:
            employees = Employee.query.limit(50).all()
        
        return jsonify([{
            'emp_id': e.emp_id,
            'emp_name': e.emp_name,
            'designation': e.designation or '',
            'dept_name': e.dept_name or '',
            'email': e.email or '',
            'phone': e.phone or '',
            'status': e.emp_status or ''
        } for e in employees])
    
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return jsonify({'error': 'Search failed'}), 500


@app.route('/api/employee/<emp_id>/lockers')
@login_required
def get_employee_lockers(emp_id):
    try:
        lockers = Locker.query.filter_by(assigned_emp_id=emp_id).all()
        
        return jsonify([{
            'locker_no': l.locker_no,
            'type_name': l.type_name,
            'floor_name': l.floor_name,
            'assigned_date': l.assigned_date.strftime('%d-%b-%y') if l.assigned_date else '',
            'keys_issued': l.keys_issued
        } for l in lockers])
    
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return jsonify({'error': 'Failed to fetch lockers'}), 500


# ============================================================
# Routes - Reports
# ============================================================
@app.route('/reports')
@login_required
@role_required('SuperAdmin', 'Admin', 'Viewer')
def reports():
    return render_template('reports.html',
                         user_name=session.get('user_name', ''),
                         user_role=session.get('user_role', ''))


@app.route('/api/reports/floor')
@login_required
def get_floor_report():
    try:
        floor_code = request.args.get('floor_code', None)
        
        # MySQL में CASE WHEN use करते हैं
        if floor_code and floor_code != 'All':
            floors = db.session.query(
                Floor.floor_code,
                Floor.floor_name,
                Floor.building,
                db.func.count(Locker.id).label('total'),
                db.func.sum(db.case((Locker.status == 'Assigned', 1), else_=0)).label('assigned'),
                db.func.sum(db.case((Locker.status == 'Available', 1), else_=0)).label('available'),
                db.func.sum(db.case((Locker.status == 'Damaged', 1), else_=0)).label('damaged')
            ).outerjoin(Locker, Floor.floor_code == Locker.floor_code).filter(
                Floor.floor_code == floor_code
            ).group_by(Floor.floor_code, Floor.floor_name, Floor.building).all()
        else:
            floors = db.session.query(
                Floor.floor_code,
                Floor.floor_name,
                Floor.building,
                db.func.count(Locker.id).label('total'),
                db.func.sum(db.case((Locker.status == 'Assigned', 1), else_=0)).label('assigned'),
                db.func.sum(db.case((Locker.status == 'Available', 1), else_=0)).label('available'),
                db.func.sum(db.case((Locker.status == 'Damaged', 1), else_=0)).label('damaged')
            ).outerjoin(Locker, Floor.floor_code == Locker.floor_code).group_by(
                Floor.floor_code, Floor.floor_name, Floor.building
            ).all()
        
        return jsonify([{
            'floor_code': f[0],
            'floor_name': f[1],
            'building': f[2] or '',
            'total': f[3] or 0,
            'assigned': int(f[4] or 0),
            'available': int(f[5] or 0),
            'damaged': int(f[6] or 0)
        } for f in floors])
    
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return jsonify({'error': 'Failed to generate report'}), 500


@app.route('/api/reports/audit')
@login_required
@role_required('SuperAdmin', 'Admin')
def get_audit_log():
    try:
        user_filter = request.args.get('user_id', 'All')
        action_filter = request.args.get('action', 'All')
        from_date = request.args.get('from_date', '')
        to_date = request.args.get('to_date', '')
        
        query = AuditLog.query
        
        if user_filter != 'All':
            query = query.filter_by(user_id=user_filter)
        
        if action_filter != 'All':
            query = query.filter_by(action=action_filter)
        
        if from_date:
            try:
                from_dt = datetime.strptime(from_date, '%Y-%m-%d')
                query = query.filter(AuditLog.log_datetime >= from_dt)
            except:
                pass
        
        if to_date:
            try:
                to_dt = datetime.strptime(to_date, '%Y-%m-%d')
                to_dt = to_dt.replace(hour=23, minute=59, second=59)
                query = query.filter(AuditLog.log_datetime <= to_dt)
            except:
                pass
        
        logs = query.order_by(AuditLog.log_datetime.desc()).limit(500).all()
        
        return jsonify([{
            'log_datetime': l.log_datetime.strftime('%d-%b-%y %H:%M:%S'),
            'user_id': l.user_id,
            'user_name': l.user_name,
            'action': l.action,
            'entity_type': l.entity_type,
            'entity_id': l.entity_id,
            'old_value': (l.old_value or '')[:50],
            'new_value': (l.new_value or '')[:50],
            'remarks': (l.remarks or '')[:50],
            'ip_address': l.ip_address or ''
        } for l in logs])
    
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return jsonify({'error': 'Failed to generate report'}), 500


# ============================================================
# Routes - Pages
# ============================================================
@app.route('/assign')
@login_required
@role_required('SuperAdmin', 'Admin', 'Operator')
def assign():
    return render_template('assign.html',
                         user_name=session.get('user_name', ''),
                         user_role=session.get('user_role', ''))


@app.route('/release')
@login_required
@role_required('SuperAdmin', 'Admin', 'Operator')
def release():
    return render_template('release.html',
                         user_name=session.get('user_name', ''),
                         user_role=session.get('user_role', ''))


# ============================================================
# Error Handlers
# ============================================================
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(500)
def server_error(error):
    logger.error(f"Server error: {str(error)}")
    return jsonify({'error': 'Server error'}), 500


# ============================================================
# Database Initialization
# ============================================================
def init_db():
    """Initialize MySQL database with sample data"""
    with app.app_context():
        try:
            # Create all tables
            db.create_all()
            logger.info("✅ MySQL database tables created successfully")
            
            # Add default users
            if User.query.count() == 0:
                users = [
                    User(user_id='superadmin', user_name='Super Administrator', 
                         password=generate_password_hash('Admin@123'), user_role='SuperAdmin'),
                    User(user_id='admin01', user_name='Rajesh Kumar', 
                         password=generate_password_hash('Admin@123'), user_role='Admin'),
                    User(user_id='oper01', user_name='Amit Singh', 
                         password=generate_password_hash('Oper@123'), user_role='Operator'),
                    User(user_id='viewer01', user_name='Guest User', 
                         password=generate_password_hash('View@123'), user_role='Viewer'),
                ]
                db.session.add_all(users)
                db.session.commit()
                logger.info("✅ Default users created")
            
            # Add sample floors
            if Floor.query.count() == 0:
                floors = [
                    Floor(floor_code='F1', floor_name='Floor 1', building='Building A'),
                    Floor(floor_code='F2', floor_name='Floor 2', building='Building A'),
                    Floor(floor_code='F3', floor_name='Floor 3', building='Building B'),
                ]
                db.session.add_all(floors)
                db.session.commit()
                logger.info("✅ Sample floors created")
            
            # Add sample departments
            if Department.query.count() == 0:
                depts = [
                    Department(dept_code='IT', dept_name='Information Technology'),
                    Department(dept_code='HR', dept_name='Human Resources'),
                    Department(dept_code='FIN', dept_name='Finance'),
                    Department(dept_code='OPS', dept_name='Operations'),
                ]
                db.session.add_all(depts)
                db.session.commit()
                logger.info("✅ Sample departments created")
            
            logger.info("✅ Database initialization complete!")
        
        except Exception as e:
            logger.error(f"❌ Database initialization error: {str(e)}")
            raise


if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
