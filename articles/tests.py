from django.test import TestCase, override_settings
from django.contrib.auth.models import User
from django.shortcuts import reverse

from articles.models import Article, ContactRequest


class TestArticle(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(
            username="test_user",
            email="testuser@mail.com",
            password="!#@123baisCCC",
        )
        for i in range(0, 11):
            Article.objects.create(
                title=f"Article {i}",
                content=f"This is the content of article {i}",
                author=user,
                is_published=True,
            )
        for i in range(11, 16):
            Article.objects.create(
                title=f"Article {i}",
                content=f"This is the content of article {i}",
                author=user,
                is_published=False,
            )

    def test_article_list_view_published_articles(self):
        response = self.client.get(reverse("articles:list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")

    def test_article_list_paginated_view_published_articles(self):
        url = reverse("articles:list")
        url = f"{url}?page=3"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")

    def test_article_list_paginated_view_unpublished_articles(self):
        url = reverse("articles:list")
        url = f"{url}?page=4"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_article_detail_view(self):
        article_1 = Article.objects.get(id=1)
        url = reverse("articles:detail", kwargs={"pk": article_1.pk, "slug": article_1.title_slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "details.html")

    def test_article_non_existent(self):
        url = reverse("articles:detail", kwargs={"pk": 100, "slug": "article-100"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


@override_settings(DEBUG=True)
class TestContactRequest(TestCase):
    def test_create_contact_request(self):
        url = reverse("articles:contact_request")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "contact_request.html")

        response = self.client.post(
            url,
            data={
                "email": "test_email@mail.com",
                "name": "test_contact_request",
                "content": "test contact request body"
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("articles:list"))

        contact_request = ContactRequest.objects.get(id=1)
        self.assertEqual(contact_request.email, "test_email@mail.com")
        self.assertEqual(contact_request.name, "test_contact_request")
        self.assertEqual(contact_request.content, "test contact request body")
