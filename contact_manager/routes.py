from contact_manager import app, db
from flask import render_template, url_for, redirect, request, flash
import hashlib
from contact_manager.forms import UserRegistrationForm, UserLoginForm, ContactCreationForm, UpdateContactForm
from contact_manager.models import User, Contact
from flask_login import login_user, logout_user, login_required, current_user


def hash_string(string):
    return hashlib.sha512(string.encode('utf-8')).hexdigest()

@app.route('/')
@app.route('/home')
@login_required
def home():
    contacts = current_user.contacts
    return render_template('home.html', contacts=contacts)

@app.route('/about')
@login_required
def about():
    return render_template('about.html', title='About')

@app.route('/register/user', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = UserRegistrationForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User(username=form.username.data, email=form.email.data, password=hash_string(form.password.data))
            db.session.add(user)
            db.session.commit()
            flash('Your Account has been created, you can now login!', 'success')
            return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login/user', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = UserLoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and user.password == hash_string(form.password.data):
                login_user(user, remember=form.remember_me.data)
                next_route = request.args.get('next')
                flash('You have been successfully logged in', 'success')
                return redirect(next_route) if next_route else redirect(url_for('home'))
            else:
                flash('Invalid credentials, please check your email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout/user')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/create/contact', methods=['GET', 'POST'])
@login_required
def create_contact():
    form = ContactCreationForm()
    if form.validate_on_submit():
        contact = Contact(name=form.name.data, email=form.email.data, phone=form.phone.data, user_id=current_user.id)
        db.session.add(contact)
        db.session.commit()
        flash('New Contact added to your list!', 'success')
        return redirect(url_for('home'))
    return render_template('create_contact.html', title='Create Contact', form=form)

@app.route('/update/contact/<int:contact_id>', methods=['GET', 'POST'])
def update_contact(contact_id):
    contact = Contact.query.get(contact_id)
    form = UpdateContactForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            contact.name = form.name.data
            contact.email = form.email.data
            contact.phone = form.phone.data
            db.session.commit()
            flash('Contact successfully updated', 'success')
            return redirect(url_for('home'))
    elif request.method == 'GET':
        form.name.data = contact.name
        form.email.data = contact.email
        form.phone.data = contact.phone
    return render_template('update_contact.html', title='Update Contact', contact=contact, form=form)

@app.route('/delete/contact/<int:contact_id>')
def delete_contact(contact_id):
    i = 0
    contacts = current_user.contacts
    for contact in contacts:
        if contact.id == contact_id:
            db.session.delete(contacts[i])
            db.session.commit()
            return redirect(url_for('home'))
        i += 1
