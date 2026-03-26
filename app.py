from flask import Flask, session, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey, Table, Column, select


# init app
app = Flask(__name__)


# init db
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)




# routes
@app.route('/')
def home():
    return render_template('home.html')


if __name__ == "__main__":
    app.run(debug=True)
