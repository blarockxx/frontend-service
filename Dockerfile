FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

# 设置环境变量
ENV FLASK_APP=app.py
ENV FLASK_ENV=development

EXPOSE 5000

# 运行测试
RUN python -m unittest discover -s tests || { echo 'Tests failed' ; exit 1; }

CMD ["python", "app.py"]
