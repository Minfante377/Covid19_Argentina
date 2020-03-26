import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import app

APP_SETTINGS="config.DevelopmentConfig"
app.config.from_object(APP_SETTINGS)
manager = Manager(app)

if __name__ == '__main__':
    manager.run()

