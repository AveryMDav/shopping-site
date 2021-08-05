"""Ubermelon shopping application Flask server.

Provides web interface for browsing melons, seeing detail about a melon, and
put melons in a shopping cart.

Authors: Joel Burton, Christian Fernandez, Meggie Mahnken, Katie Byers.
"""

from flask import Flask, render_template, redirect, flash, session, request
import jinja2

import melons
import customers

app = Flask(__name__)

# A secret key is needed to use Flask sessioning features
app.secret_key = "\x07qdh\x8f\x8d%>!'\xdb\xc5%\xa9N\xe6"

# Normally, if you refer to an undefined variable in a Jinja template,
# Jinja silently ignores this. This makes debugging difficult, so we'll
# set an attribute of the Jinja environment that says to make this an
# error.
app.jinja_env.undefined = jinja2.StrictUndefined

# This configuration option makes the Flask interactive debugger
# more useful (you should remove this line in production though)
app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = True


@app.route("/")
def index():
    """Return homepage."""

    return render_template("homepage.html")


@app.route("/melons")
def list_melons():
    """Return page showing all the melons ubermelon has to offer"""

    melon_list = melons.get_all()
    return render_template("all_melons.html",
                           melon_list=melon_list)


@app.route("/melon/<melon_id>")
def show_melon(melon_id):
    """Return page showing the details of a given melon.

    Show all info about a melon. Also, provide a button to buy that melon.
    """

    melon = melons.get_by_id(melon_id)
    print(melon)
    return render_template("melon_details.html",
                           display_melon=melon)


@app.route("/cart")
def show_shopping_cart():
    """Display content of shopping cart."""

    if "cart" not in session:
        flash('Cart is currently empty')
        return redirect("/melons")
    
    cart_dict = session["cart"]
    melon_list = []
    total_cost = 0

    for melon_id, num in cart_dict.items():
        melon = melons.get_by_id(melon_id)

        melon_total_cost = melon.price * cart_dict[melon_id]

        melon_info = {
            "name": melon.common_name,
            "quantity": num,
            "price": melon.price, 
            "total": melon_total_cost}

        total_cost = total_cost + melon_total_cost

        melon_list.append(melon_info)

    return render_template("cart.html", melon_list=melon_list, total_cost=total_cost)

@app.route("/empty")
def empty_cart():
    if session["cart"] != {}:
        session["cart"] = {}
    
    return redirect("/cart")


@app.route("/add_to_cart/<melon_id>")
def add_to_cart(melon_id):
    """Add a melon to cart and redirect to shopping cart page.

    When a melon is added to the cart, redirect browser to the shopping cart
    page and display a confirmation message: 'Melon successfully added to
    cart'."""

    if "cart" not in session:
        session["cart"] = {}
        
    if melon_id not in session["cart"]:
        session["cart"][melon_id] = 1
    else:
        session["cart"][melon_id] += 1

    flash('Melon added to cart')
    return redirect("/cart")


@app.route("/login", methods=["GET"])
def show_login():
    """Show login form."""

    return render_template("login.html")


@app.route("/login", methods=["POST"])
def process_login():
    """Log user into site.

    Find the user's login credentials located in the 'request.form'
    dictionary, look up the user, and store them in the session.
    """

    if request.method == 'POST':
        email = request.form["email"]
        entered_password = request.form["password"]
        if customers.email_exists(email):
            user = customers.get_by_email(email)
            if user.password == entered_password:
                session["logged_in_customer_email"] = email
                flash("Login successful!")
                return redirect("/melons")
            else:
                flash("Incorrect password")
                return redirect("/login")
        else:
            flash("No customer with that email found")
            return redirect("/login")

    return "Oops! This needs to be implemented"


@app.route("/checkout")
def checkout():
    """Checkout customer, process payment, and ship melons."""

    # For now, we'll just provide a warning. Completing this is beyond the
    # scope of this exercise.

    flash("Sorry! Checkout will be implemented in a future version.")
    return redirect("/melons")

@app.route("/logout")
def process_logout():
    session.pop("logged_in_customer_email")
    flash("User logged out")
    return redirect("/melons")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
