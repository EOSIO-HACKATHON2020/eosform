SETTINGS = "config.settings.dev"
PROJ = "config"

run:
	source .venv/bin/activate; export DJANGO_SETTINGS_MODULE=$(SETTINGS); WERKZEUG_DEBUG_PIN=off python manage.py runserver_plus 0.0.0.0:8000

celery:
	source .venv/bin/activate; export DJANGO_SETTINGS_MODULE=$(SETTINGS); celery -A $(PROJ) worker -B -l info

install:
	source .venv/bin/activate; export DJANGO_SETTINGS_MODULE=$(SETTINGS);
	pip install -r requirements/dev.txt
