# manage.py

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import db, create_app

# initialize app with environment=development
app = create_app(config_name = "development")
migrate = Migrate(app, db)
# an instance of Manager class that handles commands
manager = Manager(app)

# Define migration command to be preceeded by the word "db"
# e.g python manage.py db init
manager.add_command("db", MigrateCommand)

if __name__=="__main__":
    manager.run()
