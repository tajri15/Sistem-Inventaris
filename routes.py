from flask import render_template, request, redirect, url_for, flash, jsonify
from app import app, db
from models import Item, Category, Warehouse, ActivityLog
from forms import ItemForm, CategoryForm, WarehouseForm
from sqlalchemy import or_, desc
from datetime import datetime

def log_activity(action, table_name, record_id, details=None):
    """Helper function to log activities"""
    log = ActivityLog(
        action=action,
        table_name=table_name,
        record_id=record_id,
        details=details
    )
    db.session.add(log)
    db.session.commit()

@app.route('/')
def dashboard():
    """Main dashboard with key statistics"""
    total_items = Item.query.count()
    total_categories = Category.query.count()
    total_warehouses = Warehouse.query.count()
    
    # Low stock items
    low_stock_items = Item.query.filter(Item.quantity <= Item.min_stock).all()
    low_stock_count = len(low_stock_items)
    
    # Total inventory value
    total_value = sum(item.total_value for item in Item.query.all())
    
    # Recent activities
    recent_activities = ActivityLog.query.order_by(desc(ActivityLog.timestamp)).limit(10).all()
    
    return render_template('dashboard.html',
                         total_items=total_items,
                         total_categories=total_categories,
                         total_warehouses=total_warehouses,
                         low_stock_count=low_stock_count,
                         low_stock_items=low_stock_items[:5],  # Show only first 5
                         total_value=total_value,
                         recent_activities=recent_activities)

@app.route('/items')
def items():
    """View all items with search and filter functionality"""
    search = request.args.get('search', '')
    category_filter = request.args.get('category', '')
    warehouse_filter = request.args.get('warehouse', '')
    stock_filter = request.args.get('stock', '')
    
    query = Item.query
    
    # Apply search filter
    if search:
        query = query.filter(or_(
            Item.code.contains(search),
            Item.name.contains(search),
            Item.description.contains(search)
        ))
    
    # Apply category filter
    if category_filter:
        query = query.filter(Item.category_id == category_filter)
    
    # Apply warehouse filter
    if warehouse_filter:
        query = query.filter(Item.warehouse_id == warehouse_filter)
    
    # Apply stock filter
    if stock_filter == 'low':
        query = query.filter(Item.quantity <= Item.min_stock)
    elif stock_filter == 'out':
        query = query.filter(Item.quantity == 0)
    
    items = query.order_by(Item.name).all()
    categories = Category.query.order_by(Category.name).all()
    warehouses = Warehouse.query.order_by(Warehouse.name).all()
    
    return render_template('items.html',
                         items=items,
                         categories=categories,
                         warehouses=warehouses,
                         search=search,
                         category_filter=category_filter,
                         warehouse_filter=warehouse_filter,
                         stock_filter=stock_filter)

@app.route('/items/add', methods=['GET', 'POST'])
def add_item():
    """Add new item"""
    form = ItemForm()
    
    if form.validate_on_submit():
        # Check if code already exists
        existing_item = Item.query.filter_by(code=form.code.data).first()
        if existing_item:
            flash('Item code already exists. Please use a different code.', 'error')
            return render_template('items.html', form=form, action='Add')
        
        item = Item(
            code=form.code.data,
            name=form.name.data,
            description=form.description.data,
            quantity=form.quantity.data,
            min_stock=form.min_stock.data,
            unit_price=form.unit_price.data,
            supplier=form.supplier.data,
            category_id=form.category_id.data,
            warehouse_id=form.warehouse_id.data
        )
        
        db.session.add(item)
        db.session.commit()
        
        # Log activity
        log_activity('CREATE', 'items', item.id, f'Added new item: {item.name}')
        
        flash('Item added successfully!', 'success')
        return redirect(url_for('items'))
    
    return render_template('items.html', form=form, action='Add')

@app.route('/items/edit/<int:id>', methods=['GET', 'POST'])
def edit_item(id):
    """Edit existing item"""
    item = Item.query.get_or_404(id)
    form = ItemForm(obj=item)
    
    if form.validate_on_submit():
        # Check if code already exists (excluding current item)
        existing_item = Item.query.filter(Item.code == form.code.data, Item.id != id).first()
        if existing_item:
            flash('Item code already exists. Please use a different code.', 'error')
            return render_template('items.html', form=form, action='Edit', item=item)
        
        old_values = f"Code: {item.code}, Name: {item.name}, Quantity: {item.quantity}"
        
        item.code = form.code.data
        item.name = form.name.data
        item.description = form.description.data
        item.quantity = form.quantity.data
        item.min_stock = form.min_stock.data
        item.unit_price = form.unit_price.data
        item.supplier = form.supplier.data
        item.category_id = form.category_id.data
        item.warehouse_id = form.warehouse_id.data
        item.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        # Log activity
        log_activity('UPDATE', 'items', item.id, f'Updated item from ({old_values}) to ({item.code}, {item.name}, {item.quantity})')
        
        flash('Item updated successfully!', 'success')
        return redirect(url_for('items'))
    
    return render_template('items.html', form=form, action='Edit', item=item)

@app.route('/items/delete/<int:id>', methods=['POST'])
def delete_item(id):
    """Delete item"""
    item = Item.query.get_or_404(id)
    item_details = f"Code: {item.code}, Name: {item.name}"
    
    db.session.delete(item)
    db.session.commit()
    
    # Log activity
    log_activity('DELETE', 'items', id, f'Deleted item: {item_details}')
    
    flash('Item deleted successfully!', 'success')
    return redirect(url_for('items'))

@app.route('/categories')
def categories():
    """View all categories"""
    categories = Category.query.order_by(Category.name).all()
    return render_template('categories.html', categories=categories)

