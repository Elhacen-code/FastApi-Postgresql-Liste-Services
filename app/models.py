from sqlalchemy import Boolean, Column, String, Integer
import sqlalchemy
from sqlalchemy.sql.schema import ForeignKey, Table
from .database import Base
import sqlalchemy.orm as _orm
import sqlalchemy as _sql

#User model
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    password = Column(String, index = True)

    @classmethod
    async def get_user(cls, username):
        return cls.get(username=username)

    def verify_password(self, password):
        return True

#Customer model
class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    tel = Column(String, index=True)
    email = Column(String, index=True)

    #trades = _orm.relationship("Trade", back_populates="customers", uselist=False)

#Trad model
class Trade(Base):
    __tablename__ = "trads"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    tel = Column(String, index=True)
    email = Column(String, index=True)

    shop_s = _orm.relationship("Shop", back_populates="trades")

    #customers = _orm.relationship("Customer", back_populates="trades")


#association between (shpes and items)

# association_table = Table('association', Base.metadata,
#     Column('shop_id', Integer, ForeignKey('shops.id')),
#     Column('item_id', Integer, ForeignKey('items.id'))
# )

#Shop model
class Shop(Base):
    __tablename__ = "shops"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    capacity = Column(String, index=True)
    trade_id = Column(Integer, ForeignKey("trads.id"))

    trades = _orm.relationship("Trade", back_populates="shop_s")

    #itemss = _orm.relationship('Items', secondary=association_table, backref=_orm.backref('havers', lazy='dynamic'))
    
#Items model
class Items(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    category = Column(String, index=True)
    purchased = Column(Boolean, index=True)    