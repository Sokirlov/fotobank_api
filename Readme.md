# Photobank with RestApi 

## Start project

### Use PostgreSQL
If you use postgresql change in settings.py and install plugin `pip install psycopg2-binary`
```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "database",
        "USER": "db_user",
        "PASSWORD": "db_password",
        "HOST": "127.0.0.1",
        "PORT": "5432",
    }
}
```

### Install project
```shell
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic
```


## Links in project
1. Html view  `/`
2. Swagger  `/swagger/`
3. Api  `/api/`
4. Admin  `/admin/`

