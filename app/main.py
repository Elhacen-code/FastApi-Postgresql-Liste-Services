from typing import List
from fastapi import Security,FastAPI, Depends, HTTPException
from sqlalchemy.orm import session
from . import crud,models,schemas
from .database import SessionLocal, engine

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

#Configuration to add ApiKey
from fastapi.security.api_key import APIKeyQuery, APIKeyCookie, APIKeyHeader, APIKey
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi

from starlette.status import HTTP_403_FORBIDDEN
from starlette.responses import RedirectResponse, JSONResponse

API_KEY = "1234567digitransform"
API_KEY_NAME = "access_token"
COOKIE_DOMAIN = "localtest.me"

api_key_query = APIKeyQuery(name=API_KEY_NAME, auto_error=False)
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)
api_key_cookie = APIKeyCookie(name=API_KEY_NAME, auto_error=False)


async def get_api_key(
    api_key_query: str = Security(api_key_query),
    api_key_header: str = Security(api_key_header),
    api_key_cookie: str = Security(api_key_cookie),
):

    if api_key_query == API_KEY:
        return api_key_query
    elif api_key_header == API_KEY:
        return api_key_header
    elif api_key_cookie == API_KEY:
        return api_key_cookie
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )


app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)


models.Base.metadata.create_all(bind=engine)

#app = FastAPI()

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


@app.post("/register", response_model=schemas.User)
def sign_up(user: schemas.UserCreate, db: session.Session = Depends(get_db)):

    return crud.create_user(db=db, users=user)


@app.post("/login")
async def login( db: session.Session = Depends(get_db), form_data : OAuth2PasswordRequestForm = Depends()):
    name = form_data.username
    password = form_data.password

    if crud.get_user_by_name(db = db, name=name) is None:
        raise HTTPException(status_code=401, detail="Username not found")

    if crud.verify_password(db=db, password=password) is None:
        raise HTTPException(status_code=401, detail="Error password")

    return {"OK":"You are logined with succes"}

@app.get("/logout")
async def route_logout_and_remove_cookie():
    response = RedirectResponse(url="/")
    response.delete_cookie(API_KEY_NAME, domain=COOKIE_DOMAIN)
    return response



@app.get("/")
async def homepage():
    return "Welcome to the security test!"



#Items

@app.get("/items/all",tags=["Items"], response_model=List[schemas.Items])
def list_items(db:session = Depends(get_db),api_key: APIKey = Depends(get_api_key), token:str = Depends(oauth2_scheme)):

    return crud.get_items(db=db)

@app.post("/items/create",tags=["Items"], response_model=schemas.Items)
def create_ietem(item: schemas.ItemCreate, db: session.Session = Depends(get_db),token:str = Depends(oauth2_scheme)):

    return crud.create_item(db=db, item=item)

@app.put("/items/update/{id}/",tags=["Items"], response_model=schemas.Items)
def update_item(item: schemas.ItemUpdate, id: int = id, db: session.Session = Depends(get_db), token:str = Depends(oauth2_scheme)):

    item = crud.find_item(db=db, id=id)
    if item is None:
        raise HTTPException(status_code=404, detail="You can't update the item becouse he doesn't exist")
    
    return crud.update_item(db=db, item=item, id=id)

@app.delete("/items/delete/{id}",tags=["Items"])
def delete_item(id:int=id, db: session.Session = Depends(get_db), token:str = Depends(oauth2_scheme)):

    item = crud.find_item(db=db, id=id)
    if item is None:
        raise HTTPException(status_code=404, detail="You can't delete the item becouse he doesn't exist")
    
    crud.delete_item(db=db, id=id)

    return {"Message":"Item deleted succefully !"}

