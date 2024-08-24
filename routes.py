from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from .models import API, User
from .forms import LoginForm, APIForm, APIRequestForm
import requests
from .utils import login_manager
main = Blueprint('main', __name__)
@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/login?next=' + request.path)
@main.route('/')
@login_required
def index():
    user_apis = API.select().where(API.user == current_user.id)
    return render_template('index.html', apis=user_apis)

@main.route('/api/<int:api_id>', methods=['GET', 'POST'])
@login_required
def api_detail(api_id):
    api = API.get_or_none(API.ID == api_id)
    
    if not api or api.user.username != current_user.id:
        flash("API not found or you don't have permission to access it", "error")
        print(f'API not found or you dont have permission to access it {current_user.id}')
        return redirect(url_for('main.index'))

    form = APIRequestForm()
    response = None

    if form.validate_on_submit():
        method = form.request_method.data
        body_type = form.body_type.data
        headers = {}
        payload = None

        # Process headers
        if form.headers.data:
            headers = dict(line.split('=', 1) for line in form.headers.data.splitlines())

        try:
            if body_type == 'json':
                headers['Content-Type'] = 'application/json'
                payload = form.request_payload.data
                response = requests.request(method, api.endpoint, headers=headers, json=payload)
            elif body_type == 'form':
                headers['Content-Type'] = 'application/x-www-form-urlencoded'
                form_data = dict(line.split('=', 1) for line in form.form_data.data.splitlines())
                response = requests.request(method, api.endpoint, headers=headers, data=form_data)
            elif body_type == 'file':
                file = form.file_upload.data
                files = {'file': (file.filename, file.stream, file.mimetype)}
                response = requests.request(method, api.endpoint, headers=headers, files=files)
            else:  # 'none'
                response = requests.request(method, api.endpoint, headers=headers)

        except Exception as e:
            flash(f"Error sending request: {e}", "error")

    return render_template('api_detail.html', api=api, response=response, form=form)
@main.route('/api/new', methods=['GET', 'POST'])
@login_required
def new_api():
    form = APIForm()

    if form.validate_on_submit():
        API.create(
            user=current_user.id,
            name=form.name.data,
            endpoint=form.endpoint.data,
            method=form.method.data,
            description=form.description.data
        )
        #API.save()
        flash("API created successfully!", "success")
        return redirect(url_for('main.index'))

    return render_template('create_api.html', form=form)

@main.route('/api/<int:api_id>/delete', methods=['POST'])
@login_required
def delete_api(api_id):
    api = API.get_or_none(API.ID == api_id)

    if api and api.user == current_user.id:
        api.delete_instance()
        flash("API deleted successfully!", "success")
    else:
        flash("API not found or you don't have permission to delete it", "error")

    return redirect(url_for('main.index'))

@main.route('/api/<int:api_id>/request', methods=['POST'])
@login_required
def api_request(api_id):
    api = API.get_or_none(API.ID == api_id)
    
    if not api or api.user != current_user.id:
        flash("API not found or you don't have permission to access it", "error")
        return redirect(url_for('main.index'))
    
    form = APIRequestForm()

    if form.validate_on_submit():
        method = form.request_method.data
        payload = form.request_payload.data

        response = None
        try:
            headers = {'Content-Type': 'application/json'}
            if method == 'GET':
                response = requests.get(api.endpoint, headers=headers)
            elif method == 'POST':
                response = requests.post(api.endpoint, headers=headers, data=payload)
            elif method == 'PUT':
                response = requests.put(api.endpoint, headers=headers, data=payload)
            elif method == 'DELETE':
                response = requests.delete(api.endpoint, headers=headers)
        except Exception as e:
            flash(f"Error sending request: {e}", "error")

    return render_template('api_detail.html', api=api, response=response, form=form)

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.get_or_none(User.username == form.username.data)
        
        if user and user.check_password(form.password.data):
            login_user(user)
            flash("Logged in successfully!", "success")
            return redirect(url_for('main.index'))
        else:
            flash("Invalid username or password", "error")
    
    return render_template('login.html', form=form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logged out successfully!", "success")
    return redirect(url_for('main.login'))
