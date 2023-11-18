import json
import os

# Получаем полный путь к файлу 'db.json'
file_path = os.path.join('C:\\Users\\user\\PycharmProjects\\django\\deva7km', 'db.json')

# Открываем файл в текущей кодировке (ibm866)
with open(file_path, 'r', encoding='cp1251 ') as file:
    # Читаем данные из файла
    data = file.read()

# Перекодируем данные в utf-8
data_utf8 = data.encode('utf-8').decode('utf-8')

# Загружаем данные JSON
json_data = json.loads(data_utf8)

# Теперь вы можете работать с данными в кодировке utf-8

# Если вы хотите сохранить данные в новом файле в utf-8
new_file_path = os.path.join('C:\\Users\\user\\PycharmProjects\\django\\deva7km', 'новый_файл.json')
with open(new_file_path, 'w', encoding='utf-8') as new_file:
    json.dump(json_data, new_file, ensure_ascii=False, indent=4)
