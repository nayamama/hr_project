from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, SubmitField, DateField, BooleanField, DecimalField, SelectField
from wtforms.validators import DataRequired
from wtforms import validators
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from ..models import Department, Role


class DepartmentForm(FlaskForm):
    """
    Form for admin to add or edit a department
    """
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')

class RoleForm(FlaskForm):
    """
    Form for admin to add or edit a role
    """
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')

class EmployeeAssignForm(FlaskForm):
    """
    Form for admin to assign departments and roles to employees
    """
    department = QuerySelectField(query_factory=lambda: Department.query.all(),
                                  get_label="name")
    role = QuerySelectField(query_factory=lambda: Role.query.all(),
                            get_label="name")
    submit = SubmitField('Submit')

class AnchorForm(FlaskForm):
    """
    Form for detailed employee information
    """
    name = StringField('Name', validators=[DataRequired()])
    entry_time = DateField('Entry Date', format='%Y-%m-%d')
    address = StringField('Address', validators=[DataRequired()])
    momo_number = StringField('MOMO #', validators=[DataRequired()])
    mobile_number = StringField('Mobile #', validators=[DataRequired()])
    id_number = StringField('ID Number', validators=[DataRequired()])
    basic_salary_or_not = BooleanField('Whether the employee with basic salary', validators=[validators.Optional()])
    basic_salary = DecimalField('Basic Salary', validators=[validators.Optional()])
    live_time = DecimalField('Live Time', validators=[validators.Optional()])
    live_session = SelectField(
        'Live Session',
        choices=[('morning', 'Morning'), ('afternoon', 'Afternoon'), ('evening', 'Evening'), ('night', 'Night')]
    )
    percentage = DecimalField('Proportion of Commission', validators=[validators.Optional()])
    ace_anchor_or_not = BooleanField('Whether Ace anchor or not', validators=[validators.Optional()])
    agent = StringField('Agent', validators=[validators.optional()])
    #total_paid = DecimalField('Total Paid', default=0)
    #owned_salary = DecimalField('Salary Due', default=0)
    #photo = FileField(validators=[FileRequired()])
    photo = FileField()
    submit = SubmitField('Submit')

class SearchForm(FlaskForm):
    """
    Form for searching anchor information
    """
    search = StringField('please input the anchor name')
    submit = SubmitField('Search')
