Procfile

web: gunicorn homeharmonix.wsgi --log-file - 
#or works good with external database
web: python manage.py migrate && gunicorn homeharmonix.wsgi