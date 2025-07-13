from flask import render_template, request, redirect, url_for, flash, jsonify
from app import app, db
from models import User, Item, Category, ActivityLog, IncomingItem, OutgoingItem
from forms import LoginForm, RegistrationForm, ItemForm, CategoryForm, IncomingItemForm, OutgoingItemForm
from flask_login import current_user, login_user, logout_user, login_required
from sqlalchemy import or_, desc
from datetime import datetime

def log_activity(action, table_name, record_id, details=None):
    """Helper function to log activities"""
    log = ActivityLog(
        action=action,
        table_name=table_name,
        record_id=record_id,
        details=details,
        user=current_user.username if current_user.is_authenticated else 'System'
    )
    db.session.add(log)
    db.session.commit()

# --- AUTHENTICATION ROUTES ---

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        
        next_page = request.args.get('next')
        return redirect(next_page) if next_page else redirect(url_for('dashboard'))
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


# --- MAIN APPLICATION ROUTES ---

@app.route('/')
@login_required
def dashboard():
    """Main dashboard with key statistics"""
    total_items = Item.query.count()
    total_categories = Category.query.count()
    
    from datetime import timedelta
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    
    total_incoming = IncomingItem.query.filter(IncomingItem.received_date >= thirty_days_ago).count()
    total_outgoing = OutgoingItem.query.filter(OutgoingItem.issued_date >= thirty_days_ago).count()
    
    recent_activities = ActivityLog.query.order_by(desc(ActivityLog.timestamp)).limit(10).all()
    
    return render_template('dashboard.html',
                         total_items=total_items,
                         total_categories=total_categories,
                         total_incoming=total_incoming,
                         total_outgoing=total_outgoing,
                         recent_activities=recent_activities)

@app.route('/items')
@login_required
def items():
    """View all items with search and filter functionality"""
    search = request.args.get('search', '')
    category_filter = request.args.get('category', '')
    
    query = Item.query
    
    if search:
        query = query.filter(or_(
            Item.code.contains(search),
            Item.name.contains(search),
            Item.description.contains(search)
        ))
    
    if category_filter:
        query = query.filter(Item.category_id == category_filter)
    
    items_list = query.order_by(Item.name).all()
    categories_list = Category.query.order_by(Category.name).all()
    
    return render_template('items.html',
                         items=items_list,
                         categories=categories_list,
                         search=search,
                         category_filter=category_filter)

@app.route('/items/add', methods=['POST'])
@login_required
def add_item():
    """Add new item"""
    form = ItemForm()
    
    if form.validate_on_submit():
        existing_item = Item.query.filter_by(code=form.code.data).first()
        if existing_item:
            flash('Item code already exists. Please use a different code.', 'error')
        else:
            item = Item(
                code=form.code.data,
                name=form.name.data,
                description=form.description.data,
                quantity=form.quantity.data,
                unit_price=form.unit_price.data,
                supplier=form.supplier.data,
                category_id=form.category_id.data
            )
            db.session.add(item)
            db.session.commit()
            log_activity('CREATE', 'items', item.id, f'Added new item: {item.name}')
            flash('Item added successfully!', 'success')
    else:
        flash('There was an error with your submission.', 'danger')
    return redirect(url_for('items'))

@app.route('/items/edit/<int:id>', methods=['POST'])
@login_required
def edit_item(id):
    """Edit existing item"""
    item = Item.query.get_or_404(id)
    form = ItemForm()
    
    if form.validate_on_submit():
        existing_item = Item.query.filter(Item.code == form.code.data, Item.id != id).first()
        if existing_item:
            flash('Item code already exists. Please use a different code.', 'error')
        else:
            old_values = f"Code: {item.code}, Name: {item.name}, Quantity: {item.quantity}"
            item.code = form.code.data
            item.name = form.name.data
            item.description = form.description.data
            item.quantity = form.quantity.data
            item.unit_price = form.unit_price.data
            item.supplier = form.supplier.data
            item.category_id = form.category_id.data
            item.updated_at = datetime.utcnow()
            db.session.commit()
            log_activity('UPDATE', 'items', item.id, f'Updated item from ({old_values}) to ({item.code}, {item.name}, {item.quantity})')
            flash('Item updated successfully!', 'success')
    else:
        flash('There was an error with your submission.', 'danger')
    return redirect(url_for('items'))

@app.route('/items/delete/<int:id>', methods=['POST'])
@login_required
def delete_item(id):
    """Delete item"""
    item = Item.query.get_or_404(id)
    item_details = f"Code: {item.code}, Name: {item.name}"
    
    db.session.delete(item)
    db.session.commit()
    log_activity('DELETE', 'items', id, f'Deleted item: {item_details}')
    flash('Item deleted successfully!', 'success')
    return redirect(url_for('items'))

@app.route('/categories')
@login_required
def categories():
    """View all categories"""
    categories_list = Category.query.order_by(Category.name).all()
    return render_template('categories.html', categories=categories_list)

@app.route('/categories/add', methods=['POST'])
@login_required
def add_category():
    """Add new category"""
    form = CategoryForm()
    if form.validate_on_submit():
        existing_category = Category.query.filter_by(name=form.name.data).first()
        if existing_category:
            flash('Category name already exists. Please use a different name.', 'error')
        else:
            category = Category(
                name=form.name.data,
                description=form.description.data
            )
            db.session.add(category)
            db.session.commit()
            log_activity('CREATE', 'categories', category.id, f'Added new category: {category.name}')
            flash('Category added successfully!', 'success')
    return redirect(url_for('categories'))

