from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, FloatField, SelectField, SubmitField, DateField
from wtforms.validators import DataRequired, Length, NumberRange, Optional
from models import Category, Warehouse, Item

class CategoryForm(FlaskForm):
    name = StringField('Category Name', validators=[DataRequired(), Length(min=2, max=100)])
    description = TextAreaField('Description', validators=[Optional(), Length(max=500)])
    submit = SubmitField('Save Category')

class WarehouseForm(FlaskForm):
    name = StringField('Warehouse Name', validators=[DataRequired(), Length(min=2, max=100)])
    location = StringField('Location', validators=[DataRequired(), Length(min=5, max=200)])
    manager = StringField('Manager', validators=[Optional(), Length(max=100)])
    submit = SubmitField('Save Warehouse')

class ItemForm(FlaskForm):
    code = StringField('Item Code', validators=[DataRequired(), Length(min=2, max=50)])
    name = StringField('Item Name', validators=[DataRequired(), Length(min=2, max=200)])
    description = TextAreaField('Description', validators=[Optional(), Length(max=500)])
    quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=0)])
    min_stock = IntegerField('Minimum Stock', validators=[DataRequired(), NumberRange(min=1)])
    unit_price = FloatField('Unit Price', validators=[DataRequired(), NumberRange(min=0.01)])
    supplier = StringField('Supplier', validators=[Optional(), Length(max=200)])
    category_id = SelectField('Category', validators=[DataRequired()], coerce=int)
    warehouse_id = SelectField('Warehouse', validators=[DataRequired()], coerce=int)
    submit = SubmitField('Save Item')
    
    def __init__(self, *args, **kwargs):
        super(ItemForm, self).__init__(*args, **kwargs)
        self.category_id.choices = [(c.id, c.name) for c in Category.query.order_by(Category.name).all()]
        self.warehouse_id.choices = [(w.id, w.name) for w in Warehouse.query.order_by(Warehouse.name).all()]

class IncomingItemForm(FlaskForm):
    item_id = SelectField('Item', validators=[DataRequired()], coerce=int)
    quantity = IntegerField('Quantity Received', validators=[DataRequired(), NumberRange(min=1)])
    unit_price = FloatField('Unit Price', validators=[DataRequired(), NumberRange(min=0.01)])
    supplier = StringField('Supplier', validators=[Optional(), Length(max=200)])
    batch_number = StringField('Batch Number', validators=[Optional(), Length(max=100)])
    expiry_date = DateField('Expiry Date', validators=[Optional()])
    notes = TextAreaField('Notes', validators=[Optional(), Length(max=500)])
    received_by = StringField('Received By', validators=[Optional(), Length(max=100)])
    submit = SubmitField('Record Incoming Items')
    
    def __init__(self, *args, **kwargs):
        super(IncomingItemForm, self).__init__(*args, **kwargs)
        self.item_id.choices = [(i.id, f"{i.code} - {i.name}") for i in Item.query.order_by(Item.name).all()]

class OutgoingItemForm(FlaskForm):
    item_id = SelectField('Item', validators=[DataRequired()], coerce=int)
    quantity = IntegerField('Quantity Issued', validators=[DataRequired(), NumberRange(min=1)])
    destination = StringField('Destination', validators=[DataRequired(), Length(min=2, max=200)])
    purpose = StringField('Purpose', validators=[Optional(), Length(max=200)])
    request_number = StringField('Request Number', validators=[Optional(), Length(max=100)])
    notes = TextAreaField('Notes', validators=[Optional(), Length(max=500)])
    issued_by = StringField('Issued By', validators=[Optional(), Length(max=100)])
    submit = SubmitField('Record Outgoing Items')
    
    def __init__(self, *args, **kwargs):
        super(OutgoingItemForm, self).__init__(*args, **kwargs)
        self.item_id.choices = [(i.id, f"{i.code} - {i.name} (Stock: {i.quantity})") for i in Item.query.filter(Item.quantity > 0).order_by(Item.name).all()]
