# django_project

## project setup

1- compelete cookiecutter workflow (recommendation: leave project_slug empty) and go inside the project
```
cd django_project
```

2- SetUp venv
```
virtualenv -p python3.10 venv
source venv/bin/activate
```

3- install Dependencies
```
pip install -r requirements_dev.txt
pip install -r requirements.txt
```

4- create your env
```
cp .env.example .env
```

5- spin off docker compose
```
docker compose -f docker-compose.dev.yml up -d
```

6- Create tables
```
python manage.py migrate
```

7- run the project
```
python manage.py runserver
```



## Run project for production
1- create your env
```
cp .env_production .env
```

2- spin off docker compose
```
docker compose -f docker-compose.yml up -d
```

