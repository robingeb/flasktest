from flask import Flask, request, make_response
#from flask_restful import Resource, Api
from functools import wraps

#Erstellt neue Apllikationi
app = Flask(__name__)

#funktion um später @auth_required für einzelne Subdomains zu erstellen
def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if auth and auth.username == "username1" and auth.password == "password":
            return f(*args, **kwargs)

        return make_response("Could not verify!", 401, {"WWW-Authenticate" : "Basic realm='Login Required'"})
    return decorated


#Startseite mit eigenem Authentifikator (ohne auth_required)
@app.route("/")
def index():
    if request.authorization and request.authorization.username == "username" and request.authorization.password == "password":
        return "<hi>du bist eingeloggt<hi>"

    return make_response("Could not verify!", 401, {"WWW-Authenticate" : "Basic realm='Login Required'"})

#Seite mit auth_required (anderer username)
@app.route('/page')
@auth_required
def page():
    return "You are on the page"


if __name__ == '__main__':
    app.run(debug=True)