from django.forms import ModelForm

from .models import ContactRequest


class ContactRequestForm(ModelForm):
    class Meta:
        model = ContactRequest
        fields = ["email", "name", "content"]
