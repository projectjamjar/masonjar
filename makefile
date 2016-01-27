
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
redis:
	redis-server --daemonize yes

run: install redis $(MANAGER)
	python $(MANAGER) runserver $(IP):$(PORT)

debug: install $(MANAGER)
	python -m pdb $(MANAGER) runserver $(IP):$(PORT)

shell: install redis $(MANAGER)
	python $(MANAGER) shell_plus

runserver: install redis $(MANAGER)
	nohup python $(MANAGER) runserver $(IP):$(PORT) > logs/server.log 2>&1 &

test:
	cd jamjar && JAMJAR_ENV=test python manage.py test && cd -

queue: install redis
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
