# ai_bot
Bot for ai chat

Telegram bot with ai chat

1. clone repo git@github.com:user116RUS/telegram_ai.git
2. create and activate venv
3. create .env file with 
```python3
BOT_TOKEN=
OPENAI_API_KEY=
VSEGPT_API_KEY=
SECRET_KEY=
OWNER_ID=
HOOK=
```
5. install requirements 'pip install -r requirements.txt'
5. ngrok http 8000 link to HOOK in .env
6. python manage.py makemigrations
7. python manage.py migrate
8. python manage.py createsuperuser
9. python manage.py runserver
9. 127.0.0.1:8000/bot/  - setting webhook
10. ADMIN 127.0.0.1:8000/admin/
