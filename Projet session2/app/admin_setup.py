from app.models.user import User
from app.extensions import db, bcrypt

def create_admin_user():
    email = "admin@example.com"  # Admin email
    password_clair = "admin_password"  # Admin password
    
    # Hash the password
    hashed_password = bcrypt.generate_password_hash(password_clair).decode('utf-8')
    
    # Create the admin user
    admin_user = User(nom="Admin", email=email, password=hashed_password, is_admin=True)
    db.session.add(admin_user)
    db.session.commit()
    print(f"Admin user '{admin_user.nom}' created successfully!")

if __name__ == "__main__":
    from app import create_app

    app = create_app()
    with app.app_context():
        create_admin_user()