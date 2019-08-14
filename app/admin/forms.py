from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, BooleanField, DecimalField
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
    basic_salary_or_not = BooleanField('Whether the employee with basic salary', validators=[validators.Optional()])
    basic_salary = DecimalField('Basic Salary', validators=[validators.Optional()])
    percentage = DecimalField('Proportion of Commission', validators=[validators.Optional()])
    total_paid = DecimalField('Total Paid', default=0)
    owned_salary = DecimalField('Salary Due', default=0)
    #photo = FileField(validators=[FileRequired()])
    submit = SubmitField('Submit')

class SearchForm(FlaskForm):
    """
    Form for searching anchor information
    """
    search = StringField('please input the anchor name')
    submit = SubmitField('Search')
