from .models import PublicItem, SensitiveItem, User
from .persistence import db

def generate_public_items(ctx):
    try:
        with ctx:
            for n in range(25):
                db.session.add(
                    PublicItem(
                        key=f"PublicKey{n}",
                        value=f"PublicValue{n}"
                    )
                )
            db.session.commit()

    except Exception as err:
        return False

    return True

def generate_sensitive_items(ctx):
    try:
        with ctx:
            for n in range(25):
                db.session.add(
                    SensitiveItem(
                        key=f"SensitiveKey{n}",
                        value=f"SensitiveValue{n}"
                    )
                )
            db.session.commit()

    except Exception as err:
        return False

    return True

def add_user(email, name, password):
    db.session.add(
        User(email=email,
            name=name,
            password=password
        )
    )

    db.session.commit()