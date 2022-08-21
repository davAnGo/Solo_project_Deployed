from flask_app import app
#dont forget to import all of your controllers
from flask_app.controllers import users, shifts


if __name__ == "__main__":
    app.run(debug=True)