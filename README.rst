
**SqlAlchemy and Alembic testing**

work in progress, fix formatting later

Notes -

* Needs py.test
* Flask is not needed, just using it for its manage extension, will remove its
dependency soon
* no requirements.txt yet, will add later(uses sqlalchemy and flask for now)
* Tests needs to be broken down, too ginormous
* Needs a requirement.txt


Pre steps -

* create postgres database alembic-sa-experiments

 * createdb alembic-sa-experiments


Steps-

* git clone https://github.com/simplyvikram/alembic-sa-experiments.git
* alembic upgrade head
* python manage.py create_random_users
* python manage.py list_all_users
* py.test -s -v
