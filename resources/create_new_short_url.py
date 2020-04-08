from flask_restful import Resource, reqparse
import re

from models.short_url import ShortUrlModel


class CreateNewShortUrl(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("url", type=str, required=True, help="url cannot be empty")

    def post(self):
        data = CreateNewShortUrl.parser.parse_args()
        submitted_url = data["url"]

        already_exists = ShortUrlModel.find_by_original_url(submitted_url)
        if already_exists:
            return already_exists.json()

        valid_url = re.search(
            "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",
            submitted_url,
        )
        if not valid_url:
            return {"error": "invalid URL"}

        new_short_url = ShortUrlModel(submitted_url)
        new_short_url.save_to_db()
        return new_short_url.json(), 201
