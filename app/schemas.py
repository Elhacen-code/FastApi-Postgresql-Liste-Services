from typing import List
from pydantic import BaseModel
from pydantic.networks import int_domain_regex

# items 

class ItemBase(BaseModel):
    name: str
    category: str
    purchased: bool
    
class ItemCreate(ItemBase):
        pass

class ItemUpdate(ItemBase):
        pass

class Items(ItemBase):
        id:int
        class Config:
            orm_mode = True

#users

class UserBase(BaseModel):
        name: str
        

class UserCreate(UserBase):
        pass   

class UserUpdate(UserBase):
        pass  

class User(UserBase):
        id:int
        class Config:
            orm_mode = True

#shops

class ShopBase(BaseModel):

    name : str
    capacity : int
    
class ShopCreate(ShopBase):
        pass   

class ShopUpdate(ShopBase):
        pass  

class Shop(ShopBase):
        id:int
        class Config:
            orm_mode = True

class Shope(ShopBase):
        id:int
        trade_id : int
        class Config:
            orm_mode = True

class ShopeCreate(ShopBase):
        pass   


#Trades
class TradeBase(BaseModel):
    name : str
    tel : str
    email : str

class TradeCreate(TradeBase):
        pass   

class TradeUpdate(TradeBase):
        pass  

class Trade(TradeBase):
        id:int
        shop_s: List[Shop] = []
        class Config:
            orm_mode = True

