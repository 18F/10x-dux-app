from . import db
from .models import PublicItem, SensitiveItem

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