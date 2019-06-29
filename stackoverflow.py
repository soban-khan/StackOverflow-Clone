from app import app,db
from app.models import User,Question,Answers,Tag

@app.shell_context_processor
def make_shell_context():
    return{'db':db, 'User':User, 'Question':Question, 'Answers':Answers, 'Tag':Tag}