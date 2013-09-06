
from models import (
    TestUser,
    Email,
)
from sqlalchemy import (
    Table,
    Column,
    Integer,
    MetaData,
    String,
    ForeignKey,
)
from sqlalchemy.orm import (
    backref,
    mapper,
    relationship
)

metadata_classical = MetaData()

# Declare TestUser and Email mappings
test_users = Table('test_users', metadata_classical,
                   Column('id', Integer, primary_key=True),
                   Column('name', String(50)),
                   Column('fullname', String(50)),
                   Column('password', String(50)))

emails = Table('emails', metadata_classical,
               Column('id', Integer, primary_key=True),
               Column('user_id', Integer,
                      ForeignKey('test_users.id', ondelete='CASCADE')),
               Column('address', String(50)))

mapper(TestUser, test_users, properties={
    'emails': relationship(Email,
                           backref=backref('test_user'),
                           cascade="all, delete, delete-orphan",
                           passive_deletes=True,
                           order_by=emails.c.address)
})
mapper(Email, emails)