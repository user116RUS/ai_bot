import os

from django.conf import settings

def split_message(message, chunk_size=4096):
    chunks = []
    while message:
        chunk = message[:chunk_size]
        chunks.append(chunk)
        message = message[chunk_size:]
    return chunks


def save_message_to_file(message, extension):
    # Создаем уникальное имя файла
    filename = f"message_{len(os.listdir(settings.BASE_DIR / 'temp' / 'files'))+1}.{extension}"
    
    # Сохраняем сообщение в файл
    with open(settings.BASE_DIR / 'temp' / 'files' / filename, 'w', encoding='utf-8') as file:
        file.write(message)
    
    # Возвращаем полный путь к файлу
    return str(settings.BASE_DIR / 'temp' / 'files' / filename)
