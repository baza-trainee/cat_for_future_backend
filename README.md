# cat_for_future_backend

## Початок роботи

### 1. Передумови

    Python 3.10
    Django 4.1

### 2. Іністаліця
1. Склонуйте репозиторій:

   ```bash
   git clone https://github.com/baza-trainee/cat_for_future_backend.git
   cd cat_for_future_backen
   
2. Створіть віртуальне оточення(опціонально, але рекомендовано):
    
    ```bash
    python -m venv venv
    source venv/bin/activate

3. Встановіть залежності проекту:
    
    ```bash
   pip install -r requirements.txt
   
4. Мігруйте базу даних та створіть суперюзера:

    ```bash
    python manage.py migrate
    python manage.py createsuperuser

5. Запустіть сервер для розробки:
    ```bash
   python manage.py runserver
