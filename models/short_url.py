from db import db


class ShortUrlModel(db.Model):
    __tablename__ = "short_urls"
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(80))

    def __init__(self, original_url):
        self.original_url = original_url

    def json(self):
        return {"id": self.id, "original_url": self.original_url}

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
