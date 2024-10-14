from django.urls import path
from .views import create_contact, reset_contact_form

urlpatterns = [
    path("contacts/create/", create_contact, name="contact-create"),
    path("contacts/reset/", reset_contact_form, name="contact-reset"),
]
