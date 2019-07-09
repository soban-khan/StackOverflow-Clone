from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from datetime import datetime


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(30), index = True)
    email = db.Column(db.String(150), unique = True)
    location = db.Column(db.String(50))
    password_hash = db.Column(db.String(150))

    def __repr__(self):
        return '<User:{}>'.format(self.name)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash, password)


class Question(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(50), index = True)
    question = db.Column(db.String(250), index = True)
    timestamp = db.Column(db.DateTime, default = datetime.utcnow)
    answers = db.relationship('Answers', backref = 'which_question', lazy = 'dynamic')
    question_to_tags = db.relationship('QuestionTag', backref = 'which_tag', lazy = 'dynamic')

    def __repr__(self):
       return '<Question:{}>'.format(self.question)


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    tags = db.Column(db.String(20), unique = True, default='')
    tags_to_question = db.relationship('QuestionTag', backref = 'which_question_tag',
                     lazy = 'dynamic')

    def __repr__(self):
       return '{}'.format(self.tags)


class QuestionTag(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))


class Answers(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    answer = db.Column(db.String(500))
    timestamp = db.Column(db.DateTime, default = datetime.utcnow)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))

    def __repr__(self):
       return '{}'.format(self.answer)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
    return Question.query.get(int(id))
    return Tag.query.get(int(id))