@app.route('/categories/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_category(id):
    category = Category.query.get_or_404(id)
    if request.method == 'POST':
        form = CategoryForm()
        if form.validate_on_submit():
            existing_category = Category.query.filter(Category.name == form.name.data, Category.id != id).first()
            if existing_category:
                flash('Category name already exists. Please use a different name.', 'error')
                return redirect(url_for('categories'))
            
            old_name = category.name
            category.name = form.name.data
            category.description = form.description.data
            db.session.commit()
            log_activity('UPDATE', 'categories', category.id, f'Updated category from "{old_name}" to "{category.name}"')
            flash('Category updated successfully!', 'success')
            return redirect(url_for('categories'))
    # For GET request, return data as JSON to populate modal via JS
    return jsonify({
        'id': category.id,
        'name': category.name,
        'description': category.description or ''
    })


@app.route('/categories/delete/<int:id>', methods=['POST'])
@login_required
def delete_category(id):
    """Delete category"""
    category = Category.query.get_or_404(id)
    if category.items:
        flash(f'Cannot delete category "{category.name}" because it has items associated with it.', 'error')
    else:
        category_name = category.name
        db.session.delete(category)
        db.session.commit()
        log_activity('DELETE', 'categories', id, f'Deleted category: {category_name}')
        flash('Category deleted successfully!', 'success')
    return redirect(url_for('categories'))

@app.route('/activity-log')
@login_required
def activity_log():
    """View activity log"""
    page = request.args.get('page', 1, type=int)
    per_page = 50
    activities = ActivityLog.query.order_by(desc(ActivityLog.timestamp)).paginate(
        page=page, per_page=per_page, error_out=False
    )
    return render_template('activity_log.html', activities=activities)

@app.route('/incoming-items')
@login_required
def incoming_items():
    """View all incoming items"""
    page = request.args.get('page', 1, type=int)
    per_page = 20
    incoming = IncomingItem.query.order_by(desc(IncomingItem.received_date)).paginate(
        page=page, per_page=per_page, error_out=False
    )
    form = IncomingItemForm()
    # Populate received_by with current user's username
    form.received_by.data = current_user.username
    return render_template('incoming_items.html', incoming=incoming, form=form)

@app.route('/incoming-items/add', methods=['POST'])
@login_required
def add_incoming_item():
    """Add new incoming item"""
    form = IncomingItemForm()
    if form.validate_on_submit():
        item = Item.query.get(form.item_id.data)
        incoming = IncomingItem(
            item_id=form.item_id.data,
            quantity=form.quantity.data,
            unit_price=form.unit_price.data,
            supplier=form.supplier.data,
            batch_number=form.batch_number.data,
            expiry_date=form.expiry_date.data,
            notes=form.notes.data,
            received_by=form.received_by.data
        )
        item.quantity += form.quantity.data
        item.updated_at = datetime.utcnow()
        db.session.add(incoming)
        db.session.commit()
        log_activity('CREATE', 'incoming_items', incoming.id, 
                    f'Received {form.quantity.data} units of {item.name}')
        flash(f'Successfully recorded incoming {form.quantity.data} units of {item.name}!', 'success')
    else:
        flash('There was an error with your submission.', 'danger')
    return redirect(url_for('incoming_items'))

@app.route('/outgoing-items')
@login_required
def outgoing_items():
    """View all outgoing items"""
    page = request.args.get('page', 1, type=int)
    per_page = 20
    outgoing = OutgoingItem.query.order_by(desc(OutgoingItem.issued_date)).paginate(
        page=page, per_page=per_page, error_out=False
    )
    form = OutgoingItemForm()
    # Populate issued_by with current user's username
    form.issued_by.data = current_user.username
    return render_template('outgoing_items.html', outgoing=outgoing, form=form)

@app.route('/outgoing-items/add', methods=['POST'])
@login_required
def add_outgoing_item():
    """Add new outgoing item"""
    form = OutgoingItemForm()
    if form.validate_on_submit():
        item = Item.query.get(form.item_id.data)
        if item.quantity < form.quantity.data:
            flash(f'Insufficient stock! Available: {item.quantity}, Requested: {form.quantity.data}', 'error')
        else:
            outgoing = OutgoingItem(
                item_id=form.item_id.data,
                quantity=form.quantity.data,
                destination=form.destination.data,
                purpose=form.purpose.data,
                request_number=form.request_number.data,
                notes=form.notes.data,
                issued_by=form.issued_by.data
            )
            item.quantity -= form.quantity.data
            item.updated_at = datetime.utcnow()
            db.session.add(outgoing)
            db.session.commit()
            log_activity('CREATE', 'outgoing_items', outgoing.id,
                        f'Issued {form.quantity.data} units of {item.name} to {form.destination.data}')
            flash(f'Successfully recorded outgoing {form.quantity.data} units of {item.name}!', 'success')
    else:
        flash('There was an error with your submission.', 'danger')
    return redirect(url_for('outgoing_items'))