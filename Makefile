start:
	poetry run flask --app flask_example/example --debug run

run:
	poetry run gunicorn --workers=4 --bind=127.0.0.1:5000 flask_example.example:app

