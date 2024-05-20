from flask import Flask, render_template, request, redirect, url_for, flash, session
import requests
import logging
from config import Config

app = Flask(__name__)
# 优化代码-------
# app.secret_key = 'your_secret_key'
# USER_SERVICE_URL = 'http://user-service:5001'
app.config.from_object(Config)
USER_SERVICE_URL = app.config['USER_SERVICE_URL']
PAYMENT_SERVICE_URL = app.config['PAYMENT_SERVICE_URL']
# --------------

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

@app.route('/go_to_payment/<int:user_id>')
def go_to_payment(user_id):
    # 假设从用户ID获取金额等信息，这里你需要根据你的业务逻辑修改
    amount = 100.0  # 假设支付金额为100元
    status = 'pending'  # 假设支付状态为待处理
    # 发送创建支付记录的请求
    try:
        response = requests.post(f'{PAYMENT_SERVICE_URL}/payments', json={'user_id': user_id, 'amount': amount, 'status': status})
        response.raise_for_status()
        if response.status_code == 201:
            flash('支付成功！')
            print('支付成功')
        else:
            flash(response.json()['message'])
            print('支付失败')
    except Exception as e:
        logger.error(f"Error making payment: {e}")
        flash('支付失败，请稍后再试。')

    return redirect(url_for('dashboard'))


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('已注销。')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

