from app import app,db
from flask import render_template, url_for, redirect, flash, request
from app.forms import LoginForm, RegistrationForm, QuestionForm, AnswerForm
from app.models import User, Question, Answers, Tag
from flask_login import current_user,login_user,logout_user,login_required
from werkzeug.urls import url_parse

@app.route('/')
@app.route('/index')
def index():
    question = Question.query.order_by(Question.timestamp.desc())
    tags = Tag.query.all()
    return render_template('index.html', question = question, tags = tags)


@app.route('/login', methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember = form.remember_me.data)
        # return redirect(url_for('index'))
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title = 'Login', form = form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods = [ 'GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(name = form.name.data, email = form.email.data, 
        location = form.location.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You are successfully registered')
        return redirect(url_for('login'))
    return render_template('register.html', title = 'Register', form = form)


@app.route('/questions', methods = ['GET','POST'])
# @login_required
def questions():
    form = QuestionForm()
    if form.validate_on_submit():
        question = Question(title = form.title.data, question = form.question.data)
        lets_split = form.tags.data
        splitted_list = lets_split.split(',')
        check = Tag.query.all()
        for cursor in splitted_list:
            count = 0 
            for che in check:
                if cursor == che.tags:
                    count += 1
            if count == 0:
                    tag = Tag(tags = cursor)
                    db.session.add(tag)
        db.session.add(question)
        db.session.commit()
        flash('Let the knowledgable answer')
        question = Question.query.order_by(Question.timestamp.desc()).first()
        return redirect(url_for('question',question_id = question.id))
    return render_template('question_form.html', form = form)


@app.route('/questions/<question_id>', methods = ['GET', 'POST'])
@login_required
def question(question_id):
    question = Question.query.get(question_id)
    form = AnswerForm()
    if form.validate_on_submit():
        answer = Answers(answer = form.answer.data, which_question = question)
        db.session.add(answer)
        db.session.commit()
        flash('Thoughts Posted')
        return redirect(url_for('question', question_id=question.id))
    answer = question.answers.all()
    return render_template('question.html', question = question, form = form, answer = answer)