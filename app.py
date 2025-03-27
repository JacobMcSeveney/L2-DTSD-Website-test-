from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management

# Route for the welcome page
@app.route('/welcome', methods=['GET'])
def welcome():
    # Redirect to the home page (menu) directly since the banner replaces the order type
    return redirect(url_for('index'))

# Route for the home page (menu)
@app.route('/')
def index():
    # Render the menu page with the banner
    return render_template("index.html")

# Route for the store page
@app.route('/store')
def store():
    return render_template("store.html")

# Route for the about page
@app.route('/about')
def about():
    return render_template("about.html")

# Route to add items to the cart
@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    item = request.form.get('item')
    quantity = int(request.form.get('quantity', 1))  # Get the quantity from the request
    with open("G:/My Drive/DTSD L2/L2-DTSD-Website-test-/mydata.txt", "a") as file:
        for _ in range(quantity):  # Write the item to the file multiple times based on the quantity
            file.write(item + "\n")
    return jsonify(success=True)

# Route to remove an item from the cart
@app.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    item = request.form.get('item')
    if os.path.exists("G:/My Drive/DTSD L2/L2-DTSD-Website-test-/mydata.txt"):
        with open("G:/My Drive/DTSD L2/L2-DTSD-Website-test-/mydata.txt", "r") as file:
            lines = file.readlines()
        with open("G:/My Drive/DTSD L2/L2-DTSD-Website-test-/mydata.txt", "w") as file:
            removed = False
            for line in lines:
                if line.strip("\n") == item and not removed:
                    removed = True
                else:
                    file.write(line)
    return jsonify(success=True)

# Route to get the cart data
@app.route('/cart_data')
def cart_data():
    # Check if the file exists and read its contents
    if os.path.exists("G:/My Drive/DTSD L2/L2-DTSD-Website-test-/mydata.txt"):
        with open("G:/My Drive/DTSD L2/L2-DTSD-Website-test-/mydata.txt", "r") as file:
            items = file.readlines()
        return jsonify(items=[item.strip() for item in items])
    return jsonify(items=[])

if __name__ == "__main__":
    app.run(debug=True)
