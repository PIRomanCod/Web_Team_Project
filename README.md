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
  - ask your personal English AI teacher (GPT based) for help and advise
  - check correctness of your sentences by your personal English AI teacher (GPT based)
  - add contacts, notes, files
  - edit contacts, notes, files
  - delete contacts, notes, files
  - search contacts, notes, files
  - sort files
  - filter notes, files
  - download files
  - upload files
  - look your likely tags in the notes
  - mark your notes as active or done
  - check when your contact has birthdays and never forget to congratulate him/her
  - change your avatar
- other user never can see your data
- enjoy and not forget do donate us!



# How to use documentation:
- documentation link - http://localhost:63342/Team_project_Web/personal_assistant/docs/_build/html/index.html
- to create/update documentation - \personal_assistant\docs>make.bat html (Windows) or \personal_assistant\docs>make html (Linux)


# Used technologies:
- Python 3.10
- Django 4.2.1
- BeautifulSoup 4
- Sphinx
- PostgreSQL 12.0
- OpenWeatherMap API
- DOU API
- OpenAI API
- DropBox API
- Privatbank API
- Bootstrap 5.1.3
- HTML5
- CSS3
- Docker ????
- GitHub
