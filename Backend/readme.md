# setting up environment 

- create virtual environment 
- python version = 3.12.1

```
python -m venv env
```

install required dependency 
```
pip install -r requirements.txt
```

- create .env file and add your credencial 
```
MONGODB_PASSWORD = 
SECRET_KEY = 
ALGORITHM = 
```

- when you do changes make sure to update requirement.txt
```
pip freeze > requirements.txt
```