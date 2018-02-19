# coding:utf-8
from flask import Flask, render_template, request, redirect, url_for, session
import config
from models import User, Question
from exts import db
from decorators import login_required

app = Flask(__name__)
app.config.from_object(config)

db.init_app(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        telephone = request.form.get('telephone')
        password = request.form.get('password')
        user = User.query.filter(User.telephone == telephone, User.password == password).first()
        if user:
            session['user_id'] = user.id
            # 如果你想在31天内都不需要登录
            session.permanent = True
            return redirect(url_for('index'))
        else:
            return u"手机号码或者密码错误请登录"


@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        telephone = request.form.get('telephone')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # 手机号码验证，如果被注册了，就不能再注册了
        user = User.query.filter(User.telephone == telephone).first()
        if user:
            return u"改用户号码已经注册，请更换手机号码！"
        else:
            # password1要和password2 相等才可以
            if password1 != password2:
                return u"两次密码不相等，请核对后在填写！"
            else:
                user = User(telephone=telephone, username=username, password=password1)
                db.session.add(user)
                db.session.commit()
                # 如果注册成功就跳转到登录页面
                return redirect(url_for('login'))


@app.route("/question/",methods=['GET','POST'])
@login_required
def question():
    if request.method == 'GET':
        return render_template('question.html')
    else:
        title = request.form.get('title')
        content = request.form.get('content')
        question = Question(title=title, content=content)
        user_id = session.get('user_id')
        user = User.query.filter(User.id == user_id).first()
        question.author = user
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
