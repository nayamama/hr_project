import os
from flask import abort, flash, redirect, render_template, url_for, request
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename

from . import admin
from forms import DepartmentForm, RoleForm, EmployeeAssignForm, AnchorForm, SearchForm
from .. import db
from ..models import Department, Role, Employee, Anchor
from helper import get_system_info


def check_admin():
    """
    Prevent non-admins from accessing the page
    """
    if not current_user.is_admin:
        abort(403)


# Department Views


@admin.route('/departments', methods=['GET', 'POST'])
@login_required
def list_departments():
    """
    List all departments
    """
    check_admin()

    departments = Department.query.all()

    return render_template('admin/departments/departments.html',
                           departments=departments, title="Departments")


@admin.route('/departments/add', methods=['GET', 'POST'])
@login_required
def add_department():
    """
    Add a department to the database
    """
    check_admin()

    add_department = True

    form = DepartmentForm()
    if form.validate_on_submit():
        department = Department(name=form.name.data,
                                description=form.description.data)
        try:
            # add department to the database
            db.session.add(department)
            db.session.commit()
            flash('You have successfully added a new department.')
        except:
            # in case department name already exists
            flash('Error: department name already exists.')

        # redirect to departments page
        return redirect(url_for('admin.list_departments'))

    # load department template
    return render_template('admin/departments/department.html', action="Add",
                           add_department=add_department, form=form,
                           title="Add Department")


