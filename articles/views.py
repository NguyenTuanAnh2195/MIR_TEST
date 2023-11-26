from django.views.generic import ListView, DetailView, FormView
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.conf import settings

from .forms import ContactRequestForm
from .models import Article


class ArticleListView(ListView):
    model = Article
    paginate_by = 5
    template_name = "index.html"
    queryset = Article.objects.filter(is_published=True)


class ArticleDetailView(DetailView):
    model = Article
    template_name = "details.html"
    slug_field = "title_slug"


class ContactRequestView(FormView):
    form_class = ContactRequestForm
    template_name = "contact_request.html"
    success_url = reverse_lazy("articles:list")

    def form_valid(self, form):
        form.save()
        if not settings.DEBUG:
            send_mail(
                subject=form.cleaned_data["name"],
                message=form.cleaned_data["content"],
                from_email=f"Reply-to{form.cleaned_data['email']}",
                recipient_list=[settings.EMAIL_DESTINATION],
                fail_silently=False
            )
        return super().form_valid(form)
