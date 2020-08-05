from .models import PublicItem, SensitiveItem

def get_public_items():
    return PublicItem.query.all()

def get_sensitve_items():
    return SensitiveItem.query.all()    