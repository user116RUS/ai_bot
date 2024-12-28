# ai_bot
Bot for ai chat

Telegram bot with ai chat

1. clone repo git@github.com:user116RUS/telegram_ai.git
2. create and activate venv
3. create .env file with 
```python3
BOT_NAME=
BOT_TOKEN=
OPENAI_API_KEY=
VSEGPT_API_KEY=
SECRET_KEY=
OWNER_ID=
HOOK=
PAYMENT_TOKEN=
WHISPER_MODEL=
GETIMG_AI_KEY=
FUSION_API_KEY=
FUSION_SECRET_KEY=
```
4. install requirements 'pip install -r requirements.txt'
5. install ffmpeg:
    using this guide on Windows: https://phoenixnap.com/kb/ffmpeg-windows or
  *choco install ffmpeg* if you use Chocolatey or
  *scoop install ffmpeg* if you use Scoop.
    *sudo apt update && sudo apt install ffmpeg* if you use Ubuntu/Debian or based on them or
  *sudo pacman -S ffmpeg* if you use Arch linux.
    *brew install ffmpeg* if you use MacOS
7. ngrok http 8000 link to HOOK in .env
8. python manage.py makemigrations
9. python manage.py migrate
10. python manage.py createsuperuser
11. python manage.py runserver
12. 127.0.0.1:8000/bot/  - setting webhook
13. ADMIN 127.0.0.1:8000/admin/
