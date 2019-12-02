import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import config
from dotenv import load_dotenv
load_dotenv()

# creating app
app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# registering blueprints
from views.authentication import authentication_bp
app.register_blueprint(authentication_bp)


# Home route
@app.route('/')
def hello():
    return "hello"

# Main
if __name__ == '__main__':
    app.run()