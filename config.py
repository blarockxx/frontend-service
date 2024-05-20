import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    USER_SERVICE_URL = os.getenv('USER_SERVICE_URL', 'http://user-service:5001')
    PAYMENT_SERVICE_URL = os.getenv('PAYMENT_SERVICE_URL', 'http://payment-service:5003')