from sqlalchemy.orm import Session
from . import models,schemas

#Item operations

def get_items(db: Session):
    return db.query(models.Items).all()

def create_item(db:Session, item: schemas.ItemCreate):
    db_item = models.Items(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_item(db: Session,item:schemas.ItemUpdate, id: int):
    db_item = db.query(models.Items).get(id)

    db_item.name = item.name
    db_item.category = item.category
    db_item.purchased = item.purchased

    db.commit()
    db.refresh(db_item)
    return db_item

def delete_item_by_id(db: Session, id:int):
    db_item = db.query(models.Items).get(id)
    db.delete(db_item)
    db.commit()

def find_item(db:Session, id:int):

    return db.query(models.Items).filter(models.Items.id == id).first()

    
#User operations

def create_user(db:Session, users: schemas.UserCreate):
    db_user = models.User(**users.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_name(db: Session, name: str):
    return db.query(models.User).filter(models.User.name == name).first()

def verify_password(db:Session, password: str):
    return db.query(models.User).filter(models.User.password == password).first()

#Shop operations

def get_shops(db: Session):
    return db.query(models.Shop).all()

# In this methode you can create one shop without trad_1 and the las take null like default values
def create_shop(db:Session, shops: schemas.ShopeCreate):
    db_shop = models.Shop(**shops.dict())
    db.add(db_shop)
    db.commit()
    db.refresh(db_shop)
    return db_shop


def create_shop_trad(db: Session, item: schemas.ShopCreate, trade_id: int):
    db_shop = models.Shop(**item.dict(), trade_id=trade_id)
    db.add(db_shop)
    db.commit()
    db.refresh(db_shop)
    return db_shop

def update_shop(db: Session,shop:schemas.ShopUpdate, id: int):
    db_shop = db.query(models.Shop).get(id)
    
    db_shop.name = shop.name
    db_shop.capacity = shop.capacity
    db_shop.trade_id = shop.trade_id

    db.commit()
    db.refresh(db_shop)
    return db_shop

def delete_shop(db: Session, id:int):
    db_shop = db.query(models.Shop).get(id)
    db.delete(db_shop)
    db.commit()

def find_shop(db:Session, id:int):

    return db.query(models.Shop).get(id)


#Trade operations

def get_trads(db: Session, skip: int = 0, limit: int = 10): #skip and limit : to limite the number of line of list returned
    #return db.query(models.Trade).all()
    return db.query(models.Trade).offset(skip).limit(limit).all()

def create_trade(db:Session, trades: schemas.TradeCreate):
    db_trade = models.Trade(**trades.dict())
    db.add(db_trade)
    db.commit()
    db.refresh(db_trade)
    return db_trade

def update_trade(db: Session,trade:schemas.TradeUpdate, id: int):
    db_trade = db.query(models.Trade).get(id)

    db_trade.name = trade.name
    db_trade.tel = trade.tel
    db_trade.email = trade.email

    db.commit()
    db.refresh(db_trade)
    return db_trade

def delete_trade(db: Session, id:int):
    db_trade = db.query(models.Trade).get(id)
    db.delete(db_trade)
    db.commit()

def find_trade(db:Session, id:int):

    return db.query(models.Trade).get(id)


def get_shops_of_trads(db:Session, id:int):
    return find_trade(db,id).shop_s
