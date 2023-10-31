# InHome Api
 - InHome helps backedn api

## API Documentation
- Find the swagger documentation [here](http://hubbackendstagingenv-env.eba-nuhfsny2.us-east-1.elasticbeanstalk.com/api/v1/docs/)

## How to setup the application locally
### Prerequisites
- python 3
- postgresSQL

### Installation
- clone the repo 
    ```
    git clone https://github.com/inhomee/hub_cloud_api
    ```
- navigate to the project directory
    ```
    cd hub_cloud_api
    ```
- activate your virtual env
- install dependencies
    ```
    pip install -r requirements.txt
    ```
- create your local posrgresSQL db
- copy environment variable from .env-sample to your .env file
    ```
    cp .env-sample .env
    ```
- replace the env values with your correct variables
- source .env variables
    ```
    source .env
    ```
- migrate db schemas
    ```
    #using make file
    make migrate

    # python command
    python manage.py migrate
    ```
- start the server locally and access [this](http://127.0.0.1:8000/api/v1/docs/) url
    ```
    # using make file
    make server

    # python command
    python manage.py runserver
    ```
- run tests
    ```
    # using make file
    make tets

    #other option
    coverage run --source=app manage.py test --verbosity=2 && coverage report -m
    ```