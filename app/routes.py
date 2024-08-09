from flask import render_template, request, redirect, url_for, session, flash
from app import app, db
from app.models import Question, Score, User, Option
from pathlib import Path


@app.route('/')
def index():
    questions = Question.query.all() 
    return render_template('exam.html', questions=questions)


@app.route('/submit', methods=['POST'])
def submit():
    score = 0
    questions = Question.query.all()
    for question in questions:
        answer = request.form[f'question_{question.id}']
        for option in question.options:
            if option.is_correct and option.option_text == answer:
                score += 1
    
    username = request.form['username']
    session['username'] = username
    new_score = Score(username=username, score=score)
    db.session.add(new_score)
    db.session.commit()

    user_high_score = Score.query.filter_by(username=username).order_by(Score.score.desc()).first()
    high_score = user_high_score.score if user_high_score else score
    
    return render_template('result.html', score=score, high_score=high_score)