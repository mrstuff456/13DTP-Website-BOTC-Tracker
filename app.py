from flask import Flask, session, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey, Table, Column, select
from flask_login import LoginManager


# init app
app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.secret_key = 'a091e1b6b9a25a1e60fab1e0b57aae48febd2a1ffeb250a0dc7169d064f67586d'


# init db
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)

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
    ID: Mapped[int] = mapped_column(primary_key=True)
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
    Ability: Mapped[str] = mapped_column(String(200))

    Reminder: Mapped[list["Reminder"]] = relationship(back_populates="Character")
    Seat: Mapped[list["Seat"]] = relationship(back_populates="Character")
    Script: Mapped[list["Script"]] = relationship(
        secondary=ScriptCharacter, back_populates="Character"
    )


class Reminder(Base):
    __tablename__ = "Reminder"
    ID: Mapped[int] = mapped_column(primary_key=True)
    CharacterID: Mapped[int] = mapped_column(ForeignKey("Chatacter.ID"))
    ReminderText: Mapped[str] = mapped_column(String(80))

    Character: Mapped["Character"] = relationship(back_populates="Reminder")
    Seat: Mapped[list["Seat"]] = relationship(
        secondary=SeatReminder, back_populates="Reminder"
    )


class Seat(Base):
    __tablename__ = "Seat"
    ID: Mapped[int] = mapped_column(primary_key=True)
    GameID: Mapped[int] = mapped_column(ForeignKey("Game.ID"))
    SeatName: Mapped[str] = mapped_column(String(30))
    SeatRole: Mapped[int] = mapped_column(ForeignKey("Character.ID"))
    SeatNotes: Mapped[str] = mapped_column(String(2000))

    Game: Mapped["Game"] = relationship(back_populates="Seat")
    Character: Mapped["Game"] = relationship(back_populates="Seat")
    Reminder: Mapped[list["Reminder"]] = relationship(
        secondary=SeatReminder, back_populates="Seat"
    )


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


# routes
@app.route('/')
def home():
    return render_template('home.html')


@app.route('/game')
def game():
    return render_template('game.html')


if __name__ == "__main__":
    app.run(debug=True)
