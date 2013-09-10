""""
Tests use py.test framework
To run from command line: py.test -s -v filename
"""
from application import session
from application.models import (
    Customer,
    Email,
    TestUser,
    Order,
    OrderItem,
    Item)

from sqlalchemy import func

customer_name = "px78xr"
customer_phone_num = "647-416-0007"
item_names = ['cookie', 'muffin', 'latte', 'mocha']


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
    assert test_user.id == found_user.id, \
        "Both created user and user found in db should have the same id"

    # Delete created user
    session.delete(found_user)
    session.commit()
    print "Deleting the found user"
    found_user = session.query(TestUser).\
        filter(TestUser.id == test_user.id).scalar()
    assert found_user is None, "Once deleted the user should not be found in db"
    print "We were able to successfully delete the found User"


def create_user_and_sample_Items(name, phone_num):
    customer = Customer(name, phone_num)
    cookie = Item(name + "_Cookie", 1.50)
    muffin = Item(name + "_Muffin", 2.00, "Carby stuff")
    latte = Item(name + "_Latte", 4.35, "Steamed milk over expresso")
    mocha = Item(name + "_Mocha", 5.00,
                 "Steamed milk over expresso and chocolate syrup")

    session.add(customer)
    session.add(cookie)
    session.add(muffin)
    session.add(latte)
    session.add(mocha)
    session.commit()

    result = {"customer": customer}
    item_names = ['cookie', 'muffin', 'latte', 'mocha']
    for name in item_names:

        item = session.query(Item).\
            filter(func.lower(Item.name).like('%' + name + '%')).\
            filter(func.lower(Item.name).like('%' + customer_name + '%')).\
            scalar()

        result[name] = item

    return result


def test_ordering_system():
    dict = create_user_and_sample_Items(customer_name, customer_phone_num)
    customer = dict['customer']
    cookie = dict['cookie']
    muffin = dict['muffin']
    latte = dict['latte']
    mocha = dict['mocha']

    # filter(lambda x: session.add(x), [customer, cookie, muffin, latte, mocha])
    customer.orders.append(Order())
    customer.orders.append(Order())
    session.commit()

    customer = session.query(Customer).\
        filter(func.lower(Customer.name) == func.lower(customer_name)).scalar()
    assert customer is not None, "Customer should be present"
    print "Successfully created Customer"

    orders = session.query(Order).filter(Order.customer_id == customer.id).all()
    assert len(orders) == 2, "Order size isn't accurate"
    print "Successfully created Orders"

    order1, order2 = orders[0], orders[1]

    order1.order_items.append(OrderItem(cookie.id, 2))
    order1.order_items.append(OrderItem(latte.id, 2,
                                        "Sugar please! Lots of it, in both"))
    order1.order_items.append(OrderItem(mocha.id, 10,
                              "Buying for the whole group"))

    order2.order_items.append(OrderItem(cookie.id, 20))
    order2.order_items.append(OrderItem(muffin.id, 20, "In two boxes"))

    session.commit()

    order1_items = session.query(OrderItem).\
        filter(OrderItem.order_id == order1.id).all()

    order2_items = session.query(OrderItem).\
        filter(OrderItem.order_id == order2.id).all()

    assert len(order1_items) == 3, "Number of items in order1 is not accurate"
    assert len(order2_items) == 2, "Number of items in order2 is not accurate"
    print "Successfully created order items"

    # Test deleting an order item, has no effect on the customer, or the order,
    #  or the items

    session.delete(order1_items[0])
    session.commit()

    customer = session.query(Customer). \
        filter(func.lower(Customer.name) == func.lower(customer_name)).scalar()
    assert customer is not None,\
        "Deleting an order item should not delete the customer"

    orders = session.query(Order).filter(Order.customer_id == customer.id).all()
    assert len(orders) == 2,\
        "Deleting the order item should not delete the order"

    order1, order2 = orders[0], orders[1]
    assert len(order1.order_items) == 2, \
        "Deleting the order item should delete it from db"
    print "Successfully deleted order item"

    all_items = session.query(Item).\
        filter(func.lower(Item.name).like('%' + customer_name + '%')).all()
    assert len(all_items) == 4, \
        "Deleting the order item should not delete any item"


    # Test deleting an order, removes all the order items, but leaves the
    # items and customers untouched

    order1_id = order1.id
    session.delete(order1)
    session.commit()

    order_items = session.query(OrderItem).\
        filter(OrderItem.order_id == order1_id).all()
    assert len(order_items) == 0, \
        "Deleting an order should remove all its order items"

    customer = session.query(Customer). \
        filter(func.lower(Customer.name) == func.lower(customer_name)).scalar()
    assert customer is not None,\
        "Deleting an order should not delete the customer"

    orders = session.query(Order).filter(Order.customer_id == customer.id).all()
    assert len(orders) == 1,\
        "Deleting an order item should only delete that order, no other order"
    print "Successfully deleted the order"


    # Test deleting an customer deletes all the orders, and the order items,
    # but leaves all the items untouched

    order_id = customer.orders[0].id
    customer_id = customer.id
    session.delete(customer)
    session.commit()

    customer = session.query(Customer). \
        filter(func.lower(Customer.name) == func.lower(customer_name)).scalar()
    assert customer is None,\
        "Deleting a customer should remove it from db"
    print "Successfully deleted the Customer"

    orders = session.query(Order).filter(Order.customer_id == customer_id).all()
    assert len(orders) == 0, "Deleting a customer should delete its orders"

    order_items = session.query(OrderItem).\
        filter(OrderItem.order_id == order_id).all()
    assert len(order_items) == 0, \
        "Deleting a customer should delete all its order_items"
    print "    And the order items associated with the customer"

    all_items = session.query(Item). \
        filter(func.lower(Item.name).like('%' + customer_name + '%')).all()
    assert len(all_items) == 4, \
        "Deleting the order item should not delete any item"

    filter(lambda x: session.delete(x), all_items)
    session.commit()

    all_items = session.query(Item). \
        filter(func.lower(Item.name).like('%' + customer_name + '%')).all()
    assert len(all_items) == 0,\
        "Removing items to undo db changes during test should not fail"

    print "Ran test successfully to try adding/deleting orders," \
          " order items and customers"