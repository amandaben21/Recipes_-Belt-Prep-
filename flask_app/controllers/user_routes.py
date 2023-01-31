from flask import Flask, render_template, redirect, request, session
from flask_app.models import user_model
from flask_app import app

@app.route('/')
def log_reg():
    return render_template('log_reg.html')

@app.route('/register', methods=["POST"])
def save_user():
    if not user_model.User.validate_register(request.form):
        return redirect('/')
    session['user_id']=user_model.User.save_user(request.form) #if they pass validation
    return redirect('/dashboard')

@app.route('/login', methods=["POST"])
def login_user():
    if not user_model.User.validate_login(request.form):
        return redirect('/')
    user_email = {
        "email":request.form['email']
    }
    one_user = user_model.User.get_email(user_email)
    if not one_user:
        return redirect('/')
    session['user_id'] = one_user.id
    return redirect('/dashboard')



@app.route('/logout')
def logout(): 
    session.clear()
    return redirect('/')
