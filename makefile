
MANAGER=jamjar/manage.py
IP=0.0.0.0
PORT=5001

###########################################
# Install
###########################################
install: requirements.txt
	pip install -r requirements.txt


###########################################
# Migrations
###########################################
makemigrations: install $(MANGER)
	python $(MANAGER) makemigrations $(MODULE);

migrate: makemigrations
	python $(MANAGER) migrate;

dry-migrate: $(MANAGER)
	python $(MANAGER) makemigrations --dry-run --verbosity 3 $(MODULE);


###########################################
# Runners
###########################################
run: install $(MANAGER)
	python $(MANAGER) runserver $(IP):$(PORT)

debug: install $(MANAGER)
	python -m pdb $(MANAGER) runserver $(IP):$(PORT)

shell: install $(MANAGER)
	python $(MANAGER) shell_plus

run-bg: install $(MANAGER)
	python $(MANAGER) runserver $(IP):$(PORT) &

runserver: install $(MANAGER)
	nohup python $(MANAGER) runserver $(IP):$(PORT) > logs/server.log 2>&1 &

test:
	cd jamjar && JAMJAR_ENV=test python manage.py test && cd -

queue: install
	cd jamjar && celery -A jamjar.tasks.tasks.app worker --loglevel=info

kill:
	pkill -f $(MANAGER)


###########################################
# Cleanup
###########################################
clean:
	find . -name "*.pyc" -print0 | xargs -0 rm

empty-database: $(MANAGER)
	python $(MANAGER) flush
