import time

from django.contrib import messages
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.db import DatabaseError, IntegrityError, OperationalError, transaction
from django.http import HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import cache_page
from django.views.generic.list import ListView

from .forms import LinkFormCreate, LinkFormModify
from .models import Link


class LinkCreateView(View):
    form_class = LinkFormCreate
    template_name = "link_form.html"
    success_url = "/links/"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_link = None
            succeed = False
            giving_up = False
            try:
                with transaction.atomic():
                    new_link = form.save()
            except (IntegrityError, DatabaseError, OperationalError):
                transaction.rollback()
                count = 0
                while not succeed or not giving_up:
                    try:
                        time.sleep(10)
                        with transaction.atomic():
                            new_link = form.save()
                    except (IntegrityError, DatabaseError, OperationalError):
                        transaction.rollback()
                        count = count + 1
                        if count > 6:
                            new_link = None
                            giving_up = True
            if new_link is None:
                messages.error(
                    request,
                    "Sorry, we couldn't process your request because of a server error. Please \
                try again later.",
                )
                return render(request, self.template_name, {"form": form})
            return redirect(f"/links/modify/{new_link.pk}")
        else:
            new_url = form.cleaned_data["url"]
            new_type = form.cleaned_data["type"]
            old_link = Link.objects.get(url=new_url, type=new_type)
            return redirect(f"/links/modify/{old_link.pk}")


class LinkModifyView(View):
    form_class = LinkFormModify
    success_url = "/links/"
    template_name = "link_modify.html"
    object_id = None

    def get(self, request, lid):
        try:
            link = Link.objects.get(id=lid)
        except Link.DoesNotExist:
            return HttpResponseNotFound("The object was not found.")
        except DatabaseError:
            return HttpResponseServerError(
                "An error occurred while retrieving the object."
            )
        form = self.form_class(instance=link)
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            succeed = False
            giving_up = False
            oid = kwargs.get("lid")
            try:
                with transaction.atomic():
                    link_to_modify = Link.objects.get(pk=oid)
                    setattr(
                        link_to_modify,
                        "description",
                        form.cleaned_data.get("description"),
                    )
                    setattr(link_to_modify, "type", form.cleaned_data.get("type"))
                    link_to_modify.save()
            except (IntegrityError, DatabaseError, OperationalError):
                transaction.rollback()
                count = 0
                while not succeed or not giving_up:
                    try:
                        time.sleep(10)
                        with transaction.atomic():
                            link_to_modify = Link.objects.get(pk=oid)
                            setattr(
                                link_to_modify,
                                "description",
                                form.cleaned_data.get("description"),
                            )
                            setattr(
                                link_to_modify, "type", form.cleaned_data.get("type")
                            )
                            link_to_modify.save()
                    except (IntegrityError, DatabaseError, OperationalError):
                        transaction.rollback()
                        count = count + 1
                        if count > 6:
                            giving_up = True
            return redirect(f"/links/")


@method_decorator(cache_page(60 * 5), name="dispatch")
class LinkList(ListView):
    model = Link
    context_object_name = "links"
    template_name = "link_list.html"


class SearchResultsList(ListView):
    model = Link
    context_object_name = "links"
    template_name = "search.html"

    def get_queryset(self):
        query = self.request.GET.get("q")
        search_vector = SearchVector("description")
        search_query = SearchQuery(query)
        return (
            Link.objects.annotate(
                search=search_vector, rank=SearchRank(search_vector, search_query)
            )
            .filter(search=search_query)
            .order_by("-rank")
        )
