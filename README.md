task-manager/
├── app/
│   ├── __init__.py            # Initializes app, DB, login manager
│   ├── routes.py              # Flask routes
│   ├── models.py              # MongoDB models
│   ├── forms.py               # WTForms
│   ├── templates/
│   │   ├── base.html
│   │   ├── login.html
│   │   ├── signup.html
│   │   ├── dashboard.html     # List of tasks
│   │   ├── task_form.html     # Add/edit task
│   └── static/
│       └── style.css
├── config.py
├── run.py
├── requirements.txt
└── .env


===============
in cmd prompt - run -> mongo

and in project directory ->
venv\Scripts\activate
(venv) PS F:\MY_LIFE_MY_VIEWS\my projects\task_manager_app\task-manager> flask run