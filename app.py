from flask import Flask
from flask_restful import Api
from db import db
import re
import os

from resources.create_new_short_url import CreateNewShortUrl
from resources.go_to_url import GoToUrl

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///url-shortener')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)

db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

api.add_resource(CreateNewShortUrl, '/api/shorturl/new')
api.add_resource(GoToUrl, '/api/shorturl/<url_id>')

if __name__ == '__main__':
    app.run(port=5000)