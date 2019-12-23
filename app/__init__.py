from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os
from flask_mail import Mail
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
mail = Mail(app)
bootstrap = Bootstrap(app)

from app import routes, models, errors



# The following is a handler to deal with any errors that the logger encounters.
# The handler is a SMTPHandler (i.e. a handler which will deal with emails).
# The handler is configured to send emails based on the mail server configured
# in the environment variables (this could be a gmail email server for example).
# if not app.debug:
#     if app.config['MAIL_SERVER']:
#
#         # set up error logs to email
#         auth = None
#         if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
#             auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
#
#         secure = None
#         if app.config['MAIL_USE_TLS']:
#             secure = ()
#
#         mail_handler = SMTPHandler(
#             mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
#             fromaddr='no-reply@' + app.config['MAIL_SERVER'] + '.com',
#             toaddrs=app.config['ADMINS'],
#             subject='Microblogx Failure',
#             credentials=auth,
#             secure=secure
#         )
#
#         mail_handler.setLevel(logging.ERROR)
#         app.logger.addHandler(mail_handler)

#
#         # set up error logs to file
#         if not os.path.exists('logs'):
#             os.mkdir('logs')
#         file_handler = RotatingFileHandler(
#             'logs/microblogx.log',
#             maxBytes=10240,
#             backupCount=10
#         )
#         file_handler.setFormatter(logging.Formatter(
#             '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
#         ))
#         file_handler.setLevel(logging.INFO)
#         app.logger.addHandler(file_handler)
