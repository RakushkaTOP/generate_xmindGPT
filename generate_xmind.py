import os
import json
import openai
import xmind
from dotenv import load_dotenv

# Загрузить API ключ из .env файла
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

# Функция для получения ответа от OpenAI в формате Markdown
def get_openai_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    response_text = response['choices'][0]['message']['content'].strip()
    return response_text

# Функция для преобразования разметки Markdown в JSON
def parse_markdown_to_json(markdown_text):
    lines = markdown_text.split('\n')
    root = {'title': '', 'subtopics': []}
    stack = [root]
    current_level = 0

    for line in lines:
        if not line.strip():
            continue
        
        # Определяем уровень заголовка
        level = line.count('#')
        title = line.strip('#').strip()

        # Создаем новый узел
        node = {'title': title, 'subtopics': []}
        
        # Переходим на нужный уровень в стеке
        while len(stack) > level:
            stack.pop()
        
        # Добавляем узел в текущий уровень
        if stack:
            stack[-1]['subtopics'].append(node)
        
        stack.append(node)

    return root

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
    Создайте иерархию в формате Markdown для интеллект-карты по запросу: {user_input}.
    Пожалуйста, включите как можно больше уровней иерархии. Каждый раздел должен иметь несколько подразделов, и каждый подраздел должен также содержать свои собственные подразделы, и так далее, до максимально возможной глубины.

    Используйте символы # для обозначения уровней иерархии. Например:
    # Основная тема
    ## Подтема 1
    ### Подтема 1.1
    #### Подтема 1.1.1
    """

    response_text = get_openai_response(prompt)
    
    # Преобразование Markdown в JSON
    hierarchy_json = parse_markdown_to_json(response_text)
    
    if hierarchy_json:
        print("Структура данных для интеллект-карты:", json.dumps(hierarchy_json, indent=2))
        generate_xmind_map(hierarchy_json, "output1.xmind")
        print("Интеллект-карта создана и сохранена как 'output1.xmind'")
    else:
        print("Не удалось преобразовать Markdown в JSON.")

if __name__ == "__main__":
    main()
