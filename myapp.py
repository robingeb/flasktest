from flask import Flask

app=Flask(__name__)

@app.route('/')
def homepage():
    return "Hi"

if __name__=='__main__':
    app.run(debug=True)



    #virtualenv venv   erstellt eine neue venv
    # .\venv\Scripts\activate
    # deactivate
    # bei aktivierte venv eingeben python myapp.py

    