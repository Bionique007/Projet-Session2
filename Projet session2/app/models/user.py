from app.extensions import db, bcrypt

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)  # New attribute to flag admin users

    def set_password(self, mot_de_passe_clair):
        self.password = bcrypt.generate_password_hash(mot_de_passe_clair).decode('utf-8')

    def check_password(self, mot_de_passe):
        return bcrypt.check_password_hash(self.password, mot_de_passe)
