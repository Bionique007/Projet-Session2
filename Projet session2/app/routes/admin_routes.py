from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from functools import wraps
from app.extensions import db, bcrypt
from app.models.reservation import Reservation
from app.models.user import User
from app.models.events import Event
from datetime import datetime

admin = Blueprint('admin', __name__, url_prefix='/admin')

# Define the admin_required decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('is_admin'):  # Check if the user is logged in as admin
            flash('Vous devez être administrateur pour accéder à cette page.', 'danger')
            return redirect(url_for('admin.admin_login'))
        return f(*args, **kwargs)
    return decorated_function

@admin.route('/', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Verify credentials in the database
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password) and user.is_admin:
            # Store user ID and admin flag in session
            session['user_id'] = user.id
            session['is_admin'] = True
            flash('Connexion réussie !', 'success')
            return redirect(url_for('admin.admin_dashboard'))
        else:
            flash('Email ou mot de passe invalide.', 'danger')
    return render_template('admin_login.html')

@admin.route('/logout')
def admin_logout():
    session.pop('user_id', None)
    session.pop('is_admin', None)
    flash('Vous êtes déconnecté.', 'info')
    return redirect(url_for('admin.admin_login'))

@admin.route('/dashboard')
@admin_required
def admin_dashboard():
    users = User.query.all()
    return render_template('admin_dashboard.html', users=users)

@admin.route('/add_event', methods=['GET', 'POST'])
@admin_required
def add_event():

    if request.method == 'POST':
        # Retrieve form data
        titre = request.form['titre']
        cost = request.form['cost']
        description = request.form.get('description', '')

        # Convert date string to `datetime.date`
        date = datetime.strptime(request.form['date'], '%Y-%m-%d').date()

        # Create and save the new event
        new_event = Event(
            nom=titre,
            date=date,
            cost=cost,
        )
        db.session.add(new_event)
        db.session.commit()

        flash("Événement ajouté avec succès !", "success")
        return redirect(url_for('admin.admin_events'))

    return render_template('admin_add_event.html')

@admin.route('/edit_event/<int:event_id>', methods=['GET', 'POST'])
@admin_required
def edit_event(event_id):

    # Fetch the event by ID
    event = Event.query.get(event_id)
    if not event:
        flash("Événement introuvable.", "danger")
        return redirect(url_for('admin.admin_events'))

    if request.method == 'POST':
        # Update event data
        event.nom = request.form['nom']
        event.date = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
        event.cost = request.form['cost']

        # Commit changes to the database
        db.session.commit()

        flash("Événement modifié avec succès !", "success")
        return redirect(url_for('admin.admin_events'))

    # Render the edit form with the existing event details
    return render_template('admin_edit_event.html', event=event)

@admin.route('/delete_event/<int:event_id>', methods=['POST'])
@admin_required
def delete_event_admin(event_id):

    event = Event.query.get(event_id)
    if not event:
        flash("Événement introuvable.", "danger")
        return redirect(url_for('admin.admin_events'))

    # Mettre à jour les réservations associées
    reservations = Reservation.query.filter_by(titre_evenement=event.nom).all()
    for reservation in reservations:
        reservation.statut = 'Annulé'  # Met à jour le statut
    db.session.commit()

    # Supprimer l'événement
    db.session.delete(event)
    db.session.commit()

    flash("Événement supprimé avec succès. Les réservations associées ont été marquées comme 'Annulé'.", "success")
    return redirect(url_for('admin.admin_events'))

@admin.route('/reservations')
@admin_required
def manage_reservations():
    reservations = Reservation.query.all()
    return render_template('admin_manage_reservations.html', reservations=reservations)

@admin.route('/user/<int:user_id>/reservations')
@admin_required
def user_reservations(user_id):
    user = User.query.get_or_404(user_id)
    reservations = Reservation.query.filter_by(user_id=user.id).all()
    return render_template('admin_user_reservations.html', user=user, reservations=reservations)

@admin.route('/events')
@admin_required
def admin_events():
    from app.models.events import Event
    events = Event.query.all()
    return render_template('admin_events.html', events=events)

@admin.route('/delete_reservation/<int:reservation_id>', methods=['POST'])
@admin_required  # Assure que seul un admin peut accéder à cette route
def delete_reservation_admin(reservation_id):

    # Récupérer la réservation spécifique par son ID
    reservation = Reservation.query.get(reservation_id)

    if not reservation:
        flash("Réservation introuvable.", "danger")
        return redirect(request.referrer)  # Retourne à la page précédente

    # Supprimer la réservation
    db.session.delete(reservation)
    db.session.commit()
    flash("La réservation a été supprimée avec succès.", "success")

    # Retourner à la page actuelle (au lieu de manage_reservations)
    return redirect(request.referrer)