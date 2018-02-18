#coding:utf-8
from flask import Flask,render_template,request,redirect,url_for
import config
from models import User
from exts import db


app = Flask(__name__)
app.config.from_object(config)

db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login/',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        pass

@app.route('/register/',methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        telephone = request.form.get('telephone')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        #手机号码验证，如果被注册了，就不能再注册了
        user =User.query.filter(User.telephone == telephone).first()
        if user:
            return u"改用户号码已经注册，请更换手机号码！"
        else:
            #password1要和password2 相等才可以
            if password1 !=password2:
                return u"两次密码不相等，请核对后在填写！"
            else:
                user =User(telephone=telephone,username=username,password=password1)
                db.session.add(user)
                db.session.commit()
                #如果注册成功就跳转到登录页面
                return redirect(url_for('login'))

if __name__ == '__main__':
    app.run()
