from ollama import chat

prompt =('Ты раздражённый преподаватель по имени Боев. '
         'Отвечай кратко, максимум 50 символов, быстро. '
         'Добавляй много смайликов 😂,😡,🤬')
def ai_responce(message_text):
    response = chat(
        model='gemma3:270m',  # маленькая модель → ultra fast
        messages=[
            {
                'role': 'system',
                'content': (
                    prompt
                )
            },
            {
                'role': 'user',
                'content': message_text
            }
        ]
    )
    return(response.message.content)
