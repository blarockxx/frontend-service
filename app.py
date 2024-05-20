from flask import Flask, render_template, request, redirect, url_for, flash, session
import requests
import logging

app = Flask(__name__)
app.secret_key = 'your_secret_key'

USER_SERVICE_URL = 'http://user-service:5001'

# 设置日志记录器
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        response = requests.post(f'{USER_SERVICE_URL}/login', json={'username': username, 'password': password})
        if response.status_code == 200:
            session['user_id'] = response.json()['user_id']
            flash(response.json())
            flash('登录成功！')
            return redirect(url_for('dashboard'))
        else:
            flash(response.json()['message'])
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        response = requests.post(f'{USER_SERVICE_URL}/register', json={'username': username, 'password': password})
        if response.status_code == 201:
            flash('注册成功！')
            return redirect(url_for('login'))
        else:
            flash(response.json()['message'])
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    try:
        response = requests.get(f'{USER_SERVICE_URL}/users')
        response.raise_for_status()  # 如果响应状态码不是 2xx，则抛出异常
        users = response.json()
    except Exception as e:
        logger.error(f"Error fetching user data: {e}")
        flash('无法获取用户数据，请稍后再试。')
        users = []  # 如果发生异常，将 users 设置为空列表
    return render_template('dashboard.html', users=users)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('已注销。')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

