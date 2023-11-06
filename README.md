# lab2_BE
Для встановлення проекту використовуйте наступні кроки:

1. Клонуйте репозиторій:

   ```bash
   git clone https://github.com/Blindcoke/lab2_BE
   
2. Перейдіть до папки проекту:
    ```bash
   cd yourproject
3. Створіть та активуйте віртуальне середовище
    ```bash
   python3 -m venv env
   source ./env/bin/activate
   source ./env/Scripts/activate
4. Встановіть Flask
    ```bash
   pip install flask
5. Запишіть всі залежності проекту в файл requirements.txt:
    ```bash
   pip freeze > requirements.txt

6. Додайте код у app.py
   
7. Тепер ви можете запустити застосунок командою:
    ```bash
   flask run --host 0.0.0.0 -p 10000
8. Відкрийте веб-браузер і перейдіть за адресою http://localhost:10000 для перевірки застосунку локально.


# lab3_BE
Номер у списку групи:9
Група ІО-16
9/3=0
Варіант 0 - Облік доходів

Для встановлення проекту використовуйте наступні кроки:

1. Клонуйте репозиторій:

   ```bash
   git clone https://github.com/Blindcoke/lab2_3_BE
   
2. Перейдіть до папки проекту:
    ```bash
   cd yourproject
3. Створіть та активуйте віртуальне середовище
    ```bash
   python3 -m venv env
   source ./env/bin/activate
   source ./env/Scripts/activate

4. -Для локального запуску додайте конфігурацію для контейнера бази даних в файл docker-compose.yaml
   
   -Після цього перевірте що контейнер запускається командою docker-compose up db.
   -Тепер встановіть бібліотеки: Flask-Migrate - для роботи з міграціями, flask-sqlalchemy - ORM, та psycopg2-binary - для роботи з самою базою даних.
   pip install psycopg2-binary flask-sqlalchemy Flask-Migrate
   ```bash
   -Додати залежності
   pip install flask-smorest
   ```bash

5. Оновити requirements.txt:
    ```bash
   pip freeze > requirements.txt

6. -Додайте код у app.py
   -Додати config.py

7. Тепер ви можете запустити застосунок командою:
    ```bash
   flask run --host 0.0.0.0 -p 10000
8. Відкрийте веб-браузер і перейдіть за адресою http://localhost:10000 для перевірки застосунку локально.
