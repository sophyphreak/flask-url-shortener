from flask import Flask, request, redirect
from flask_restful import Api, Resource, reqparse
from db import db
import re
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///pop-lockers')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)

db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

class ShortUrlModel(db.Model):
    __tablename__ = 'shorturls'
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(80))

    def __init__(self, original_url):
        self.original_url = original_url

    def json(self):
        return {
            'id': self.id,
            'original_url': self.original_url
        }

    @classmethod
    def find_by_original_url(cls, original_url):
        # SELECT * FROM items WHERE name=name LIMIT 1
        return cls.query.filter_by(original_url=original_url).first()

    @classmethod
    def find_by_id(cls, id):
        # SELECT * FROM items WHERE name=name LIMIT 1
        return cls.query.filter_by(id=id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


class CreateNewShortUrl(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('URL',
        type=str,
        required=True,
        help="URL cannot be empty"
    )

    def post(self):
        data = CreateNewShortUrl.parser.parse_args()
        submitted_url = data['URL'] 

        already_exists = ShortUrlModel.find_by_original_url(submitted_url)
        if already_exists:
            return already_exists.json()

        valid_url = re.search(
            'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
            submitted_url
        )
        if not valid_url:
            return {"error": "invalid URL"}

        new_short_url = ShortUrlModel(submitted_url)
        new_short_url.save_to_db()
        return new_short_url.json(), 201

class GoToUrl(Resource):
    def get(self, url_id):
        target_url = ShortUrlModel.find_by_id(url_id).original_url
        return redirect(target_url, code=302)

api.add_resource(CreateNewShortUrl, '/api/shorturl/new')
api.add_resource(GoToUrl, '/api/shorturl/<url_id>')

if __name__ == '__main__':
    app.run(debug=True)