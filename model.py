

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


##############################################################################
# Model definitions


class Character(db.Model):
    """Character."""

    __tablename__ = "characters"

    char_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    char_name = db.Column(db.String(100), nullable=False, unique=True)
    char_male = db.Column(db.Boolean)
    char_house = db.Column(db.String(100))
    char_alive = db.Column(db.Boolean)

    def __repr__(self):
        return "<Char_id id=%d name=%s male=%s house=%s alive=%s>" % (self.char_id,
                                                                      self.char_name,
                                                                      self.male,
                                                                      self.house,
                                                                      self.alive)


class Title(db.Model):
    """Character titles."""

    __tablename__ = "titles"

    title_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title_name = db.Column(db.String(200))

    def __repr__(self):
        return "<Title_id=%d char_name=%s char_title=%s>" % (self.title_id,
                                                             self.char_title)


class Episode(db.Model):
    """Episodes."""

    __tablename__ = "episodes"

    ep_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    ep_season = db.Column(db.Integer)
    ep_name = db.Column(db.String(100))

    def __repr__(self):
        return "<Episode_id=%d ep_season=%d ep_name=%s>" % (self.ep_id,
                                                            self.ep_season,
                                                            self.ep_name)


class TitleChar(db.Model):
    """Titles and Characters."""

    __tablename__ = "titles_char"

    title_char_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    char_id = db.Column(db.Integer, db.ForeignKey('characters.char_id'))
    title_id = db.Column(db.Integer, db.ForeignKey('titles.title_id'))

    title = db.relationship("Title", backref=db.backref("titles"))
    char = db.relationship("Character", backref=db.backref("characters"))

    def __repr__(self):
        return "<Title_id=%d char_id=%d title_id=%d>" % (self.title_char_id,
                                                         self.char_id,
                                                         self.title_id)


class EpChar(db.Model):
    """Episodes and Characters."""

    __tablename__ = "episodes_char"

    ep_char_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    char_id = db.Column(db.Integer, db.ForeignKey('characters.char_id'))
    ep_id = db.Column(db.Integer, db.ForeignKey('episodes.ep_id'))

    ep = db.relationship("Episode", backref=db.backref("episodes"))
    char = db.relationship("Character", backref=db.backref("characters"))

    def __repr__(self):
        return "<Epchar_id=%d char_id=%s ep_id=%s>" % (self.ep_char_id,
                                                       self.char_id,
                                                       self.ep_id)




##############################################################################
# Helper functions


def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our Postgres database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///characters'
    app.config['SQLALCHEMY_ECHO'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    # So that we can use Flask-SQLAlchemy, we'll make a Flask app
    from flask import Flask

    app = Flask(__name__)

    connect_to_db(app)
    print "Connected to DB."

    db.create_all()
