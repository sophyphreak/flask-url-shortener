from flask import redirect
from flask_restful import Resource

from models.short_url import ShortUrlModel


class GoToUrl(Resource):
    def get(self, url_id):
        target_url = ShortUrlModel.find_by_id(url_id).original_url
        return redirect(target_url, code=302)
