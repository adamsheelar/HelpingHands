from select import select
from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy import desc
from .models import Note
from .models import User
from . import db
import json


views = Blueprint('views', __name__)

@views.route('/about/')
def about():
    return render_template('about.html', user=current_user)

@views.route('/privacypolicy/')
def privacypolicy():
    return render_template('privacypolicy.html', user=current_user)

@views.route('/contact/')
def contact():
    return render_template('contact.html', user=current_user)

@views.route('/termsofuse/')
def termsofuse():
    return render_template('termsofuse.html', user=current_user)

@views.route('/', methods=['GET'])
def welcome():
    return render_template('index.html')
@views.route('/profile/<username>')
def interact(username):
    return render_template('userinfo.html', user=User.query.filter_by(username=username).first())

@views.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')
        ntitle = request.form.get('note_title')
        search = request.form.get('search')
        if search is not None:
            if len(search) > 0:
                current_user.search_post = search
                db.session.commit()
                return redirect(url_for('views.results')) 
        if len(note) < 1:
            print()
        else:
            new_note = Note(data=note, title=ntitle, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()

    return render_template("home.html", user=current_user)

@views.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        status = request.form.getlist('customSwitch1')
        note = request.form.get('note')
        nTitle = request.form.get('note_title')
        search = request.form.get('search')
        if search is not None:
            if len(search) > 0:
                current_user.search_post = search
                db.session.commit()
                return redirect(url_for('views.results')) 
        if len(note) < 1:
            print()
        else:
            new_note = Note(data=note, title=nTitle, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()

    return render_template("profile.html", user=current_user)

@views.route('/delete-post', methods=['POST'])
def delete_post():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return redirect(url_for('views.home'))

@views.route('/results', methods=['GET'])
def results():
    search_results_title = Note.query.filter(Note.title.contains(current_user.search_post)).all()
    search_results_text = Note.query.filter(Note.data.contains(current_user.search_post)).all()
    search_results = search_results_title + search_results_text
    return render_template('results.html', user=current_user, search_results=search_results)
