from app import app, loginManager
from flask_login import login_required, login_user, current_user, logout_user
from flask import render_template, flash, redirect,  make_response, request, g, redirect, json
from .forms import LoginForm, SearchForm, ProductUpdateForm, QueryForm, BulkForm
import sqlite3
import subprocess
from models import User
from datetime import datetime
from werkzeug.utils import secure_filename

image_dir = '/home/cs564djj/bakery/app/static/images'

@app.route('/', methods=['GET', 'POST'])
@app.route('/search', methods=['GET', 'POST'])
def search():

    # default query db
    query = 'SELECT * FROM Product'
    query_where = []
    query_args = [];

    # get search form
    form = SearchForm()

    # set form choices:
    form.category.choices = [("", "")]
    form.category.choices.extend(((str(row["CategoryID"]), row["CatName"]) for row in query_db('SELECT * FROM Category')))

    print(form.category.choices)
    if form.validate_on_submit():

      print("VALID FOR SUBMITTED")
      #update name search
      if (form.searchField.data):
        query_where.append("Name LIKE ?")
        query_args.append("%" + str(form.searchField.data) + "%",)

      # update category filtering
      if (form.category.data):
	query = 'SELECT * FROM Product NATURAL JOIN ProductCategories NATURAL JOIN Category'
        print("CATEGORY DATA = ")
        print(form.category.data)
        query_where.append("CategoryID = ?")
        query_args.append(str(form.category.data))

      # update price filtering
      if (form.price.data):
        query_where.append("Price < ?")
        query_args.append(str(form.price.data))


    if query_where:
      query += " WHERE " + query_where[0]

    for i in range(1, len(query_where)):
      query += " AND " + query_where[i]

    print("Running query: " + str(query))
    db_results = query_db(query, args = query_args)

    return render_template("search.html",
                           title='Home',
                           messages=db_results,
                           form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    # validate form data
    if form.validate_on_submit():

        query = ('SELECT EmployeeID, Name FROM Employee WHERE' +
                ' EmployeeID = \'' + str(form.username.data) + '\''
                ' AND Password = \'' + str(form.password.data) + '\'')

        user = load_user(form.username.data)
        if (user):
            if (form.password.data == user.password):
                login_user(user)
                flash("You successfully logged in as %s" % user.name)

                print("USER EMPLOYEE?")
                print(user.isEmployee)
                if user.isEmployee:
                    return redirect('/orders')
                return redirect('/myorder')

        flash("Incorrect login/password. Try again.")


    return render_template('login.html',
                           title='Sign In',
                           form=form)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    response = make_response(redirect('/'))
    response.set_cookie('userid', '1')
    return response


@app.route('/orders', methods=['GET', 'POST'])
@login_required
def orders():

    query = ('SELECT a.OrderId as orderid, a.Created as created, ' +
            ' d.Name as customer, b.Name as employee, a.TotalSum as sum, ' +
            ' a.isClosed as closed FROM _Order a ' +
            ' LEFT JOIN Employee b ON a.PerformedBy = b.EmployeeID ' +
            ' LEFT JOIN CustomerOrders c ON a.OrderId = c.OrderID ' +
            ' LEFT JOIN Customer d ON c.CustomerId = d.CustomerID' +
            ' ORDER BY orderid DESC LIMIT 100;')

    db_results = query_db(query)

    return render_template('orders.html',
                            username=current_user.name,
                            title='Orders',
                            messages=db_results)


@app.route('/myorder', methods=['GET', 'POST'])
@login_required
def myorder():

  if not current_user.isEmployee:

    try:
      query = 'SELECT a.OrderId as orderid, a.Created as created, ' \
           + ' d.Name as customer, b.Name as employee, a.TotalSum as sum, ' \
           + ' a.isClosed as closed FROM _Order a ' \
           + ' LEFT JOIN Employee b ON a.PerformedBy = b.EmployeeID ' \
           + ' LEFT JOIN CustomerOrders c ON a.OrderId = c.OrderID ' \
           + ' LEFT JOIN Customer d ON c.CustomerId = d.CustomerID ' \
           + ' WHERE c.CustomerId = "' + current_user.id + '"'

      print(query)
      db_results = query_db(query, )


    except Exception as e:
      db_results = None
      print(e)
      flash("Error loading orders")


    return render_template('myorder.html', messages=db_results)

  return redirect('/search')


@app.route('/employee', methods=['GET', 'POST'])
@login_required
def employee():

    query = ('SELECT EmployeeID, Name, SSN, Password FROM Employee;')
    db_results = query_db(query)

    return render_template('employee.html',
                            username=current_user.name,
                            title='Employees',
                            messages=db_results)

@app.route('/product/<productID>', methods=['GET', 'POST'])
def productPage(productID):

  form = ProductUpdateForm()

  activeRecipe = query_db('SELECT * FROM Recipe NATURAL JOIN Product WHERE IsActive = 1 AND ProductID = ' + str(productID))[0]
  product = query_db("SELECT * FROM Product WHERE ProductID = " + str(productID))[0]

  if form.validate_on_submit:
    try:

      Product_query = 'UPDATE Product SET Name = "' \
      + str(form.pName.data) + '", Price = ' + str(form.price.data) \
      + ' WHERE ProductID = ' + str(product["ProductID"])

      Recipe_update_query = "UPDATE Recipe SET ProductID = " \
      + str(form.productID.data) + ', Title = "' + form.title.data \
      + '", Text = "' + form.text.data  + '", IsActive = 1' \
      + ' WHERE RecipeID = ' + str(activeRecipe["RecipeID"])

      max_recipe_ID = query_db("SELECT max(RecipeID) FROM Recipe")[0][0]

      Recipe_insert_query = "INSERT INTO Recipe VALUES (?, ?, ?, ?, ?)"
      print("MAX")
      print(max_recipe_ID)
      Recipe_insert_args = [max_recipe_ID + 1, activeRecipe["ProductID"], activeRecipe["Title"], activeRecipe["Text"], 0]
      print(Product_query)
      print(Recipe_update_query)

      # update db
      query_db(Product_query)
      query_db(Recipe_update_query)
      query_db(Recipe_insert_query, Recipe_insert_args)
      flash("Update Complete")

      # That dooesn't work
      # image_data = request.FILES[form.imageFile.name].read()
      # open(os.path.join('some_path/', form.imageFile.data), 'w').write(image_data)

      return redirect('/search')
    except TypeError as e:
        print(e)


  form.pName.data = product["Name"]
  form.price.data = product["Price"]
  form.title.data = activeRecipe["Title"]
  form.text.data = activeRecipe["Text"]
  form.productID.data = activeRecipe["ProductID"]

  allRecipe = query_db("SELECT * FROM Recipe NATURAL JOIN Product WHERE ProductID = " + str(productID))

  return render_template('product.html', product = product, recipes=allRecipe, form=form)


@app.route('/add_product', methods=['GET', 'POST'])
@login_required
def add_product():
  print("in ADD PRODUCT")

  new_id = query_db("SELECT max(ProductID) FROM Product")[0][0] + 1

  return redirect('/product/new/' + str(new_id))


@app.route('/add_bulk', methods=['GET', 'POST'])
@login_required
def add_bulk():
    print("in ADD PRODUCT IN BULK")

    form = BulkForm()

    if form.validate_on_submit:
        try:

            strings = []
            strings.append("");
            str_n = 0

            for letter in form.bulk.data:
                if (letter == "\n"):
                    str_n = str_n + 1
                    strings.append("");
                else:
                    strings[str_n] = strings[str_n] + letter

            for string in strings:
                values = string.split("|")
                new_id = query_db("SELECT max(ProductID) FROM Product")[0][0] + 1


                # Make product
                print(new_id)
                query = "INSERT INTO Product VALUES (?, ?, ?)"
                query_params = (str(new_id), values[0], values[1])
                query_db(query, query_params)

                # Make recipe
                max_recipe_ID = query_db("SELECT max(RecipeID) FROM Recipe")[0][0] + 1
                query = "INSERT INTO Recipe VALUES (?, ?, ?, ?, ?)"
                query_params = (max_recipe_ID, str(new_id), "New recipe", "New recipe description", 1)
                query_db(query, query_params)


                # Add new photo
                cmd = ["cp", image_dir + "/default_image.jpg", image_dir + "/prod-" + str(new_id) + ".jpg"]
                p = subprocess.Popen(cmd, stdout = subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                stdin=subprocess.PIPE)
                out,err = p.communicate()
                print(err)


            flash("Products Added")


        except TypeError as e:
            print(e)



    return render_template('product_add_bulk.html', form=form)


@app.route('/product/new/<productID>', methods=['GET', 'POST'])
@login_required
def newProductPage(productID):
  print("in newProductPage")

  form = ProductUpdateForm()

  form.productID.data = str(productID)

  # new_recID = query_db("SELECT max(RecipeID) FROM Recipe")[0][0] + 1
  # activeRecipe = {"ProductID": str(productID), "Title": "", "Text": "", "RecipeID": str(new_recID)}
  product = {"ProductID": str(productID), "Name":"", "Price":"" }

  print(form.errors)


  if form.validate():
    print("FORM IS VALID")
    try:
      # Make product
      print(productID)
      query = "INSERT INTO Product VALUES (?, ?, ?)"
      query_params = (productID, form.pName.data, form.price.data)
      query_db(query, query_params)

      # Make recipe
      max_recipe_ID = query_db("SELECT max(RecipeID) FROM Recipe")[0][0] + 1
      query = "INSERT INTO Recipe VALUES (?, ?, ?, ?, ?)"
      query_params = (max_recipe_ID, productID, form.title.data, form.text.data, 1)
      query_db(query, query_params)

      flash("Product Added")

      # Add new photo
      cmd = ["cp", image_dir + "/default_image.jpg", image_dir + "/prod-" + productID + ".jpg"]
      p = subprocess.Popen(cmd, stdout = subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        stdin=subprocess.PIPE)
      out,err = p.communicate()
      print(err)

      return redirect('/search')
    except TypeError as e:
        print(e)

  print("here 3")
  return render_template('product.html', product = product, recipes=[], form=form)


@app.route('/products', methods=['GET', 'POST'])
@login_required
def products():
    return render_template('products.html',
                            username=current_user.name)


@app.route('/recipes', methods=['GET', 'POST'])
@login_required
def recipes():
    return render_template('recipes.html',
                            username=current_user.name)

@app.route('/product/<productID>/order_product', methods=['GET', 'POST'])
@login_required
def order_product(productID):

  try:
    print("in order_product")
    # find max OrderID
    max_ID = query_db("SELECT max(OrderID) FROM _Order")[0][0] + 1
    product_price = query_db("SELECT Price FROM Product WHERE ProductID = ?", (productID,))[0][0]
    t = datetime.now().timetuple()
    time = str(datetime(t[0],t[1],t[2],t[3],t[4],t[5],t[6]))

    print(max_ID)
    print(product_price)
    print(time)
    # Update Order
    query = "INSERT INTO _Order VALUES (?, ?, ?, ?, ?)"
    query_params = [max_ID, product_price, time, 1, -1]
    query_db(query, query_params)


    # Update CustomerOrder
    query = "INSERT INTO CustomerOrders VALUES (?, ?)"
    query_params = [max_ID, current_user.id]
    query_db(query, query_params)

    # Update OrderProducts
    query = "INSERT INTO OrderProducts VALUES (?, ?)"
    query_params = [max_ID, productID]
    query_db(query, query_params)


    flash("product has been ordered")
    return redirect('/product/' + str(productID))

  except Exception as e:
    print(e)
    flash("Could not order item")
    return redirect('/product/' + str(productID))


@app.route('/superadmin', methods=['GET', 'POST'])
@login_required
def superadmin():

    if not current_user.isEmployee:
        flash("Sorry, you are not allowed to do that.")
        return redirect('/')

    # get query form
    form = QueryForm()

    if form.validate_on_submit():
        try:

          query = str(form.query.data)

          if "drop" in query.lower() or "truncate" in query.lower() or "delete" in query.lower():
		flash("No data destruction querys are allowed")
		raise TypeError("Destructive query")
	  con = get_db()
          try:
            cur = con.execute(query)
            dbresult = cur.fetchall()
            rownumber = len(dbresult)
            if rownumber > 30:
                raise Exception('Not more then 30 tuples in the result ' \
                        + ' allowed! Use "LIMIT" clause in your statement.')
            cur.close()
            con.commit()
          except Exception as e:
              flash(e)
              return render_template('superadmin.html',
                            form=form)

          return render_template('superadmin.html',
                                dbresult=dbresult,
                                form=form )
        except TypeError as e:
            print(e)


    return render_template('superadmin.html',
                            form=form)


# make user global
@app.before_request
def before_request():
    g.user = current_user


######################################################################
# Auxiliary functions

@loginManager.user_loader
def load_user(id):

    if isInt(id):
        # employee is loggin in
        isEmployee = True
        query = "SELECT * FROM Employee WHERE EmployeeID = " + str(id)
    else:
        # user is logging in (with email)
        isEmployee = False
        query = 'SELECT * FROM Customer WHERE CustomerID = "' + str(id) + '"'

    user = query_db(query)

    if not user:
        print("No user found with given name")
        return None

    firstUser = user[0]
    firstUser = User(firstUser[0], firstUser["Name"], firstUser["password"], True, isEmployee)

    print("returning user")
    return firstUser

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        con = sqlite3.connect(app.config['DATABASE'])
        con.row_factory = sqlite3.Row
        db = g._database = con
    return db

def query_db(query, args=()) :
    con = get_db()
    cur = con.execute(query, args)
    rv = cur.fetchall()
    cur.close()
    con.commit()
    return rv

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def checkuser():
    cookie_data = request.cookies.get('userid')
    if int(cookie_data) > 6000:
        username = request.cookies.get('username')
        return username
    return 0

def isInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
