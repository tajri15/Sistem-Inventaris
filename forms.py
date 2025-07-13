from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, IntegerField, FloatField, SelectField, DateField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length, NumberRange, Optional
from models import User, Category, Item

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match.')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('This username is already taken.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('This email address is already registered.')

class CategoryForm(FlaskForm):
    name = StringField('Category Name', validators=[DataRequired(), Length(min=2, max=100)])
    description = TextAreaField('Description', validators=[Optional(), Length(max=500)])
    submit = SubmitField('Save Category')

class ItemForm(FlaskForm):
    code = StringField('Item Code', validators=[DataRequired(), Length(min=2, max=50)])
    name = StringField('Item Name', validators=[DataRequired(), Length(min=2, max=200)])
    description = TextAreaField('Description', validators=[Optional(), Length(max=500)])
    quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=0)])
    unit_price = FloatField('Unit Price', validators=[DataRequired(), NumberRange(min=0.01)])
    supplier = StringField('Supplier', validators=[Optional(), Length(max=200)])
    category_id = SelectField('Category', validators=[DataRequired()], coerce=int)
    submit = SubmitField('Save Item')
    
    def __init__(self, *args, **kwargs):
        super(ItemForm, self).__init__(*args, **kwargs)
        self.category_id.choices = [(c.id, c.name) for c in Category.query.order_by(Category.name).all()]

class IncomingItemForm(FlaskForm):
    item_id = SelectField('Item', validators=[DataRequired()], coerce=int)
    quantity = IntegerField('Quantity Received', validators=[DataRequired(), NumberRange(min=1)])
    unit_price = FloatField('Unit Price', validators=[DataRequired(), NumberRange(min=0.01)])
    supplier = StringField('Supplier', validators=[Optional(), Length(max=200)])
    batch_number = StringField('Batch Number', validators=[Optional(), Length(max=100)])
    expiry_date = DateField('Expiry Date', validators=[Optional()])
    notes = TextAreaField('Notes', validators=[Optional(), Length(max=500)])
    received_by = StringField('Received By', validators=[DataRequired(), Length(max=100)])
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
    issued_by = StringField('Issued By', validators=[DataRequired(), Length(max=100)])
    submit = SubmitField('Record Outgoing Items')
    
    def __init__(self, *args, **kwargs):
        super(OutgoingItemForm, self).__init__(*args, **kwargs)
        self.item_id.choices = [(i.id, f"{i.code} - {i.name} (Stock: {i.quantity})") for i in Item.query.filter(Item.quantity > 0).order_by(Item.name).all()]