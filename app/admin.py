from flask import render_template, request, redirect, url_for, session, flash
from app import app, db
from app.models import Question, Option, User
from functools import wraps
from passlib.hash import sha256_crypt
from pathlib import Path

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session['isAdminLoggedIn']:
            return f(*args, **kwargs)
        else:
            flash("Bu Sayfayı Görüntülemek İçin Lütfen Giriş Yapın",
                  category="danger")
            return redirect(url_for("admin_login"))
    return decorated_function

def add_admin():
    with app.app_context():
        try:
            users = User.query.all()
            if len(users) == 0:
                admin_user = User(username = 'admin', password = sha256_crypt.encrypt("123456789"), user_type = "admin")
                db.session.add(admin_user)
                db.session.commit() 
        except:
            db.create_all()

            questions = Question.query.all()
            if len(questions) == 0:
                current_path = Path.cwd()
                with open(current_path / "default" / "questions.txt", 'r', encoding='utf-8') as file:
                    lines = file.readlines()
                    for line in lines:
                        question, answers = line.split('~')[0], line.split('~')[1]
                        answers = answers.split('-')
                        questionDB = Question(question_text = question.strip())
                        db.session.add(questionDB)
                        db.session.commit()
                        for answer in answers:
                            answerDB = Option(option_text = answer.replace('(True)','').strip(), is_correct = True if answer.find('(True)') >= 0 else False, question_id = questionDB.id)
                            db.session.add(answerDB)
                            db.session.commit()  

            users = User.query.all()
            if len(users) == 0:
                admin_user = User(username = 'admin', password = sha256_crypt.encrypt("123456789"), user_type = "admin")
                db.session.add(admin_user)
                db.session.commit()      

    

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username, user_type='admin').first()
        try:
            if user and sha256_crypt.verify(password, user.password):
                session['isAdminLoggedIn'] = True
                return redirect(url_for('admin'))
            else:
                flash('Kullanıcı Adı Veya Şifre Yanlış!', 'danger')
                return redirect(url_for('admin_login'))
        except:
            flash('Kullanıcı Adı Veya Şifre Yanlış! EXCEPT', 'danger')
            return redirect(url_for('admin_login'))
        
    return render_template('admin_login.html')

@app.route('/admin')
@login_required
def admin():
    session['isAdminLoggedIn'] = True
    flash("Admin Girişi Başarıyla Yapıldı",category="success")
    questions = Question.query.all()
    return render_template('admin.html', questions=questions)


@app.route('/logout')
@login_required
def logout():
    session['isAdminLoggedIn'] = False
    flash("Başarıyla Çıkış Yapıldı",category="success")
    return redirect(url_for('index'))

@app.route('/add_question', methods=['GET', 'POST'])
@login_required
def add_question():
    if request.method == 'POST':
        question_text = request.form['question_text']

        options = []
        i = 1
        while f'option_{i}' in request.form:
            option_text = request.form[f'option_{i}']
            options.append({
                'text' : option_text,
                'is_correct' : (request.form.get('answer') == str(i))
            })
            i += 1

        new_question = Question(question_text=question_text)
        db.session.add(new_question)
        db.session.commit()

        for count in options:
            new_option = Option(option_text=count['text'], is_correct=count['is_correct'], question_id = new_question.id)
            db.session.add(new_option)
            db.session.commit()

        flash('Soru Başarıyla Eklendi!', 'success')
        return redirect(url_for('admin'))

    return redirect(url_for('admin'))

@app.route('/update_question/<int:question_id>', methods=['GET', 'POST'])
@login_required
def update_question(question_id):
    question = Question.query.get_or_404(question_id)
    
    if request.method == 'POST':
        for option in question.options:        
            option.option_text = request.form[f'option_{option.id}']
            option.is_correct = request.form['answer'] == str(option.id)
        
        db.session.commit()
        flash('Soru başarıyla güncellendi!', 'success')
        return redirect(url_for('admin'))
    
    return render_template('update_question.html', question=question)

@app.route('/delete_question/<int:question_id>', methods=['POST'])
@login_required
def delete_question(question_id):
    if request.method == "POST":

        question = Question.query.get_or_404(question_id)

        for option in question.options:
            db.session.delete(option)
    
        db.session.delete(question)
        db.session.commit()
    
        flash('Soru başarıyla silindi!', 'success')

        return redirect(url_for('admin'))