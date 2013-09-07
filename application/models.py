from sqlalchemy import (
    Column,
    Float,
    ForeignKey,
    Integer,
    String
)

from sqlalchemy.orm import backref, relationship

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


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    phone_number = Column(String(20), nullable=False)

    orders = relationship("Order", backref=backref("customer"),
                          cascade="all, delete, delete-orphan",
                          passive_deletes=True,
                          order_by="Order.id")

    def __init__(self, name, phone_number):
        self.name = name
        self.phone_number = phone_number
        self.orders = []

        self.id = None

    def __repr__(self):
        return "<Customer -  id:%s, name:%s, orders:%s>" % \
               (str(self.id), self.name, self.orders)


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customers.id'))

    order_items = relationship("OrderItem",
                               cascade="all, delete, delete-orphan")

    def __init__(self):
        self.customer = None
        self.order_items = []

        self.id = None

    def __repr__(self):
        return "<Order - id:%s, customer_id:%s, customer_name:%s>" % \
               (str(self.id), str(self.customer.id), self.customer.name)


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    name = Column(String(40), nullable=False)
    description = Column(String(200), nullable=True)
    unit_price = Column(Float(2), nullable=True)

    order_items = relationship("OrderItem")

    def __init__(self, name, unit_price, description=None):
        self.name = name
        self.unit_price = unit_price
        self.description = description

        self.id = None
        self.order_items = []

    def __repr__(self):
        return "<Item - id:%s, name:%s, unit_price:%s>" % \
               (str(self.id), self.name, str(self.unit_price))


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    item_id = Column(Integer, ForeignKey('items.id'))
    quantity = Column(Integer)
    special_note = Column(String(200))

    def __init__(self, item_id, quantity, special_note=None):
        self.item_id = item_id
        self.quantity = quantity
        self.special_note = special_note

        self.id = None
        self.order_id = None

    def __repr__(self):
        return "<OrderItem - id:%s, order_id:%s, item_id:%s, quantity:%d>" % \
               (str(self.id), str(self.order_id),
                str(self.item_id), self.quantity)