@app.route('/categories/add', methods=['GET', 'POST'])
def add_category():
    """Add new category"""
    form = CategoryForm()
    
    if form.validate_on_submit():
        # Check if name already exists
        existing_category = Category.query.filter_by(name=form.name.data).first()
        if existing_category:
            flash('Category name already exists. Please use a different name.', 'error')
            return render_template('categories.html', form=form, action='Add')
        
        category = Category(
            name=form.name.data,
            description=form.description.data
        )
        
        db.session.add(category)
        db.session.commit()
        
        # Log activity
        log_activity('CREATE', 'categories', category.id, f'Added new category: {category.name}')
        
        flash('Category added successfully!', 'success')
        return redirect(url_for('categories'))
    
    return render_template('categories.html', form=form, action='Add')

@app.route('/categories/edit/<int:id>', methods=['GET', 'POST'])
def edit_category(id):
    """Edit existing category"""
    category = Category.query.get_or_404(id)
    form = CategoryForm(obj=category)
    
    if form.validate_on_submit():
        # Check if name already exists (excluding current category)
        existing_category = Category.query.filter(Category.name == form.name.data, Category.id != id).first()
        if existing_category:
            flash('Category name already exists. Please use a different name.', 'error')
            return render_template('categories.html', form=form, action='Edit', category=category)
        
        old_name = category.name
        category.name = form.name.data
        category.description = form.description.data
        
        db.session.commit()
        
        # Log activity
        log_activity('UPDATE', 'categories', category.id, f'Updated category from "{old_name}" to "{category.name}"')
        
        flash('Category updated successfully!', 'success')
        return redirect(url_for('categories'))
    
    return render_template('categories.html', form=form, action='Edit', category=category)

@app.route('/categories/delete/<int:id>', methods=['POST'])
def delete_category(id):
    """Delete category"""
    category = Category.query.get_or_404(id)
    
    # Check if category has items
    if category.items:
        flash(f'Cannot delete category "{category.name}" because it has {len(category.items)} items associated with it.', 'error')
        return redirect(url_for('categories'))
    
    category_name = category.name
    db.session.delete(category)
    db.session.commit()
    
    # Log activity
    log_activity('DELETE', 'categories', id, f'Deleted category: {category_name}')
    
    flash('Category deleted successfully!', 'success')
    return redirect(url_for('categories'))

@app.route('/warehouses')
def warehouses():
    """View all warehouses"""
    warehouses = Warehouse.query.order_by(Warehouse.name).all()
    return render_template('warehouses.html', warehouses=warehouses)

@app.route('/warehouses/add', methods=['GET', 'POST'])
def add_warehouse():
    """Add new warehouse"""
    form = WarehouseForm()
    
    if form.validate_on_submit():
        # Check if name already exists
        existing_warehouse = Warehouse.query.filter_by(name=form.name.data).first()
        if existing_warehouse:
            flash('Warehouse name already exists. Please use a different name.', 'error')
            return render_template('warehouses.html', form=form, action='Add')
        
        warehouse = Warehouse(
            name=form.name.data,
            location=form.location.data,
            manager=form.manager.data
        )
        
        db.session.add(warehouse)
        db.session.commit()
        
        # Log activity
        log_activity('CREATE', 'warehouses', warehouse.id, f'Added new warehouse: {warehouse.name}')
        
        flash('Warehouse added successfully!', 'success')
        return redirect(url_for('warehouses'))
    
    return render_template('warehouses.html', form=form, action='Add')

@app.route('/warehouses/edit/<int:id>', methods=['GET', 'POST'])
def edit_warehouse(id):
    """Edit existing warehouse"""
    warehouse = Warehouse.query.get_or_404(id)
    form = WarehouseForm(obj=warehouse)
    
    if form.validate_on_submit():
        # Check if name already exists (excluding current warehouse)
        existing_warehouse = Warehouse.query.filter(Warehouse.name == form.name.data, Warehouse.id != id).first()
        if existing_warehouse:
            flash('Warehouse name already exists. Please use a different name.', 'error')
            return render_template('warehouses.html', form=form, action='Edit', warehouse=warehouse)
        
        old_name = warehouse.name
        warehouse.name = form.name.data
        warehouse.location = form.location.data
        warehouse.manager = form.manager.data
        
        db.session.commit()
        
        # Log activity
        log_activity('UPDATE', 'warehouses', warehouse.id, f'Updated warehouse from "{old_name}" to "{warehouse.name}"')
        
        flash('Warehouse updated successfully!', 'success')
        return redirect(url_for('warehouses'))
    
    return render_template('warehouses.html', form=form, action='Edit', warehouse=warehouse)

@app.route('/warehouses/delete/<int:id>', methods=['POST'])
def delete_warehouse(id):
    """Delete warehouse"""
    warehouse = Warehouse.query.get_or_404(id)
    
    # Check if warehouse has items
    if warehouse.items:
        flash(f'Cannot delete warehouse "{warehouse.name}" because it has {len(warehouse.items)} items associated with it.', 'error')
        return redirect(url_for('warehouses'))
    
    warehouse_name = warehouse.name
    db.session.delete(warehouse)
    db.session.commit()
    
    # Log activity
    log_activity('DELETE', 'warehouses', id, f'Deleted warehouse: {warehouse_name}')
    
    flash('Warehouse deleted successfully!', 'success')
    return redirect(url_for('warehouses'))

@app.route('/activity-log')
def activity_log():
    """View activity log"""
    page = request.args.get('page', 1, type=int)
    per_page = 50
    
    activities = ActivityLog.query.order_by(desc(ActivityLog.timestamp)).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return render_template('activity_log.html', activities=activities)
