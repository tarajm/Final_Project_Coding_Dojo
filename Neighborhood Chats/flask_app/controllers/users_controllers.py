from flask import render_template, session, redirect, request, flash
from flask_app import app
from flask_app.models.user_model import User
from flask_app.models.chat_model import Chat
from flask_bcrypt import Bcrypt
import requests
import config as config
bcrypt = Bcrypt(app)

@app.route('/')
def reg_log():
    return render_template('register_login.html')

@app.route('/register', methods = ["POST"])
def register():
    if not User.is_valid_reg(request.form):
        return redirect('/')
    data={
        "fname": request.form['fname'],
        "lname": request.form['lname'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    users_id = User.create(data)
    session['users_id'] =  users_id
    return redirect('/dashboard')

@app.route('/login', methods = ["POST"])
def login():
    user = User.get_by_email(request.form)
    if not user:
        flash("Invalid email/password!", "login")
        return redirect("/")
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Email/Password!", "login")
        return redirect("/")
    session['users_id'] = user.id
    return redirect('/dashboard')

@app.route("/dashboard")
def dashboard():
    if 'users_id' not in session:
        return redirect('/logout')
    data = {
        "id": session['users_id']
    }
    user_in_session = User.get_by_id(data)
    session['fname'] = user_in_session.fname
    session['lname'] = user_in_session.lname

    one_chat = Chat.get_all_chats_with_users()
    return render_template("dashboard.html", user = User.get_by_id(data), one_chat = one_chat)

@app.route('/user_page/<int:users_id>')
def user_page(users_id):
    if 'users_id' not in session:
        return redirect('/')
    else: 
        data = {
            'id' : users_id,
            'users_id' : session['users_id']
        }
    chat = Chat.get_chats_w_user(data)
    return render_template('user_page.html', user = User.get_by_id(data), chat = chat)

@app.route('/run_weather', methods = ['POST'])
def run_weather():
    data={
        "zipcode": request.form['zipcode']
    }
    if not User.is_valid_zip(data):
        return redirect('/dashboard')
    weather_key = config.weather_api_key
    the_call = requests.get(f"https://api.openweathermap.org/data/2.5/weather?zip={request.form['zipcode']}&appid={weather_key}&units=imperial").json()
    # print('the_call', the_call
    # for key,value in the_call.items():
    #     print(key, "\t\t", value)
    session['city'] = the_call['name']
    session['humidity'] = the_call['main']['humidity']
    session['wind'] = the_call['wind']['speed']
    session['temp'] = the_call['main']['temp']
    session['description'] = the_call['weather'][0]['description']
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')