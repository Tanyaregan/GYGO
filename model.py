
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

##############################################################################
# Model Definitions


class Character(db.Model):
    """Character."""

    __tablename__ = "characters"

    char_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    char_name = db.Column(db.String(100), nullable=False, unique=True)
    char_male = db.Column(db.Boolean)
    char_dead = db.Column(db.String(50))

    r_title = db.relationship("Title", backref="titles", secondary="char_titles")
    r_episode = db.relationship("Episode", backref="episodes", secondary="char_eps")
    r_house = db.relationship("House", backref="houses", secondary="char_houses")

    def __repr__(self):
        return "<char_id=%d name=%s male=%s dead=%s>" % (self.char_id,
                                                         self.char_name,
                                                         self.char_male,
                                                         self.char_dead)


class Title(db.Model):
    """Character titles."""

    __tablename__ = "titles"

    title_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title_name = db.Column(db.String(200))

    def __repr__(self):
        return "<title_id=%d title_name=%s>" % (self.title_id,
                                                self.title_name)


class Episode(db.Model):
    """Episodes."""

    __tablename__ = "episodes"

    ep_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    ep_season = db.Column(db.Integer)
    ep_name = db.Column(db.String(100))

    def __repr__(self):
        return "<episode_id=%d ep_season=%d ep_name=%s>" % (self.ep_id,
                                                            self.ep_season,
                                                            self.ep_name)


class House(db.Model):
    """Houses"""

    __tablename__ = "houses"

    house_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    house_name = db.Column(db.String(200))

    def __repr__(self):
        return "<house_id=%d house_name=%s>" % (self.house_id,
                                                self.house_name)


class CharTitle(db.Model):
    """Titles and Characters."""

    __tablename__ = "char_titles"

    chartitle_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    char_id = db.Column(db.Integer, db.ForeignKey('characters.char_id'))
    title_id = db.Column(db.Integer, db.ForeignKey('titles.title_id'))

    def __repr__(self):
        return "<chartitle_id=%d char_id=%d title_id=%d>" % (self.chartitle_id,
                                                             self.char_id,
                                                             self.title_id)


class CharEp(db.Model):
    """Episodes and Characters."""

    __tablename__ = "char_eps"

    charep_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    char_id = db.Column(db.Integer, db.ForeignKey('characters.char_id'))
    ep_id = db.Column(db.Integer, db.ForeignKey('episodes.ep_id'))

    def __repr__(self):
        return "<charep_id=%d char_id=%s ep_id=%s>" % (self.charep_id,
                                                       self.char_id,
                                                       self.ep_id)


class CharHouse(db.Model):
    """Houses and Characters"""

    __tablename__ = "char_houses"

    charhouse_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    char_id = db.Column(db.Integer, db.ForeignKey('characters.char_id'))
    house_id = db.Column(db.Integer, db.ForeignKey('houses.house_id'))

    def __repr__(self):
        return "<charhouse_id=%d char_id=%s house_id=%s>" % (self.charhouse_id,
                                                       self.char_id,
                                                       self.house_id)

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

    from flask import Flask

    app = Flask(__name__)

    connect_to_db(app)
    print "Connected to DB."

    db.create_all()
