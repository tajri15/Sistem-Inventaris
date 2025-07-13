from datetime import datetime
from app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(256))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

class Category(db.Model):
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    items = db.relationship('Item', backref='category', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Category {self.name}>'

class Item(db.Model):
    __tablename__ = 'items'
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), nullable=False, unique=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    unit_price = db.Column(db.Float, nullable=False, default=0.0)
    supplier = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    
    def __repr__(self):
        return f'<Item {self.code}: {self.name}>'

class IncomingItem(db.Model):
    __tablename__ = 'incoming_items'
    
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Float, nullable=False, default=0.0)
    supplier = db.Column(db.String(200))
    batch_number = db.Column(db.String(100))
    expiry_date = db.Column(db.Date)
    received_date = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.Text)
    received_by = db.Column(db.String(100), default='System Admin')
    
    item = db.relationship('Item', backref='incoming_transactions')
    
    @property
    def total_value(self):
        return self.quantity * self.unit_price
    
    def __repr__(self):
        return f'<IncomingItem {self.quantity} of {self.item.name}>'

class OutgoingItem(db.Model):
    __tablename__ = 'outgoing_items'
    
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    destination = db.Column(db.String(200), nullable=False)
    purpose = db.Column(db.String(200))
    request_number = db.Column(db.String(100))
    issued_date = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.Text)
    issued_by = db.Column(db.String(100), default='System Admin')
    
    item = db.relationship('Item', backref='outgoing_transactions')
    
    @property
    def total_value(self):
        return self.quantity * self.item.unit_price
    
    def __repr__(self):
        return f'<OutgoingItem {self.quantity} of {self.item.name}>'

class ActivityLog(db.Model):
    __tablename__ = 'activity_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(100), nullable=False)
    table_name = db.Column(db.String(50), nullable=False)
    record_id = db.Column(db.Integer, nullable=False)
    details = db.Column(db.Text)
    user = db.Column(db.String(100), default='System')
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ActivityLog {self.action} on {self.table_name}>'