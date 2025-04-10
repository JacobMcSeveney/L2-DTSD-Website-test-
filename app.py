from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management

# Route for the home page (menu)
@app.route('/')
def index():
    # Render the menu page with the banner
    return render_template("index.html")

@app.route('/payment')
def payment():
    return render_template("payment.html")# Create a payment.html template

@app.route('/store')
def store():
    return render_template("store.html")  # Create a store.html template

# Route to add items to the cart
@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    data = request.get_json()  # Parse JSON data from the request
    item = data.get('item')  # Get the item name
    quantity = int(data.get('quantity', 1))  # Default quantity to 1 if not provided

    if item:
        # Append the item to mydata.txt
        with open("G:/My Drive/DTSD L2/website/L2-DTSD-Website-test-/mydata.txt", "a") as file:
            for _ in range(quantity):
                file.write(item + "\n")
        return jsonify(success=True)  # Return success response
    return jsonify(success=False)  # Return failure response if item is missing

# Route to remove an item from the cart
@app.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    item = request.form.get('item')
    if os.path.exists("G:/My Drive/DTSD L2/website/L2-DTSD-Website-test-/mydata.txt"):
        with open("G:/My Drive/DTSD L2/website/L2-DTSD-Website-test-/mydata.txt", "r") as file:
            lines = file.readlines()
        with open("G:/My Drive/DTSD L2/website/L2-DTSD-Website-test-/mydata.txt", "w") as file:
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
    # Define item prices
    item_prices = {
        "MeatLovers Pizza": 18.90,
        "Cheese Pizza": 11.99,
        "Pepperoni Pizza": 14.99,
        "White Pizza": 14.90,
        "Meatball Pizza": 19.90,
        "New York Style Pizza": 21.90,
        "Veggie Pizza": 17.50,
        "Hawaiian Pizza": 16.90,
        "BBQ Chicken Pizza": 20.90,
        "Buffalo Chicken Pizza": 18.90,
        "Supreme Pizza": 16.50,
        "Margherita Pizza": 15.90,
    }

    # Check if the file exists and read its contents
    cart_items = []
    total_price = 0.0
    if os.path.exists("G:/My Drive/DTSD L2/website/L2-DTSD-Website-test-/mydata.txt"):
        with open("G:/My Drive/DTSD L2/website/L2-DTSD-Website-test-/mydata.txt", "r") as file:
            for line in file:
                item = line.strip()
                cart_items.append({"name": item, "price": item_prices.get(item, 0.0)})
                total_price += item_prices.get(item, 0.0)

    return jsonify(items=cart_items, total_price=round(total_price, 2))

@app.route('/success', methods=['POST'])
def success():
    email = request.form.get('email')
    card_number = request.form.get('card_number')
    expiry_date = request.form.get('expiry_date')
    cvv = request.form.get('cvv')

    # Save the payment details to payment.txt with the prefix 'user'
    with open("G:/My Drive/DTSD L2/website/L2-DTSD-Website-test-/paymentdata.txt", "a") as file:
        file.write(f"user: {email}, card_number: {card_number}, expiry_date: {expiry_date}, cvv: {cvv}\n")
    return render_template("success.html")  # Create a store.html template
if __name__ == "__main__":
    app.run(debug=True)
