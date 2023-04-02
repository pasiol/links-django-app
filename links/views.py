import time
from django.db import IntegrityError, DatabaseError, transaction
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from .forms import LinkForm
from .models import Link


class LinkCreateView(View):
    form_class = LinkForm
    template_name = "link/link_form.html"
    success_url = "/links/"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            succeed = False
            while not succeed:
                try:
                    with transaction.atomic():
                        new_link = form.save()
                        succeed = True
                except IntegrityError:
                    messages.error(request, "Sorry, we couldn't process your request because of a server error. Please \
                    try again later or contact our support team if the problem persists.")
                    return render(request, self.template_name, {'form': form})
            succeed = None
            return redirect(f'/links/show/{new_link.pk}')
        return render(request, self.template_name, {'form': form})


class LinkShowView(View):
    template_name = 'link/link_show.html'

    def get(self, request, lid):
        link = None
        succeed = False
        while not succeed:
            try:
                link = Link.objects.get(id=lid)
                succeed = True
            except Link.DoesNotExist:
                return HttpResponseNotFound("The object was not found.")
            except DatabaseError:
                time.sleep(10) #TODO: The notification of malfunction database connection
        context = {'link': link}
        return render(request, self.template_name, context)

