from app import app,db
from flask import render_template, url_for, redirect, flash, request
from app.forms import LoginForm, RegistrationForm, QuestionForm, AnswerForm
from app.models import User, Question, Answers, Tag, QuestionTag
from flask_login import current_user,login_user,logout_user,login_required
from werkzeug.urls import url_parse

@app.route('/')
@app.route('/index')
def index():
    question = Question.query.order_by(Question.timestamp.desc())
    # q = Question.query.filter_by()
    # tags = q.question_to_tags.all()
    return render_template('index.html', question = question, Tag = Tag)


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
        db.session.add(question)
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

                    tag_question_entry = QuestionTag(tag_id = Tag.query.filter_by(tags = cursor).first().id,
                                                     question_id = question.id)
                    db.session.add(tag_question_entry)
            else:
                tag_question_entry = QuestionTag(tag_id = Tag.query.filter_by(tags = cursor).first().id, 
                                        question_id = question.id)
                db.session.add(tag_question_entry)
        
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


# @app.route('/tags/<tag_id>')
# def tag(tag_id):
#     print(QuestionTag.query.filter_by(tag_id = tag_id).question_id.all())
#     return "papa"

@app.route('/edit_questions/<id>', methods = ['GET','POST'])
def edit_questions(id):
    temp = Question.query.get(id)
    form = QuestionForm(obj = temp)    
    for tag in temp.question_to_tags.all():
        print(Tag.query.get(tag.tag_id).tags)
    if form.validate_on_submit():
        temp.question = form.question.data
        temp.title = form.title.data
        db.session.commit()
        return redirect(url_for('questions', question_id = temp))
    return render_template('question_form.html', form = form)
