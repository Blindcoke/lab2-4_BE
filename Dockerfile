# Використовуйте офіційний образ Python з потрібною версією
FROM python:3.11.3-slim-bullseye

# Встановлюємо робочу директорію в /app
WORKDIR .

# Копіюємо файл requirements.txt в контейнер
COPY requirements.txt .

# Встановлюємо Python-залежності за допомогою pip
RUN python -m pip install -r requirements.txt

# Копіюємо весь вміст поточної директорії в контейнер
COPY . /app


ENV FLASK_APP=app.py

CMD flask run -h 0.0.0.0 -p 5000