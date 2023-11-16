# lab4_BE
Для встановлення проекту використовуйте наступні кроки:

1. Клонуйте репозиторій:

   ```bash
   git clone https://github.com/Blindcoke/lab2-4_BE
   
2. Перейдіть до папки проекту:
    ```bash
   cd yourproject
3. Створіть та активуйте віртуальне середовище
    ```bash
   python3 -m venv env
   source ./env/bin/activate
   source ./env/Scripts/activate
4. Встановити порібні бібліотеки

   ```bash
   pip install passlib
   pip install flask-jwt-extended
   pip freeze > requirements.txt
5. Згенерувати секретний ключ для JWT в консолі python 
   ```bash
   import secrets
   secrets.SystemRandom().getrandbits(128)
6. присвоїти його змінній середовища JWT_SECRET_KEY 
   ```bash
   export JWT_SECRET_KEY="your secret key from previous step"

   
7. Тепер ви можете запустити застосунок командою:
    ```bash
   flask run --host 0.0.0.0 -p 8082
8. Відкрийте веб-браузер і перейдіть за адресою http://localhost:8082 для перевірки застосунку локально.


