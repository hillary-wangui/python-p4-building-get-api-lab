from server import db, create_app
from models import Bakery

app = create_app()
db.app = app
db.init_app(app)

def seed():
    bakery1 = Bakery(name='Sweet Treats Bakery', location='123 Main St')
    bakery2 = Bakery(name='Bread and Butter Bakery', location='456 Elm St')

    db.session.add(bakery1)
    db.session.add(bakery2)

    db.session.commit()

if __name__ == '__main__':
    seed()