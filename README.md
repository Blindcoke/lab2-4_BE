# lab2_BE
## Інсталяція

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
