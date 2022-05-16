from app import  create_app
from flask_script import Manager, Server
from app import db
from app.models import Users,Posts,Comments, Likes,Dislikes
from flask_migrate import Migrate,MigrateCommand
# app instances
app = create_app('development')
# app = create_app('development_mode')

manager = Manager(app)
manager.add_command('server', Server)

# initialize migrate class that has been imported
migrate = Migrate(app,db)
manager.add_command('db',MigrateCommand)
@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

@manager.shell
def make_shell_context():
    return dict(app =app,db=db,Users=Users,Posts=Posts,Comments =Comments,Likes=Likes,Dislikes = Dislikes)

if __name__ == '__main__':
    # app.run()
    manager.run()