Тестовое задание.

API по работе с записями транспортных средств:
- CRUD
- загрузка и выгрузка списка записей в csv, xlsx

Тестовые пользователи:
- кузя/кузя123 (админ)

<b>Для проверки необходимо:</b>
1) Установить ПО для отправки запросов (Postman)
2) Выгрузить репозиторий командой "git clone {repo_link}"
3) Запустить сервер командой: python3 manage.py runserver
4) Получить токен для работы, выполнив POST-запрос по адресу <b>"127.0.0.1:8000/api/token/"</b>. 
   В теле запроса необходимо передать JSON с логином и паролем:
   {
    "username": "кузя",
    "password": "кузя123"
   } 
   В ответ придет структура данных, содержащая JSON вида: {"refresh": "refresh_token", "access": "access_token"}
5) Из полученного JSON в первую очередь понадобится access_token. 
   Его следует вставить в следующую структуру данных, добавив приставку "Bearer_". 
   Полученная запись должна иметь вид:
      { "Authorization": "Bearer_eyJ0eXAi..."}.
   Ее следует указывать при каждом запросе, иначе данные не будут предоставленны.
6) Для работы с приложением реализовано следующее API:
    - [GET] <b>127.0.0.1:8000/api/auto</b> - получение списка автомобилей
    - [POST] <b>127.0.0.1:8000/api/auto/create</b> - добавление нового автомобиля, для чего в теле запроса необходимо
      передать структуру, вида: 
      {
        "mark": "",
        "model": "",
        "reg_number": "",
        "issue_year": int,
        "vin": "",
        "sts_number": "",
        "sts_date": "YYYY-MM-DD",
        "description": "",
        "category": int
      }
    - [POST] <b>127.0.0.1:8000/api/auto/update/<int:pk></b> - редактирование уже существующего автомобиля, в теле запроса следует передать
    - структуру данных с изменениями:
      {
        "mark": "",
        "model": "",
        "reg_number": "",
        "issue_year": int,
        "vin": "",
        "sts_number": "",
        "sts_date": "YYYY-MM-DD",
        "description": "",
        "category": int
      }
    - [GET] <b>127.0.0.1:8000/api/auto/<int:pk></b> - получение информации об уже существующем автомобиле по id
    - [GET] <b>127.0.0.1:8000/api/auto/search/<str:query>/</b> - поиск автомобилей по запросу для проверки поиска следует запустить установить elasticsearch, например используя докер:
       https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html
    - [GET] - <b>127.0.0.1:8000/api/auto/excel</b> - выгрузка данных об автомобилях в формате excel
    - [POST] - <b>127.0.0.1:8000/api/auto/excel</b> - загрузка данных об автомобилях в формате excel,  
      в загружаемой таблице должны быть следующие столбцы:
        <table>
          <tr>
            <td>id</td>
            <td>mark</td>
            <td>model</td>
            <td>reg_number</td>
            <td>issue_year</td>
            <td>vin</td>
            <td>sts_number</td>
            <td>sts_date</td>
            <td>description</td>
            <td>category</td>
          </tr>
        </table>
      - [GET] - <b>127.0.0.1:8000/api/auto/csv</b> - выгрузка данных об автомобилях в формате csv
      - [POST] - <b>127.0.0.1:8000/api/auto/csv</b> - загрузка данных об автомобилях в формате csv,  
        в загружаемом текстовом файле должны быть обозначены следующие столбцы: id, mark, model, reg_number, issue_year, vin, 
        sts_number, sts_date, description, category

    <b>Для запуска из Docker необходимо:</b>
   1) Убедиться, что Docker установлен
   2) Выполнить в терминале команды:
        - docker pull bazhil/search_auto:v1
        - docker run --publish 8000:8000 auto_search:v1
