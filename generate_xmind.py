import os
import json
import openai
import xmind
from dotenv import load_dotenv

# Загрузить API ключ из .env файла
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

# Функция для получения ответа от OpenAI в формате JSON
def get_openai_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    response_text = response['choices'][0]['message']['content'].strip()
    try:
        response_json = json.loads(response_text)
    except json.JSONDecodeError as e:
        print(f"Ошибка при парсинге JSON: {e}. Ответ: {response_text}")
        response_json = None
    return response_json

# Функция для рекурсивного создания структуры XMind
def create_xmind_structure(data, parent_topic):
    for item in data.get('subtopics', []):
        topic = parent_topic.addSubTopic()
        topic.setTitle(item['title'])
        create_xmind_structure(item, topic)

# Основная функция для генерации XMind карты
def generate_xmind_map(data, file_name):
    workbook = xmind.load(file_name)
    sheet = workbook.createSheet()
    sheet.setTitle(data['title'])
    root_topic = sheet.getRootTopic()
    root_topic.setTitle(data['title'])

    create_xmind_structure(data, root_topic)
    xmind.save(workbook, file_name)

def main():
    user_input = input("Введите ваш запрос: ")
    prompt = f"""
    Создайте иерархию в формате JSON для интеллект-карты по запросу: {user_input}.
    Пожалуйста, включите как можно больше уровней иерархии. Каждый раздел должен иметь несколько подразделов, и каждый подраздел должен также содержать свои собственные подразделы, и так далее, до максимально возможной глубины.

    Каждая тема должна содержать от 2 до 5 подтем, если это возможно.
    Подтемы также должны следовать этому правилу для создания своих собственных подуровней.

    Пример JSON структуры:

    {{
        "title": "Основная тема",
        "subtopics": [
            {{
                "title": "Подтема 1",
                "subtopics": [
                    {{
                        "title": "Подтема 1.1",
                        "subtopics": [
                            {{
                                "title": "Подтема 1.1.1",
                                "subtopics": [
                                    {{
                                        "title": "Подтема 1.1.1.1",
                                        "subtopics": [
                                            {{
                                                "title": "Подтема 1.1.1.1.1",
                                                "subtopics": [
                                                    {{
                                                        "title": "Подтема 1.1.1.1.1.1",
                                                        "subtopics": [
                                                            {{
                                                                "title": "Подтема 1.1.1.1.1.1.1",
                                                                "subtopics": []
                                                            }},
                                                            {{
                                                                "title": "Подтема 1.1.1.1.1.1.2",
                                                                "subtopics": []
                                                            }}
                                                        ]
                                                    }},
                                                    {{
                                                        "title": "Подтема 1.1.1.1.1.2",
                                                        "subtopics": []
                                                    }}
                                                ]
                                            }},
                                            {{
                                                "title": "Подтема 1.1.1.1.2",
                                                "subtopics": []
                                            }}
                                        ]
                                    }},
                                    {{
                                        "title": "Подтема 1.1.1.2",
                                        "subtopics": []
                                    }}
                                ]
                            }},
                            {{
                                "title": "Подтема 1.1.2",
                                "subtopics": []
                            }}
                        ]
                    }},
                    {{
                        "title": "Подтема 1.2",
                        "subtopics": []
                    }}
                ]
            }},
            {{
                "title": "Подтема 2",
                "subtopics": [
                    {{
                        "title": "Подтема 2.1",
                        "subtopics": []
                    }},
                    {{
                        "title": "Подтема 2.2",
                        "subtopics": []
                    }}
                ]
            }}
        ]
    }}
    """
    response = get_openai_response(prompt)
    if response:
        print("Структура данных для интеллект-карты:", response)
        generate_xmind_map(response, "output1.xmind")
        print("Интеллект-карта создана и сохранена как 'output1.xmind'")
    else:
        print("Не удалось получить корректный ответ от OpenAI.")
        print("Не удалось получить корректный ответ от OpenAI.")

if __name__ == "__main__":
    main()
123