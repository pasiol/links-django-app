from django.urls import path

from .views import LinkCreateView, LinkList, LinkModifyView, SearchResultsList

app_name = "links"

urlpatterns = [
    path("", LinkList.as_view(), name="all_links"),
    path("search/", SearchResultsList.as_view(), name="search_results"),
    path("create/", LinkCreateView.as_view(), name="link-create"),
    path("modify/<uuid:lid>", LinkModifyView.as_view(), name="link-modify"),
]
