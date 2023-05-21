# What is Personal Assistant?
- Personal Assistant is a web application that allows you to store contacts, notes, and files in one place.
- Personal Assistant is a web application that you can adjust for yourself.
- Personal Assistant is a cloud storage in which you can be sure of the safety of your data.
- Personal Assistant is coded by Django and Python.

# What is the purpose of Personal Assistant?
- The purpose of Personal Assistant is to make your life easier.
- The purpose of Personal Assistant is to make your life more organized.
- The purpose of Personal Assistant is to make your life more productive.
- The purpose of Personal Assistant is to make your life more secure.

# How to deploy Personal Assistant?
- Clone this repository to your computer.
- Install Python 3.10 or higher.
- Install poetry and create environment.
- Create .env file by env.example.
- Repeat steps from First Start of application.
- Enjoy!

# First Start of application:
- by env.example create .env file
- for creating dropbox variables you need to create app in dropbox and get access token:
  - https://www.dropbox.com/developers/apps
  - in your app give permissions for read and write
  - add to .env DROPBOX_APP_KEY=APPKEYHERE
  - add to .env DROPBOX_APP_SECRET=APPSECRETHERE
  - by this link you can get access token, only replace APPKEYHERE with your app key
  - https://www.dropbox.com/oauth2/authorize?client_id=APPKEYHERE&response_type=code&token_access_type=offline
  - in the result you'll get AUTHORIZATIONCODEHERE, replace it in next CURL and run it in terminal:
    curl https://api.dropbox.com/oauth2/token \
      -d code=AUTHORIZATIONCODEHERE \
      -d grant_type=authorization_code \
      -u APPKEYHERE:APPSECRETHERE
  - it will turn you answer in dictionary type, take there refresh token and use it as DROPBOX_REFRESH_TOKEN in .env 
  
- for correct working application on Windows you need to adjust DropBox library:
  - find file: services/file_services.py
  - find function: save_file_dropbox_and_get_new_name 
  - this function save file in dropbox by Django services, but incorrect(it is adding Disc letter (C: or other) to path)
  - so now you know why you need to correct this function
  - on top the same file find import: from storages.backends.dropbox import DropBoxStorage
  - with Ctrl + click on DropBoxStorage you are going to DropBox library 
  - find ~line 115 with next code:
      def _full_path(self, name):
          if name == '/':
              name = ''
          return safe_join(self.root_path, name).replace('\\', '/')
  - and change it to:
      def _full_path(self, name):
          if name == '/':
              name = '' 
          from os.path import join
          final_path = join(self.root_path, name)
          return final_path.replace('\\', '/')
  - 
- python manage.py makemigrations  - create migrations
- python manage.py migrate - applying migrations
- python manage.py create_storageapp_tables - create tables for dropbox
- python manage.py createsuperuser - create superuser
- python manage.py runserver - start app

# For next starts:
- python manage.py runserver - start app

# How to use application:
- go to http://localhost:8000/
- read fresh news
- prepare yourself for any weather's joke
- cry about exchange rates
- check your salary offers at DOU and cry again
- login or register for more features
- only logined users can:
  - ask your personal English AI (GPT based) teacher for help and advise
  - add contacts, notes, files
  - edit contacts, notes, files
  - delete contacts, notes, files
  - search contacts, notes, files
  - sort files
  - filter notes, files
  - download files
  - upload files
  - look your likely tags in the notes
- other user never can see your data
- enjoy!



# How to use documentation (it will be delete):
- documentation link - http://localhost:63342/Team_project_Web/personal_assistant/docs/_build/html/index.html
- personal_assistant/docs/modules - documentation files by modules - треба кожному свій файл перевірити 
- \personal_assistant\docs>make.bat html - create/update documentation - команда для оновлення документації
  - варіант для автоматичного написання документації:
    Полегшити написання рядків документації може допомогти плагін для PyCharm 
    Trelent - AI Docstrings on Demand. Він за допомогою AI дозволяє створювати досить 
    хороші рядки документації для популярних мов програмування. (комбінація клавіш Alt-D на імені кожної функції)



# Критерії прийому (it will be delete):
1.	Web-інтерфейс може бути реалізований на фреймворку Django.
2.	Проєкт має бути збережений в окремому репозиторії та бути загальнодоступним (GitHub, GitLab або BitBucket).
3.	Проєкт містить докладну інструкцію щодо встановлення та використання.
4.	“Personal Assistant” зберігає інформацію в базі даних і може бути перезапущений без втрати даних.
5.	Для надійності та підвищення продуктивності всю інформацію зберігати у базі даних PostgreSQL.
6.	Всі критичні дані до доступу до бази даних та налаштування програми зберігаються в змінних середовищах і не завантажуються в репозитарій.
7.	Проєкт повністю реалізує всі пункти вимог, описані в завданні.

P.S.: Ви можете розширити функціонал проєкту на свій розсуд обов'язково проконсультувавшись з ментором перед цим. Розглядайте цей проєкт, як частину вашого портфоліо і корисний вам інструмент. З цієї причини ініціатива у розширенні та доповненні вимог до проєкту вітається. Наприклад ви можете додати файл Dockerfile, щоб програма могла бути розміщена в контейнері Docker та образ завантажений на dockerhub.


# Links (it will be delete):

https://trello.com/b/pUA5sy8P/web-personal-assistant - Board

https://docs.google.com/document/d/1bUUMeaFmykmLw1PX6nAtBGu6k14mvYX8ukmBIPLw1AU/edit?usp=sharing - Questions

