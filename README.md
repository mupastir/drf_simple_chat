# drf_simple_chat

**Download and install**
- Download project to any directory and unzip it. 
- After that, it is recommended to create virtual environment in folder with project. Execute in terminal next commands:

    `python3 -m venv venv`

- Activate venv (`source venn/bin/activate`)
- Also you need to install some libraries in pip:

    `pip install -r requirements/base.txt`
    
- Go to project work directory (`cd application`)
- Apply project migrations (`./manage.py migrate`)

**Run**

To run application execute command in directory with project:

    python manage.py runserver 