@app.get("/items/find/{id}", tags=["Items"])
def get_by_id(id:int = id, db: session.Session = Depends(get_db), token:str = Depends(oauth2_scheme)):

    item = crud.find_item(db=db, id=id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item doesn't exist")

    return item


#Shops

@app.get("/shops/all",tags=["Shops"], response_model=List[schemas.Shop])
def list_shps(db:session = Depends(get_db), token:str = Depends(oauth2_scheme)):

    return crud.get_shops(db=db)

@app.post("/shops/create",tags=["Shops"], response_model=schemas.Shop)
def create_shop(shop: schemas.ShopCreate, db: session.Session = Depends(get_db),token:str = Depends(oauth2_scheme)):

    return crud.create_shop(db=db, shops=shop)

@app.post("/shop/{trade_id}/",tags=["Shops"], response_model=schemas.Shop)
def create_shop_for_trad(trade_id: int, item: schemas.ShopCreate, db: session.Session = Depends(get_db), token:str = Depends(oauth2_scheme)):

    return crud.create_shop_trad(db=db, item=item, trade_id=trade_id)

@app.put("/shops/update/{id}/",tags=["Shops"], response_model=schemas.Shop)
def update_shop(shop: schemas.ShopUpdate, id: int = id, db: session.Session = Depends(get_db), token:str = Depends(oauth2_scheme)):

    shop = crud.find_shop(db=db, id=id)
    if shop is None:
        raise HTTPException(status_code=404, detail="You can't update the shop becouse he does't exist")

    return crud.update_shop(db=db, shop=shop, id=id)

@app.delete("/shops/delete/{id}",tags=["Shops"])
def delete_shop(id:int=id, db: session.Session = Depends(get_db), token:str = Depends(oauth2_scheme)):

    shop = crud.find_shop(db=db, id=id)
    if shop is None:
        raise HTTPException(status_code=404, detail="You can't delete the shop becouse he does't exist")
    crud.delete_shop(db=db, id=id)

    return {"Message":"shope deleted succefully !"}

@app.get("/shops/find/{id}",tags=["Shops"])
def get_by_id(id:int = id, db: session.Session = Depends(get_db), token:str = Depends(oauth2_scheme)):

    shop = crud.find_shop(db=db, id=id)
    if shop is None:
        raise HTTPException(status_code=404, detail="Shop does't exist")

    return shop


#Trads

@app.get("/trads/all",tags=["Trads"], response_model=List[schemas.Trade])
def list_trads(db:session = Depends(get_db), token:str = Depends(oauth2_scheme)):

    return crud.get_trads(db=db)

@app.post("/trads/create", response_model=schemas.Trade)
def create_trade(trade: schemas.TradeCreate, db: session.Session = Depends(get_db),token:str = Depends(oauth2_scheme)):

    return crud.create_trade(db=db, trades=trade)

@app.put("/trads/update/{id}/",tags=["Trads"], response_model=schemas.Trade)
def update_trade(trade: schemas.TradeUpdate, id: int = id, db: session.Session = Depends(get_db), token:str = Depends(oauth2_scheme)):

    trade = crud.find_trade(db=db, id=id)
    if trade is None:
        raise HTTPException(status_code=404, detail="You can't update the trade becouse he  does't exist")

    return crud.update_trade(db=db, trade=trade, id=id)

@app.delete("/trads/delete/{id}",tags=["Trads"])
def delete_trade(id:int=id, db: session.Session = Depends(get_db), token:str = Depends(oauth2_scheme)):

    trade = crud.find_trade(db=db, id=id)
    if trade is None:
        raise HTTPException(status_code=404, detail="You can't delete the trade becouse he  does't exist")
    crud.delete_trade(db=db, id=id)

    return {"Message":"trade deleted succefully !"}

@app.get("/trads/find/{id}",tags=["Trads"])
def get_by_id(id:int = id, db: session.Session = Depends(get_db), token:str = Depends(oauth2_scheme)):

    trade = crud.find_trade(db=db, id=id)
    if trade is None:
        raise HTTPException(status_code=404, detail="Trade does't exist")

    return trade

@app.get("/trads/shops_in_trade/{id}",tags=["Trads"])
def get_by_id(id:int = id, db: session.Session = Depends(get_db), token:str = Depends(oauth2_scheme)):

    trade = crud.find_trade(db=db, id=id)
    if trade is None:
        raise HTTPException(status_code=404, detail="Trade does't exist so he can't have any shopers")

    return crud.get_shops_of_trads(db=db, id=id)



#Router documentation

@app.get("/openapi.json", tags=["documentation"])
async def get_open_api_endpoint(api_key: APIKey = Depends(get_api_key)):
    response = JSONResponse(
        get_openapi(title="FastAPI security test", version=1, routes=app.routes)
    )
    return response

@app.get("/documentation", tags=["documentation"])
async def get_documentation(api_key: APIKey = Depends(get_api_key)):
    response = get_swagger_ui_html(openapi_url="/openapi.json", title="docs")
    response.set_cookie(
        API_KEY_NAME,
        value=api_key,
        domain=COOKIE_DOMAIN,
        httponly=True,
        max_age=1800,
        expires=1800,
    )
    return response

@app.get("/secure_endpoint", tags=["test"])
async def get_open_api_endpoint(api_key: APIKey = Depends(get_api_key)):
    response = "How cool is this?"
    return response