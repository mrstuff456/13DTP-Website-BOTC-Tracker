import os
from flask import Flask, session, render_template, url_for, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session
from sqlalchemy import String, Integer, ForeignKey, Table, Column, select, create_engine, insert
from authlib.integrations.flask_client import OAuth


# init apps
app = Flask(__name__)
app.secret_key = 'a091e1b6b9a25a1e60fab1e0b57aae48febd2a1ffeb250a0dc7169d064f67586d'


# init Oauth
oauth = OAuth(app)
google = oauth.register(
    name="google",
    client_id="45222915885-ildth7lsb5vajdskmkd3r4hr6tglbk6k.apps.googleusercontent.com",
    client_secret="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",
    server_metadata_url="https://accounts.google.com/.well-known/oauth-authorization-server",
    client_kwargs={"scope": "openid email profile"},
)

# SQLAlchemy Database Model
class Base(DeclarativeBase):
    pass


ScriptCharacter = Table(
    "ScriptCharacter",
    Base.metadata,
    Column("ScriptID", ForeignKey("Script.ID"), primary_key=True),
    Column("CharacterID", ForeignKey("Character.ID"), primary_key=True),
)


SeatReminder = Table(
    "SeatReminder",
    Base.metadata,
    Column("SeatID", ForeignKey("Seat.ID"), primary_key=True),
    Column("ReminderID", ForeignKey("Reminder.ID"), primary_key=True),
)


class User(Base):
    __tablename__ = "User"
    ID: Mapped[str] = mapped_column(String(255), primary_key=True)
    Name: Mapped[str] = mapped_column(String(30))
    Game: Mapped[list["Game"]] = relationship(back_populates="User")


class Script(Base):
    __tablename__ = "Script"
    ID: Mapped[int] = mapped_column(primary_key=True)
    Name: Mapped[str] = mapped_column(String(30))
    Author: Mapped[str] = mapped_column(String(30))

    Game: Mapped[list["Game"]] = relationship(back_populates="Script")
    Character: Mapped[list["Character"]] = relationship(
        secondary=ScriptCharacter, back_populates="Script"
    )


class Game(Base):
    __tablename__ = "Game"
    ID: Mapped[int] = mapped_column(primary_key=True)
    UserID: Mapped[int] = mapped_column(ForeignKey("User.ID"))
    ScriptID: Mapped[int] = mapped_column(ForeignKey("Script.ID"))

    Seat: Mapped[list["Seat"]] = relationship(back_populates="Game")
    User: Mapped["User"] = relationship(back_populates="Game")
    Script: Mapped["Script"] = relationship(back_populates="Game")


class Character(Base):
    __tablename__ = "Character"
    ID: Mapped[int] = mapped_column(primary_key=True)
    NamedID: Mapped[str] = mapped_column(String(30))
    Name: Mapped[str] = mapped_column(String(30))
    Type: Mapped[str] = mapped_column(String(30))
    Ability: Mapped[str] = mapped_column(String(300))
    Flavour: Mapped[str] = mapped_column(String(300))
    Icon: Mapped[str] = mapped_column(String(300))
    Wiki: Mapped[str] = mapped_column(String(300))


    Reminder: Mapped[list["Reminder"]] = relationship(back_populates="Character")
    Seat: Mapped[list["Seat"]] = relationship(back_populates="Character")
    Script: Mapped[list["Script"]] = relationship(
        secondary=ScriptCharacter, back_populates="Character"
    )


class Reminder(Base):
    __tablename__ = "Reminder"
    ID: Mapped[int] = mapped_column(primary_key=True)
    CharacterID: Mapped[int] = mapped_column(ForeignKey("Character.ID"))
    ReminderText: Mapped[str] = mapped_column(String(80))

    Character: Mapped["Character"] = relationship(back_populates="Reminder")
    Seat: Mapped[list["Seat"]] = relationship(
        secondary=SeatReminder, back_populates="Reminder"
    )


class Seat(Base):
    __tablename__ = "Seat"
    ID: Mapped[int] = mapped_column(primary_key=True)
    InternalID: Mapped[str] = mapped_column(String(30))
    GameID: Mapped[int] = mapped_column(ForeignKey("Game.ID"))
    SeatName: Mapped[str] = mapped_column(String(30))
    SeatRole: Mapped[int] = mapped_column(ForeignKey("Character.ID"))
    SeatNotes: Mapped[str] = mapped_column(String(2000))

    Game: Mapped["Game"] = relationship(back_populates="Seat")
    Character: Mapped["Character"] = relationship(back_populates="Seat")
    Reminder: Mapped[list["Reminder"]] = relationship(
        secondary=SeatReminder, back_populates="Seat"
    )


# init db
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)
engine = create_engine("sqlite:///database.db")
Base.metadata.create_all(engine)


# ROUTES
# login page
@app.route("/login")
def login():
    redirect_uri = url_for("authorize", _external=True)
    return google.authorize_redirect(redirect_uri)


# login authorize
@app.route("/login/authorize")
def authorize():
    # obtain user's data
    token = google.authorize_access_token()
    user_info = token.get("userinfo")
    if user_info:
        session["user"] = user_info
    user = dict(session.get("user"))
    userid = user.get("sub")
    name = user.get("name")

    # if the user doesnt exist in the database, add it
    userexists = db.session.scalar(select(User).where(User.ID == userid))
    if userexists == None:
        db.session.add(User(ID=userid, Name=name))
        db.session.commit()
    
    # redirect user to home
    return redirect("/")


# logout
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")


# routes
@app.route('/')
def home():
    #check if the user is logged in, if so send them to the logged in version of the home page
    if session:
        # gain the users data to display on the page
        user = dict(session.get("user"))
        userid = user.get('sub')

        # gain data on any games the user has created
        games = db.session.execute(select(Game).where(Game.UserID == userid)).scalars()
        characters = db.session.execute(select(Character)).scalars()

        # render page
        return render_template('home_logged_in.html', user=user, games=games, characters=characters)
    # else send the user to the non-logged in version of the home page
    else:
        return render_template('home.html')


@app.route('/game')
def game():
    return render_template('game.html')


# run the program
if __name__ == "__main__":
    app.run(debug=True)
