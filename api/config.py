import os
AIRBNB_ENV = os.environ.get('AIRBNB_ENV')

if AIRBNB_ENV == "development": # add all variables we want to set
    DEBUG = True
    HOST = 'localhost'
    PORT = 3333
    DATABASE = {'host': '158.69.79.7', 'user': 'airbnb_user_dev', 'database': 'airbnb_dev', 'port': 3306, 'charset': 'utf8', 'password': os.environ.get('AIRBNB_DATABASE_PWD_DEV')}
elif AIRBNB_ENV == "production":
    DEBUG = False
    HOST = '0.0.0.0'
    PORT = 3000
    DATABASE = {'host': '158.69.79.7', 'user': 'airbnb_user_prod', 'database': 'airbnb_prod', 'port': 3306, 'charset': 'utf8', 'password': os.environ.get('AIRBNB_DATABASE_PWD_PROD')}

elif AIRBNB_ENV == "test":
    DEBUG = False
    HOST = 'localhost'
    PORT = 5555
    DATABASE = {
        'host': '158.69.92.181',
        'user': 'airbnb_user_test',
        'database': 'airbnb_test',
        'port': 3306,
        'charset': 'utf8',
        'password': os.environ.get('AIRBNB_DATABASE_PWD_TEST')
    }


