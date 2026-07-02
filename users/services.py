import stripe
from django.conf import settings


stripe.api_key = settings.STRIPE_SECRET_KEY

def create_stripe_product(name,description):
    products = stripe.Product.create(name=name, description=description)
    return products



def create_stripe_price(product_id, amount):
    price = stripe.Price.create(
        product=product_id,
        unit_amount=int(amount*100),
        currency="rub"
        )


def create_stripe_session(price_id):
    session = stripe.checkout.Session.create(
        seccess_url="https://stripe.com",
        line_items=[
            {
                "price": price_id,
                "quantity": 1,
            }
        ],
        mode = "payment",
    )
    return session