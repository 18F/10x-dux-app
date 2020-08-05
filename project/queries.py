from . import db
from .models import PublicItem, SensitiveItem

def get_public_items(grouping=None):
    if  grouping:
        return PublicItem.query().grouping(grouping).all()
        
    return PublicItem.query.all()

def get_public_items_groupings():
    model = PublicItem
    return [m.key for m in model.__table__.columns]

def get_sensitve_items(grouping=None):
    if  grouping:
        return SensitiveItem.query().grouping(grouping).all()

    return SensitiveItem.query.all()

def get_sensitive_items_groupings():
    model = SensitiveItem
    return [m.key for m in model.__table__.columns]