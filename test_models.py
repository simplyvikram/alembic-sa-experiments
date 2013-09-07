""""
Tests use py.test framework
To run from command line: py.test -s -v filename
"""
from application import session
from application.models import Email, TestUser


def create_in_memory_user():
    name, full_name, password = "tu1", "test user1", "tu1 password"
    test_user = TestUser(name, full_name, password)

    for x in range(1, 4):
        test_user.emails.append(Email(full_name + "_" + str(x) + "@foo.com"))
    return test_user


def test_user_creation_and_deletion():
    print "Inside test_creation"

    # Create user
    test_user = create_in_memory_user()
    session.add(test_user)
    session.commit()
    print "Created user with id " + str(test_user.id)

    # Find user from db and check if it exists
    found_user = session.query(TestUser).\
        filter(TestUser.id == test_user.id).scalar()

    print "Found user in db with id " + str(found_user.id)
    assert test_user.id is not None, "Created user id should not be None"
    assert found_user.id is not None, "User found in db should not be None"
    assert test_user.id == found_user.id, "Both created user and user found" \
                                            " in db should have the same id"

    # Delete created user
    session.delete(found_user)
    session.commit()
    print "Deleting the found user"
    found_user = session.query(TestUser).\
        filter(TestUser.id == test_user.id).scalar()
    assert found_user is None, "Once deleted the user should not be found in db"
    print "We were able to successfully delete the found User"
