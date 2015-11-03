
MANAGER=jamjar/manage.py

install:
	pip install -r requirements.txt;

migrate: $(MANAGER)
	python $(MANAGER) makemigrations;
	python $(MANAGER) migrate;

run: install
	python $(MANAGER) runserver 0.0.0.0:5001

run_server: install
	nohup python $(MANAGER) runserver 0.0.0.0:5001 > server.log 2>&1 &

kill:
	pkill -f $(MANAGER)

clean:
	find . -name "*.pyc" -print0 | xargs -0 rm
