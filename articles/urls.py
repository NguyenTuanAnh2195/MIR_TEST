from django.urls import path

from . import views


app_name = "articles"
urlpatterns = [
    path("", views.ArticleListView.as_view(), name="list"),
    path("<int:pk>/<slug:slug>", views.ArticleDetailView.as_view(), name="detail"),
    path("contact-request/add", views.ContactRequestView.as_view(), name="contact_request")
]
