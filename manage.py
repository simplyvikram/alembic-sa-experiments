from flask.ext.script import Manager

from application import app, session
from application.models import (
    Email,
    TestUser
)

manager = Manager(app)

@manager.command
def hello():
    print "Whateverrrr!! :-/"

@manager.command
def create_db():
    print "use alembic for dropping and creating database"
    print "alembic upgrade head"
    # metadata_classical.create_all(engine)
    # print "created database schema from classical mapping"
    # metadata_declarative.create_all(engine)
    # print "created database schema from declarative mapping"


@manager.command
def drop_db():
    print "use alembic for dropping and creating database"
    print "alembic downgrade base"
    # metadata_classical.drop_all()
    # print "dropped database schema from classical mapping"
    # metadata_declarative.drop_all(engine)
    # print "dropped database schema from declarative mapping"


def create_a_user(base, prefix, email):
    name = base + prefix
    fullname = name + " singh"
    pwd = "password-" + name
    user = TestUser(name, fullname, pwd)
    if email:
        emails = [name + '_foo@foo.com', name + '_bar@bar.com',
                  name + '_zoo@zoo.com']
        user.add_email(emails[0])
        user.add_email(emails[1])
        user.add_email(emails[2])

    print "user id before commit - " + str(user.id) + "for user - " + str(user)
    session.add(user)
    session.commit()
    print "user id before commit - " + str(user.id) + "for user - " + str(user)


@manager.command
def create_random_users():
    for x in range(10, 13):
        create_a_user("Jack", str(x), True)

    for x in range(14, 16):
        create_a_user("noEmailUser", str(x), False)


@manager.command
def list_all_users():
    q = session.query(TestUser)
    print q.all()


@manager.option('-id', help='id of TestUser(pk)')
def delete_user(id):
    query = session.query(TestUser).filter(TestUser.id == id)
    user = query.one()
    print 'About to delete', type(user), '---', user
    session.delete(user)
    session.commit()


@manager.command
def find_all_users():
    r = session.query(TestUser).all()
    for x in r:
        print x

if __name__ == '__main__':
    manager.run()

