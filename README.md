# ZoomAPi - создание встречи и вывод прошедших встреч

### Загрузить репозиторий

    git clone <http>

### Создать виртуальное окружение

    python3 -m venv venv

### Активировать виртуально окружение

    source venv/bin/activate

### Установить зависимости

    pip install -r requirements.txt

### Зарегистрировать приложение server to server

[//]: # (    https://marketplace.zoom.us/)
    [Zoom Marketpalce Media](https://marketplace.zoom.us/ "Перейти на zoom marketpace")

    перейти по ссылке, авторизироваться. 
    
    Создать или использовать уже имещиеся приложение server to server
    В scopes приложения добавить : 

            * meeting:read:summary:admin
            * meeting:read:list_summaries:admin          
            * meeting:read:past_meeting:admin
            * meeting:read:alert:admin
            * meeting:read:meeting:admin
            * meeting:read:list_meetings:admin
            * meeting:write:meeting:admin
            * meeting:write:meeting:master
            * meeting:read:list_meetings:master


    Добавить данные приложение в файл .env-example  переименовать в .env

### Установить параметры создаваемой встречи 

    self.meeting_param -  параметры создаваемой встречи. 

### Запуск
    
    Создать обьект классa Meetings_Worker
    Meetings_Worker.create_meeting  - создание встречи и запись в файл 
    Meetings_Worker.get_meeteng_history - вывод встреч за последниее 7 дней в консоль 

    

    




