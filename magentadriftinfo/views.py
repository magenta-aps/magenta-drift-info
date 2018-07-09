from django.shortcuts import render
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import View
from django.views.generic.base import TemplateResponseMixin
from django.db.models import Q

from .models import Event


def index(request):
    events = Event.objects.all()
    return render(request, 'magentadriftinfo/index.html', {'events', events})


class IndexView(TemplateResponseMixin, View):
    template_name = 'magentadriftinfo/index.html'
    model = Event
    ordering = '-startTime'

    def get_context_data(self, **kwargs):
        qs = Event.objects.all()
        filter = {}
        if 'server' in self.kwargs:
            qs = qs.filter(servers__name = self.kwargs['server'])
        if 'system' in self.kwargs:
            qs = qs.filter(systems__name = self.kwargs['system'])
        if 'customer' in self.kwargs:
            qs = qs.filter(
                Q(servers__customers__name = self.kwargs['customer']) |
                Q(systems__customers__name = self.kwargs['customer'])
            )
        qs = qs.distinct().order_by(self.ordering)

        context = {
            'active_qs': Event.filter_active(qs),
            'former_qs': Event.filter_former(qs),
            'future_qs': Event.filter_future(qs),
        }
        return context

    def get(self, request, *args, **kwargs):
        return self.render_to_response(self.get_context_data())
