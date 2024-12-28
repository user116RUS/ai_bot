import os

from docx import Document

from django.conf import settings


def split_message(message, chunk_size=4096):
    chunks = []
    while message:
        chunk = message[:chunk_size]
        chunks.append(chunk)
        message = message[chunk_size:]
    return chunks


def save_message_to_file(message, extension):
    if extension == "txt":
        filename = f"message_{len(os.listdir(settings.BASE_DIR / 'temp' / 'files'))+1}.{extension}"

        with open(settings.BASE_DIR / 'temp' / 'files' / filename, 'w', encoding='utf-8') as file:
            file.write(message)
    elif extension == "docx":
        doc = Document()
        doc.add_paragraph(message)
        filename = f"message_{len(os.listdir(settings.BASE_DIR / 'temp' / 'files'))+1}.{extension}"
        doc.save(settings.BASE_DIR / 'temp' / 'files' / filename)
    
    # Возвращаем полный путь к файлу
    return str(settings.BASE_DIR / 'temp' / 'files' / filename)
