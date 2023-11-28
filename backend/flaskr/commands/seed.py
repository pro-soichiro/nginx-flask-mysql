from faker import Faker
faker = Faker('ja_JP')

from flaskr import db
from flaskr.models.user import User
from flaskr.models.blog import Blog
from flask.cli import with_appcontext
import click

@click.command("seed")
@with_appcontext
def seed():
    create_dummy_data()

def create_dummy_data(users_count=100, blogs_per_user=10):
    for _ in range(users_count):
        user = User(name=faker.name(),
                    email=generate_unique_email(),
                    is_active=True,
                    birthday=faker.date_of_birth())
        db.session.add(user)
        db.session.commit()

        for _ in range(blogs_per_user):
            blog = Blog(title=faker.sentence(),
                        body=faker.text(),
                        user_id=user.id)
            db.session.add(blog)
    db.session.commit()

generated_emails = set()

def generate_unique_email():
    while True:
        email = faker.email()
        if email not in generated_emails:
            generated_emails.add(email)
            return email