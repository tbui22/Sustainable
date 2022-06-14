from flask_app import app
from flask import render_template, session, redirect, request
from flask import flash
from flask_app.models.user import User
from flask_app.models.item import Item
from datetime import datetime

#================================================
# Show One Category
#================================================

@app.route("/showinventory/")
def showInventory():
    user = {
        "id" : session['user_id']
    } 
    user_info = User.showOneUser(user)

    shopping_list = User.getShoppingList(user)
    shopping_list_info = {
        "shopping_list_id" : shopping_list[0]["id"]
    }

    products = Item.showList(shopping_list_info)
    items = Item.showAllItems(user)
    
    for item in items:
        print(item)
        item['restock_date'] = item['restock_date'].strftime('%Y-%m-%d')

    return render_template("singlecategory.html", user_info = user_info, products = products, items = items,)

#================================================
# Add Item to Category
#================================================

@app.route("/additem/", methods =["POST"])
def addItem():
    item_info = {
        "category_id" : request.form["category_id"],
        "name" : request.form["name"], 
        "quantity" : request.form['quantity'],
        "restock_date" : request.form['restock_date'],
        "user_id" : session['user_id']
    }

    if not Item.validateItem(request.form):
        return redirect('/showinventory/')
        
    Item.saveItem(item_info)

    return redirect("/showinventory/")


#================================================
# Edit Item
#================================================

@app.route("/editquantity/", methods=["post"])
def edit_item():
    if "user_id" not in session: 
        flash("Please Log In")
        return redirect('/')

    item_info = {
        "id" : request.form["id"],
        "user_id" : session["user_id"],
        "category_id" : request.form["category_id"],
        "name" : request.form["name"],
        "quantity" : request.form['quantity'],
        "restock_date" : request.form['restock_date']
    }
    if not Item.validateItem(request.form):
        return redirect('/showinventory/')

    Item.edit_item(item_info)

    flash("Items Updated")
    return redirect('/showinventory/' )


#================================================
# Delete Item
#================================================

@app.route("/delete/<int:item_id>/<int:category_id>/")
def delete_item(item_id, category_id):
    id = {
        "id" : item_id,
        }
    print(category_id)
    print("lkajsfoeihtlkasdjflawiehtlaksdjfoweihrt")
    Item.delete_item(id)
    return redirect("/showinventory/")

#================================================
# Shopping List Page
#================================================

@app.route('/shoppinglist/')
def shoppinglistPage():

    if "user_id" not in session: 
        flash("Please Log In")
        return redirect('/')
    
    
    user_info = {
        "id" : session["user_id"]
    }

    user = User.showOneUser(user_info)

    # categories = Item.getAllItemsByCategory()
    # print(categories[0]['id'])

    shopping_list = User.getShoppingList(user_info)

    shopping_list_info = {
        "shopping_list_id" : shopping_list[0]["id"]
    }

    products = Item.showList(shopping_list_info)
    return render_template('shoppinglist.html', products = products, user_info = user)

#================================================
# Add Item to Shopping List 
#================================================

@app.route('/addtolist/<int:item_id>/<int:category_id>/')
def addtoList(item_id, category_id):
    user_info = {
        "id": session['user_id']
    }
    shoppingList = User.getShoppingList(user_info)
    item_info = {
        "item_id" : item_id,
        "shoppinglist_id" : shoppingList[0]['id']
    }
    Item.appendtoList(item_info)

    flash("Item Added to List")
    return redirect("/showinventory/")


#================================================
# Update Items in Shopping List 
#================================================

@app.route('/updateshoppinglist/', methods=["POST"])
def updateShoppingList():
    selectedItems = request.form.getlist('checkbox')
    print(selectedItems)
    
    for item in selectedItems:
        item_info = {
            "item_id" : item,
        }
        Item.deletefromList(item_info)
    
    
    return redirect("/showinventory/")

