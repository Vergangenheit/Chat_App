from flask import Flask, render_template, redirect, url_for, session

NAME_KEY = 'name'
app = Flask(__name__)
app.secret_key = "hello"


@app.route("/login")
def login():
    return render_template("")


@app.route("/logout")
def logout():
    session.pop(NAME_KEY, None)
    return redirect(url_for("login"))


@app.route("/")
@app.route("/")
def home():
    if NAME_KEY not in session:
        return redirect(url_for("home"))
    name = session[NAME_KEY]

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