@admin.route('/departments/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_department(id):
    """
    Edit a department
    """
    check_admin()

    add_department = False

    department = Department.query.get_or_404(id)
    form = DepartmentForm(obj=department)
    if form.validate_on_submit():
        department.name = form.name.data
        department.description = form.description.data
        db.session.commit()
        flash('You have successfully edited the department.')

        # redirect to the departments page
        return redirect(url_for('admin.list_departments'))

    form.description.data = department.description
    form.name.data = department.name
    return render_template('admin/departments/department.html', action="Edit",
                           add_department=add_department, form=form,
                           department=department, title="Edit Department")


@admin.route('/departments/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_department(id):
    """
    Delete a department from the database
    """
    check_admin()

    department = Department.query.get_or_404(id)
    db.session.delete(department)
    db.session.commit()
    flash('You have successfully deleted the department.')

    # redirect to the departments page
    return redirect(url_for('admin.list_departments'))

    return render_template(title="Delete Department")


@admin.route('/roles')
@login_required
def list_roles():
    check_admin()
    """
    List all roles
    """
    roles = Role.query.all()
    return render_template('admin/roles/roles.html',
                           roles=roles, title='Roles')


@admin.route('/roles/add', methods=['GET', 'POST'])
@login_required
def add_role():
    """
    Add a role to the database
    """
    check_admin()

    add_role = True

    form = RoleForm()
    if form.validate_on_submit():
        role = Role(name=form.name.data,
                    description=form.description.data)

        try:
            # add role to the database
            db.session.add(role)
            db.session.commit()
            flash('You have successfully added a new role.')
        except:
            # in case role name already exists
            flash('Error: role name already exists.')

        # redirect to the roles page
        return redirect(url_for('admin.list_roles'))

    # load role template
    return render_template('admin/roles/role.html', add_role=add_role,
                           form=form, title='Add Role')


@admin.route('/roles/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_role(id):
    """
    Edit a role
    """
    check_admin()

    add_role = False

    role = Role.query.get_or_404(id)
    form = RoleForm(obj=role)
    if form.validate_on_submit():
        role.name = form.name.data
        role.description = form.description.data
        db.session.add(role)
        db.session.commit()
        flash('You have successfully edited the role.')

        # redirect to the roles page
        return redirect(url_for('admin.list_roles'))

    form.description.data = role.description
    form.name.data = role.name
    return render_template('admin/roles/role.html', add_role=add_role,
                           form=form, title="Edit Role")


@admin.route('/roles/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_role(id):
    """
    Delete a role from the database
    """
    check_admin()

    role = Role.query.get_or_404(id)
    db.session.delete(role)
    db.session.commit()
    flash('You have successfully deleted the role.')

    # redirect to the roles page
    return redirect(url_for('admin.list_roles'))

    return render_template(title="Delete Role")

@admin.route('/employees')
@login_required
def list_employees():
    """
    List all employees
    """
    check_admin()

    employees = Employee.query.all()
    return render_template('admin/employees/employees.html',
                           employees=employees, title='Employees')


@admin.route('/employees/assign/<int:id>', methods=['GET', 'POST'])
@login_required
def assign_employee(id):
    """
    Assign a department and a role to an employee
    """
    check_admin()

    employee = Employee.query.get_or_404(id)

    # prevent admin from being assigned a department or role
    if employee.is_admin:
        abort(403)

    form = EmployeeAssignForm(obj=employee)
    if form.validate_on_submit():
        employee.department = form.department.data
        employee.role = form.role.data
        db.session.add(employee)
        db.session.commit()
        flash('You have successfully assigned a department and role.')

        # redirect to the roles page
        return redirect(url_for('admin.list_employees'))

    return render_template('admin/employees/employee.html',
                           employee=employee, form=form,
                           title='Assign Employee')

@admin.route('/anchors')
@login_required
def list_anchors():
    check_admin()
    """
    List all anchors
    """
    anchors = Anchor.query.all()
    return render_template('admin/anchors/anchors.html',
                           anchors=anchors, title='Anchors')

@admin.route('/anchors/add_salary_anchor', methods=['GET', 'POST'])
@login_required
def add_salary_anchor():
    """
    Add an anchor with salary to the database
    """
    check_admin()

    add_anchor = "anchor_with_salary"

    form = AnchorForm()

    # remove no-relative fields
    del form.basic_salary_or_not
    del form.percentage
    del form.photo

    if form.validate_on_submit():
        anchor = Anchor(name=form.name.data,
                        entry_time=form.entry_time.data,
                        #basic_salary_or_not=form.basic_salary_or_not.data
                        basic_salary_or_not=True,
                        basic_salary=form.basic_salary.data)
                        #percentage=form.percentage.data
                        #total_paid=form.total_paid.data,
                        #owned_salary=form.owned_salary.data

        try:
            db.session.add(anchor)
            db.session.commit()

            # create folder to store personal image files
            directory = '/home/qi/projects/maomao_files/' + form.name.data
            if not os.path.exists(directory):
                os.mkdir(directory)
            flash('You have successfully added a new anchor.')
        except:
            flash('Error: anchor name already exists.')

        return redirect(url_for('admin.list_anchors'))

    # load anchor template
    return render_template('admin/anchors/anchor.html', action="Add",
                           add_anchor=add_anchor, form=form,
                           title="Add Anchor with Salary")

@admin.route('/anchors/add_commission_anchor', methods=['GET', 'POST'])
@login_required
def add_commission_anchor():
    """
    Add an anchor with commission to the database
    """
    check_admin()

    add_anchor = "anchor_with_commission"

    form = AnchorForm()
    del form.basic_salary
    del form.basic_salary_or_not
    del form.photo

    if form.validate_on_submit():
        anchor = Anchor(
            name=form.name.data,
            entry_time=form.entry_time.data,
            basic_salary_or_not=False,
            percentage=form.percentage.data
        )
        try:
            db.session.add(anchor)
            db.session.commit()

            directory = '/home/qi/projects/maomao_files/' + form.name.data
            if not os.path.exists(directory):
                os.mkdir(directory)

            flash('You have successfully added a new anchor.')
        except:
            flash('Error: anchor name already exists.')

        return redirect(url_for('admin.list_anchors'))

    return render_template('admin/anchors/anchor.html', action="Add",
                           add_anchor=add_anchor, form=form,
                           title="Add Anchor with Commission")

@admin.route('/anchors/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_anchor(id):
    """
    Edit an anchor
    """
    check_admin()

    add_anchor = False

    anchor = Anchor.query.get_or_404(id)
    form = AnchorForm(obj=anchor)
    if form.validate_on_submit():
        anchor.name = form.name.data
        anchor.entry_time = form.entry_time.data
        anchor.basic_salary_or_not = form.basic_salary_or_not.data
        anchor.basic_salary = form.basic_salary.data
        anchor.percentage = form.percentage.data
        anchor.total_paid = form.total_paid.data
        anchor.owned_salary = form.owned_salary.data

        # save image file
        if form.photo.data:
            f = form.photo.data
            filename = secure_filename(f.filename)
            UPLOAD_FOLDER = '/home/qi/projects/maomao_files'
            f.save(os.path.join(UPLOAD_FOLDER, form.name.data, filename))

        db.session.add(anchor)
        db.session.commit()
        flash('You have successfully edited the anchor.')

        # redirect to the anchors page
        return redirect(url_for('admin.list_anchors'))

    form.name.data = anchor.name
    form.entry_time.data = anchor.entry_time
    form.basic_salary_or_not = anchor.basic_salary_or_not
    form.basic_salary = anchor.basic_salary
    form.percentage = anchor.percentage
    form.total_paid = anchor.total_paid
    form.owned_salary = anchor.owned_salary
    return render_template('admin/anchors/anchor.html', add_anchor=add_anchor,
                           form=form, title="Edit Anchor")
"""
@admin.route('/anchors/delete/<int:id>/<string:action>', methods=['GET', 'POST'])
@login_required
def delete_anchor_request(id):
    check_admin()
    # redirect to the roles page
    return redirect(url_for('admin.list_anchors'), id=)
"""

@admin.route('/anchors/delete/<int:id>/<string:name>/<string:action>', methods=['GET', 'POST'])
@login_required
def delete_anchor(id, action, name):
    """
    Delete an anchor from the database
    """
    check_admin()

    if action == "request":
        return render_template('admin/confirmation.html', id=id, name=name)
    if action == "confirm":
        anchor = Anchor.query.get_or_404(id)
        db.session.delete(anchor)
        db.session.commit()
        flash('You have successfully deleted the anchor.')

    # redirect to the roles page
    return redirect(url_for('admin.list_anchors'))

@admin.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    """
    Search the anchor information
    """
    check_admin()
    form = SearchForm(request.form)
    if request.method == "POST" and form.validate_on_submit():
        return redirect((url_for('admin.search_result', query=form.search.data)))
    return render_template('admin/search/search.html', form=form)


@admin.route('/results/<query>')
@login_required
def search_result(query):
    result = Anchor.query.filter_by(name=query).first()
    if not result:
        flash('No results found.')
        return redirect(url_for('admin.search'))
    else:
        form = AnchorForm(obj=result)
        name = form.name.data
        del form.submit
        return render_template('admin/search/result.html', query=query, form=form, name=name)

@admin.route('/system')
@login_required
def system_info():
    used_cpu_percent, used_disk_percent, free_disk_size = get_system_info()
    return render_template('admin/system.html', cpu=used_cpu_percent, disk=used_disk_percent, free=free_disk_size)