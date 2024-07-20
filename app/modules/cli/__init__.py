from flask import Flask

from app.modules.cli.commands import create_admin_command


def init_cli(app: Flask):
    app.cli.add_command(create_admin_command)
