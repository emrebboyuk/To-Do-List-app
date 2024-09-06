import click
from flask.cli import with_appcontext
from app.modules.cli.utils import create_admin


@click.command("create-admin")
@with_appcontext
def create_admin_command():
    username = click.prompt("Please enter the admin's username")
    email = click.prompt("Please enter the admin's email")
    password = click.prompt(
        "Please enter the admin's password", hide_input=False, confirmation_prompt=True
    )

    try:
        new_admin = create_admin(username, email, password)
        print(f"Admin {new_admin.username} created successfully.")
    except ValueError as e:
        print(f"Error: {e}")
