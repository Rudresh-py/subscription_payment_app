from django.shortcuts import render

# Create your views here.
import stripe
from django.conf import settings
from django.shortcuts import redirect
from django.views import View
from django.views.generic.base import TemplateView

from payment.models import Price, Product, Blogs
from django.shortcuts import get_object_or_404

stripe.api_key = settings.STRIPE_SECRET_KEY


class CreateCheckoutSessionView(View):

    def post(self, request, *args, **kwargs):
        price = Price.objects.get(id=self.kwargs["pk"])
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price': price.stripe_price_id,
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=settings.BASE_URL + '/payment/success/',
            cancel_url=settings.BASE_URL + '/payment/cancel/',
        )
        return redirect(checkout_session.url)


class SuccessView(TemplateView):
    template_name = "payment/success.html"


class CancelView(TemplateView):
    template_name = "payment/cancel.html"


class HomePageView(TemplateView):
    template_name = "payment/home.html"

    def get_context_data(self, **kwargs):
        product = Product.objects.get(name='blog')
        prices = Price.objects.filter(product=product).values()
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['product'] = product
        context['prices'] = prices

        return context


class BlogPage(TemplateView):
    template_name = 'payment/blog_page.html'

    def get_context_data(self, **kwargs):
        product = Product.objects.get(name='blog')
        blogs = Blogs.objects.filter(product=product).values()
        context = super(BlogPage, self).get_context_data(**kwargs)
        context['blogs'] = blogs

        return context
