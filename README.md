# Inforce_test

### How to run the project:

```
docker compose build

docker compose up

docker-compose run app python manage.py createsuperuser 

docker-compose run app python manage.py makemigrations 

docker-compose run app python manage.py migrate
```