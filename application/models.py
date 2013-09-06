
from sqlalchemy import (
    Column,
    Integer,
    String
)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata_declarative = Base.metadata


class TestUser(object):

    def __init__(self, name, fullname, password):
        """
        id is the primary key, will be intialized by ORM upon insertion into db
        """
        self.name = name
        self.fullname = fullname
        self.password = password
        self.emails = []
        self.id = None

    def add_email(self, address):

        self.emails.append(Email(address))

    def __repr__(self):
        return '<TestUser - fullname : %s, emails : %s>'\
               % (self.fullname, self.emails)


class Email(object):
    """
    id is the primary key, will be initialized by ORM upon insertion into db
    user_id is a foreign key, maps to User.id which is the primary key in
    TestUser table
    """
    def __init__(self, address):
        self.address = address
        self.test_user = None
        self.id = None

    def __repr__(self):
        return '<Email - address:%s>' % self.address


class FirstDeclarative(Base):
    __tablename__ = 'first_declarative'

    id = Column(Integer, primary_key=True)
    value = Column(String(50))


# class Customer(Base):
#     __tablename__ = "customer"
#
#     customer_id = Column(Integer, primary_key=True)
#     name = Column(String(50))
#     phone_number = Column(String(20))
#
#     def __init__(self, name, phone_number):
#         self.name = name
#         self.phone_number = phone_number
#
#
#     # may reference an array of orders
#
#
# class Order(Base):
#     __tablename__ = "order"
#
#     order_id = Column(Integer, primary_key=True)
#     customer_id = Column(Integer)
#
#     def __init__(self, customer_id):
#         self.customer_id = customer_id
# #   includes an array of order_items
#
#
# class Item(Base):
#     __tablename__ = "item"
#
#     item_id = Column(Integer, primary_key=True)
#     name = Column(String(40))
#     description = Column(String(200))
#     unit_price = Column(Float(2))
#
#     def __init__(self, name, description, unit_price):
#         self.name = name
#         self.description = description
#         self.unit_price = unit_price
#
#
# class OrderItem(Base):
#     __tablename__ = "order_item"
#
#     order_item_id = Column(Integer, primary_key=True)
#     order_id = Column(Integer)
#     item_id = Column(Integer)
#     item_quantity = Column(Integer)
#     special_note = Column(String(200))
#
#     def __init__(self, order_id, item_id, item_quantity, special_note):
#         self.order_id = order_id
#         self.item_id = item_id
#         self.item_quantity = item_quantity
#         self.special_note = special_note