from flask.cli import with_appcontext, AppGroup
import click
from faker import Faker
faker = Faker('ja_JP')
from flaskr import db
from flaskr.models.user import User
from flaskr.models.blog import Blog

database_cli = AppGroup('database')

@database_cli.command("setup")
@click.option('--without-seed', is_flag=True, help='Without seed')
@click.option('--users-count', default=100, help='Number of users')
@click.option('--blogs-per-user', default=10, help='Number of blogs per user')
@with_appcontext
def database_setup(without_seed=False, users_count=100, blogs_per_user=10):
    """Drop all tables and create new tables. If without-seed is not set, seed database with fake data."""
    click.echo('Dropping all tables...')
    db.drop_all()
    click.echo('Creating all tables...')
    db.create_all()
    if not without_seed:
        click.echo('Seeding database...')
        ctx = click.get_current_context()
        ctx.invoke(database_seed, users_count=users_count, blogs_per_user=blogs_per_user)
    click.echo('Setting up database completed.')

@database_cli.command("seed")
@click.option('--users-count', default=100, help='Number of users')
@click.option('--blogs-per-user', default=10, help='Number of blogs per user')
@with_appcontext
def database_seed(users_count=100, blogs_per_user=10):
    """Seed database with fake data."""
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
    click.echo('Seeding database completed.')

generated_emails = set()
def generate_unique_email():
    while True:
        email = faker.email()
        if email not in generated_emails:
            generated_emails.add(email)
            return email


@database_cli.command("reset")
@with_appcontext
def database_reset():
    """Drop all tables and create new tables."""
    click.echo('Dropping all tables...')
    db.drop_all()
    click.echo('Creating all tables...')
    db.create_all()
    click.echo('Resetting database completed.')