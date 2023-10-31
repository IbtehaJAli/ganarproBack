migrations:
	python manage.py makemigrations
migrate:
	python3 manage.py migrate
collectstatic:
	python manage.py collectstatic
server:
	python3 manage.py runserver
tests:
	coverage run --source=app manage.py test --verbosity=2 && coverage report -m
