from app import create_app
from app.models.user import User, db
from app.models.reservation import Reservation
from app.models.events import Event

app = create_app()

with app.app_context():
    db.create_all()
    print("Base de données Bionics Events.")