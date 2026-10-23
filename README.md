# Watch Mates 💬

Watch Mates is a chat platform where you can connect with your friends, share content in the chat, and discuss it together.

## Features 🚀 
- Connect with friends and build your friends list
- Chat with friends one-to-one and in group
- Share content (links, videos, posts) directly in the chat
- Discuss shared content in the conversation
- User registration and login

## Technologies 📦 
- **Backend:** Python, Django
- **Database:** PostgreSQL
- **Templating:** Jinja2
- **Frontend:** HTML, CSS, JavaScript


## Installation ⬇️

1. Clone the repository
```bash
   git clone https://github.com/growingrohit/watch_mates_be.git
   cd watch-mates
```

2. Create and activate a virtual environment
```bash
   python -m venv venv
   source venv/bin/activate
   # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
   pip install pipenv
   pipenv install
```

4. Apply migrations
```bash
   python manage.py migrate
```
 
5. Create an admin user
```bash
   python manage.py createsuperuser
```
 
6. Start the development server
```bash
   python manage.py runserver
```

The app will be available at `http://127.0.0.1:8000/`.

## Project Structure 🛠️

```
watch-mates/
├── manage.py
├── watchmates/     # Project settings and URL configuration
├── accounts/       # User Login and Info
|   ├── migrations/
|   ├── models/
|   ├── serializers/
|   ├── tests/
|   ├── utils/
|   ├── views/
|   ├── __init__.py
|   ├── admin.py
|   ├── apps.py
|   ├── factories.py
|   ├── page_urls.py    # Web urls for frontend
|   └── urls.py         # Urls for apis
|
├── chat/           # All conversation and groups
|   ├── migrations/
|   ├── models/
|   ├── serializers/
|   ├── tests/
|   ├── utils/
|   ├── views/
|   ├── __init__.py
|   ├── admin.py
|   ├── apps.py
|   ├── factories.py
|   ├── page_urls.py    # Web urls for frontend
|   └── urls.py         # Urls for apis
|
├── common/         # Common methods to use throughout project   
|   ├── abstract.py
|   └── factories.py
|
├── templates/      # Jinja templates
|   ├── accounts/
|   ├── chat/
|   ├── components/
|   └── base.jinja
|
└── static/         # CSS, JavaScript, images
    ├── css/
    └── js/
```

 
## Running Tests 📝
```bash
python manage.py test
```
 