
MANAGER=jamjar/manage.py

install:
	pip install -r requirements.txt;

migrate: $(MANAGER)
	python $(MANAGER) makemigrations;
	python $(MANAGER) migrate;

run: install
	python $(MANAGER) runserver 0.0.0.0:5001

clean:
	find . -name "*.pyc" -print0 | xargs -0 rm
