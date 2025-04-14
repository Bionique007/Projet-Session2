from app.extensions import db

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    nom_utilisateur = db.Column(db.String(100), nullable=False)
    titre_evenement = db.Column(db.String(120), nullable=False)
    date_evenement = db.Column(db.String(50), nullable=False)
    statut = db.Column(db.String(50), default='Actif')  # Nouveau champ

    user = db.relationship('User', backref=db.backref('reservations', lazy=True))