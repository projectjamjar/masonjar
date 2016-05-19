
MANAGER=jamjar/manage.py
IP=0.0.0.0
PORT=5001

SEED?=seed_data/basic_seed.json
PRESENTATION_SEED?=seed_data/presentation_seed.json
FAKE_SEED?=seed_data/fake_seed.json

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

seed: $(MANAGER)
	python $(MANAGER) loaddata $(SEED)

dump: $(MANAGER)
	python $(MANAGER) dumpdata --natural-foreign --exclude auth.permission --exclude contenttypes --indent 4 > seed_data/seed.json


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
	#JAMJAR_ENV=prod gunicorn jamjar.wsgi:application --bind 0.0.0.0:5001 --threads 4

test:
	cd jamjar && JAMJAR_ENV=test python manage.py test && cd -

queue: install redis
	cd jamjar && celery multi start worker -A jamjar.tasks.tasks.app --logfile=../logs/queue.log --loglevel=info -c 1

kill-server:
	pkill -f $(MANAGER)

kill-queue:
	pkill -f celery

kill: kill-queue kill-server
	echo "Server and Queue killed."


###########################################
# Cleanup
###########################################
clean:
	find . -name "*.pyc" -print0 | xargs -0 rm

empty-database: $(MANAGER)
	python $(MANAGER) flush

# this runs in whatever your JAMJAR_ENV is set to!
drop-fingerprints:
	bash database_reset.py

# this only works on localhost for setting up jamjar db/user/etc
local-database-setup:
	bash database_setup.sh

base_db_reset:
	yes 'yes' | python $(MANAGER) flush
	python database_reset.py

fuck: base_db_reset
	make seed

present: base_db_reset
	python $(MANAGER) loaddata $(PRESENTATION_SEED)
	python presentation_fingerprints.py

fake: base_db_reset
	#python  generate_data.py
	python $(MANAGER) loaddata $(FAKE_SEED)

