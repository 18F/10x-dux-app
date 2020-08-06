from .models import PublicItem, SensitiveItem
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
            print("Done!")
    except Exception as err:
        print(err)
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
            print("Done!")

    except Exception as err:
        print(err)
        return False

    return True