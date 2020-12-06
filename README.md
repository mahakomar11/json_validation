# Валидатор JSON 

### Как использовать

Запустить скрипт validate_json.py

### Результаты

[Таблица с ошибками](errors_table.html)

### Как читать результаты

Столбцы в таблице:
* **File** - имя файла
* **Scheme** - название схемы, с которой сверялся файл
* **Error** - сообщение ошибки
* **Property with error** - свойство в файле, в котором нашлось нарушение схемы 
(значение этого свойства не того формата, или внутри этого свойства отсутсвуют нужные подсвойства)
* **Path to rule in schema** - путь к правилу в схеме, которое было нарушено

Значения последних двух колонок записываются в формате "свойство: подсвойство: подподсвойство: ...". 
Если в свойстве лежит список объектов, то вместо подсвойства может быть порядковый номер объекта, 
в котором нашлась ошибка. 

### Ошибки

| Error                                          | Description                                                                           | What to do                                                                            |
|------------------------------------------------|---------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------|
| File is OK                                     | Файл соответствует схеме                                                              | Радоваться:)                                                                          |
| Invalid schema                                 | Схема не соответствует эталонной http://json-schema.org/draft-07/schema#              | Исправить схему                                                                       |
| Invalid format                                 | JSON-файл пустой или содержит данные в неправильном формате                           | Добавить данные в правильном формате                                                  |
| Missing key 'event'                            | В JSON-файле не указано, для какого события данные                                    | Добавить 'event'                                                                      |
| Missing key 'data'                             | В JSON-файле отсутствуют данные для события, либо записаны под неправильным свойством | Добавить данные в свойство 'data'                                                     |
| File with key 'event'=? is valid for ??.schema | Для типа события, указанного в JSON-файле нет схемы, но ему подходит другая схема     | Исправить 'event', либо переименовать схему                                           |
| There is no ?.schema                           | Для типа события, указанного в JSON-файле нет схемы                                   | Добавить схему для этого типа события                                                 |
| Все другие сообщения                           | Описывает несоответствие JSON-файла и схемы                                           | Исправить свойство Property with error в соответствии со схемой, либо исправить схему |

### Пример

| Error |                       Property with error | Path to rule in schema |
|-------|----------------------                     |-----------             |
|'type' is a required property| type_ranges: 29     |properties: type_ranges: items: required |

Это означает, что в JSON-файле, в свойстве *type_ranges* в 29-ом объекте отсутствует свойство *type*, 
хотя в схеме прописано, что оно обязательно

**JSON-файл**:\
'type_ranges': [ ...,
{'date': '2020-08-27T08:34:00-04:00'}, ...]

**А должно быть**:\
'type_ranges': [ ...,
{'date': '2020-08-27T08:34:00-04:00', 'type': 'строка'}, ...]

Уточнить правило можно по схеме, по указанному пути.