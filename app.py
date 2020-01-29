import os
import africastalking
from flask import Flask, render_template, request, url_for

app = Flask(__name__)

username = "sandbox"
api_key = "ccd47dc852b1e6411b8541cda86492b3a42af3e6bb6a423b2777a13c83490a3b"

africastalking.initialize(username, api_key)

pay = africastalking.Payment
sms = africastalking.SMS
global phone_number


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")


@app.route("/checkout", methods=["GET", "POST"])
def check_out():

    if request.method == "POST":
        product_name = "DUKA"
        phone_number = request.form["phoneNumber"]
        currency_code = "KES"
        amount = 250

        try:
            response = pay.mobile_checkout(
                product_name, phone_number, currency_code, amount
            )
            print(response)
        except Exception as e:
            print(e)

    return render_template("checkout.html")


@app.route("/paymentnotification", methods=["POST"])
def payment_notification():
    print(request.values.get("status"))

    if request.values.get("status") is "Success":
        sms.send(
            "Thank you for shopping with us! Your payment has been confirmed",
            [request.values.get("phoneNumber")],
        )
    else:
        print("An error occured")

    return render_template("index.html")


if __name__ == "__main__":
    app.run(port=os.environ.get("PORT"), host="0.0.0.0")
