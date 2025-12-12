import secrets
import sqlite3
from flask import Flask, flash
from flask import redirect, render_template, request, session, abort
import config, forum, users,db

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    initiatives = forum.get_initiatives()
    return render_template("index.html", initiatives=initiatives)

@app.route("/search")
def search():
    query = request.args.get("query")
    results = forum.search(query) if query else []
    return render_template("search.html", query=query, results=results)


@app.route("/initiative/<int:initiative_id>")
def show_initiative(initiative_id):
    initiative = forum.get_initiative(initiative_id)
    if not initiative:
        abort(404)
    votes = forum.get_votes(initiative_id)
    comments = forum.get_comments(initiative_id)
    hashtags = forum.get_hashtags(initiative_id)
    return render_template("initiative.html", initiative=initiative, comments=comments,votes=votes, hashtags=hashtags)

@app.route("/new_initiative", methods=["POST"])
def new_initiative():
    check_csrf()
    require_login()
    title = request.form["title"]
    content = request.form["content"]
    user_id = session["user_id"]

    if not title or len(title) > 100 or not content or len(content) > 5000:
        abort(403)
    
    initiative_id = forum.add_initiative(title, content, user_id)

    selected_tags = request.form.getlist("predefined_tags")

    forum.add_hashtags(initiative_id, content, selected_tags=selected_tags)

    return redirect("/initiative/" + str(initiative_id))

@app.route("/vote_initiative", methods=["POST"])
def vote_initiative():
    check_csrf()
    require_login()
    initiative_id = request.form["initiative_id"]
    user_id = session["user_id"]

    if forum.has_voted(user_id, initiative_id):
        return redirect("/initiative/" + str(initiative_id))
    try:
        forum.add_vote(user_id, initiative_id)
    except sqlite3.IntegrityError:
        abort(403)

    return redirect("/initiative/" + str(initiative_id))

@app.route("/new_comment", methods=["POST"])
def new_comment():
    check_csrf()
    require_login()
    content = request.form["content"]
    user_id = session["user_id"]
    initiative_id = request.form["initiative_id"]

    if not content or len(content) > 5000:
        abort(403)

    try:
        forum.add_comment(content, user_id, initiative_id)
    except sqlite3.IntegrityError:
        abort(403)
    return redirect("/initiative/" + str(initiative_id))

@app.route("/edit/<int:comment_id>", methods=["GET", "POST"])
def edit_comment(comment_id):
    check_csrf()
    require_login()
    comment = forum.get_comment(comment_id)
    if not comment:
        abort(404)

    if comment["user_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("edit.html", comment=comment)

    if request.method == "POST":
        content = request.form["content"]
        forum.update_comment(comment["id"], content)
        return redirect("/initiative/" + str(comment["initiative_id"]))

@app.route("/remove/<int:comment_id>", methods=["GET", "POST"])
def remove_comment(comment_id):
    check_csrf()
    require_login()
    comment = forum.get_comment(comment_id)
    if not comment:
        abort(404)

    if request.method == "GET":
        return render_template("remove.html", comment=comment)

    if request.method == "POST":
        if "continue" in request.form:
            forum.remove_comment(comment["id"])
        return redirect("/initiative/" + str(comment["initiative_id"]))

@app.route("/register")
def register():
    return render_template("register.html")

def require_login():
    if "user_id" not in session:
        abort(403)

def require_logout():
    if "user_id" in session:
        abort(403)

@app.route("/create", methods=["POST"])
def create():
    require_logout()
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return "VIRHE: salasanat eivät ole samat"
    
    try:
        users.create_user(username, password1)
    except sqlite3.IntegrityError:
        return "VIRHE: tunnus on jo varattu"

    return render_template("new_user.html", username=username)

def check_csrf():
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)

@app.route("/login", methods=["GET", "POST"])
def login():
    require_logout()
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user_id = users.check_login(username, password)
        if user_id:
            session["user_id"] = user_id
            session["csrf_token"] = secrets.token_hex(16)
            print(session)
            return redirect("/")
        else:
            return "VIRHE: väärä tunnus tai salasana"

@app.route("/logout")
def logout():
    del session["user_id"]
    return redirect("/")

@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)
    if not user:
        abort(404)
    comments = users.get_user_comments(user_id)
    return render_template("user.html", user=user, comments=comments)