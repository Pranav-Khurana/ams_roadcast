import os
from app import app, db
from models import User
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash


def add_initial_manager():
    static_images_dir = os.path.join(app.root_path, 'static', 'images')
    os.makedirs(static_images_dir, exist_ok=True)

    with app.app_context():
        db.create_all()

        manager = User.query.filter_by(role='Manager').first()

        if manager:
            print('Manager user already exists.')
            return

        username = input('Enter main manager username: ')
        firstname = input('Enter First Name: ')
        lastname = input('Enter Last Name: ')
        password = input('Enter main manager password: ')

        hashed_password = generate_password_hash(password)

        new_manager = User(username=username, fname=firstname, lname=lastname, password=hashed_password, role='Manager')

        try:
            db.session.add(new_manager)
            db.session.commit()
            print('Manager user added successfully.')
        except IntegrityError:
            db.session.rollback()
            print('Error: Username already exists.')

if __name__ == '__main__':
    add_initial_manager()
