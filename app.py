import os

import stripe
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

stripe_keys = {
    "secret_key": os.environ["STRIPE_SECRET_KEY"],
    "publishable_key": os.environ["STRIPE_PUBLISHABLE_KEY"],
}

stripe.api_key = stripe_keys["secret_key"]


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/config")
def get_publishable_key():
    stripe_config = {"publicKey": stripe_keys["publishable_key"]}
    return jsonify(stripe_config)

@app.route("/product-list")
def productList():
    stripe.api_key  = stripe_keys["secret_key"]
    list = stripe.Product.list()
    return jsonify(list)

@app.route("/payments")
def paymentList():
    payment_intents = stripe.PaymentIntent.list()
    payment_info_list = []

    for payment_intent in payment_intents.data:
        payment_info = {
            'id': payment_intent.id,
            'amount': payment_intent.amount / 100,
            'status': payment_intent.status,
            'created': payment_intent.created,
        }
        payment_info_list.append(payment_info)

    return render_template("payments.html", payment_info_list=payment_info_list)



@app.route("/success")
def success():
    return render_template("success.html")


@app.route("/cancelled")
def cancelled():
    return render_template("cancelled.html")

# Configure a chave secreta do Stripe

@app.route("/create-checkout-session")
def create_checkout_session():
    domain_url = "http://localhost:5000/"
    stripe.api_key = stripe_keys["secret_key"]
    try:

        checkout_session = stripe.checkout.Session.create(
            success_url=domain_url + "success?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=domain_url + "cancelled",
            payment_method_types=["card"],
            mode="payment",

            line_items=[{
                'price_data': {
                    'currency': 'brl',
                    'unit_amount': 500,
                    'product_data': {
                        'name': 'Alfajor',
                        'description':'Recheado com doce de leite.',
                        'images': ['https://stripe-camo.global.ssl.fastly.net/2d9ac2988e0538ed0663e39b809acb88afb8852049337a7a5fba689a19802c5a/68747470733a2f2f63646e2d70726f647563746462696d616765732e62617272792d63616c6c65626175742e636f6d2f73697465732f62635f70726f6475637464625f696d616765732f66696c65732f7374796c65732f7765625f676d5f63616c6c65626175742d64657461696c2f7075626c69632f65787465726e616c732f66626230313332623461343963303333363132663761306566393637326638642e6a70673f69746f6b3d456851734d377747']
                    },
                },
                'quantity': 3,},

                {'price_data': {
                    'currency': 'brl',
                    'unit_amount': 400,
                    'product_data': {
                        'name': 'Bala de coco',
                        'description':'Feita de coco natural.',
                        'images': ['https://cdn0.tudoreceitas.com/pt/posts/9/4/2/bala_de_coco_baiana_simples_10249_600_square.jpg']
                    },
                },
                'quantity': 6,}

            ]
        )

        return jsonify({"sessionId": checkout_session["id"]})
    except Exception as e:
        return jsonify(error=str(e)), 403


@app.route("/createPayment", methods=["GET"])
def createPayment():
    data = request.get_json()
    return jsonify(data)

@app.route("/webhook", methods=["POST"])
def stripe_webhook():
    payload = request.get_data(as_text=True)
    sig_header = request.headers.get("Stripe-Signature")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, stripe_keys["endpoint_secret"]
        )

    except ValueError as e:
        # Invalid payload
        return "Invalid payload", 400
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return "Invalid signature", 400

    # Handle the checkout.session.completed event
    if event["type"] == "checkout.session.completed":
        print("Pagamento bem sucedido.")
        # TODO: run some custom code here

    return "Success", 200
if __name__ == "__main__":
    app.run(debug=True)