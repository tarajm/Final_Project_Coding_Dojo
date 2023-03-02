from flask import render_template, session, redirect, request, flash
from flask_app import app
from flask_app.models.chat_model import Chat
from flask_app.models.user_model import User
import json
import requests
import config as config
# from geopy import geocoders, Nominatim


@app.route('/create_chat')
def create_chat():
    return render_template('create_chat.html')

@app.route('/create', methods=['POST'])
def create():
    if 'users_id' not in session:
        return redirect('/')
    data = {
        'name': request.form['name'],
        'description': request.form['description'],
        'location': request.form['location'],
        'date': request.form['date'],
        'users_id': session['users_id']
    }
    if not Chat.validate_chat(data):
        return redirect('/create_chat')
    Chat.add_chat(data)
    return redirect('/dashboard')

@app.route('/show/<int:chats_id>')
def show(chats_id):
    if 'users_id' not in session:
        return redirect('/')
    else: 
        data = {
            'users_id' : session['users_id'],
            'id' : chats_id,
    }
    chat = Chat.get_one(data)
    chat_in_session = Chat.get_by_id(data)
    session['location'] = chat_in_session.location
    session['api_key'] = config.FLASK_APP_API_KEY
    return render_template('show.html', chat = chat)

@app.route('/edit/<int:chat_id>')
def edit_chat(chat_id):
    if 'users_id' not in session:
        return redirect('/')
    else: 
        data = {
        'id' : chat_id,
        'users_id' : session['users_id']
    }
    one_chat = Chat.get_one(data)
    return render_template('edit_chat.html', one_chat = one_chat)

@app.route('/update/<int:chats_id>', methods = ['POST'])
def update_chat(chats_id):
    if 'users_id' not in session:
            return redirect('/')
    data = {
        'id': chats_id,
        'name': request.form['name'],
        'description': request.form['description'],
        'location': request.form['location'],
        'date': request.form['date'],
        'users_id': session['users_id']
    }
    if not Chat.validate_chat(request.form):
        return redirect(f'/edit/{chats_id}')
    Chat.update_chat(data)
    return redirect('/dashboard')


@app.route('/delete/<int:chat_id>')
def delete(chat_id):
    if 'users_id' not in session:
        return redirect('/')
    data = {
        'id' : chat_id
    }
    Chat.delete_chat(data)
    return redirect('/dashboard')

