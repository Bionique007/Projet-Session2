from app.extensions import db

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    cost = db.Column(db.Integer, nullable=False)  # Ajoute le coût dans le modèle