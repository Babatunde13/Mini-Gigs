'''Main file used for running the flask app'''

# Importing the flask app
from app import app


if __name__ == "__main__":
    #runs the app if this module is ran directly.
    app.run(debug=True)