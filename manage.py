import os
from app import create_app, db
from app.models import User, RSSChanel, Theme
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand


app = create_app(os.environ.get('RSSREADER_CONFIG') or 'heroku')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User, RSSChanel=RSSChanel, Theme=Theme)


manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def deploy():
    from flask_migrate import upgrade
    from app.models import RSSChanel

    # upgrade db
    upgrade()

    # insert chanels
    RSSChanel.add_chanels()


if __name__ == '__main__':
    manager.run()
