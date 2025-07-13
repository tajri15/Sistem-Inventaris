from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, FloatField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, Optional
from models import Category, Warehouse

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
