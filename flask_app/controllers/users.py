from flask_app import app
from flask import render_template, session, redirect, request
from flask_app.models.user import User
from flask_app.models.item import Item
from flask_bcrypt import Bcrypt
from flask import flash
bcrypt = Bcrypt(app)

###################################
# LOGIN/Register
###################################
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register/', methods=["post"])
def register():

    if not User.validate(request.form):
        return redirect("/")

    pw_hash = bcrypt.generate_password_hash(request.form['password'])

    data = {
        "first_name" : request.form["first_name"],
        "last_name" : request.form['last_name'],
        "email" : request.form['email'],
        "password" : pw_hash
    }

    user_id= User.saveInfo(data)
    
    session['user_id'] = user_id

    shopping_list = {
        "user_id": user_id
    }
    
    User.createShoppingList(shopping_list)

    return redirect("/dashboard/")

@app.route('/login/', methods=['POST'])
def login():

    data = {
        "email" : request.form["email"], 
    }

    user_in_db = User.get_by_email(data)

    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect('/')

    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Email/Password")
        return redirect('/')

    session['user_id'] = user_in_db.id

    user_id = user_in_db.id
    print(user_id)

    return redirect("/dashboard/")

@app.route('/logout/')
def logout():
    session.clear()
    return redirect('/')

###################################
# Dashboard
###################################

@app.route('/dashboard/')
def dashboard():

    if "user_id" not in session: 
        flash("Please Log In")
        return redirect('/')


    user_id = session["user_id"]

    user = {
        "id" : user_id
    }

    user_info = User.showOneUser(user)
    print(user_info)
    items = Item.showAllItems(user)
    return render_template("dashboard.html", user_info = user_info, items = items)


@app.route('/create/')
def createPage():
    return render_template("create.html")



