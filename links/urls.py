from django.urls import path
from .views import LinkCreateView, LinkShowView

app_name = "links"

urlpatterns = [
    path("create/",  LinkCreateView.as_view(), name="link-create"),
    path('show/<uuid:lid>',  LinkShowView.as_view(), name="link-show"),
]
