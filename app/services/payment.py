import uuid

import razorpay
import stripe

from config import settings


class PaymentService:
    def __init__(self):
        self.stripe_enabled = bool(settings.stripe_secret_key and settings.stripe_price_id)
        self.razorpay_enabled = bool(settings.razorpay_key_id and settings.razorpay_key_secret)

        if self.stripe_enabled:
            stripe.api_key = settings.stripe_secret_key

        self.razorpay_client = None
        if self.razorpay_enabled:
            self.razorpay_client = razorpay.Client(
                auth=(settings.razorpay_key_id, settings.razorpay_key_secret)
            )

    def create_stripe_checkout(self, email: str) -> tuple[bool, str]:
        if not self.stripe_enabled:
            return False, "Stripe is not configured"

        try:
            session = stripe.checkout.Session.create(
                customer_email=email,
                mode="subscription",
                line_items=[{"price": settings.stripe_price_id, "quantity": 1}],
                success_url=settings.stripe_success_url,
                cancel_url=settings.stripe_cancel_url,
            )
            return True, session.url
        except Exception as exc:
            return False, f"Stripe error: {exc}"

    def create_razorpay_order(self, amount_inr: int = 49900) -> tuple[bool, str]:
        if not self.razorpay_enabled or not self.razorpay_client:
            return False, "Razorpay is not configured"

        try:
            order = self.razorpay_client.order.create(
                {
                    "amount": amount_inr,
                    "currency": "INR",
                    "receipt": f"mediahub-{uuid.uuid4().hex[:12]}",
                    "payment_capture": 1,
                }
            )
            order_id = order.get("id", "")
            if not order_id:
                return False, "Unable to create Razorpay order"
            return True, (
                f"Order created: {order_id}. "
                "Collect payment using Razorpay Checkout in your web flow."
            )
        except Exception as exc:
            return False, f"Razorpay error: {exc}"


payment_service = PaymentService()
