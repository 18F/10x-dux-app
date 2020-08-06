from .models import PublicItem, SensitiveItem, User
from .persistence import db

def get_user(user_id):
    if not user_id:
        return None

    if not isinstance(user_id, int):
        return None

    result = db.session().query(User).get(user_id)
    print(result)
    return result

def filter_by_user(email):
    if not email:
        return None

    result = db.session().query(User).filter_by(email=email).first()
    print(result)
    return result

def get_public_items(order=None):
    if  order:
        return db.session().query(PublicItem).order_by(order).all()
        
    return db.session().query(PublicItem).all()

def get_public_items_orders():
    model = PublicItem
    return [m.key for m in model.__table__.columns]

def get_sensitve_items(order=None):
    if  order:
        return db.session().query(SensitiveItem).order_by(order).all()

    return db.session().query(SensitiveItem).all()

def get_sensitive_items_orders():
    model = SensitiveItem
    return [m.key for m in model.__table__.columns]