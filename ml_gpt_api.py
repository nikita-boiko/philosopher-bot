# Модуль для работы с OpenAPI

import openai 
from config import OPENAI_API_KEY, PHILOSOPHER_PROMPT

# устанавливаем API ключ
openai.api_key = OPENAI_API_KEY

# функция принемает сообщение и возвращает ответ
def get_philosophical_response(user_message):
    # обработка запроса, форматирование
    try: 
        prompt = PHILOSOPHER_PROMPT.format(user_message=user_message)
        # создаем запрос к OpenAI
        response = openai.ChatCompletion.create(
            model='gpt-5-nano',
            messages=[
                {'role':'system', 'content':'Ты - мудрый философ, который дает глубокие, вдумчивые ответы.'},
                {'role':'system', 'content': user_message}
            ],
            max_tokens=150,
            temperature=0.8
        ) 
        # возврат результата
        return response.choices[0].message.content.strip()
    # обработка ошибок
    except Exception as e:
        return f'Задумался над твоим вопросом... но мысль ушла в странствие. Ошибка {str(e)}'


